from torch import Tensor
import torch.nn as nn
import torch
from torch.utils.data import DataLoader

from wttch.train.torch.utils import tensor_to


def evaluate_model(model: nn.Module, test_dataloader: DataLoader) -> float:
    model.eval()
    acc = 0
    total = 0
    with torch.no_grad():
        for X, y in test_dataloader:
            X, y = tensor_to(X, y)  # type: Tensor, Tensor
            acc += accuracy(model(X), y)
            total += y.numel()

    return acc / total


def accuracy(y_hat: Tensor, y: Tensor) -> int:
    if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:
        y_hat = torch.argmax(y_hat, dim=1)
    cmp = y_hat.to(dtype=y.dtype) == y
    return torch.sum(cmp) / y_hat.numel()

