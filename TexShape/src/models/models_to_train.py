import torch.nn as nn
import torch
from abc import ABC, abstractmethod

# Encoder class
class Encoder(nn.Module, ABC):
    def __init__(self):
        super().__init__()
        self.in_dim = None
        self.out_dim = None
        self.hidden_dims = None

    @abstractmethod
    def forward(self, x: torch.Tensor):
        pass

    # @property
    # @abstractmethod
    # def in_dim(self):
    #     raise NotImplementedError

    # @property
    # @abstractmethod
    # def out_dim(self):
    #     raise NotImplementedError
    
    # @property
    # @abstractmethod
    # def hidden_dims(self):
    #     raise NotImplementedError

class MIModel(nn.Module):
    def __init__(self, in_dim, hidden_dims, out_dim):
        super(MIModel, self).__init__()
        self.input_sizes = in_dim
        self.hidden_sizes = hidden_dims
        self.output_size = out_dim
        
        layers = []
        prev_size = sum(in_dim)
        
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_size, hidden_dim))
            layers.append(nn.ReLU())
            prev_size = hidden_dim
        
        layers.append(nn.Linear(prev_size, out_dim))
        
        self.layers = nn.Sequential(*layers)

    def forward(self, *inputs):
        inputs = [x.float().view(x.size(0), -1) for x in inputs]
        cat = torch.cat(inputs, 1)
        return self.layers(cat)


    
# class DenseEncoder(nn.Module):
#     # This is the function that its parameters are optimized for encoding
#     def __init__(self, in_size, hidden_size1, hidden_size2, out_size, dropout_rate=0.1):
#         super().__init__()
#         self.in_size = in_size
#         self.out_size = out_size
#         self.layers = nn.Sequential(
#             nn.Linear(in_size, hidden_size1),
#             nn.ReLU(),
#             nn.Dropout(p=dropout_rate),
#             nn.Linear(hidden_size1, hidden_size2),
#             nn.ReLU(),
#             nn.Dropout(p=dropout_rate),
#             nn.Linear(hidden_size2, out_size),
#             nn.ReLU()
#         )

#     def forward(self, x: torch.Tensor):
#         x = x.float()
#         x = self.layers(x)
#         return x
    
class DenseEncoder2(Encoder):
    def __init__(self, in_dim, hidden_dims, out_dim):
        super(DenseEncoder2, self).__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim

        layers = []
        prev_size = in_dim

        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_size, hidden_dim))
            layers.append(nn.ReLU())
            prev_size = hidden_dim

        layers.append(nn.Linear(prev_size, out_dim))
        # layers.append(nn.Tanh())

        self.main = nn.Sequential(*layers)

    def forward(self, x):
        return self.main(x)
    
# class DenseEncoder3(Encoder):
#     def __init__(self, in_dim, hidden_sizes, out_size):
#         super(DenseEncoder3, self).__init__()
#         self.in_size = in_dim
#         self.out_size = out_size

#         layers = []
#         prev_size = in_dim

#         for hidden_size in hidden_sizes:
#             layers.append(nn.Linear(prev_size, hidden_size))
#             layers.append(nn.ReLU())
#             prev_size = hidden_size

#         layers.append(nn.Linear(prev_size, out_size))
#         layers.append(nn.ReLU())
#         # layers.append(nn.Tanh())

#         self.main = nn.Sequential(*layers)

#     def forward(self, x):
#         return self.main(x)

class FlexibleDenseEncoder(Encoder):
    def __init__(self, in_dim, hidden_dims, out_dim):
        super(FlexibleDenseEncoder, self).__init__()
        self.in_size = in_dim
        self.out_size = out_dim

        layers = []
        prev_size = in_dim

        for hidden_size in hidden_dims:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.Tanh())
            prev_size = hidden_size

        layers.append(nn.Linear(prev_size, out_dim))
        layers.append(nn.Tanh())

        self.main = nn.Sequential(*layers)

    def forward(self, x):
        return self.main(x)

# class FlexibleDenseEncoderGELU(Encoder):
#     def __init__(self, in_dim, hidden_sizes, out_size):
#         super(FlexibleDenseEncoderGELU, self).__init__()
#         self.in_size = in_dim
#         self.out_size = out_size

#         layers = []
#         prev_size = in_dim

#         for hidden_size in hidden_sizes:
#             layers.append(nn.Linear(prev_size, hidden_size))
#             layers.append(nn.GELU())
#             prev_size = hidden_size

#         layers.append(nn.Linear(prev_size, out_size))
#         layers.append(nn.Tanh())

#         self.main = nn.Sequential(*layers)

#     def forward(self, x):
#         return self.main(x)

# class FlexibleDenseEncoder2(Encoder):
#     def __init__(self, in_dim, hidden_sizes, out_size):
#         super(FlexibleDenseEncoder2, self).__init__()
#         self.in_size = in_dim
#         self.out_size = out_size

#         layers = []
#         prev_size = in_dim

#         for hidden_size in hidden_sizes:
#             layers.append(nn.Linear(prev_size, hidden_size))
#             layers.append(nn.BatchNorm1d(hidden_size))  # Batch Norm before activation
#             layers.append(nn.GELU())
#             prev_size = hidden_size

#         layers.append(nn.Linear(prev_size, out_size))
#         layers.append(nn.BatchNorm1d(out_size))  # Batch Norm before activation
#         layers.append(nn.Tanh())

#         self.main = nn.Sequential(*layers)

#     def forward(self, x):
#         return self.main(x)

# class MINE(nn.Module):
#     def __init__(self, enc_out_num_nodes):
#         super().__init__()
#         self.layers = nn.Sequential(
#             nn.Linear(enc_out_num_nodes + 1, 100),
#             nn.ReLU(),
#             nn.Linear(100, 100),
#             nn.ReLU(),
#             nn.Linear(100, 1)
#         )

#     def forward(self, z, labels):
#         z, labels = z.float().to(device), labels.float().to(device)
#         z = z.view(z.size(0), -1)
#         cat = torch.cat((z, labels.unsqueeze(-1)), 1)
#         return self.layers(cat)