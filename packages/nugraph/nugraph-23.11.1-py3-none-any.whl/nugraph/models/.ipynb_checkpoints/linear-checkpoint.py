import torch
from torch import Tensor
import torch.nn as nn

class ClassLinear(nn.Module):
    '''Linear convolution module grouped by class'''
    def __init__(self,
                 in_features: int,
                 out_features: int,
                 num_classes: int):
        super().__init__()

        self.num_classes = num_classes

        self.net = nn.ModuleList()
        for _ in range(num_classes):
            self.net.append(nn.Linear(in_features, out_features))

    def forward(self, X: Tensor) -> Tensor:
        x = torch.tensor_split(X, self.num_classes, dim=1)
        return torch.cat([ net(x[i]) for i, net in enumerate(self.net) ], dim=1)

class PaddedSoftmax(nn.Module):
    '''Softmax padded with extra value'''
    def __init__(self):
        super().__init__()

    def forward(self, x: Tensor) -> Tensor:
        pad = torch.zeros(x.size(0), 1, x.size(2), device=x.device)
        x = torch.cat((x, pad), dim=1).softmax(dim=1)
        return x[:,0:-1,:]
