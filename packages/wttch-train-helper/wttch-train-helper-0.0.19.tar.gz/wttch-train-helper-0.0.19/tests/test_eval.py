import unittest

import torch
from torch import nn

from wttch.train.eval import evaluate_model
from wttch.train.torch.utils import module_to, tensor_to


class TestEval(unittest.TestCase):

    def test_eval(self):
        net = nn.Linear(100, 10)
        module_to(net)
        x = torch.randn((100, 100))
        y = torch.randn((100, 1))
        x, y = tensor_to(x, y)
        print(evaluate_model(net, [(x, y)]))
