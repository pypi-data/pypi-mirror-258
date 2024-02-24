#!/usr/bin/env python
# Created by "Thieu" at 09:29, 23/09/2020 ----------%
#       Email: nguyenthieu2102@gmail.com            %
#       Github: https://github.com/thieu1995        %
# --------------------------------------------------%

from permetrics.evaluator import Evaluator
from permetrics.utils import data_util as du
from permetrics.utils import classifier_util as cu
import numpy as np


class ClassificationMetric(Evaluator):
    """
    Defines a ClassificationMetric class that hold all classification metrics
    (for both binary and multiple classification problem)

    Parameters
    ----------
    y_true: tuple, list, np.ndarray, default = None
        The ground truth values.

    y_pred: tuple, list, np.ndarray, default = None
        The prediction values.

    labels: tuple, list, np.ndarray, default = None
        List of labels to index the matrix. This may be used to reorder or select a subset of labels.

    average: (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"
        If None, the scores for each class are returned. Otherwise, this determines the type of averaging performed on the data:

        ``'micro'``:
            Calculate metrics globally by considering each element of the label indicator matrix as a label.
        ``'macro'``:
            Calculate metrics for each label, and find their unweighted mean.  This does not take label imbalance into account.
        ``'weighted'``:
            Calculate metrics for each label, and find their average, weighted by support (the number of true instances for each label).
    """

    SUPPORT = {
        "PS": {"type": "max", "range": "[0, 1]", "best": "1"},
        "NPV": {"type": "max", "range": "[0, 1]", "best": "1"},
        "RS": {"type": "max", "range": "[0, 1]", "best": "1"},
        "AS": {"type": "max", "range": "[0, 1]", "best": "1"},
        "F1S": {"type": "max", "range": "[0, 1]", "best": "1"},
        "F2S": {"type": "max", "range": "[0, 1]", "best": "1"},
        "FBS": {"type": "max", "range": "[0, 1]", "best": "1"},
        "SS": {"type": "max", "range": "[0, 1]", "best": "1"},
        "MCC": {"type": "max", "range": "[-1, +1]", "best": "1"},
        "HS": {"type": "max", "range": "[0, 1]", "best": "1"},
        "CKS": {"type": "max", "range": "[-1, +1]", "best": "1"},
        "JSI": {"type": "max", "range": "[0, 1]", "best": "1"},
        "GMS": {"type": "max", "range": "[0, 1]", "best": "1"},
        "ROC-AUC": {"type": "max", "range": "[0, 1]", "best": "1"},
        "LS": {"type": "max", "range": "[0, +inf)", "best": "no best"},
        "GINI": {"type": "min", "range": "[0, 1]", "best": "0"},
        "CEL": {"type": "min", "range": "[0, +inf)", "best": "0"},
        "HL": {"type": "min", "range": "[0, +inf)", "best": "0"},
        "KLDL": {"type": "min", "range": "[0, +inf)", "best": "0"},
        "BSL": {"type": "min", "range": "[0, 1]", "best": "0"}
    }

    def __init__(self, y_true=None, y_pred=None, **kwargs):
        super().__init__(y_true, y_pred, **kwargs)
        if kwargs is None: kwargs = {}
        self.set_keyword_arguments(kwargs)
        self.binary = True
        self.representor = "number"     # "number" or "string"
        self.le = None  # LabelEncoder

    @staticmethod
    def get_support(name=None, verbose=True):
        if name == "all":
            if verbose:
                for key, value in ClassificationMetric.SUPPORT.items():
                    print(f"Metric {key} : {value}")
            return ClassificationMetric.SUPPORT
        if name not in list(ClassificationMetric.SUPPORT.keys()):
            raise ValueError(f"ClassificationMetric doesn't support metric named: {name}")
        else:
            if verbose:
                print(f"Metric {name}: {ClassificationMetric.SUPPORT[name]}")
            return ClassificationMetric.SUPPORT[name]

    def get_processed_data(self, y_true=None, y_pred=None):
        """
        Args:
            y_true (tuple, list, np.ndarray): The ground truth values
            y_pred (tuple, list, np.ndarray): The prediction values

        Returns:
            y_true_final: y_true used in evaluation process.
            y_pred_final: y_pred used in evaluation process
            one_dim: is y_true has 1 dimensions or not
        """
        if (y_true is not None) and (y_pred is not None):
            y_true, y_pred, binary, representor = du.format_classification_data(y_true, y_pred)
        else:
            if (self.y_true is not None) and (self.y_pred is not None):
                y_true, y_pred, binary, representor = du.format_classification_data(self.y_true, self.y_pred)
            else:
                raise ValueError("y_true or y_pred is None. You need to pass y_true and y_pred to object creation or function called.")
        return y_true, y_pred, binary, representor

    def get_processed_data2(self, y_true=None, y_pred=None):
        """
        Args:
            y_true (tuple, list, np.ndarray): The ground truth values
            y_pred (tuple, list, np.ndarray): The prediction scores

        Returns:
            y_true_final: y_true used in evaluation process.
            y_pred_final: y_pred used in evaluation process
            one_dim: is y_true has 1 dimensions or not
        """
        if (y_true is not None) and (y_pred is not None):
            y_true, y_pred, binary, representor = du.format_y_score(y_true, y_pred)
        else:
            if (self.y_true is not None) and (self.y_pred is not None):
                y_true, y_pred, binary, representor = du.format_y_score(self.y_true, self.y_pred)
            else:
                raise ValueError("y_true or y_pred is None. You need to pass y_true and y_pred to object creation or function called.")
        return y_true, y_pred, binary, representor

    def confusion_matrix(self, y_true=None, y_pred=None, labels=None, normalize=None, **kwargs):
        """
        Generate confusion matrix and useful information

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            normalize ('true', 'pred', 'all', None): Normalizes confusion matrix over the true (rows), predicted (columns) conditions or all the population.

        Returns:
            matrix (np.ndarray): a 2-dimensional list of pairwise counts
            imap (dict): a map between label and index of confusion matrix
            imap_count (dict): a map between label and number of true label in y_true
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize)
        return matrix, imap, imap_count

    def precision_score(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Generate precision score for multiple classification problem
        Higher is better (Best = 1), Range = [0, 1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"
                If None, the scores for each class are returned. Otherwise, this determines the type of averaging performed on the data:

                ``'micro'``:
                    Calculate metrics globally by considering each element of the label indicator matrix as a label.
                ``'macro'``:
                    Calculate metrics for each label, and find their unweighted mean.  This does not take label imbalance into account.
                ``'weighted'``:
                    Calculate metrics for each label, and find their average, weighted by support (the number of true instances for each label).

        Returns:
            precision (float, dict): the precision score
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_precision = np.array([item["precision"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])

        if average == "micro":
            tp_global = np.sum(np.diag(matrix))
            fp_global = fn_global = np.sum(matrix) - tp_global
            result = tp_global / (tp_global + fp_global)
        elif average == "macro":
            result = np.mean(list_precision)
        elif average == "weighted":
            result = np.dot(list_weights, list_precision) / np.sum(list_weights)
        else:
            result = dict([(label, item["precision"]) for label, item in metrics.items()])
        return result

    def negative_predictive_value(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Generate negative predictive value for multiple classification problem
        Higher is better (Best = 1), Range = [0, 1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            npv (float, dict): the negative predictive value
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_npv = np.array([item["negative_predictive_value"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])

        if average == "micro":
            tp_global = tn_global = np.sum(np.diag(matrix))
            fp_global = fn_global = np.sum(matrix) - tp_global
            result = tn_global / (tn_global + fn_global)
        elif average == "macro":
            result = np.mean(list_npv)
        elif average == "weighted":
            result = np.dot(list_weights, list_npv) / np.sum(list_weights)
        else:
            result = dict([(label, item["negative_predictive_value"]) for label, item in metrics.items()])
        return result

    def specificity_score(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Generate specificity score for multiple classification problem
        Higher is better (Best = 1), Range = [0, 1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            ss (float, dict): the specificity score
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_ss = np.array([item["specificity"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])

        if average == "micro":
            tp_global = tn_global = np.sum(np.diag(matrix))
            fp_global = fn_global = np.sum(matrix) - tp_global
            result = tn_global / (tn_global + fp_global)
        elif average == "macro":
            result = np.mean(list_ss)
        elif average == "weighted":
            result = np.dot(list_weights, list_ss) / np.sum(list_weights)
        else:
            result = dict([(label, item["specificity"]) for label, item in metrics.items()])
        return result

    def recall_score(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Generate recall score for multiple classification problem
        Higher is better (Best = 1), Range = [0, 1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            recall (float, dict): the recall score
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_recall = np.array([item["recall"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])

        if average == "micro":
            tp_global = np.sum(np.diag(matrix))
            fp_global = fn_global = np.sum(matrix) - tp_global
            result = tp_global / (tp_global + fn_global)
        elif average == "macro":
            result = np.mean(list_recall)
        elif average == "weighted":
            result = np.dot(list_weights, list_recall) / np.sum(list_weights)
        else:
            result = dict([(label, item["recall"]) for label, item in metrics.items()])
        return result

    def accuracy_score(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Generate accuracy score for multiple classification problem
        Higher is better (Best = 1), Range = [0, 1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            accuracy (float, dict): the accuracy score
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_accuracy = np.array([item["accuracy"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])
        list_tp = np.array([item['tp'] for item in metrics.values()])

        if average == "micro":
            result = np.sum(list_tp) / np.sum(list_weights)
        elif average == "macro":
            result = np.mean(list_accuracy)
        elif average == "weighted":
            result = np.dot(list_weights, list_accuracy) / np.sum(list_weights)
        else:
            result = dict([(label, item["accuracy"]) for label, item in metrics.items()])
        return result

    def f1_score(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Generate f1 score for multiple classification problem
        Higher is better (Best = 1), Range = [0, 1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            f1 (float, dict): the f1 score
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_f1 = np.array([item["f1"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])

        if average == "micro":
            tp_global = np.sum(np.diag(matrix))
            fp_global = fn_global = np.sum(matrix) - tp_global
            precision = tp_global / (tp_global + fp_global)
            recall = tp_global / (tp_global + fn_global)
            result = (2 * precision * recall) / (precision + recall)
        elif average == "macro":
            result = np.mean(list_f1)
        elif average == "weighted":
            result = np.dot(list_weights, list_f1) / np.sum(list_weights)
        else:
            result = dict([(label, item["f1"]) for label, item in metrics.items()])
        return result

    def f2_score(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Generate f2 score for multiple classification problem
        Higher is better (Best = 1), Range = [0, 1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            f2 (float, dict): the f2 score
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_f2 = np.array([item["f2"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])

        if average == "micro":
            tp_global = np.sum(np.diag(matrix))
            fp_global = fn_global = np.sum(matrix) - tp_global
            precision = tp_global / (tp_global + fp_global)
            recall = tp_global / (tp_global + fn_global)
            result = (5 * precision * recall) / (4 * precision + recall)
        elif average == "macro":
            result = np.mean(list_f2)
        elif average == "weighted":
            result = np.dot(list_weights, list_f2) / np.sum(list_weights)
        else:
            result = dict([(label, item["f2"]) for label, item in metrics.items()])
        return result

    def fbeta_score(self, y_true=None, y_pred=None, beta=1.0, labels=None, average="macro", **kwargs):
        """
        The beta parameter determines the weight of recall in the combined score.
        beta < 1 lends more weight to precision, while beta > 1 favors recall
        (beta -> 0 considers only precision, beta -> +inf only recall).
        Higher is better (Best = 1), Range = [0, 1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            beta (float): the weight of recall in the combined score, default = 1.0
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            fbeta (float, dict): the fbeta score
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count, beta=beta)

        list_fbeta = np.array([item["fbeta"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])

        if average == "micro":
            tp_global = np.sum(np.diag(matrix))
            fp_global = fn_global = np.sum(matrix) - tp_global
            precision = tp_global / (tp_global + fp_global)
            recall = tp_global / (tp_global + fn_global)
            result = ((1 + beta ** 2) * precision * recall) / (beta ** 2 * precision + recall)
        elif average == "macro":
            result = np.mean(list_fbeta)
        elif average == "weighted":
            result = np.dot(list_weights, list_fbeta) / np.sum(list_weights)
        else:
            result = dict([(label, item["fbeta"]) for label, item in metrics.items()])
        return result

    def matthews_correlation_coefficient(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Generate Matthews Correlation Coefficient
        Higher is better (Best = 1), Range = [-1, +1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            mcc (float, dict): the Matthews correlation coefficient
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_mcc = np.array([item["mcc"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])

        if average == "micro":
            tp = tn = np.sum(np.diag(matrix))
            fp = fn = np.sum(matrix) - tp
            result = (tp * tn - fp * fn) / np.sqrt(((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)))
        elif average == "macro":
            result = np.mean(list_mcc)
        elif average == "weighted":
            result = np.dot(list_weights, list_mcc) / np.sum(list_weights)
        else:
            result = dict([(label, item["mcc"]) for label, item in metrics.items()])
        return result

    def hamming_score(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Generate hamming score for multiple classification problem
        Higher is better (Best = 1), Range = [0, 1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            hl (float, dict): the hamming score
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_hs = np.array([item["hamming_score"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])
        list_tp = np.array([item['tp'] for item in metrics.values()])

        if average == "micro":
            result = 1.0 - np.sum(list_tp) / np.sum(list_weights)
        elif average == "macro":
            result = np.mean(list_hs)
        elif average == "weighted":
            result = np.dot(list_weights, list_hs) / np.sum(list_weights)
        else:
            result = dict([(label, item["hamming_score"]) for label, item in metrics.items()])
        return result

    def lift_score(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Generate lift score for multiple classification problem
        Higher is better (Best = +1), Range = [0, +1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            ls (float, dict): the lift score
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_ls = np.array([item["lift_score"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])

        if average == "micro":
            tp = tn = np.sum(np.diag(matrix))
            fp = fn = np.sum(matrix) - tp
            result = (tp/(tp + fp)) / ((tp + fn) / (tp + tn + fp + fn))
        elif average == "macro":
            result = np.mean(list_ls)
        elif average == "weighted":
            result = np.dot(list_weights, list_ls) / np.sum(list_weights)
        else:
            result = dict([(label, item["lift_score"]) for label, item in metrics.items()])
        return result

    def cohen_kappa_score(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Generate Cohen Kappa score for multiple classification problem
        Higher is better (Best = +1), Range = [-1, +1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            cks (float, dict): the Cohen Kappa score
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_kp = np.array([item["kappa_score"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])

        if average == 'weighted':
            result = np.dot(list_weights, list_kp) / np.sum(list_weights)
        elif average == 'macro':
            result = np.mean(list_kp)
        elif average == 'micro':
            result = np.average(list_kp)
        else:
            result = dict([(label, item["kappa_score"]) for label, item in metrics.items()])
        return result

    def jaccard_similarity_index(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Generate Jaccard similarity index for multiple classification problem
        Higher is better (Best = +1), Range = [0, +1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            jsi (float, dict): the Jaccard similarity index
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_js = np.array([item["jaccard_similarities"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])

        if average == "micro":
            tp = tn = np.sum(np.diag(matrix))
            fp = fn = np.sum(matrix) - tp
            result = tp / (tp + fp + fn)
        elif average == "macro":
            result = np.mean(list_js)
        elif average == "weighted":
            result = np.dot(list_weights, list_js) / np.sum(list_weights)
        else:
            result = dict([(label, item["jaccard_similarities"]) for label, item in metrics.items()])
        return result

    def g_mean_score(self, y_true=None, y_pred=None, labels=None, average="macro", **kwargs):
        """
        Calculates the G-mean (Geometric mean) score between y_true and y_pred.
        Higher is better (Best = +1), Range = [0, +1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes
            labels (tuple, list, np.ndarray): List of labels to index the matrix. This may be used to reorder or select a subset of labels.
            average (str, None): {'micro', 'macro', 'weighted'} or None, default="macro"

        Returns:
            float, dict: The G-mean score.
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        matrix, imap, imap_count = cu.calculate_confusion_matrix(y_true, y_pred, labels, normalize=None)
        metrics = cu.calculate_single_label_metric(matrix, imap, imap_count)

        list_gm = np.array([item["g_mean"] for item in metrics.values()])
        list_weights = np.array([item["n_true"] for item in metrics.values()])

        if average == "micro":
            tp = tn = np.sum(np.diag(matrix))
            fp = fn = np.sum(matrix) - tp
            result = np.sqrt((tp / (tp + fn)) * (tn / (tn + fp)))
        elif average == "macro":
            result = np.mean(list_gm)
        elif average == "weighted":
            result = np.dot(list_weights, list_gm) / np.sum(list_weights)
        else:
            result = dict([(label, item["g_mean"]) for label, item in metrics.items()])
        return result

    def gini_index(self, y_true=None, y_pred=None, **kwargs):
        """
        Calculates the Gini index between y_true and y_pred.
        Smaller is better (Best = 0), Range = [0, +1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of integers or strings for y_pred classes

        Returns:
            float, dict: The Gini index
        """
        y_true, y_pred, binary, representor = self.get_processed_data(y_true, y_pred)
        # Calculate class probabilities
        total_samples = len(y_true)
        y_prob = np.zeros(total_samples)
        for idx in range(0, total_samples):
            if y_true[idx] == y_pred[idx]:
                y_prob[idx] = 1
            else:
                y_prob[idx] = 0
        positive_samples = np.sum(y_prob)
        negative_samples = total_samples - positive_samples
        p_positive = positive_samples / total_samples
        p_negative = negative_samples / total_samples
        # Calculate Gini index
        result = 1 - (p_positive ** 2 + p_negative ** 2)
        return result

    def crossentropy_loss(self, y_true=None, y_pred=None, **kwargs):
        """
        Calculates the Cross-Entropy loss between y_true and y_pred.
        Smaller is better (Best = 0), Range = [0, +inf)

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): A LIST OF PREDICTED SCORES (NOT LABELS)

        Returns:
            float: The Cross-Entropy loss
        """
        y_true, y_pred, binary, representor = self.get_processed_data2(y_true, y_pred)
        num_classes = len(np.unique(y_true))
        y_true = np.eye(num_classes)[y_true]
        y_pred = np.clip(y_pred, self.EPSILON, 1 - self.EPSILON)
        result = -np.mean(np.sum(y_true * np.log(y_pred), axis=1))
        return result

    def hinge_loss(self, y_true=None, y_pred=None, **kwargs):
        """
        Calculates the Hinge loss between y_true and y_pred.
        Smaller is better (Best = 0), Range = [0, +inf)

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of labels (or predicted scores in case of multi-class)

        Returns:
            float: The Hinge loss
        """
        y_true, y_pred, binary, representor = self.get_processed_data2(y_true, y_pred)
        # Convert y_true to one-hot encoded array
        num_classes = len(np.unique(y_true))
        y_true = np.eye(num_classes)[y_true]
        neg = np.max((1 - y_true) * y_pred, axis=1)
        pos = np.sum(y_true * y_pred, axis=1)
        result = neg - pos + 1
        result[result < 0] = 0
        return np.mean(result)

    def kullback_leibler_divergence_loss(self, y_true=None, y_pred=None, **kwargs):
        """
        Calculates the Kullback-Leibler divergence loss between y_true and y_pred.
        Smaller is better (Best = 0), Range = [0, +inf)

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of labels (or predicted scores in case of multi-class)

        Returns:
            float: The Kullback-Leibler divergence loss
        """
        y_true, y_pred, binary, representor = self.get_processed_data2(y_true, y_pred)
        y_pred = np.clip(y_pred, self.EPSILON, 1 - self.EPSILON)  # Clip predicted probabilities
        # Convert y_true to one-hot encoded array
        num_classes = len(np.unique(y_true))
        y_true = np.eye(num_classes)[y_true]
        y_true = np.clip(y_true, self.EPSILON, 1 - self.EPSILON)  # Clip true labels
        res = np.sum(y_true * np.log(y_true / y_pred), axis=1)
        result = np.mean(res)
        return result

    def brier_score_loss(self, y_true=None, y_pred=None, **kwargs):
        """
        Calculates the Brier Score Loss between y_true and y_pred.
        Smaller is better (Best = 0), Range = [0, 1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): a list of labels (or predicted scores in case of multi-class)

        Returns:
            float, dict: The Brier Score Loss
        """
        y_true, y_pred, binary, representor = self.get_processed_data2(y_true, y_pred)
        # Convert y_true to one-hot encoded array
        num_classes = len(np.unique(y_true))
        y_true = np.eye(num_classes)[y_true]
        result = np.mean(np.sum((y_true - y_pred) ** 2, axis=1))
        return result

    def roc_auc_score(self, y_true=None, y_pred=None, average="macro", **kwargs):
        """
        Calculates the ROC-AUC score between y_true and y_score.
        Higher is better (Best = +1), Range = [0, +1]

        Args:
            y_true (tuple, list, np.ndarray): a list of integers or strings for known classes
            y_pred (tuple, list, np.ndarray): A LIST OF PREDICTED SCORES (NOT LABELS)
            average (str, None): {'macro', 'weighted'} or None, default="macro"

        Returns:
            float, dict: The AUC score.
        """
        y_true, y_score, binary, representor = self.get_processed_data2(y_true, y_pred)
        list_weights = cu.calculate_class_weights(y_true, y_pred=None, y_score=y_score)
        # one-vs-all (rest) approach
        tpr = dict()
        fpr = dict()
        thresholds = dict()
        auc = []
        n_classes = len(np.unique(y_true))
        for i in range(n_classes):
            y_true_i = np.array([1 if y == i else 0 for y in y_true])
            y_score_i = y_score[:, i]
            tpr[i], fpr[i], thresholds[i] = cu.calculate_roc_curve(y_true_i, y_score_i)
            # Calculate the area under the curve (AUC) using the trapezoidal rule
            auc.append(np.trapz(tpr[i], fpr[i]))
        if average == "macro":
            result = np.mean(auc)
        elif average == "weighted":
            result = np.dot(list_weights, auc) / np.sum(list_weights)
        else:
            result = dict([(idx, auc[idx]) for idx in range(n_classes)])
        return result

    CM = confusion_matrix
    PS = precision_score
    NPV = negative_predictive_value
    RS = recall_score
    AS = accuracy_score
    F1S = f1_score
    F2S = f2_score
    FBS = fbeta_score
    SS = specificity_score
    MCC = matthews_correlation_coefficient
    HS = hamming_score
    LS = lift_score
    CKS = cohen_kappa_score
    JSI = JSC = jaccard_similarity_coefficient = jaccard_similarity_index
    GMS = g_mean_score
    GINI = gini_index
    CEL = crossentropy_loss
    HL = hinge_loss
    KLDL = kullback_leibler_divergence_loss
    BSL = brier_score_loss
    ROC = AUC = RAS = roc_auc_score
