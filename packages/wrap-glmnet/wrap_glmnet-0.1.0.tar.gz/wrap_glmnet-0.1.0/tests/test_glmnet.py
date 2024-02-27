import functools
import numpy as np
import pandas as pd
import sklearn.base
import pytest
from wrap_glmnet import GlmnetLogitNetWrapper
import glmnet.scorer
from sklearn.metrics import matthews_corrcoef
from sklearn.model_selection import StratifiedGroupKFold


@pytest.fixture
def data():
    np.random.seed(0)
    X = pd.DataFrame(np.random.randn(15, 5)).rename(columns=lambda s: f"col{s}")
    y = np.array(["Covid19", "Healthy", "HIV"] * 5)
    participant_label = np.array(
        [
            "covid1",
            "healthy1",
            "hiv1",
            "covid2",
            "healthy2",
            "hiv2",
            "covid3",
            "healthy3",
            "hiv3",
            "covid1",
            "healthy1",
            "hiv1",
            "covid2",
            "healthy2",
            "hiv2",
        ]
    )
    return X, y, participant_label


@pytest.fixture
def data_binary():
    np.random.seed(0)
    X = pd.DataFrame(np.random.randn(24, 5)).rename(columns=lambda s: f"col{s}")
    y = np.array(["Covid19", "Healthy"] * 12)
    participant_label = np.array(
        [
            "covid1",
            "healthy1",
            "covid2",
            "healthy2",
            "covid3",
            "healthy3",
        ]
        * 4
    )
    return X, y, participant_label


@pytest.mark.parametrize("use_lambda_1se", [True, False])
@pytest.mark.parametrize("alpha", [1.0, 0.5, 0.0])
def test_sklearn_clonable(data, use_lambda_1se: bool, alpha: float):
    X, y, groups = data
    estimator = GlmnetLogitNetWrapper(
        use_lambda_1se=use_lambda_1se, alpha=alpha, n_lambda=5, n_splits=3
    )
    # Check that supports cloning with sklearn.base.clone
    estimator_clone = sklearn.base.clone(estimator)

    # not fitted yet
    assert not hasattr(estimator, "classes_")
    assert not hasattr(estimator_clone, "classes_")
    # inner and outer parameters preserved (makes sure that get_params() is implemented correctly)
    assert estimator.use_lambda_1se == estimator_clone.use_lambda_1se == use_lambda_1se
    assert estimator.alpha == estimator_clone.alpha == alpha

    # fit
    estimator = estimator.fit(X, y, groups=groups)

    # confirm fitted
    estimator.classes_ = np.array(["a", "b"])
    assert hasattr(estimator, "classes_")
    # inner and outer parameters preserved
    assert estimator.use_lambda_1se == estimator_clone.use_lambda_1se == use_lambda_1se
    assert estimator.alpha == estimator_clone.alpha == alpha

    # confirm clone is not fitted
    estimator_clone_2 = sklearn.base.clone(estimator)
    assert not hasattr(estimator_clone_2, "classes_")
    # inner and outer parameters preserved
    assert (
        estimator.use_lambda_1se == estimator_clone_2.use_lambda_1se == use_lambda_1se
    )
    assert estimator.alpha == estimator_clone_2.alpha == alpha


@pytest.mark.parametrize(
    "dataset", [pytest.lazy_fixture("data"), pytest.lazy_fixture("data_binary")]
)
def test_scorer(dataset):
    for scorer in [
        GlmnetLogitNetWrapper.rocauc_scorer,
        glmnet.scorer.make_scorer(matthews_corrcoef),
        GlmnetLogitNetWrapper.deviance_scorer,
        None,  # default scorer
    ]:
        X, y, groups = dataset
        clf = GlmnetLogitNetWrapper(alpha=1, n_lambda=5, n_splits=3, scoring=scorer)
        clf = clf.fit(X, y, groups=groups)
        assert clf.cv_mean_score_final_ is not None, f"scorer {scorer} failed"


def test_has_sklearn_properties(data):
    X, y, groups = data
    clf = GlmnetLogitNetWrapper(
        alpha=1, n_lambda=5, n_splits=3, scoring=GlmnetLogitNetWrapper.rocauc_scorer
    )

    # Fit with feature names first
    clf = clf.fit(X, y, groups=groups)
    # make sure these attributes exist
    assert clf.n_features_in_ == 5
    assert np.array_equal(
        clf.feature_names_in_, ["col0", "col1", "col2", "col3", "col4"]
    )
    assert np.array_equal(clf.classes_, ["Covid19", "HIV", "Healthy"])
    assert clf.predict(X).shape == (15,)
    assert clf.predict_proba(X).shape == (15, 3)
    # make sure the labels are encoded
    assert all(predicted_label in clf.classes_ for predicted_label in clf.predict(X))
    assert clf.coef_.shape == (3, 5)

    # Refit without feature names
    clf = clf.fit(X.values, y, groups=groups)
    assert clf.n_features_in_ == 5
    assert not hasattr(clf, "feature_names_in_")

    # Confirm again that cloning works, even after a real fit
    clf = sklearn.base.clone(clf)
    assert not hasattr(clf, "n_features_in_")
    assert not hasattr(clf, "feature_names_in_")
    assert not hasattr(clf, "classes_")


def test_lambda(data):
    X, y, groups = data
    clf = GlmnetLogitNetWrapper(
        alpha=1, n_lambda=100, n_splits=3, scoring=GlmnetLogitNetWrapper.rocauc_scorer
    ).fit(X, y, groups=groups)

    # lambda_max_ is always a scalar
    assert np.isscalar(clf.lambda_max_)
    assert np.isscalar(clf._inner.lambda_max_)
    assert clf._inner.lambda_max_ == clf.lambda_max_

    # lambda_best_ is wrapped in an array, but we unwrap it
    assert np.isscalar(clf.lambda_best_)
    assert not np.isscalar(clf._inner.lambda_best_)
    assert clf._inner.lambda_best_[0] == clf.lambda_best_

    # lambda_max_inx_ is always a scalar
    assert np.isscalar(clf.lambda_max_inx_)
    assert np.isscalar(clf._inner.lambda_max_inx_)
    assert clf._inner.lambda_max_inx_ == clf.lambda_max_inx_

    # lambda_best_inx_ is wrapped in an array, but we unwrap it
    assert np.isscalar(clf.lambda_best_inx_)
    assert not np.isscalar(clf._inner.lambda_best_inx_)
    assert clf._inner.lambda_best_inx_[0] == clf.lambda_best_inx_

    # test selection of the lambda we want to use
    lambda_best_performance: float = clf.lambda_max_
    lambda_best_performance_inx: int = clf.lambda_max_inx_
    lambda_1se_performance_simpler_model: float = clf.lambda_best_
    lambda_1se_performance_simpler_model_inx: int = clf.lambda_best_inx_
    assert (
        lambda_best_performance != lambda_1se_performance_simpler_model
    ), "lambda_best_performance should not equal lambda_1se_performance_simpler_model, otherwise our test is meaningless"
    sample_input = np.random.randn(1, 5)

    def test(clf, correct_value, correct_index, incorrect_value, incorrect_index):
        assert clf._lambda_for_prediction_ == correct_value
        assert clf._lambda_inx_for_prediction_ == correct_index

        assert np.array_equal(
            clf.predict(sample_input), clf.predict(sample_input, lamb=correct_value)
        )

        assert np.array_equal(
            clf.predict_proba(sample_input),
            clf.predict_proba(sample_input, lamb=correct_value),
        )
        assert not np.array_equal(
            clf.predict_proba(sample_input),
            clf.predict_proba(sample_input, lamb=incorrect_value),
        )

        assert np.array_equal(
            clf.decision_function(sample_input),
            clf.decision_function(sample_input, lamb=correct_value),
        )
        assert not np.array_equal(
            clf.decision_function(sample_input),
            clf.decision_function(sample_input, lamb=incorrect_value),
        )

        assert np.array_equal(clf.coef_, clf.coef_path_[:, :, correct_index])
        assert not np.array_equal(clf.coef_, clf.coef_path_[:, :, incorrect_index])

        assert np.array_equal(clf.intercept_, clf.intercept_path_[:, correct_index])
        assert not np.array_equal(
            clf.intercept_, clf.intercept_path_[:, incorrect_index]
        )

        assert np.array_equal(
            clf.cv_mean_score_final_, clf.cv_mean_score_[correct_index]
        )
        assert not np.array_equal(
            clf.cv_mean_score_final_, clf.cv_mean_score_[incorrect_index]
        )

        assert np.array_equal(
            clf.cv_standard_error_final_, clf.cv_standard_error_[correct_index]
        )
        assert not np.array_equal(
            clf.cv_standard_error_final_, clf.cv_standard_error_[incorrect_index]
        )

    test_confirm_lambda1se = functools.partial(
        test,
        correct_value=lambda_1se_performance_simpler_model,
        correct_index=lambda_1se_performance_simpler_model_inx,
        incorrect_value=lambda_best_performance,
        incorrect_index=lambda_best_performance_inx,
    )
    test_confirm_lambda_max = functools.partial(
        test,
        correct_value=lambda_best_performance,
        correct_index=lambda_best_performance_inx,
        incorrect_value=lambda_1se_performance_simpler_model,
        incorrect_index=lambda_1se_performance_simpler_model_inx,
    )

    # test with default first
    assert clf.use_lambda_1se
    test_confirm_lambda1se(
        clf=clf,
    )

    # switch to non-default and retest
    clf.use_lambda_1se = False
    assert not clf.use_lambda_1se
    test_confirm_lambda_max(
        clf=clf,
    )

    # use the copy and switch function, then retest
    assert not clf.use_lambda_1se
    copied_clf = clf.switch_lambda(use_lambda_1se=False)  # expected: no change
    assert not copied_clf.use_lambda_1se
    test_confirm_lambda_max(
        clf=copied_clf,
    )
    assert copied_clf.n_train_samples_ == clf.n_train_samples_
    assert id(copied_clf) != id(clf)
    # make sure the _inner is also a copy, not a pointer to the same inner object
    assert id(copied_clf._inner) != id(clf._inner)
    copied_clf.plot_cross_validation_curve()

    copied_clf = copied_clf.switch_lambda(use_lambda_1se=True)  # expected: change
    assert copied_clf.use_lambda_1se
    test_confirm_lambda1se(
        clf=copied_clf,
    )
    assert copied_clf.n_train_samples_ == clf.n_train_samples_
    assert id(copied_clf) != id(clf)
    # make sure the _inner is also a copy, not a pointer to the same inner object
    assert id(copied_clf._inner) != id(clf._inner)
    copied_clf.plot_cross_validation_curve()


def test_require_cv_group_labels(data):
    # Confirm require_cv_group_labels is respected
    X, y, groups = data

    clf = GlmnetLogitNetWrapper(
        require_cv_group_labels=False,
        alpha=1,
        n_lambda=5,
        n_splits=3,
        scoring=GlmnetLogitNetWrapper.rocauc_scorer,
    )
    clf = clf.fit(X, y, groups=groups)
    clf = clf.fit(X, y)

    clf = GlmnetLogitNetWrapper(
        require_cv_group_labels=True,
        alpha=1,
        n_lambda=5,
        n_splits=3,
        scoring=GlmnetLogitNetWrapper.rocauc_scorer,
    )
    clf = clf.fit(X, y, groups=groups)
    with pytest.raises(
        ValueError,
        match="requires groups parameter in fit()",
    ):
        clf = clf.fit(X, y)


def test_accept_cv_splitter(data):
    # Confirms that we can pass a splitter to internal_cv and have it incorporated by glmnet,
    # i.e. our wrapper of _score_lambda_path is applied (tested in test_cv_split_wrapper_applied),
    # and the inner model's _cv is set to our provided CV splitter (tested here).

    X, y, groups = data
    splitter = StratifiedGroupKFold(n_splits=4)

    clf = GlmnetLogitNetWrapper(
        alpha=1,
        n_lambda=5,
        scoring=GlmnetLogitNetWrapper.rocauc_scorer,
        internal_cv=splitter,
        # notice we are not passing n_splits. it gets defaulted to n_splits=3 at initialization
    )
    clf = clf.fit(X, y, groups=groups)
    assert clf.cv_mean_score_final_ is not None, "no CV score generated"
    assert (
        clf._inner._cv == splitter
    ), "clf._inner._cv should be replaced by our splitter"
    assert (
        clf.n_splits == 4
    ), "clf.n_splits should be autofilled by our splitter's n_splits"
    assert (
        clf._inner.n_splits == 4
    ), "clf._inner.n_splits should be replaced by our splitter's n_splits"


def test_cv_split_wrapper_applied(data):
    # separating this out from the above test in case the imports change anything
    # __wrapped__ is set by functools.wraps
    import glmnet.util
    import glmnet.logistic

    assert hasattr(glmnet.util._score_lambda_path, "__wrapped__")
    assert hasattr(glmnet.logistic._score_lambda_path, "__wrapped__")
    assert hasattr(glmnet.util._fit_and_score, "__wrapped__")

    X, y, groups = data
    n_splits = 3
    splitter = StratifiedGroupKFold(n_splits=n_splits)
    n_lambda = 5

    clf = GlmnetLogitNetWrapper(
        alpha=1,
        n_lambda=n_lambda,
        scoring=GlmnetLogitNetWrapper.rocauc_scorer,
        # notice we are not passing n_splits
        internal_cv=splitter,
        store_cv_predicted_probabilities=True,
    )
    clf = clf.fit(X, y, groups=groups)

    # Confirm that clf._cv was replaced with clf._cv_override
    assert clf._cv == clf._cv_override

    # Confirm that the expected new attributes were set and have the expected shapes.
    assert hasattr(clf, "_cv_scores_") and hasattr(clf, "cv_pred_probs_")
    assert clf._cv_scores_ is not None and clf.cv_pred_probs_ is not None
    # _cv_scores_ is a list of length n_folds. Each entry is a 1d array of length n_lambda. These are scores for each value of lambda over all CV folds.
    assert len(clf._cv_scores_) == n_splits
    assert clf._cv_scores_[0].shape[0] == n_lambda
    # cv_pred_probs_ has shape (n_samples, n_classes, n_lambda), with the samples in original order
    assert clf.cv_pred_probs_.shape == (15, 3, n_lambda)

    # still wrapped
    assert hasattr(glmnet.util._score_lambda_path, "__wrapped__")
    assert hasattr(glmnet.logistic._score_lambda_path, "__wrapped__")
    assert hasattr(glmnet.util._fit_and_score, "__wrapped__")


def test_nsplits_below_3_still_accepted(data):
    # glmnet special cases n_splits<3, but we override that

    X, y, groups = data
    splitter = StratifiedGroupKFold(n_splits=2)

    clf = GlmnetLogitNetWrapper(
        alpha=1,
        n_lambda=5,
        scoring=GlmnetLogitNetWrapper.rocauc_scorer,
        internal_cv=splitter,
        # notice we are not passing n_splits. it gets defaulted to n_splits=3 at initialization
    )
    clf = clf.fit(X, y, groups=groups)
    assert clf.cv_mean_score_final_ is not None, "no CV score generated"
    assert (
        clf.n_splits == 2
    ), "clf.n_splits should be autofilled by our splitter's n_splits"
    assert (
        clf._inner.n_splits == 3
    ), "clf._inner.n_splits should be falsely set to 3 to avoid glmnet not doing CV"


def test_nsplits_below_3_still_accepted_also_pass_nsplits_explicitly(data):
    # glmnet special cases n_splits<3, but we override that

    X, y, groups = data
    splitter = StratifiedGroupKFold(n_splits=2)

    clf = GlmnetLogitNetWrapper(
        alpha=1,
        n_lambda=5,
        scoring=GlmnetLogitNetWrapper.rocauc_scorer,
        internal_cv=splitter,
        n_splits=2,  # variant: pass explicitly
    )
    clf = clf.fit(X, y, groups=groups)
    assert clf.cv_mean_score_final_ is not None, "no CV score generated"
    assert (
        clf.n_splits == 2
    ), "clf.n_splits should be autofilled by our splitter's n_splits"
    assert (
        clf._inner.n_splits == 3
    ), "clf._inner.n_splits should be falsely set to 3 to avoid glmnet not doing CV"


def test_plot(data):
    X, y, groups = data
    clf = GlmnetLogitNetWrapper(
        alpha=1, n_lambda=5, n_splits=3, scoring=GlmnetLogitNetWrapper.rocauc_scorer
    )
    clf = clf.fit(X, y, groups=groups)
    clf.plot_cross_validation_curve("ROC AUC")


def test_with_single_row(data):
    # This was an edge case that was failing in the past.
    # We expand on this in further tests below, but this is a first minimal pass.
    X, y, _ = data
    clf = GlmnetLogitNetWrapper().fit(X, y)
    assert clf.decision_function(X.values[0:1, :]).shape == (1, 3)
    assert clf.predict_proba(X.values[0:1, :]).shape == (1, 3)

    y_binary = y.copy()
    y_binary[y_binary == "HIV"] = "Covid19"
    clf = GlmnetLogitNetWrapper().fit(X, y_binary)
    assert clf.decision_function(X.values[0:1, :]).shape == (1,)
    assert clf.predict_proba(X.values[0:1, :]).shape == (1, 2)


def test_decision_function_shape_matches_sklearn_convention():
    """
    Expected decision_function shapes:
    For multiclass:
    - With multiple lambdas, the shape should be (n_samples, n_classes, n_lambdas).
    - With a single lambda, the shape should be (n_samples, n_classes).

    For binary:
    - With multiple lambdas, the shape should be (n_samples, 1, n_lambdas).
    - With a single lambda, the shape should be (n_samples,)
    """
    # Before internal LogitNet decision_function does squeeze(), we have an array of shape (n_samples, n_classes, n_lambda)
    # Then squeeze will:
    # - drop the last dimension (lambda) when we are predicting for a single value of lambda
    # - drop the middle dimension (class) when we are predicting from a binomial model
    # Let's test these cases.

    # - Multiclass, multiple lambdas
    assert GlmnetLogitNetWrapper._reshape_logits_after_squeeze(
        logits=np.ones((10, 3, 2)).squeeze(),
        n_classes=3,
        n_lambdas=2,
    ).shape == (10, 3, 2)

    # - Multiclass, single lambda
    assert GlmnetLogitNetWrapper._reshape_logits_after_squeeze(
        logits=np.ones((10, 3, 1)).squeeze(),
        n_classes=3,
        n_lambdas=1,
    ).shape == (10, 3)

    # - Binary, multiple lambdas
    assert GlmnetLogitNetWrapper._reshape_logits_after_squeeze(
        logits=np.ones((10, 1, 2)).squeeze(),
        n_classes=2,
        n_lambdas=2,
    ).shape == (10, 1, 2)

    # - Binary, single lambda
    assert GlmnetLogitNetWrapper._reshape_logits_after_squeeze(
        logits=np.ones((10, 1, 1)).squeeze(),
        n_classes=2,
        n_lambdas=1,
    ).shape == (10,)

    # - Multiclass, multiple lambdas, and a single sample
    assert GlmnetLogitNetWrapper._reshape_logits_after_squeeze(
        logits=np.ones((1, 3, 2)).squeeze(),
        n_classes=3,
        n_lambdas=2,
    ).shape == (1, 3, 2)

    # - Multiclass, single lambda, and a single sample
    assert GlmnetLogitNetWrapper._reshape_logits_after_squeeze(
        logits=np.ones((1, 3, 1)).squeeze(),
        n_classes=3,
        n_lambdas=1,
    ).shape == (1, 3)

    # - Binary, multiple lambdas, and a single sample
    assert GlmnetLogitNetWrapper._reshape_logits_after_squeeze(
        logits=np.ones((1, 1, 2)).squeeze(),
        n_classes=2,
        n_lambdas=2,
    ).shape == (1, 1, 2)

    # - Binary, single lambda, and a single sample
    assert GlmnetLogitNetWrapper._reshape_logits_after_squeeze(
        logits=np.ones((1, 1, 1)).squeeze(),
        n_classes=2,
        n_lambdas=1,
    ).shape == (1,)


def test_decision_function_and_predict_proba_shapes_match_sklearn_conventions(data):
    """
    Expected decision_function shape is as document above.

    Expected predict_proba shape is (n_samples, n_classes) or (n_samples, n_classes, n_lambda),
    regardless of whether the problem is binary or multiclass.

    Here, we test in the whole classifier wrapper.
    """
    X, y_multiclass, _ = data
    X = X.to_numpy()

    y_binary = y_multiclass.copy()
    y_binary[y_binary == "HIV"] = "Covid19"

    clf_binary = GlmnetLogitNetWrapper().fit(X, y_binary)
    clf_multiclass = GlmnetLogitNetWrapper().fit(X, y_multiclass)
    n_multiclass_classes = len(np.unique(y_multiclass))

    # Test with input as full 2d array, or just as the first row of the 2d array.
    for input in [X, X[0:1, :]]:
        ## Single lambdas:
        # Binary case
        assert clf_binary.decision_function(input, lamb=None).shape == (input.shape[0],)
        assert clf_binary.predict_proba(input, lamb=None).shape == (input.shape[0], 2)
        # Multiclass case
        assert clf_multiclass.decision_function(input, lamb=None).shape == (
            input.shape[0],
            n_multiclass_classes,
        )
        assert clf_multiclass.predict_proba(input, lamb=None).shape == (
            input.shape[0],
            n_multiclass_classes,
        )

        ## Multiple lambdas:
        lambdas_binary = np.array([clf_binary.lambda_max_, clf_binary.lambda_best_])
        lambdas_multiclass = np.array(
            [clf_multiclass.lambda_max_, clf_multiclass.lambda_best_]
        )
        # Binary case
        assert clf_binary.decision_function(input, lamb=lambdas_binary).shape == (
            input.shape[0],
            1,
            len(lambdas_binary),
        )
        assert clf_binary.predict_proba(input, lamb=lambdas_binary).shape == (
            input.shape[0],
            2,
            len(lambdas_binary),
        )
        # Multiclass case
        assert clf_multiclass.decision_function(
            input, lamb=lambdas_multiclass
        ).shape == (input.shape[0], n_multiclass_classes, len(lambdas_multiclass))
        assert clf_multiclass.predict_proba(input, lamb=lambdas_multiclass).shape == (
            input.shape[0],
            n_multiclass_classes,
            len(lambdas_multiclass),
        )
