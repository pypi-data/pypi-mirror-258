import copy
import inspect
import random
from typing import Optional, Any, Union, Type, Dict, Tuple, List, Callable

import torch
import numpy as np
import pandas as pd
from torch.optim import Optimizer, Adam
from torch.utils.data import DataLoader, Dataset, Subset
from tqdm.auto import tqdm

from torch_mist.estimators import MultiMIEstimator
from torch_mist.estimators.base import MIEstimator
from torch_mist.estimators.factories import instantiate_estimator
from torch_mist.utils.data.utils import infer_dims, TensorDictLike, make_dataset, filter_dataset, is_data_loader
from torch_mist.utils.logging import PandasLogger
from torch_mist.utils.logging.logger.base import Logger, DummyLogger
from torch_mist.utils.train.mi_estimator import train_mi_estimator
from torch_mist.utils.evaluation import evaluate_mi

DEFAULT_MAX_ITERATIONS = 5000
DEFAULT_MAX_EPOCHS = 10

def _instantiate_estimator(
    instantiation_func: Callable[[Any], MIEstimator],
    data: TensorDictLike,
    x_key: Optional[str] = None,
    y_key: Optional[str] = None,
    verbose: bool = True,
    **kwargs,
) -> MIEstimator:
    dims = infer_dims(data)
    if x_key is None:
        x_key = "x"
    if y_key is None:
        y_key = "y"

    if x_key in dims:
        x_dim = dims[x_key]
    else:
        raise ValueError(
            "The data does not contain a key for 'x'.\n"
            + f"Please specify a value for x_key among {dims.keys()}"
        )

    if y_key in dims:
        y_dim = dims[y_key]
    else:
        raise ValueError(
            "The data does not contain a key for 'y'.\n"
            + f"Please specify a value for y_key among {dims.keys()}"
        )

    if "x_dim" in inspect.signature(instantiation_func).parameters:
        kwargs["x_dim"] = x_dim
    if "y_dim" in inspect.signature(instantiation_func).parameters:
        kwargs["y_dim"] = y_dim

    if verbose:
        print(f"Instantiating the estimator with {kwargs}")

    estimator = instantiation_func(
        **kwargs,
    )

    if verbose:
        print(estimator)

    return estimator


def estimate_mi(
    data: TensorDictLike,
    estimator_name: Optional[str] = None,
    estimator: Optional[MIEstimator] = None,
    valid_data: Optional[TensorDictLike] = None,
    test_data: Optional[TensorDictLike] = None,
    valid_percentage: float = 0.1,
    device: Union[torch.device, str] = torch.device("cpu"),
    max_epochs: Optional[int] = None,
    max_iterations: Optional[int] = None,
    optimizer_class: Type[Optimizer] = Adam,
    optimizer_params: Optional[Dict[str, Any]] = None,
    verbose: bool = True,
    logger: Optional[Union[Logger, bool]] = None,
    lr_annealing: bool = False,
    warmup_percentage: float = 0,
    batch_size: Optional[int] = 128,
    evaluation_batch_size: Optional[int] = None,
    num_workers: int = 0,
    early_stopping: bool = True,
    patience: Optional[int] = None,
    tolerance: float = 0.001,
    return_estimator: bool = False,
    fast_train: bool = False,
    hidden_dims: List[int] = [128, 64],
    x_key: str = "x",
    y_key: str = "y",
    **kwargs,
) -> Union[
    float,
    Tuple[float, pd.DataFrame],
    Tuple[float, MIEstimator],
    Tuple[float, MIEstimator, pd.DataFrame],
]:

    if max_epochs is None and max_iterations is None:
        if is_data_loader(data):
            max_epochs = DEFAULT_MAX_EPOCHS
            print(
                f"[Info]: max_epochs and max_iterations are not specified, using max_epochs={max_epochs} by default."
            )
        else:
            max_iterations = DEFAULT_MAX_ITERATIONS
            print(
                f"[Info]: max_epochs and max_iterations are not specified, using max_iterations={max_iterations} by default."
            )

    if estimator is None and estimator_name is None:
        raise ValueError(
            "Please specify a value for estimator or estimator_name."
        )

    if estimator is None:
        # Instantiate the estimator while inferring the size for x and y
        if verbose:
            print(f"Instantiating the {estimator_name} estimator")

        estimator = _instantiate_estimator(
            instantiation_func=instantiate_estimator,
            data=data,
            x_key=x_key,
            y_key=y_key,
            verbose=verbose,
            estimator_name=estimator_name,
            hidden_dims=hidden_dims,
            **kwargs,
        )

    # If using different key instead of 'x' and 'y'
    if x_key != "x" or y_key != "y":
        if not isinstance(estimator, MultiMIEstimator):
            estimator = MultiMIEstimator({(x_key, y_key): estimator})
        else:
            assert (x_key, y_key) in estimator.estimators

    if verbose:
        print("Training the estimator")

    if logger is None:
        logger = PandasLogger()
    elif logger is False:
        logger = DummyLogger()

    train_log = train_mi_estimator(
        estimator=estimator,
        data=data,
        valid_data=valid_data,
        valid_percentage=valid_percentage,
        device=device,
        max_epochs=max_epochs,
        max_iterations=max_iterations,
        optimizer_class=optimizer_class,
        optimizer_params=optimizer_params,
        verbose=verbose,
        logger=logger,
        lr_annealing=lr_annealing,
        warmup_percentage=warmup_percentage,
        batch_size=batch_size,
        early_stopping=early_stopping,
        patience=patience,
        tolerance=tolerance,
        num_workers=num_workers,
        fast_train=fast_train,
    )

    if verbose:
        print("Evaluating the value of Mutual Information")

    if test_data is None:
        print(
            "[Warning]: using the train_data to estimate the value of mutual information. Please specify test_data."
        )
        test_data = data

    if evaluation_batch_size is None:
        evaluation_batch_size = batch_size

    with logger.test():
        with logger.logged_methods(
                estimator,
                methods=['mutual_information'],
        ):
            mi_value = evaluate_mi(
                estimator=estimator,
                data=test_data,
                batch_size=evaluation_batch_size,
                device=device,
                num_workers=num_workers,
            )

    if not (train_log is None) and return_estimator:
        return mi_value, estimator, train_log
    elif not (train_log is None):
        return mi_value, train_log
    elif return_estimator:
        return mi_value, estimator
    else:
        return mi_value



def k_fold_mi_estimate(
    data: TensorDictLike,
    estimator_name: Optional[str] = None,
    estimator: Optional[MIEstimator] = None,
    device: Union[torch.device, str] = torch.device("cpu"),
    max_epochs: Optional[int] = None,
    max_iterations: Optional[int] = None,
    optimizer_class: Type[Optimizer] = Adam,
    optimizer_params: Optional[Dict[str, Any]] = None,
    verbose: bool = True,
    verbose_train: bool = False,
    logger: Optional[Union[Logger, bool]] = None,
    lr_annealing: bool = False,
    warmup_percentage: float = 0,
    batch_size: Optional[int] = 128,
    num_workers: int = 0,
    early_stopping: bool = True,
    patience: Optional[int] = None,
    tolerance: float = 0.001,
    fast_train: bool = True,
    hidden_dims: List[int] = [128, 64],
    x_key: str = "x",
    y_key: str = "y",
    seed: Optional[int] = None,
    folds: int = 10,
    n_estimations: Optional[int] = None,
    **kwargs,
) -> Tuple[
    float,
    Any
]:
    if max_epochs is None and max_iterations is None:
        max_iterations = DEFAULT_MAX_ITERATIONS

        print(
            f"[Info]: max_epochs and max_iterations are not specified, using max_iterations={max_iterations} by default."
        )

    if estimator is None and estimator_name is None:
        raise ValueError(
            "Please specify a value for estimator or estimator_name."
        )

    if estimator is None:
        # Instantiate the estimator while inferring the size for x and y
        if verbose:
            print(f"Instantiating the {estimator_name} estimator")

        estimator = _instantiate_estimator(
            instantiation_func=instantiate_estimator,
            data=data,
            x_key=x_key,
            y_key=y_key,
            verbose=verbose,
            estimator_name=estimator_name,
            hidden_dims=hidden_dims,
            **kwargs,
        )

    # If using different key instead of 'x' and 'y'
    if x_key != "x" or y_key != "y":
        if not isinstance(estimator, MultiMIEstimator):
            estimator = MultiMIEstimator({(x_key, y_key): estimator})
        else:
            assert (x_key, y_key) in estimator.estimators

    if verbose:
        print("Training the estimator")

    if logger is None:
        logger = PandasLogger()
    elif logger is False:
        logger = DummyLogger()

    if not(seed is None):
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)

    full_dataset = make_dataset(data)

    # Create k train-test splits
    if verbose:
        print(f"The dataset has {len(full_dataset)} entries.")
        print(f"Creating the {folds} train/validation/test splits")

    data_splits = []
    # Create a permutation
    ids_permutation = np.random.permutation(len(full_dataset))

    # Drop the last to make each split the same size
    if len(full_dataset)%folds != 0:
        ids_permutation = ids_permutation[:-(len(full_dataset) % folds)]

    # Create 10 folds
    ids_folds = np.split(ids_permutation, folds)

    if verbose:
        print(f'Train size: {sum([len(split) for split in ids_folds[:-2]])}')
        print(f'Validation size: {len(ids_folds[0])}')
        print(f'Test size: {len(ids_folds[0])}')

    # Save the original estimator
    original_estimator = estimator

    if not estimator.lower_bound and not estimator.upper_bound:
        if early_stopping:
            raise ValueError(
                f"The {estimator.__class__.__name__} estimator does not produce a lower or an upper bound of "+
                "Mutual Information. Consider using a different estimator or disable early_stopping (not recommended)."
            )

    if not early_stopping:
        print(
            "[Warning]: The k-fold evaluation procedure relies on early_stopping to train."+
            " Without it, the validation set is not used for parameter tuning."
        )

    results = []
    iterations = 0
    epochs = 0

    if n_estimations is None:
        n_estimations = folds

    if n_estimations > folds:
        raise ValueError(
            "The number of estimations has to be less than the number of folds n_estimations<=n_folds (default=n_folds)"
        )

    tqdm_fold = (
        tqdm(total=n_estimations, desc="Fold", position=1)
        if verbose
        else None
    )
    for fold in range(n_estimations):
        test_fold = fold
        valid_fold = (test_fold + 1) % folds
        train_folds = [f for f in range(folds) if f != test_fold and f != valid_fold]

        test_ids = ids_folds[test_fold]
        valid_ids = ids_folds[valid_fold]
        train_ids = np.concatenate([ids_folds[train_fold] for train_fold in train_folds], 0)

        # Check there is no intersection
        assert len(train_ids) + len(valid_ids) + len(test_ids) == len(set(train_ids).union(valid_ids).union(test_ids))

        # Create the splits and filter out NaNs
        datasets = {
            'train': filter_dataset(Subset(full_dataset, train_ids)),
            'valid': filter_dataset(Subset(full_dataset, valid_ids)),
            'test': filter_dataset(Subset(full_dataset, test_ids))
        }

        estimator = copy.deepcopy(original_estimator)

        train_logger = DummyLogger()
        train_mi_estimator(
            estimator=estimator,
            data=datasets['train'],
            valid_data=datasets['valid'],
            device=device,
            max_epochs=max_epochs,
            max_iterations=max_iterations,
            optimizer_class=optimizer_class,
            optimizer_params=optimizer_params,
            verbose=verbose_train,
            logger=train_logger,
            lr_annealing=lr_annealing,
            warmup_percentage=warmup_percentage,
            batch_size=batch_size,
            early_stopping=early_stopping,
            patience=patience,
            tolerance=tolerance,
            num_workers=num_workers,
            fast_train=fast_train,
            valid_percentage=0
        )

        iterations += train_logger._iteration
        epochs += train_logger._iteration

        # Evaluate on the splits
        for split, dataset in datasets.items():
            mi = evaluate_mi(
                estimator,
                data=dataset,
                batch_size=batch_size,
            )
            if isinstance(mi, dict):
                if len(mi) > 1:
                    raise ValueError(
                        "k_fold_mi_estimation is not supported when estimating multiple values of mutual information"
                    )
                mi = next(iter(mi.values()))

            logger._log(
                data=mi,
                name='mutual_information',
                split=split,
                iteration=iterations,
                epoch=epochs,
            )

            if split == 'test':
                results.append(mi)
                if tqdm_fold:
                    tqdm_fold.set_postfix_str(f'mutual_information: {np.mean(results)} nats')

        if tqdm_fold:
            tqdm_fold.update(1)

    log = logger.get_log()

    return np.mean(results), log