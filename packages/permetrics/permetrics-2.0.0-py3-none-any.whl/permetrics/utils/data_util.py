#!/usr/bin/env python
# Created by "Thieu" at 12:12, 19/05/2022 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np
import copy as cp
from permetrics.utils.encoder import LabelEncoder
import permetrics.utils.constant as co


def format_regression_data_type(y_true: np.ndarray, y_pred: np.ndarray):
    if isinstance(y_true, co.SUPPORTED_LIST) and isinstance(y_pred, co.SUPPORTED_LIST):
        ## Remove all dimensions of size 1
        y_true, y_pred = np.squeeze(np.asarray(y_true, dtype='float64')), np.squeeze(np.asarray(y_pred, dtype='float64'))
        if y_true.ndim == y_pred.ndim:
            if y_true.ndim == 1:
                return y_true.reshape(-1, 1), y_pred.reshape(-1, 1), 1      # n_outputs
            if y_true.ndim > 2:
                raise ValueError("y_true and y_pred must be 1D or 2D arrays.")
            return y_true, y_pred, y_true.shape[1]      # n_outputs
        else:
            raise ValueError("y_true and y_pred must have the same number of dimensions.")
    else:
        raise TypeError("y_true and y_pred must be lists, tuples or numpy arrays.")


def get_regression_non_zero_data(y_true, y_pred, one_dim=True, rule_idx=0):
    """
    Get non-zero data based on rule

    Args:
        y_true (tuple, list, np.ndarray): The ground truth values
        y_pred (tuple, list, np.ndarray): The prediction values
        one_dim (bool): is y_true has 1 dimensions or not
        rule_idx (int): valid values [0, 1, 2] corresponding to [y_true, y_pred, both true and pred]

    Returns:
        y_true: y_true with positive values based on rule
        y_pred: y_pred with positive values based on rule

    """
    if rule_idx == 0:
        y_rule = cp.deepcopy(y_true)
    elif rule_idx == 1:
        y_rule = cp.deepcopy(y_pred)
    else:
        if one_dim:
            y_true_non, y_pred_non = y_true[y_true != 0], y_pred[y_true != 0]
            y_true, y_pred = y_true_non[y_pred_non != 0], y_pred_non[y_pred_non != 0]
        else:
            y_true_non, y_pred_non = y_true[~np.any(y_true == 0, axis=1)], y_pred[~np.any(y_true == 0, axis=1)]
            y_true, y_pred = y_true_non[~np.any(y_pred_non == 0, axis=1)], y_pred_non[~np.any(y_pred_non == 0, axis=1)]
        return y_true, y_pred
    if one_dim:
        y_true, y_pred = y_true[y_rule != 0], y_pred[y_rule != 0]
    else:
        y_true, y_pred = y_true[~np.any(y_rule == 0, axis=1)], y_pred[~np.any(y_rule == 0, axis=1)]
    return y_true, y_pred


def get_regression_positive_data(y_true, y_pred, one_dim=True, rule_idx=0):
    """
    Get positive data based on rule

    Args:
        y_true (tuple, list, np.ndarray): The ground truth values
        y_pred (tuple, list, np.ndarray): The prediction values
        one_dim (bool): is y_true has 1 dimensions or not
        rule_idx (int): valid values [0, 1, 2] corresponding to [y_true, y_pred, both true and pred]

    Returns:
        y_true: y_true with positive values based on rule
        y_pred: y_pred with positive values based on rule
    """
    if rule_idx == 0:
        y_rule = cp.deepcopy(y_true)
    elif rule_idx == 1:
        y_rule = cp.deepcopy(y_pred)
    else:
        if one_dim:
            y_true_non, y_pred_non = y_true[y_true > 0], y_pred[y_true > 0]
            y_true, y_pred = y_true_non[y_pred_non > 0], y_pred_non[y_pred_non > 0]
        else:
            y_true_non, y_pred_non = y_true[np.all(y_true > 0, axis=1)], y_pred[np.all(y_true > 0, axis=1)]
            y_true, y_pred = y_true_non[np.all(y_pred_non > 0, axis=1)], y_pred_non[np.all(y_pred_non > 0, axis=1)]
        return y_true, y_pred
    if one_dim:
        y_true, y_pred = y_true[y_rule > 0], y_pred[y_rule > 0]
    else:
        y_true, y_pred = y_true[np.all(y_rule > 0, axis=1)], y_pred[np.all(y_rule > 0, axis=1)]
    return y_true, y_pred


def format_classification_data(y_true: np.ndarray, y_pred: np.ndarray):
    if not (isinstance(y_true, co.SUPPORTED_LIST) and isinstance(y_pred, co.SUPPORTED_LIST)):
        raise TypeError("y_true and y_pred must be lists, tuples or numpy arrays.")
    else:
        ## Remove all dimensions of size 1
        y_true, y_pred = np.squeeze(np.asarray(y_true)), np.squeeze(np.asarray(y_pred))
        if np.issubdtype(y_true.dtype, np.number):
            if np.isnan(y_true).any() or np.isinf(y_true).any():
                raise ValueError(f"Invalid y_true. It contains NaN or Inf value.")
        if np.issubdtype(y_pred.dtype, np.number):
            if np.isnan(y_pred).any() or np.isinf(y_pred).any():
                raise ValueError(f"Invalid y_pred. It contains NaN or Inf value.")

        if y_true.ndim == y_pred.ndim:
            if np.issubdtype(y_true.dtype, np.number) and np.issubdtype(y_pred.dtype, np.number):
                var_type = "number"
                if y_true.ndim > 1:
                    y_true, y_pred = y_true.argmax(axis=1), y_pred.argmax(axis=1)
                else:
                    y_true, y_pred = np.round(y_true).astype(int), np.round(y_pred).astype(int)
            elif np.issubdtype(y_true.dtype, str) and np.issubdtype(y_pred.dtype, str):
                var_type = "string"
                if y_true.ndim > 1:
                    raise ValueError("y_true and y_pred with ndim > 1 need to have data type as number.")
            else:
                raise TypeError(f"y_true and y_pred need to have the same data type. {y_true.dtype} != {y_pred.dtype}")
            unique_true, unique_pred = sorted(np.unique(y_true)), sorted(np.unique(y_pred))
            if len(unique_pred) <= len(unique_true) and np.isin(unique_pred, unique_true).all():
                binary = len(unique_true) == 2
            else:
                raise ValueError(f"Invalid y_pred, existed at least one new label in y_pred.")
            return y_true, y_pred, binary, var_type
        else:
            if np.issubdtype(y_true.dtype, np.number):
                if y_true.ndim == 1:
                    if np.issubdtype(y_pred.dtype, np.number):
                        y_pred = y_pred.argmax(axis=1)
                        var_type = "number"
                        binary = len(np.unique(y_true)) == 2
                        return y_true, y_pred, binary, var_type
                    else:
                        raise TypeError("Invalid y_pred, it should have data type as numeric.")
                else:
                    y_true = y_true.argmax(axis=1)
                    if np.issubdtype(y_pred.dtype, np.number):
                        var_type = "number"
                        binary = len(np.unique(y_true)) == 2
                        return y_true, y_pred, binary, var_type
                    else:
                        raise TypeError("Invalid y_pred, it should have data type as numeric.")
            else:
                raise ValueError("y_true has ndim > 1 and data type is string. You need to convert y_true to 1-D vector.")


def format_y_score(y_true: np.ndarray, y_score: np.ndarray):
    if not (isinstance(y_true, co.SUPPORTED_LIST) and isinstance(y_score, co.SUPPORTED_LIST)):
        raise TypeError("y_true and y_score must be lists, tuples or numpy arrays.")
    else:
        y_true, y_score = np.squeeze(np.asarray(y_true)), np.squeeze(np.asarray(y_score))
        if np.issubdtype(y_true.dtype, np.number):
            if np.isnan(y_true).any() or np.isinf(y_true).any():
                raise ValueError(f"Invalid y_true. It contains NaN or Inf value.")
        if np.issubdtype(y_score.dtype, np.number):
            if np.isnan(y_score).any() or np.isinf(y_score).any():
                raise ValueError(f"Invalid y_score. It contains NaN or Inf value.")

        if y_true.ndim > 1:
            if np.issubdtype(y_true.dtype, np.number):
                y_true = y_true.argmax(axis=1)
            else:
                raise TypeError(f"Invalid y_true. Its data type should be number and its shape is 1D vector")
        var_type = "string" if np.issubdtype(y_true.dtype, str) else "number"
        binary = len(np.unique(y_true)) == 2
        le = LabelEncoder()
        y_true = le.fit_transform(y_true).ravel()

        if np.issubdtype(y_score.dtype, str) and y_score.ndim == 1:
            y_score = le.transform(y_score).ravel()
            y_score = np.eye(np.unique(y_true).size)[y_score]
            return y_true, y_score, binary, var_type
        elif np.issubdtype(y_score.dtype, np.number):
            if y_score.ndim == 1:
                y_score = le.transform(y_score).ravel()
                y_score = np.eye(np.unique(y_true).size)[y_score]
                return y_true, y_score, binary, var_type
            elif y_score.ndim == 2:
                if len(np.unique(y_true)) == y_score.shape[1]:
                    return y_true, y_score, binary, var_type
                else:
                    raise TypeError(f"Invalid y_score. It should has the number of columns = {len(np.unique(y_true))}")
            else:
                raise TypeError(f"Invalid y_score. It should has shape of 1 or 2 dimensions")
        else:
            raise TypeError(f"Invalid y_true and y_score. Y_true data type should be number and y_score data type should be 1-hot matrix.")


def is_unique_labels_consecutive_and_start_zero(vector):
    labels = np.sort(np.unique(vector))
    if 0 in labels:
        if np.all(np.diff(labels) == 1):
            return True
    return False


def format_external_clustering_data(y_true: np.ndarray, y_pred: np.ndarray):
    """
    Need both of y_true and y_pred to format
    """
    if not (isinstance(y_true, co.SUPPORTED_LIST) and isinstance(y_pred, co.SUPPORTED_LIST)):
        raise TypeError("To calculate external clustering metrics, y_true and y_pred must be lists, tuples or numpy arrays.")
    else:
        ## Remove all dimensions of size 1
        y_true, y_pred = np.squeeze(np.asarray(y_true)), np.squeeze(np.asarray(y_pred))
        if not (y_true.ndim == y_pred.ndim):
            raise TypeError("To calculate external clustering metrics, y_true and y_pred must have the same number of dimensions.")
        else:
            if y_true.ndim == 1:
                if np.issubdtype(y_true.dtype, np.number):
                    if is_unique_labels_consecutive_and_start_zero(y_true):
                        return y_true, y_pred, None
                le = LabelEncoder()
                y_true = le.fit_transform(y_true)
                y_pred = le.transform(y_pred)
                return y_true, y_pred, le
            else:
                raise TypeError("To calculate clustering metrics, y_true and y_pred must be a 1-D vector.")


def format_internal_clustering_data(y_pred: np.ndarray):
    if not (isinstance(y_pred, co.SUPPORTED_LIST)):
        raise TypeError("To calculate internal clustering metrics, y_pred must be lists, tuples or numpy arrays.")
    else:
        ## Remove all dimensions of size 1
        y_pred = np.squeeze(np.asarray(y_pred))
        if y_pred.ndim == 1:
            if np.issubdtype(y_pred.dtype, np.number):
                y_pred = np.round(y_pred).astype(int)
                if is_unique_labels_consecutive_and_start_zero(y_pred):
                    return y_pred, None
            le = LabelEncoder()
            labels = le.fit_transform(y_pred)
            return labels, le
        else:
            raise TypeError("To calculate clustering metrics, labels must be a 1-D vector.")
