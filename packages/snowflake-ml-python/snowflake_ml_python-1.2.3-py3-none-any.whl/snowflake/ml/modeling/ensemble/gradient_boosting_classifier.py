#
# This code is auto-generated using the sklearn_wrapper_template.py_template template.
# Do not modify the auto-generated code(except automatic reformatting by precommit hooks).
#
import inspect
import os
import posixpath
from typing import Iterable, Optional, Union, List, Any, Dict, Callable, Set
from typing_extensions import TypeGuard
from uuid import uuid4

import cloudpickle as cp
import pandas as pd
import numpy as np
from numpy import typing as npt

import numpy
import sklearn
import sklearn.ensemble
from sklearn.utils.metaestimators import available_if

from snowflake.ml.modeling.framework.base import BaseTransformer, _process_cols
from snowflake.ml._internal import telemetry
from snowflake.ml._internal.exceptions import error_codes, exceptions, modeling_error_messages
from snowflake.ml._internal.env_utils import SNOWML_SPROC_ENV
from snowflake.ml._internal.utils import pkg_version_utils, identifier
from snowflake.snowpark import DataFrame, Session
from snowflake.snowpark._internal.type_utils import convert_sp_to_sf_type
from snowflake.ml.modeling._internal.snowpark_implementations.snowpark_handlers import SnowparkHandlers as HandlersImpl
from snowflake.ml.modeling._internal.model_trainer_builder import ModelTrainerBuilder
from snowflake.ml.modeling._internal.model_trainer import ModelTrainer
from snowflake.ml.modeling._internal.estimator_utils import (
    gather_dependencies,
    original_estimator_has_callable,
    transform_snowml_obj_to_sklearn_obj,
    validate_sklearn_args,
)
from snowflake.ml.modeling._internal.estimator_protocols import TransformerHandlers

from snowflake.ml.model.model_signature import (
    DataType,
    FeatureSpec,
    ModelSignature,
    _infer_signature,
    _rename_signature_with_snowflake_identifiers,
    BaseFeatureSpec,
)
from snowflake.ml.model._signatures import utils as model_signature_utils

_PROJECT = "ModelDevelopment"
# Derive subproject from module name by removing "sklearn"
# and converting module name from underscore to CamelCase
# e.g. sklearn.linear_model -> LinearModel.
_SUBPROJECT = "".join([s.capitalize() for s in "sklearn.ensemble".replace("sklearn.", "").split("_")])


def _is_fit_predict_method_enabled() -> Callable[[Any], bool]:
    def check(self: BaseTransformer) -> TypeGuard[Callable[..., object]]:
        return False and callable(getattr(self._sklearn_object, "fit_predict", None))
    return check


def _is_fit_transform_method_enabled() -> Callable[[Any], bool]:
    def check(self: BaseTransformer) -> TypeGuard[Callable[..., object]]:
        return False and callable(getattr(self._sklearn_object, "fit_transform", None))
    return check


class GradientBoostingClassifier(BaseTransformer):
    r"""Gradient Boosting for classification
    For more details on this class, see [sklearn.ensemble.GradientBoostingClassifier]
    (https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html)

    Parameters
    ----------

    input_cols: Optional[Union[str, List[str]]]
        A string or list of strings representing column names that contain features.
        If this parameter is not specified, all columns in the input DataFrame except
        the columns specified by label_cols, sample_weight_col, and passthrough_cols
        parameters are considered input columns. Input columns can also be set after
        initialization with the `set_input_cols` method.
    
    label_cols: Optional[Union[str, List[str]]]
        A string or list of strings representing column names that contain labels.
        Label columns must be specified with this parameter during initialization
        or with the `set_label_cols` method before fitting.

    output_cols: Optional[Union[str, List[str]]]
        A string or list of strings representing column names that will store the
        output of predict and transform operations. The length of output_cols must
        match the expected number of output columns from the specific predictor or
        transformer class used.
        If you omit this parameter, output column names are derived by adding an
        OUTPUT_ prefix to the label column names for supervised estimators, or
        OUTPUT_<IDX>for unsupervised estimators. These inferred output column names
        work for predictors, but output_cols must be set explicitly for transformers.
        In general, explicitly specifying output column names is clearer, especially
        if you don’t specify the input column names.
        To transform in place, pass the same names for input_cols and output_cols.
        be set explicitly for transformers. Output columns can also be set after
        initialization with the `set_output_cols` method.

    sample_weight_col: Optional[str]
        A string representing the column name containing the sample weights.
        This argument is only required when working with weighted datasets. Sample
        weight column can also be set after initialization with the
        `set_sample_weight_col` method.

    passthrough_cols: Optional[Union[str, List[str]]]
        A string or a list of strings indicating column names to be excluded from any
        operations (such as train, transform, or inference). These specified column(s)
        will remain untouched throughout the process. This option is helpful in scenarios
        requiring automatic input_cols inference, but need to avoid using specific
        columns, like index columns, during training or inference. Passthrough columns
        can also be set after initialization with the `set_passthrough_cols` method.

    drop_input_cols: Optional[bool], default=False
        If set, the response of predict(), transform() methods will not contain input columns.

    loss: {'log_loss', 'exponential'}, default='log_loss'
        The loss function to be optimized. 'log_loss' refers to binomial and
        multinomial deviance, the same as used in logistic regression.
        It is a good choice for classification with probabilistic outputs.
        For loss 'exponential', gradient boosting recovers the AdaBoost algorithm.

    learning_rate: float, default=0.1
        Learning rate shrinks the contribution of each tree by `learning_rate`.
        There is a trade-off between learning_rate and n_estimators.
        Values must be in the range `[0.0, inf)`.

    n_estimators: int, default=100
        The number of boosting stages to perform. Gradient boosting
        is fairly robust to over-fitting so a large number usually
        results in better performance.
        Values must be in the range `[1, inf)`.

    subsample: float, default=1.0
        The fraction of samples to be used for fitting the individual base
        learners. If smaller than 1.0 this results in Stochastic Gradient
        Boosting. `subsample` interacts with the parameter `n_estimators`.
        Choosing `subsample < 1.0` leads to a reduction of variance
        and an increase in bias.
        Values must be in the range `(0.0, 1.0]`.

    criterion: {'friedman_mse', 'squared_error'}, default='friedman_mse'
        The function to measure the quality of a split. Supported criteria are
        'friedman_mse' for the mean squared error with improvement score by
        Friedman, 'squared_error' for mean squared error. The default value of
        'friedman_mse' is generally the best as it can provide a better
        approximation in some cases.

    min_samples_split: int or float, default=2
        The minimum number of samples required to split an internal node:

        - If int, values must be in the range `[2, inf)`.
        - If float, values must be in the range `(0.0, 1.0]` and `min_samples_split`
          will be `ceil(min_samples_split * n_samples)`.

    min_samples_leaf: int or float, default=1
        The minimum number of samples required to be at a leaf node.
        A split point at any depth will only be considered if it leaves at
        least ``min_samples_leaf`` training samples in each of the left and
        right branches.  This may have the effect of smoothing the model,
        especially in regression.

        - If int, values must be in the range `[1, inf)`.
        - If float, values must be in the range `(0.0, 1.0)` and `min_samples_leaf`
          will be `ceil(min_samples_leaf * n_samples)`.

    min_weight_fraction_leaf: float, default=0.0
        The minimum weighted fraction of the sum total of weights (of all
        the input samples) required to be at a leaf node. Samples have
        equal weight when sample_weight is not provided.
        Values must be in the range `[0.0, 0.5]`.

    max_depth: int or None, default=3
        Maximum depth of the individual regression estimators. The maximum
        depth limits the number of nodes in the tree. Tune this parameter
        for best performance; the best value depends on the interaction
        of the input variables. If None, then nodes are expanded until
        all leaves are pure or until all leaves contain less than
        min_samples_split samples.
        If int, values must be in the range `[1, inf)`.

    min_impurity_decrease: float, default=0.0
        A node will be split if this split induces a decrease of the impurity
        greater than or equal to this value.
        Values must be in the range `[0.0, inf)`.

        The weighted impurity decrease equation is the following::

            N_t / N * (impurity - N_t_R / N_t * right_impurity
                                - N_t_L / N_t * left_impurity)

        where ``N`` is the total number of samples, ``N_t`` is the number of
        samples at the current node, ``N_t_L`` is the number of samples in the
        left child, and ``N_t_R`` is the number of samples in the right child.

        ``N``, ``N_t``, ``N_t_R`` and ``N_t_L`` all refer to the weighted sum,
        if ``sample_weight`` is passed.

    init: estimator or 'zero', default=None
        An estimator object that is used to compute the initial predictions.
        ``init`` has to provide :term:`fit` and :term:`predict_proba`. If
        'zero', the initial raw predictions are set to zero. By default, a
        ``DummyEstimator`` predicting the classes priors is used.

    random_state: int, RandomState instance or None, default=None
        Controls the random seed given to each Tree estimator at each
        boosting iteration.
        In addition, it controls the random permutation of the features at
        each split (see Notes for more details).
        It also controls the random splitting of the training data to obtain a
        validation set if `n_iter_no_change` is not None.
        Pass an int for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    max_features: {'sqrt', 'log2'}, int or float, default=None
        The number of features to consider when looking for the best split:

        - If int, values must be in the range `[1, inf)`.
        - If float, values must be in the range `(0.0, 1.0]` and the features
          considered at each split will be `max(1, int(max_features * n_features_in_))`.
        - If 'sqrt', then `max_features=sqrt(n_features)`.
        - If 'log2', then `max_features=log2(n_features)`.
        - If None, then `max_features=n_features`.

        Choosing `max_features < n_features` leads to a reduction of variance
        and an increase in bias.

        Note: the search for a split does not stop until at least one
        valid partition of the node samples is found, even if it requires to
        effectively inspect more than ``max_features`` features.

    verbose: int, default=0
        Enable verbose output. If 1 then it prints progress and performance
        once in a while (the more trees the lower the frequency). If greater
        than 1 then it prints progress and performance for every tree.
        Values must be in the range `[0, inf)`.

    max_leaf_nodes: int, default=None
        Grow trees with ``max_leaf_nodes`` in best-first fashion.
        Best nodes are defined as relative reduction in impurity.
        Values must be in the range `[2, inf)`.
        If `None`, then unlimited number of leaf nodes.

    warm_start: bool, default=False
        When set to ``True``, reuse the solution of the previous call to fit
        and add more estimators to the ensemble, otherwise, just erase the
        previous solution. See :term:`the Glossary <warm_start>`.

    validation_fraction: float, default=0.1
        The proportion of training data to set aside as validation set for
        early stopping. Values must be in the range `(0.0, 1.0)`.
        Only used if ``n_iter_no_change`` is set to an integer.

    n_iter_no_change: int, default=None
        ``n_iter_no_change`` is used to decide if early stopping will be used
        to terminate training when validation score is not improving. By
        default it is set to None to disable early stopping. If set to a
        number, it will set aside ``validation_fraction`` size of the training
        data as validation and terminate training when validation score is not
        improving in all of the previous ``n_iter_no_change`` numbers of
        iterations. The split is stratified.
        Values must be in the range `[1, inf)`.

    tol: float, default=1e-4
        Tolerance for the early stopping. When the loss is not improving
        by at least tol for ``n_iter_no_change`` iterations (if set to a
        number), the training stops.
        Values must be in the range `[0.0, inf)`.

    ccp_alpha: non-negative float, default=0.0
        Complexity parameter used for Minimal Cost-Complexity Pruning. The
        subtree with the largest cost complexity that is smaller than
        ``ccp_alpha`` will be chosen. By default, no pruning is performed.
        Values must be in the range `[0.0, inf)`.
        See :ref:`minimal_cost_complexity_pruning` for details.
    """

    def __init__(  # type: ignore[no-untyped-def]
        self,
        *,
        loss="log_loss",
        learning_rate=0.1,
        n_estimators=100,
        subsample=1.0,
        criterion="friedman_mse",
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.0,
        max_depth=3,
        min_impurity_decrease=0.0,
        init=None,
        random_state=None,
        max_features=None,
        verbose=0,
        max_leaf_nodes=None,
        warm_start=False,
        validation_fraction=0.1,
        n_iter_no_change=None,
        tol=0.0001,
        ccp_alpha=0.0,
        input_cols: Optional[Union[str, Iterable[str]]] = None,
        output_cols: Optional[Union[str, Iterable[str]]] = None,
        label_cols: Optional[Union[str, Iterable[str]]] = None,
        passthrough_cols: Optional[Union[str, Iterable[str]]] = None,
        drop_input_cols: Optional[bool] = False,
        sample_weight_col: Optional[str] = None,
    ) -> None:
        super().__init__()

        self.set_input_cols(input_cols)
        self.set_output_cols(output_cols)
        self.set_label_cols(label_cols)
        self.set_passthrough_cols(passthrough_cols)
        self.set_drop_input_cols(drop_input_cols)
        self.set_sample_weight_col(sample_weight_col)
        self._use_external_memory_version = False
        self._batch_size = -1        
        deps: Set[str] = set([f'numpy=={np.__version__}', f'scikit-learn=={sklearn.__version__}', f'cloudpickle=={cp.__version__}'])
        
        self._deps = list(deps)
        
        init_args = {'loss':(loss, "log_loss", False),
            'learning_rate':(learning_rate, 0.1, False),
            'n_estimators':(n_estimators, 100, False),
            'subsample':(subsample, 1.0, False),
            'criterion':(criterion, "friedman_mse", False),
            'min_samples_split':(min_samples_split, 2, False),
            'min_samples_leaf':(min_samples_leaf, 1, False),
            'min_weight_fraction_leaf':(min_weight_fraction_leaf, 0.0, False),
            'max_depth':(max_depth, 3, False),
            'min_impurity_decrease':(min_impurity_decrease, 0.0, False),
            'init':(init, None, False),
            'random_state':(random_state, None, False),
            'max_features':(max_features, None, False),
            'verbose':(verbose, 0, False),
            'max_leaf_nodes':(max_leaf_nodes, None, False),
            'warm_start':(warm_start, False, False),
            'validation_fraction':(validation_fraction, 0.1, False),
            'n_iter_no_change':(n_iter_no_change, None, False),
            'tol':(tol, 0.0001, False),
            'ccp_alpha':(ccp_alpha, 0.0, False),}
        cleaned_up_init_args = validate_sklearn_args(
            args=init_args,
            klass=sklearn.ensemble.GradientBoostingClassifier
        )
        self._sklearn_object: Any = sklearn.ensemble.GradientBoostingClassifier(
            **cleaned_up_init_args,
        )
        self._model_signature_dict: Optional[Dict[str, ModelSignature]] = None
        # If user used snowpark dataframe during fit, here it stores the snowpark input_cols, otherwise the processed input_cols
        self._snowpark_cols: Optional[List[str]] = self.input_cols
        self._handlers: TransformerHandlers = HandlersImpl(class_name=GradientBoostingClassifier.__class__.__name__, subproject=_SUBPROJECT, autogenerated=True)
        self._autogenerated = True

    def _get_rand_id(self) -> str:
        """
        Generate random id to be used in sproc and stage names.

        Returns:
            Random id string usable in sproc, table, and stage names.
        """
        return str(uuid4()).replace("-", "_").upper()

    def set_input_cols(self, input_cols: Optional[Union[str, Iterable[str]]]) -> "GradientBoostingClassifier":
        """
        Input columns setter.

        Args:
            input_cols: A single input column or multiple input columns.

        Returns:
            self
        """
        self.input_cols = _process_cols(input_cols)
        self._snowpark_cols = self.input_cols
        return self

    def _get_active_columns(self) -> List[str]:
        """"Get the list of columns that are relevant to the transformer."""
        selected_cols = (
            self.input_cols +
            self.label_cols +
            ([self.sample_weight_col] if self.sample_weight_col is not None else [])
        )
        return selected_cols

    @telemetry.send_api_usage_telemetry(
        project=_PROJECT,
        subproject=_SUBPROJECT,
        custom_tags=dict([("autogen", True)]),
    )
    def fit(self, dataset: Union[DataFrame, pd.DataFrame]) -> "GradientBoostingClassifier":
        """Fit the gradient boosting model
        For more details on this function, see [sklearn.ensemble.GradientBoostingClassifier.fit]
        (https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier.fit)


        Raises:
            TypeError: Supported dataset types: snowpark.DataFrame, pandas.DataFrame.

        Args:
            dataset: Union[snowflake.snowpark.DataFrame, pandas.DataFrame]
                Snowpark or Pandas DataFrame.

        Returns:
            self
        """
        self._infer_input_output_cols(dataset)
        if isinstance(dataset, DataFrame):
            session = dataset._session
            assert session is not None  # keep mypy happy
            # Specify input columns so column pruning will be enforced
            selected_cols = self._get_active_columns()
            if len(selected_cols) > 0:
                dataset = dataset.select(selected_cols)

            self._snowpark_cols = dataset.select(self.input_cols).columns

             # If we are already in a stored procedure, no need to kick off another one.
            if SNOWML_SPROC_ENV in os.environ:
                statement_params = telemetry.get_function_usage_statement_params(
                    project=_PROJECT,
                    subproject=_SUBPROJECT,
                    function_name=telemetry.get_statement_params_full_func_name(inspect.currentframe(), GradientBoostingClassifier.__class__.__name__),
                    api_calls=[Session.call],
                    custom_tags=dict([("autogen", True)]) if self._autogenerated else None,
                )
                pd_df: pd.DataFrame = dataset.to_pandas(statement_params=statement_params)
                pd_df.columns = dataset.columns
                dataset = pd_df

        model_trainer = ModelTrainerBuilder.build(
            estimator=self._sklearn_object,
            dataset=dataset,
            input_cols=self.input_cols,
            label_cols=self.label_cols,
            sample_weight_col=self.sample_weight_col,
            autogenerated=self._autogenerated,
            subproject=_SUBPROJECT,
            use_external_memory_version=self._use_external_memory_version,
            batch_size=self._batch_size,
        )
        self._sklearn_object = model_trainer.train()
        self._is_fitted = True
        self._get_model_signatures(dataset)
        return self

    def _get_pass_through_columns(self, dataset: DataFrame) -> List[str]:
        if self._drop_input_cols:
            return []
        else:
            return list(set(dataset.columns) - set(self.output_cols))

    def _batch_inference(
        self,
        dataset: DataFrame,
        inference_method: str,
        expected_output_cols_list: List[str],
        expected_output_cols_type: str = "",
        *args: Any,
        **kwargs: Any,
    ) -> DataFrame:
        """Util method to create UDF and run batch inference.
        """
        if not self._is_fitted:
            raise exceptions.SnowflakeMLException(
                error_code=error_codes.METHOD_NOT_ALLOWED,
                original_exception=RuntimeError(
                    f"Estimator {self.__class__.__name__} not fitted before calling {inference_method} method."
                ),
            )

        session = dataset._session
        if session is None:
            raise exceptions.SnowflakeMLException(
                error_code=error_codes.NOT_FOUND,
                original_exception=ValueError(
                    "Session must not specified for snowpark dataset."
                ),
            )
        # Validate that key package version in user workspace are supported in snowflake conda channel
        pkg_version_utils.get_valid_pkg_versions_supported_in_snowflake_conda_channel(
            pkg_versions=self._get_dependencies(), session=session, subproject=_SUBPROJECT)

        return self._handlers.batch_inference(
            dataset,
            session,
            self._sklearn_object,
            self._get_dependencies(),
            inference_method,
            self.input_cols,
            self._get_pass_through_columns(dataset),
            expected_output_cols_list,
            expected_output_cols_type,
            *args,
            **kwargs,
        )


    def _sklearn_inference(
        self,
        dataset: pd.DataFrame,
        inference_method: str,
        expected_output_cols_list: List[str],
        *args: Any,
        **kwargs: Any,
    ) -> pd.DataFrame:
        output_cols = expected_output_cols_list.copy()

        # Model expects exact same columns names in the input df for predict call.
        # Given the scenario that user use snowpark DataFrame in fit call, but pandas DataFrame in predict call
        # input cols need to match unquoted / quoted
        input_cols = self.input_cols
        assert self._snowpark_cols is not None  # Keep mypy happy
        _snowpark_input_cols: List[str] = self._snowpark_cols
        
        estimator = self._sklearn_object

        if hasattr(estimator, "feature_names_in_"):
            features_required_by_estimator =  getattr(estimator, "feature_names_in_")  
        else:
            features_required_by_estimator = _snowpark_input_cols
        missing_features = []
        features_in_dataset = set(dataset.columns)
        
        columns_to_select = []
        for i, f in enumerate(features_required_by_estimator):
            if (
                    i >= len(input_cols)
                    or (input_cols[i] != f and _snowpark_input_cols[i] != f)
                    or (input_cols[i] not in features_in_dataset and _snowpark_input_cols[i] not in features_in_dataset)
                ):
                missing_features.append(f)
            elif input_cols[i] in features_in_dataset:
                columns_to_select.append(input_cols[i])
            elif _snowpark_input_cols[i] in features_in_dataset:
                columns_to_select.append(_snowpark_input_cols[i])

        if len(missing_features) > 0:
            raise exceptions.SnowflakeMLException(
                error_code=error_codes.NOT_FOUND,
                original_exception=ValueError(
                    "The feature names should match with those that were passed during fit.\n"
                    f"Features seen during fit call but not present in the input: {missing_features}\n"
                    f"Features in the input dataframe : {input_cols}\n"
                ),
            )
        input_df = dataset[columns_to_select]
        input_df.columns = features_required_by_estimator

        inference_res = getattr(estimator, inference_method)(input_df, *args, **kwargs)

        if (
            isinstance(inference_res, list)
            and len(inference_res) > 0
            and isinstance(inference_res[0], np.ndarray)
        ):
            # In case of multioutput estimators, predict_proba, decision_function etc., functions return a list of
            # ndarrays. We need to concatenate them.

            # First compute output column names
            if len(output_cols) == len(inference_res):
                actual_output_cols = []
                for idx, np_arr in enumerate(inference_res):
                    for i in range(1 if len(np_arr.shape) <= 1 else np_arr.shape[1]):
                        actual_output_cols.append(f"{output_cols[idx]}_{i}")
                output_cols = actual_output_cols

            # Concatenate np arrays
            transformed_numpy_array = np.concatenate(inference_res, axis=1)
        elif (
                isinstance(inference_res, tuple)
                and len(inference_res) > 0
                and isinstance(inference_res[0], np.ndarray)
            ):
                # In case of kneighbors, functions return a tuple of ndarrays.
                transformed_numpy_array = np.stack(inference_res, axis=1)
        else:
            transformed_numpy_array = inference_res

        if (len(transformed_numpy_array.shape) == 3) and inference_method != "kneighbors":
            # VotingClassifier will return results of shape (n_classifiers, n_samples, n_classes)
            # when voting = "soft" and flatten_transform = False. We can't handle unflatten transforms,
            # so we ignore flatten_transform flag and flatten the results.
            transformed_numpy_array = np.hstack(transformed_numpy_array)  # type: ignore[call-overload]

        if len(transformed_numpy_array.shape) == 1:
            transformed_numpy_array = np.reshape(transformed_numpy_array, (-1, 1))

        shape = transformed_numpy_array.shape
        if shape[1] != len(output_cols):
            if len(output_cols) != 1:
                raise exceptions.SnowflakeMLException(
                    error_code=error_codes.INVALID_ARGUMENT,
                    original_exception=TypeError(
                        "expected_output_cols_list must be same length as transformed array or "
                        "should be of length 1"
                    ),
                )
            actual_output_cols = []
            for i in range(shape[1]):
                actual_output_cols.append(f"{output_cols[0]}_{i}")
            output_cols = actual_output_cols

        if inference_method == "kneighbors":
            if (len(transformed_numpy_array.shape) == 3):  # return_distance=True
                shape = transformed_numpy_array.shape
                data = [transformed_numpy_array[:, i, :].tolist() for i in range(shape[1])]
                kneighbors_df = pd.DataFrame({output_cols[i]: data[i] for i in range(shape[1])})
            else:  # return_distance=False
                kneighbors_df = pd.DataFrame(
                    {output_cols[0]: [
                        transformed_numpy_array[i, :].tolist() for i in range(transformed_numpy_array.shape[0])
                    ]}
                )

            if self._drop_input_cols:
                dataset = kneighbors_df
            else:
                dataset = pd.concat([dataset, kneighbors_df], axis=1)
        else:
            if self._drop_input_cols:
                dataset = pd.DataFrame(data=transformed_numpy_array, columns=output_cols)
            else:
                dataset = dataset.copy()
                dataset[output_cols] = transformed_numpy_array
        return dataset

    @available_if(original_estimator_has_callable("predict"))  # type: ignore[misc]
    @telemetry.send_api_usage_telemetry(
        project=_PROJECT,
        subproject=_SUBPROJECT,
        custom_tags=dict([("autogen", True)]),
    )
    def predict(self, dataset: Union[DataFrame, pd.DataFrame]) -> Union[DataFrame, pd.DataFrame]:
        """Predict class for X
        For more details on this function, see [sklearn.ensemble.GradientBoostingClassifier.predict]
        (https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier.predict)


        Raises:
            TypeError: Supported dataset types: snowpark.DataFrame, pandas.DataFrame.

        Args:
            dataset: Union[snowflake.snowpark.DataFrame, pandas.DataFrame]
                Snowpark or Pandas DataFrame.

        Returns:
            Transformed dataset.
        """
        super()._check_dataset_type(dataset)
        if isinstance(dataset, DataFrame):
            expected_type_inferred = ""
            # when it is classifier, infer the datatype from label columns
            if expected_type_inferred == "" and 'predict' in self.model_signatures:
                # Batch inference takes a single expected output column type. Use the first columns type for now.
                label_cols_signatures = [row for row in self.model_signatures['predict'].outputs if row.name in self.output_cols]
                if len(label_cols_signatures) == 0:
                    error_str = f"Output columns {self.output_cols} do not match model signatures {self.model_signatures['predict'].outputs}."
                    raise exceptions.SnowflakeMLException(
                        error_code=error_codes.INVALID_ATTRIBUTE,
                        original_exception=ValueError(error_str),
                    )
                expected_type_inferred = convert_sp_to_sf_type(
                    label_cols_signatures[0].as_snowpark_type()
                )
            
            output_df = self._batch_inference(
                dataset=dataset,
                inference_method="predict",
                expected_output_cols_list=self.output_cols,
                expected_output_cols_type=expected_type_inferred,
            )
        elif isinstance(dataset, pd.DataFrame):
            output_df = self._sklearn_inference(
                dataset=dataset,
                inference_method="predict",
                expected_output_cols_list=self.output_cols,)

        return output_df

    @available_if(original_estimator_has_callable("transform"))  # type: ignore[misc]
    @telemetry.send_api_usage_telemetry(
        project=_PROJECT,
        subproject=_SUBPROJECT,
        custom_tags=dict([("autogen", True)]),
    )
    def transform(self, dataset: Union[DataFrame, pd.DataFrame]) -> Union[DataFrame, pd.DataFrame]:
        """Method not supported for this class.


        Raises:
            TypeError: Supported dataset types: snowpark.DataFrame, pandas.DataFrame.

        Args:
            dataset: Union[snowflake.snowpark.DataFrame, pandas.DataFrame]
                Snowpark or Pandas DataFrame.

        Returns:
            Transformed dataset.
        """
        super()._check_dataset_type(dataset)
        if isinstance(dataset, DataFrame):
            expected_dtype = ""
            if False:  # is child of _BaseHeterogeneousEnsemble
                # transform() method of HeterogeneousEnsemble estimators return responses of varying shapes
                # from (n_samples, n_estimators) to (n_samples, n_estimators * n_classes) (and everything in between)
                # based on init param values. We will convert that to pandas dataframe of shape (n_samples, 1) with
                # each row containing a list of values.
                expected_dtype = "ARRAY"

            # If we were unable to assign a type to this transform in the factory, infer the type here.
            if expected_dtype == "":
                # If this is a clustering transformer, if the number of output columns does not equal the number of clusters the response will be an "ARRAY"
                if hasattr(self._sklearn_object, "n_clusters") and getattr(self._sklearn_object, "n_clusters") != len(self.output_cols):
                    expected_dtype = "ARRAY"
                # If this is a decomposition transformer, if the number of output columns does not equal the number of components the response will be an "ARRAY"
                elif hasattr(self._sklearn_object, "n_components") and getattr(self._sklearn_object, "n_components") != len(self.output_cols):
                    expected_dtype = "ARRAY"
                else:
                    output_types = [signature.as_snowpark_type() for signature in _infer_signature(dataset[self.input_cols], "output", use_snowflake_identifiers=True)]
                    # We can only infer the output types from the input types if the following two statemetns are true:
                    # 1) All of the output types are the same. Otherwise, we still have to fall back to variant because `_sklearn_inference` only accepts one type.
                    # 2) The length of the input columns equals the length of the output columns. Otherwise the transform will likely result in an `ARRAY`.
                    if all(x == output_types[0] for x in output_types) and len(output_types) == len(self.output_cols):
                        expected_dtype = convert_sp_to_sf_type(output_types[0])
            
            output_df = self._batch_inference(
                dataset=dataset,
                inference_method="transform",
                expected_output_cols_list=self.output_cols,
                expected_output_cols_type=expected_dtype,
            )
        elif isinstance(dataset, pd.DataFrame):
            output_df = self._sklearn_inference(
                dataset=dataset,
                inference_method="transform",
                expected_output_cols_list=self.output_cols,
            )

        return output_df
    
    @available_if(_is_fit_predict_method_enabled())  # type: ignore[misc]
    def fit_predict(self, dataset: Union[DataFrame, pd.DataFrame]) -> Union[Any, npt.NDArray[Any]]:
        """ Method not supported for this class.


        Raises:
            TypeError: Supported dataset types: snowpark.DataFrame, pandas.DataFrame.

        Args:
            dataset: Union[snowflake.snowpark.DataFrame, pandas.DataFrame]
                Snowpark or Pandas DataFrame.
        Returns:
            Predicted dataset.
        """
        self.fit(dataset)
        assert self._sklearn_object is not None
        return self._sklearn_object.labels_


    @available_if(_is_fit_transform_method_enabled())  # type: ignore[misc]
    def fit_transform(self, dataset: Union[DataFrame, pd.DataFrame]) -> Union[Any, npt.NDArray[Any]]:
        """ 
        Returns:
            Transformed dataset.
        """
        self.fit(dataset)
        assert self._sklearn_object is not None
        return self._sklearn_object.embedding_


    def _get_output_column_names(self, output_cols_prefix: str, output_cols: Optional[List[str]] = None) -> List[str]:
        """ Returns the list of output columns for predict_proba(), decision_function(), etc.. functions.
        Returns a list with output_cols_prefix as the only element if the estimator is not a classifier.
        """
        output_cols_prefix = identifier.resolve_identifier(output_cols_prefix)
        if output_cols:
            output_cols = [
                identifier.concat_names([output_cols_prefix, identifier.resolve_identifier(c)])
                for c in output_cols
            ]
        elif getattr(self._sklearn_object, "classes_", None) is None:
            output_cols = [output_cols_prefix]
        elif self._sklearn_object is not None:
            classes = self._sklearn_object.classes_
            if isinstance(classes, numpy.ndarray):
                output_cols = [f'{output_cols_prefix}{str(c)}' for c in classes.tolist()]
            elif isinstance(classes, list) and len(classes) > 0 and isinstance(classes[0], numpy.ndarray):
                # If the estimator is a multioutput estimator, classes_ will be a list of ndarrays.
                output_cols = []
                for i, cl in enumerate(classes):
                    # For binary classification, there is only one output column for each class
                    # ndarray as the two classes are complementary.
                    if len(cl) == 2:
                        output_cols.append(f'{output_cols_prefix}{i}_{cl[0]}')
                    else:
                        output_cols.extend([
                            f'{output_cols_prefix}{i}_{c}' for c in cl.tolist()
                        ])
        else:
            output_cols = []

        # Make sure column names are valid snowflake identifiers.
        assert output_cols is not None  # Make MyPy happy
        rv = [identifier.rename_to_valid_snowflake_identifier(c) for c in output_cols]

        return rv

    @available_if(original_estimator_has_callable("predict_proba"))  # type: ignore[misc]
    @telemetry.send_api_usage_telemetry(
        project=_PROJECT,
        subproject=_SUBPROJECT,
        custom_tags=dict([("autogen", True)]),
    )
    def predict_proba(
        self, dataset: Union[DataFrame, pd.DataFrame], output_cols_prefix: str = "predict_proba_"
    ) -> Union[DataFrame, pd.DataFrame]:
        """Predict class probabilities for X
        For more details on this function, see [sklearn.ensemble.GradientBoostingClassifier.predict_proba]
        (https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier.predict_proba)


        Raises:
            TypeError: Supported dataset types: snowpark.DataFrame, pandas.DataFrame.

        Args:
            dataset: Union[snowflake.snowpark.DataFrame, pandas.DataFrame]
                Snowpark or Pandas DataFrame.
            output_cols_prefix: Prefix for the response columns

        Returns:
            Output dataset with probability of the sample for each class in the model.
        """
        super()._check_dataset_type(dataset)
        if isinstance(dataset, DataFrame):
            output_df = self._batch_inference(
                dataset=dataset,
                inference_method="predict_proba",
                expected_output_cols_list=self._get_output_column_names(output_cols_prefix),
                expected_output_cols_type="float"
            )
        elif isinstance(dataset, pd.DataFrame):
            output_df = self._sklearn_inference(
                dataset=dataset,
                inference_method="predict_proba",
                expected_output_cols_list=self._get_output_column_names(output_cols_prefix),
            )
        
        return output_df

    @available_if(original_estimator_has_callable("predict_log_proba"))  # type: ignore[misc]
    @telemetry.send_api_usage_telemetry(
        project=_PROJECT,
        subproject=_SUBPROJECT,
        custom_tags=dict([("autogen", True)]),
    )
    def predict_log_proba(
        self, dataset: Union[DataFrame, pd.DataFrame], output_cols_prefix: str = "predict_log_proba_"
    ) -> Union[DataFrame, pd.DataFrame]:
        """Predict class probabilities for X
        For more details on this function, see [sklearn.ensemble.GradientBoostingClassifier.predict_proba]
        (https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier.predict_proba)


        Raises:
            TypeError: Supported dataset types: snowpark.DataFrame, pandas.DataFrame.

        Args:
            dataset: Union[snowflake.snowpark.DataFrame, pandas.DataFrame]
                Snowpark or Pandas DataFrame.
            output_cols_prefix: str
                Prefix for the response columns

        Returns:
            Output dataset with log probability of the sample for each class in the model.
        """
        super()._check_dataset_type(dataset)
        if isinstance(dataset, DataFrame):
            output_df = self._batch_inference(
                dataset=dataset,
                inference_method="predict_log_proba",
                expected_output_cols_list=self._get_output_column_names(output_cols_prefix),
                expected_output_cols_type="float"
            )
        elif isinstance(dataset, pd.DataFrame):
            output_df = self._sklearn_inference(
                dataset=dataset,
                inference_method="predict_log_proba",
                expected_output_cols_list=self._get_output_column_names(output_cols_prefix),
            )

        return output_df

    @available_if(original_estimator_has_callable("decision_function"))  # type: ignore[misc]
    def decision_function(
        self, dataset: Union[DataFrame, pd.DataFrame], output_cols_prefix: str = "decision_function_"
    ) -> Union[DataFrame, pd.DataFrame]:
        """Compute the decision function of ``X``
        For more details on this function, see [sklearn.ensemble.GradientBoostingClassifier.decision_function]
        (https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier.decision_function)


        Raises:
            TypeError: Supported dataset types: snowpark.DataFrame, pandas.DataFrame.

        Args:
            dataset: Union[snowflake.snowpark.DataFrame, pandas.DataFrame]
                Snowpark or Pandas DataFrame.
            output_cols_prefix: str
                Prefix for the response columns

        Returns:
            Output dataset with results of the decision function for the samples in input dataset.
        """
        super()._check_dataset_type(dataset)
        if isinstance(dataset, DataFrame):
            output_df = self._batch_inference(
                dataset=dataset,
                inference_method="decision_function",
                expected_output_cols_list=self._get_output_column_names(output_cols_prefix),
                expected_output_cols_type="float"
            )
        elif isinstance(dataset, pd.DataFrame):
            output_df = self._sklearn_inference(
                dataset=dataset,
                inference_method="decision_function",
                expected_output_cols_list=self._get_output_column_names(output_cols_prefix),
            )

        return output_df

    @available_if(original_estimator_has_callable("score_samples"))  # type: ignore[misc]
    @telemetry.send_api_usage_telemetry(
        project=_PROJECT,
        subproject=_SUBPROJECT,
        custom_tags=dict([("autogen", True)]),
    )
    def score_samples(
        self, dataset: Union[DataFrame, pd.DataFrame], output_cols_prefix: str = "score_samples_"
    ) -> Union[DataFrame, pd.DataFrame]:
        """Method not supported for this class.


        Raises:
            TypeError: Supported dataset types: snowpark.DataFrame, pandas.DataFrame.

        Args:
            dataset: Union[snowflake.snowpark.DataFrame, pandas.DataFrame]
                Snowpark or Pandas DataFrame.
            output_cols_prefix: Prefix for the response columns

        Returns:
            Output dataset with probability of the sample for each class in the model.
        """
        super()._check_dataset_type(dataset)
        if isinstance(dataset, DataFrame):
            output_df = self._batch_inference(
                dataset=dataset,
                inference_method="score_samples",
                expected_output_cols_list=self._get_output_column_names(output_cols_prefix),
                expected_output_cols_type="float"
            )
        elif isinstance(dataset, pd.DataFrame):
            output_df = self._sklearn_inference(
                dataset=dataset,
                inference_method="score_samples",
                expected_output_cols_list=self._get_output_column_names(output_cols_prefix),
            )
        
        return output_df

    @available_if(original_estimator_has_callable("score"))  # type: ignore[misc]
    @telemetry.send_api_usage_telemetry(
        project=_PROJECT,
        subproject=_SUBPROJECT,
        custom_tags=dict([("autogen", True)]),
    )
    def score(self, dataset: Union[DataFrame, pd.DataFrame]) -> float:
        """Return the mean accuracy on the given test data and labels
        For more details on this function, see [sklearn.ensemble.GradientBoostingClassifier.score]
        (https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier.score)


        Raises:
            TypeError: Supported dataset types: snowpark.DataFrame, pandas.DataFrame.

        Args:
            dataset: Union[snowflake.snowpark.DataFrame, pandas.DataFrame]
                Snowpark or Pandas DataFrame.

        Returns:
            Score.
        """
        self._infer_input_output_cols(dataset)
        super()._check_dataset_type(dataset)
        if isinstance(dataset, pd.DataFrame):
            output_score = self._handlers.score_pandas(
                dataset,
                self._sklearn_object,
                self.input_cols,
                self.label_cols,
                self.sample_weight_col

            )
        elif isinstance(dataset, DataFrame):
            output_score = self._score_snowpark(dataset)
        return output_score

    def _score_snowpark(self, dataset: DataFrame) -> float:
        # Specify input columns so column pruing will be enforced
        selected_cols = self._get_active_columns()
        if len(selected_cols) > 0:
            dataset = dataset.select(selected_cols)

        session = dataset._session
        assert session is not None  # keep mypy happy

        score = self._handlers.score_snowpark(
            dataset,
            session,
            self._sklearn_object,
            ["snowflake-snowpark-python"] + self._get_dependencies(),
            ['sklearn'],
            self.input_cols,
            self.label_cols,
            self.sample_weight_col,
        )

        return score

    @available_if(original_estimator_has_callable("kneighbors"))  # type: ignore[misc]
    @telemetry.send_api_usage_telemetry(
        project=_PROJECT,
        subproject=_SUBPROJECT,
        custom_tags=dict([("autogen", True)]),
    )
    def kneighbors(
        self,
        dataset: Union[DataFrame, pd.DataFrame],
        n_neighbors: Optional[int] = None,
        return_distance: bool = True,
        output_cols_prefix: str = "kneighbors_",
    ) -> Union[DataFrame, pd.DataFrame]:
        """Method not supported for this class.


        Raises:
            TypeError: Supported dataset types: snowpark.DataFrame, pandas.DataFrame.

        Args:
            dataset: Union[snowflake.snowpark.DataFrame, pandas.DataFrame]
                Snowpark or Pandas DataFrame.
            output_cols_prefix: str
                Prefix for the response columns

        Returns:
            Output dataset with results of the K-neighbors for the samples in input dataset.
        """
        super()._check_dataset_type(dataset)
        output_cols = ["neigh_ind"]
        if return_distance:
            output_cols.insert(0, "neigh_dist")
        if isinstance(dataset, DataFrame):
            output_df = self._batch_inference(
                dataset=dataset,
                inference_method="kneighbors",
                expected_output_cols_list=self._get_output_column_names(output_cols_prefix, output_cols),
                expected_output_cols_type="array",
                n_neighbors=n_neighbors,
                return_distance=return_distance,
            )
        elif isinstance(dataset, pd.DataFrame):
            output_df = self._sklearn_inference(
                dataset=dataset,
                inference_method="kneighbors",
                expected_output_cols_list=self._get_output_column_names(output_cols_prefix, output_cols),
                n_neighbors=n_neighbors,
                return_distance=return_distance,
            )

        return output_df

    def _get_model_signatures(self, dataset: Union[DataFrame, pd.DataFrame]) -> None:
        self._model_signature_dict = dict()

        PROB_FUNCTIONS = ["predict_log_proba", "predict_proba", "decision_function"]

        inputs = list(_infer_signature(dataset[self.input_cols], "input"))
        outputs: List[BaseFeatureSpec] = []
        if hasattr(self, "predict"):
            # keep mypy happy
            assert self._sklearn_object is not None and hasattr(self._sklearn_object, "_estimator_type") 
            # For classifier, the type of predict is the same as the type of label
            if self._sklearn_object._estimator_type == 'classifier':
                 # label columns is the desired type for output
                outputs = list(_infer_signature(dataset[self.label_cols], "output", use_snowflake_identifiers=True))
                # rename the output columns
                outputs = list(model_signature_utils.rename_features(outputs, self.output_cols))
                self._model_signature_dict["predict"] = ModelSignature(inputs,
                                                                       ([] if self._drop_input_cols else inputs)
                                                                       + outputs)
            # For mixture models that use the density mixin, `predict` returns the argmax of the log prob.
            # For outlier models, returns -1 for outliers and 1 for inliers.
            # Clusterer returns int64 cluster labels. 
            elif self._sklearn_object._estimator_type in ["DensityEstimator", "clusterer", "outlier_detector"]:
                outputs = [FeatureSpec(dtype=DataType.INT64, name=c) for c in self.output_cols]
                self._model_signature_dict["predict"] = ModelSignature(inputs,
                                                                       ([] if self._drop_input_cols else inputs)
                                                                       + outputs)
            
            # For regressor, the type of predict is float64
            elif self._sklearn_object._estimator_type == 'regressor':
                outputs = [FeatureSpec(dtype=DataType.DOUBLE, name=c) for c in self.output_cols]
                self._model_signature_dict["predict"] = ModelSignature(inputs,
                                                                       ([] if self._drop_input_cols else inputs)
                                                                       + outputs)
                
        for prob_func in PROB_FUNCTIONS:
            if hasattr(self, prob_func):
                output_cols_prefix: str = f"{prob_func}_"
                output_column_names = self._get_output_column_names(output_cols_prefix)
                outputs = [FeatureSpec(dtype=DataType.DOUBLE, name=c) for c in output_column_names]
                self._model_signature_dict[prob_func] = ModelSignature(inputs,
                                                                       ([] if self._drop_input_cols else inputs)
                                                                       + outputs)

        # Output signature names may still need to be renamed, since they were not created with `_infer_signature`.
        items = list(self._model_signature_dict.items())
        for method, signature in items:
            signature._outputs = _rename_signature_with_snowflake_identifiers(signature._outputs)
            self._model_signature_dict[method] = signature

    @property
    def model_signatures(self) -> Dict[str, ModelSignature]:
        """Returns model signature of current class.

        Raises:
            exceptions.SnowflakeMLException: If estimator is not fitted, then model signature cannot be inferred

        Returns:
            Dict[str, ModelSignature]: each method and its input output signature
        """
        if self._model_signature_dict is None:
            raise exceptions.SnowflakeMLException(
                error_code=error_codes.INVALID_ATTRIBUTE,
                original_exception=RuntimeError("Estimator not fitted before accessing property model_signatures!"),
            )
        return self._model_signature_dict

    def to_sklearn(self) -> Any:
        """Get sklearn.ensemble.GradientBoostingClassifier object.
        """
        if self._sklearn_object is None:
            self._sklearn_object = self._create_sklearn_object()
        return self._sklearn_object

    def to_xgboost(self) -> Any:
        raise exceptions.SnowflakeMLException(
            error_code=error_codes.METHOD_NOT_ALLOWED,
            original_exception=AttributeError(
                modeling_error_messages.UNSUPPORTED_MODEL_CONVERSION.format(
                    "to_xgboost()", 
                    "to_sklearn()"
                )
            ),
        )

    def to_lightgbm(self) -> Any:
        raise exceptions.SnowflakeMLException(
            error_code=error_codes.METHOD_NOT_ALLOWED,
            original_exception=AttributeError(
                modeling_error_messages.UNSUPPORTED_MODEL_CONVERSION.format(
                    "to_lightgbm()", 
                    "to_sklearn()"
                )
            ),
        )

    def _get_dependencies(self) -> List[str]:
        return self._deps
