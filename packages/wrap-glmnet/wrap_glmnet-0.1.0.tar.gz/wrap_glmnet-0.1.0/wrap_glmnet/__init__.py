"""Wrap Glmnet."""
from __future__ import annotations
from typing import Optional, Union, Callable
import numpy as np
from typing_extensions import Self
import glmnet
from multiclass_metrics import roc_auc_score
from extendanything import ExtendAnything
from sklearn.base import ClassifierMixin, BaseEstimator
from sklearn.utils.validation import _get_feature_names
import sklearn.model_selection
import sklearn.utils.class_weight
import sklearn.metrics
import functools
import logging
import genetools
import inspect

__author__ = """Maxim Zaslavsky"""
__email__ = "maxim@maximz.com"
__version__ = "0.1.0"

# Set default logging handler to avoid "No handler found" warnings.
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

logger = logging.getLogger(__name__)


def apply_glmnet_wrapper():
    """
    Replace a glmnet internal function with a wrapper, so that we can override internal CV.

    python-glmnet forces use of their own cross validation splitters.
    But we can inject our own right before _score_lambda_path is called (the function that actually uses the splitter).
    See https://github.com/civisanalytics/python-glmnet/blob/813c06f5fcc9604d8e445bd4992f53c4855cc7cb/glmnet/logistic.py#L245
    """

    # def wrap_with_cv_update(original_method):
    #     @functools.wraps(original_method)
    #     def wrapped_method_that_replaces_original_method(est, *args, **kwargs):
    #         # Wrapped function is called f"{original_method.__name__}"
    #         # est is the estimator instance

    #         # Before calling _score_lambda_path, glmnet sets est._cv.
    #         # We will modify est._cv if est._cv_override is set and available.
    #         # Pass through unmodified otherwise.
    #         if hasattr(est, "_cv_override") and est._cv_override is not None:
    #             est._cv = est._cv_override

    #         # Proceed with original method
    #         return original_method(est, *args, **kwargs)

    #     return wrapped_method_that_replaces_original_method

    # Update: Let's add more functionality - though this really should put us in the realm of a fork:
    # - _score_lambda_path should pass groups into _fit_and_score
    # - _fit_and_score should pass groups[test_inx] into scorer if scorer accepts a groups argument
    # - _score_lambda_path should store the cross validation scores in est._cv_scores_ before returning them
    # - _score_lambda_path should also store, in est.cv_pred_probs_, the predicted probabilities for each example when it is in the held-out set, for each value of lambda, and in the original order of the examples
    # That's in addition to the desired functionality expressed in the wrapper above, where we swap est._cv with est._cv_override if that's set and available.
    def make_custom_score_lambda_path_wrapper(original_method, wrapped_fit_and_score):
        import warnings
        from sklearn.exceptions import UndefinedMetricWarning
        from joblib import Parallel, delayed
        from glmnet.scorer import check_scoring

        @functools.wraps(original_method)
        def wrapped_method_that_replaces_original_method(
            est: glmnet.LogitNet,
            X,
            y,
            groups,
            sample_weight,
            relative_penalties,
            scoring,
            n_jobs,
            verbose,
        ):
            # This is our custom implementation of _score_lambda_path.
            # Wrapped function is called f"{original_method.__name__}"
            # est is the estimator instance (caution: this is a LogitNet object, not a GlmnetLogitNetWrapper object)
            # In this case, we are *not* going to call original_method.

            # From earlier wrapper above:
            # Before calling _score_lambda_path, glmnet sets est._cv.
            # We will modify est._cv if est._cv_override is set and available.
            # Pass through unmodified otherwise.
            if hasattr(est, "_cv_override") and est._cv_override is not None:
                est._cv = est._cv_override

            scorer = check_scoring(est, scoring)
            cv_split = list(est._cv.split(X, y, groups))

            with warnings.catch_warnings():
                action = "always" if verbose else "ignore"
                warnings.simplefilter(action, UndefinedMetricWarning)

                results = Parallel(n_jobs=n_jobs, verbose=verbose, backend="threading")(
                    delayed(wrapped_fit_and_score)(
                        est=est,
                        scorer=scorer,
                        X=X,
                        y=y,
                        sample_weight=sample_weight,
                        relative_penalties=relative_penalties,
                        score_lambda_path=est.lambda_path_,
                        train_inx=train_idx,
                        test_inx=test_idx,
                        # new parameters:
                        groups=groups,
                        compute_probabilities=est.store_cv_predicted_probabilities,
                    )
                    for (train_idx, test_idx) in cv_split
                )

                # results is a list of tuples (score, prob, classes). the full results list is of length n_folds.
                # unpack into three lists of length n_folds each: scores, probs, classes_in_each_model
                # each entry in scores is a 1d array of length n_lambda
                # each entry in probs is a 3d array of shape (n_samples, n_classes, n_lambda)
                # each entry in classes_in_each_model is a 1d array of length n_classes
                # Caution: these submodels may have fewer classes than the total number of classes in the full model.
                scores, probs, classes_in_each_model = zip(*results)

                # New:
                if est.store_cv_predicted_probabilities:
                    # est.classes_ is available because the full model was already fit, before we run this CV fit-and-score function
                    total_n_classes = len(est.classes_)
                    # cv_pred_probs_ will have shape (n_samples, n_classes, n_lambdas), even in binary case.
                    # Initialize to zeros, because some CV folds may not have any examples of a particular class, so we will want those missing class columns to be predicted class probabilities of 0.
                    est.cv_pred_probs_ = np.zeros(
                        (X.shape[0], total_n_classes, len(est.lambda_path_))
                    )
                    for (_, test_idx), prob, model_classes in zip(
                        cv_split, probs, classes_in_each_model
                    ):
                        # We need to handle the possibility that this CV fold had no examples of a particular class, so the returned probability array has a middle dimension less than expected.
                        # Therefore, we can't just do this:
                        # est.cv_pred_probs_[test_idx, :, :] = prob

                        # Determine the indices of the classes present in the current model
                        model_class_indices = np.array(
                            [
                                np.where(est.classes_ == cls)[0][0]
                                for cls in model_classes
                            ]
                        )
                        # Subset the first two dimensions. Third dimension will be populated fully by prob.
                        est.cv_pred_probs_[np.ix_(test_idx, model_class_indices)] = prob
                elif hasattr(est, "cv_pred_probs_"):
                    # If we're not storing predicted probabilities, but the attribute exists from a previous run, then delete it.
                    del est.cv_pred_probs_

                # _cv_scores_ is a list of length n_folds. Each entry is a 1d array of length n_lambda. These are scores for each value of lambda over all CV folds.
                # The outer LogitNet calling code will then take the mean of these scores over all CV folds, leaving one average score per lambda. (That will be clf.cv_mean_score_)
                est._cv_scores_ = scores

                return est._cv_scores_

        return wrapped_method_that_replaces_original_method

    def make_custom_fit_and_score_wrapper(original_method):
        from sklearn.base import clone

        @functools.wraps(original_method)
        def wrapped_method_that_replaces_original_method(
            est,
            scorer,
            X,
            y,
            sample_weight,
            relative_penalties,
            score_lambda_path,
            train_inx,
            test_inx,
            # new parameters:
            groups,
            compute_probabilities: bool,
        ):
            # This is our custom implementation of _fit_and_score.
            # Wrapped function is called f"{original_method.__name__}"
            # est is the estimator instance
            # In this case, we are *not* going to call original_method.
            m = clone(est)
            m = m._fit(
                X[train_inx, :],
                y[train_inx],
                sample_weight[train_inx],
                relative_penalties,
            )

            lamb = np.clip(score_lambda_path, m.lambda_path_[-1], m.lambda_path_[0])

            # Check if scorer accepts a 'groups' argument or arbitrary kwargs
            scorer_parameters = inspect.signature(scorer).parameters
            scorer_supports_groups = "groups" in scorer_parameters.keys()
            scorer_supports_kwargs = any(
                parameter.kind == inspect.Parameter.VAR_KEYWORD
                for parameter in scorer_parameters.values()
            )
            if scorer_supports_groups or scorer_supports_kwargs:
                score = scorer(
                    m, X[test_inx, :], y[test_inx], lamb=lamb, groups=groups[test_inx]
                )
            else:
                score = scorer(m, X[test_inx, :], y[test_inx], lamb=lamb)

            # Generate held-out set probabilities.
            if compute_probabilities:
                prob = m.predict_proba(X[test_inx, :], lamb=lamb)
            else:
                prob = None

            # Return:
            # score has shape (n_lambda,)
            # prob has shape (n_samples, n_classes, n_lambda)
            # m.classes_ is shape (n_classes,)
            return score, prob, m.classes_

        return wrapped_method_that_replaces_original_method

    # Hot swap the function
    import glmnet.util

    # wrapped_score_lambda_path = wrap_with_cv_update(glmnet.util._score_lambda_path)
    wrapped_fit_and_score = make_custom_fit_and_score_wrapper(
        glmnet.util._fit_and_score
    )
    wrapped_score_lambda_path = make_custom_score_lambda_path_wrapper(
        glmnet.util._score_lambda_path, wrapped_fit_and_score
    )
    glmnet.util._score_lambda_path = wrapped_score_lambda_path
    glmnet.util._fit_and_score = wrapped_fit_and_score

    # It's likely it has already been imported by glmnet.logistic, because glmnet.__init__ import glmnet.logistic,
    # so we need to hot swap the imported version too.
    import glmnet.logistic

    glmnet.logistic._score_lambda_path = wrapped_score_lambda_path


# Do this replacement at import time.
apply_glmnet_wrapper()


class GlmnetLogitNetWrapper(ExtendAnything, ClassifierMixin, BaseEstimator):
    """
    Wrapper around python-glmnet's LogitNet that exposes some additional features:

    - standard sklearn API properties
    - control over choice of lambda
    - multiclass ROC-AUC scorer for internal cross validation
    - automatic class weight rebalancing as in sklearn

    Use this wrapper in place of python-glmnet's LogitNet.
    """

    # ExtendAnything passes everything else on to _inner automatically
    _inner: glmnet.LogitNet

    # Define our own scorers, following glmnet.scorer signatures.
    @staticmethod
    def rocauc_scorer(
        clf,
        X: np.ndarray,
        y_true: np.ndarray,
        lamb: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
    ):
        """
        Multiclass ROC-AUC scorer for LogitNet's internal cross validation.
        To use, pass `scoring=GlmnetLogitNetWrapper.rocauc_scorer` to the GlmnetLogitNetWrapper model constructor.
        """
        # Make a multiclass CV scorer for ROC-AUC for glmnet models.
        # `scoring="roc_auc"`` doesn't suffice: multiclass not supported.

        # We have the same problem for sklearn models, but we can't repurpose sklearn's make_scorer output here.
        # The scorer function here has a different signature than sklearn's make_scorer output function: lambdas are passed to the scorer.
        # Specifically, the scoring function will be called with arguments: `(clf, X[test_inx, :], y[test_inx], lamb)`, where `lamb` is an array.

        # Unfortunately, glmnet.scorer.make_scorer is not sufficient, because it does not set the "labels" parameter used in roc_auc_score.
        # This does not work:
        # rocauc_scorer = glmnet.scorer.make_scorer(
        #     roc_auc_score,
        #     average="weighted",
        #     multi_class="ovo",
        #     needs_proba=True,
        # )

        # Instead we roll our own.

        # y_preds_proba shape is (n_samples, n_classes, n_lambdas)
        y_preds_proba = clf.predict_proba(X, lamb=lamb)

        # One score per lambda. Shape is (n_lambdas,)
        scores = np.array(
            [
                roc_auc_score(
                    y_true=y_true,
                    y_score=y_preds_proba[:, :, lambda_index],
                    average="weighted",
                    labels=clf.classes_,
                    multi_class="ovo",
                    sample_weight=sample_weight,
                )
                for lambda_index in range(y_preds_proba.shape[2])
            ]
        )
        return scores

    @staticmethod
    def deviance_scorer(
        clf,
        X: np.ndarray,
        y_true: np.ndarray,
        lamb: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
    ):
        """
        Deviance scorer for LogitNet's internal cross validation.
        To use, pass `scoring=GlmnetLogitNetWrapper.deviance_scorer` to the GlmnetLogitNetWrapper model constructor.
        """
        # Roll our own deviance (log loss) minimizer too.
        # glmnet.scorer.log_loss_scorer is almost exactly what we want: minimizing the deviance is equivalent to minimizing the log loss.
        # But as above, we can't use glmnet's make_scorer because it doesn't set the "labels" parameter used in log_loss.
        # Otherwise, we get errors like: "y_true and y_pred contain different number of classes 2, 3. Please provide the true labels explicitly through the labels argument."

        # y_preds_proba shape is (n_samples, n_classes, n_lambdas)
        y_preds_proba = clf.predict_proba(X, lamb=lamb)

        # One score per lambda. Shape is (n_lambdas,)
        scores = np.array(
            [
                sklearn.metrics.log_loss(
                    y_true=y_true,
                    # y_pred is shape (n_samples, n_classes).
                    # for binary, shape (n_samples,) is accepted too, but not required to extract positive class in this way.
                    y_pred=y_preds_proba[:, :, lambda_index],
                    # provide labels explicitly to avoid error
                    labels=clf.classes_,
                    sample_weight=sample_weight,  # may be None
                )
                for lambda_index in range(y_preds_proba.shape[2])
            ]
        )
        # greater is worse; we want to minimize log loss
        return -1 * scores

    def __init__(
        self,
        use_lambda_1se=True,
        require_cv_group_labels=False,
        n_splits: Optional[int] = 3,
        internal_cv: Optional[sklearn.model_selection.BaseCrossValidator] = None,
        class_weight: Optional[Union[dict, str]] = None,
        scoring: Optional[Union[str, Callable]] = None,  # string, callable or None
        store_cv_predicted_probabilities: bool = True,
        **kwargs,
    ) -> None:
        """
        Initialize a LogitNet model. All kwargs are passed to LogitNet.

        Extra arguments:
        - `use_lambda_1se` determines which lambda is used for prediction, coef_, and intercept_:
            If True (default), use lambda_1se (larger lambda but performance still within 1 standard error).
            This is the default behavior of LogitNet.
            This lambda and its index are available as properties lambda_best_ and lambda_best_inx_.

            If False, use the lambda value that achieved highest cross validation performance for prediction.
            This lambda and its index are available as properties lambda_max_ and lambda_max_inx_.

            Pass `use_lambda_1se=False` to switch LogitNet's default behavior to use the lambda with highest CV performance,
            rather than use a simpler model that still performs within 1 standard error of the best observed performance.

            The more parsimonious model (lambda_1se=True) is a good choice when focused on interpretation over prediction.
            Lambda_max may generalize better than lambda_1se, because it retains more variables -- the model is more robust when not hanging its hat entirely on a small set of variables.
            Call switch_lambda() after fitting to duplicate the fitted model and toggle its lambda_1se setting, so you can analyze performance both ways.

        - `require_cv_group_labels` (disabled by default) determines whether to require groups parameter in fit() call.
            Glmnet is often used with internal cross-validation.
            If `require_cv_group_labels` is True, then the `groups` parameter must be passed to fit(), otherwise an error is thrown.
            This adds a safety net to make sure that the user is aware that they are using internal cross-validation
            and that the internal cross-validation is performing the correct splits.

        - `class_weight`: dict or 'balanced' or None, defaults to 'balanced'.
            Behaves just like class_weight in sklearn models, see e.g. LogisticRegression.

        - `internal_cv`: an optional sklearn-style cross validation split generator like KFold, StratifiedKFold, etc.
            Optional override of glmnet's default cross validation split generator.
            Note that specifying internal_cv will cause the n_splits argument to be overwritten with the value of `internal_cv.get_n_splits()`.
            If internal_cv is not specified, then n_splits will be used with glmnet's default CV split strategy. Either n_splits or internal_cv must be specified.

        - `scoring`: an optional cross validation scoring function, defaults to minimizing deviance as in R glmnet.
        - `store_cv_predicted_probabilities`: if True, store the predicted probabilities for each example when it is in the held-out set, for each value of lambda, and in the original order of the examples.
        """
        # for sklearn clone compatibility, in the constructor we should only set these variables, and not do any modifications yet
        self.use_lambda_1se = use_lambda_1se
        self.require_cv_group_labels = require_cv_group_labels
        self.class_weight = class_weight
        self.internal_cv = internal_cv
        self.n_splits = (
            n_splits  # may be null for now - we will fill later from internal_cv
        )
        self.store_cv_predicted_probabilities = store_cv_predicted_probabilities

        if self.n_splits is None and self.internal_cv is None:
            raise ValueError("Either n_splits or internal_cv must be specified.")

        if scoring is None:
            # Unlike glmnet.LogitNet, we set default scorer to deviance, as done by R glmnet.
            scoring = self.deviance_scorer

        # sets self._inner
        super().__init__(
            glmnet.LogitNet(
                # default if not provided. we will override later with the correct value from internal_cv
                n_splits=n_splits if n_splits is not None else 3,
                scoring=scoring,
                **kwargs,
            )
        )
        # also set this attribute on the LogitNet object, so it can be picked up by our wrapped version of _score_lambda_path.
        self._inner.store_cv_predicted_probabilities = store_cv_predicted_probabilities

    def get_params(self, deep=True):
        # Support sklearn cloning properly.
        # Return the inner LogitNet's constructor parameters (will be passed as kwargs through our constructor), plus our own constructor parameters.
        return self._inner.get_params(deep=deep) | super().get_params(deep=deep)

    ######
    # Fix some inconsistencies in the python-glmnet API
    # (Note: because of how ExtendAnything works, these only affect outside users of the wrapper.
    # Glmnet internal code will still see Glmnet's internal values for these properties, not our modified version.)

    @property
    def lambda_best_(self) -> float:
        # lambda_max_ is a scalar, but lambda_best_ is wrapped in an array for some reason
        # unwrap it
        return self._inner.lambda_best_.item(0)

    @property
    def lambda_best_inx_(self) -> float:
        # lambda_max_inx_ is a scalar, but lambda_best_inx_ is wrapped in an array for some reason
        # unwrap it
        return self._inner.lambda_best_inx_.item(0)

    ######
    # Internal properties to determine which lambda to use for prediction, based on self.use_lambda_1se setting

    @property
    def _lambda_for_prediction_(self) -> float:
        if self.use_lambda_1se:
            return self.lambda_best_
        else:
            return self.lambda_max_

    @property
    def _lambda_inx_for_prediction_(self) -> float:
        if self.use_lambda_1se:
            return self.lambda_best_inx_
        else:
            return self.lambda_max_inx_

    ######

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
        groups: Optional[np.ndarray] = None,
        **kwargs,
    ) -> Self:
        # just in case, make sure the glmnet wrapper has been applied
        # (consider checking if already wrapped first, so we don't wrap an already-wrapped function?)
        apply_glmnet_wrapper()

        if self.internal_cv is not None:
            # Set a new attribute on the inner glmnet.LogitNet object.
            # This will get picked up by our wrapped version of _score_lambda_path.
            # See https://github.com/civisanalytics/python-glmnet/blob/813c06f5fcc9604d8e445bd4992f53c4855cc7cb/glmnet/logistic.py#L245
            self._inner._cv_override = self.internal_cv

            # Fill wrapper's n_splits from internal_cv
            self.n_splits = self.internal_cv.get_n_splits()

            # Check n_splits, then fill wrapped object's n_splits accordingly.
            if self.n_splits < 3:
                logger.warning(
                    f"Cross-validation strategy only performs {self.n_splits} splits. Python-Glmnet will not perform cross validation unless n_splits >= 3. We are setting the wrapped glmnet object's n_splits=3 to avoid this issue."
                )
                self._inner.n_splits = 3
            else:
                self._inner.n_splits = self.n_splits

        if groups is None and self.require_cv_group_labels:
            raise ValueError(
                "GlmnetLogitNetWrapper requires groups parameter in fit() call because require_cv_group_labels was set to True."
            )

        if self.class_weight is not None:
            # Use sklearn to compute class weights, then map to individual sample weights
            # Note: these weights are not necessarily normalized to sum to 1
            sample_weight_computed = sklearn.utils.class_weight.compute_sample_weight(
                class_weight=self.class_weight, y=y
            )
            if sample_weight is None:
                # No sample weights were provided. Just use the ones derived from class weights.
                sample_weight = sample_weight_computed
            else:
                # Sample weights were already provided. We need to combine with class-derived weights.
                # First, confirm shape matches
                if sample_weight.shape[0] != sample_weight_computed.shape[0]:
                    raise ValueError(
                        "Provided sample_weight has different number of samples than y."
                    )
                # Then, multiply the two
                sample_weight = sample_weight * sample_weight_computed

        # Fit as usual
        if sample_weight is not None:
            # To be safe, normalize weights to sum to 1
            sample_weight = np.array(sample_weight)
            sample_weight /= np.sum(sample_weight)
        self._inner = self._inner.fit(
            X=X, y=y, sample_weight=sample_weight, groups=groups, **kwargs
        )

        # Add properties to be compatible with sklearn API
        self.n_features_in_ = X.shape[1]

        feature_names = _get_feature_names(X)
        # If previously fitted, delete attribute
        if hasattr(self, "feature_names_in_"):
            delattr(self, "feature_names_in_")
        # Set new attribute if feature names are available (otherwise leave unset)
        if feature_names is not None:
            self.feature_names_in_ = feature_names

        # Add our own extra properties
        self.n_train_samples_ = X.shape[0]

        return self

    ######
    # Allow user to choose which lambda to use as default

    def predict(
        self, X: np.ndarray, lamb: Optional[Union[float, np.ndarray]] = None
    ) -> np.ndarray:
        return self._inner.predict(
            X, lamb=self._lambda_for_prediction_ if lamb is None else lamb
        )

    @staticmethod
    def _reshape_logits_after_squeeze(
        logits: np.ndarray, n_classes: int, n_lambdas: int
    ) -> np.ndarray:
        """
        Reshape logits after internal LogitNet does a squeeze().

        Input is squeeze(arr),
            where arr is an array of shape (n_samples, n_classes, n_lambda) if multiclass,
            or shape (n_samples, 1, n_lambda) if binary.

        Output:
            For multiclass:
            - With multiple lambdas, the shape should be (n_samples, n_classes, n_lambdas).
            - With a single lambda, the shape should be (n_samples, n_classes).

            For binary:
            - With multiple lambdas, the shape should be (n_samples, 1, n_lambdas).
            - With a single lambda, the shape should be (n_samples,)

        This extends sklearn convention to allow multiple lambdas.
        Sklearn convention is to return logit shape (n_samples, n_classes) in multiclass case, or (n_samples,) in binary case.
        """
        if n_classes == 2:  # Binary case
            if n_lambdas == 1:
                # The shape will be (n_samples,)
                return logits.reshape(
                    -1,
                )
            else:
                # The shape will be (n_samples, 1, n_lambdas)
                return logits.reshape(-1, 1, n_lambdas)
        else:  # Multiclass case
            if n_lambdas == 1:
                # The shape will be (n_samples, n_classes)
                return logits.reshape(-1, n_classes)
            else:
                # The shape will be (n_samples, n_classes, n_lambdas)
                return logits.reshape(-1, n_classes, n_lambdas)

    def decision_function(
        self, X: np.ndarray, lamb: Optional[Union[float, np.ndarray]] = None
    ) -> np.ndarray:
        """Override decision_function to use the selected default lambda, and to return shapes compatible with sklearn conventions."""
        # Per sklearn convention:
        # decision_function() shape should return shape (n_samples, ) in binary case, or (n_samples, n_classes) in multiclass case.
        # But this model’s decision_function accepts an optional parameter lamb, which can be a single float by default, or a numpy array of floats.
        # These values are hyperparameter values at which the model can be evaluated.
        # If multiple lamb’s are provided, we should extend the shape with an extra dimension of size n_lamb.
        # See _reshape_logits_after_squeeze documentation and tests.

        if lamb is None:
            lamb = self._lambda_for_prediction_
        logits = self._inner.decision_function(X, lamb=lamb)
        # The inner function starts with an array of shape (n_samples, n_classes, n_lambda) if multiclass or (n_samples, 1, n_lambda) if binary,
        # but then runs squeeze() to remove any axes of length one.
        # We pick it up from there and add back any extra axes as needed.
        return self._reshape_logits_after_squeeze(
            logits=logits,
            n_classes=len(self.classes_),
            n_lambdas=np.atleast_1d(lamb).shape[0],
        )

    def predict_proba(
        self, X: np.ndarray, lamb: Optional[Union[float, np.ndarray]] = None
    ) -> np.ndarray:
        """
        Override predict_proba not just to use the selected default lambda, but also to properly handle normalization in multiclass setting.

        Civis Glmnet's predict_proba divides the per-class probabilities vector by its sum. Instead we should use softmax to normalize probabilities to sum to 1.
        This will be consistent with how sklearn and glmnet handle multinomial regression — also known as *softmax* regression.
        See also https://en.wikipedia.org/wiki/Multinomial_logistic_regression#As_a_set_of_independent_binary_regressions

        Output will have shape (n_samples, n_classes), even in binary case (n_classes == 2).
        predict_proba can also accept several lambda values, in which case the shape will be (n_samples, n_classes, n_lambdas).
        """
        # See _reshape_logits_after_squeeze documentation and tests for expected logits shape.
        logits = self.decision_function(X, lamb=lamb)

        # Convert logits to probabilities using sigmoid if binary, or softmax if multiclass.
        # If there are multiple lambdas, apply the conversion function separately for each lambda.
        if logits.ndim == 3:  # This means we have multiple lambdas
            n_samples, _, n_lambdas = logits.shape
            # Initialize an empty array to store the probabilities
            probs = np.empty((n_samples, len(self.classes_), n_lambdas))
            for i in range(n_lambdas):
                probs[
                    :, :, i
                ] = genetools.stats.run_sigmoid_if_binary_and_softmax_if_multiclass(
                    logits[:, :, i]
                )
            return probs
        else:
            # Single lambda case
            # This function can already handle binary vs multiclass case.
            return genetools.stats.run_sigmoid_if_binary_and_softmax_if_multiclass(
                logits
            )

    # TODO: in predict(), decision_function(), predict_proba(), check feature names match those in fit()?
    # https://github.com/scikit-learn/scikit-learn/blob/d52e946fa4fca4282b0065ddcb0dd5d268c956e7/sklearn/base.py#L364

    @property
    def coef_(self) -> np.ndarray:
        return self._inner.coef_path_[:, :, self._lambda_inx_for_prediction_]

    @property
    def intercept_(self) -> np.ndarray:
        return self._inner.intercept_path_[:, self._lambda_inx_for_prediction_]

    def switch_lambda(self, use_lambda_1se: bool) -> GlmnetLogitNetWrapper:
        """Return copy (preserving fit) with different use_lambda_1se setting."""
        from copy import deepcopy

        # copy entirely, including inner object and underscore-suffixed properties
        copied_instance = deepcopy(self)
        # in tests, we make sure the _inner is also a copy, not a pointer to the same inner object
        copied_instance.use_lambda_1se = use_lambda_1se
        return copied_instance

    ######
    # Expose new properties based on the best lambda

    @property
    def cv_mean_score_final_(self) -> float:
        return self._inner.cv_mean_score_[self._lambda_inx_for_prediction_]

    @property
    def cv_standard_error_final_(self) -> float:
        return self._inner.cv_standard_error_[self._lambda_inx_for_prediction_]

    ######
    # Add analysis methods
    def plot_cross_validation_curve(
        self, scorer_name: Optional[str] = None, compare_to_sklearn: bool = True
    ):
        """
        Plot cross validation results versus lambda settings.
        Arguments:
            - scorer_name (str, optional): Sets the y-axis label for the plot. Defaults to self.scoring's name, or "Score" if self.scoring was not set.
            - compare_to_sklearn (bool, default True): Whether to compare to scikit-learn LogisticRegression's default lambda=1/n_train_samples (at C=1.0).
        Returns matplotlib figure.
        """
        import matplotlib.pyplot as plt

        fig = plt.figure()
        plt.errorbar(
            np.log(self.lambda_path_), self.cv_mean_score_, yerr=self.cv_standard_error_
        )

        plt.axvline(np.log(self.lambda_best_), color="k", label="lambda_1se")
        plt.axvline(np.log(self.lambda_max_), color="r", label="lambda_max")

        if compare_to_sklearn:
            plt.axvline(
                np.log(1 / self.n_train_samples_),
                color="blue",
                linestyle="dashed",
                label="sklearn LogisticReg",
            )

        plt.xlabel("log(lambda)")

        if scorer_name is None:
            # Get scorer name, if it was not provided by the user
            # Model.scoring is a function, a string, or None
            if self.scoring is None:
                scorer_name = "Score"
            elif isinstance(self.scoring, Callable):
                if hasattr(self.scoring, "_score_func") and hasattr(
                    self.scoring._score_func, "__name__"
                ):
                    # Reach into the inner _score_func if it exists
                    scorer_name = self.scoring._score_func.__name__
                elif hasattr(self.scoring, "__name__"):
                    # Might have a name directly
                    scorer_name = self.scoring.__name__
                elif hasattr(self.scoring, "__class__") and hasattr(
                    self.scoring.__class__, "__name__"
                ):
                    # Use class name otherwise
                    scorer_name = self.scoring.__class__.__name__
            else:
                scorer_name = str(self.scoring)

        plt.ylabel(scorer_name)

        # Plot legend outside the figure
        plt.legend(
            bbox_to_anchor=(1.05, 0.5),
            loc="center left",
            borderaxespad=0.0,
            title="Lambda",
        )
        return fig
