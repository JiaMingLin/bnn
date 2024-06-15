import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.datasets as dsets
from torch import Tensor
import torch.nn.functional as F

import pdb
import math

class LSTMCell(nn.Module):
    def __init__(self, input_size, hidden_size, bias=True):
        super(LSTMCell, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.bias = bias
        self.x2h = nn.Linear(input_size, 4 * hidden_size, bias=bias)
        self.h2h = nn.Linear(hidden_size, 4 * hidden_size, bias=bias)
        self.c2c = Tensor(hidden_size)
        self.reset_parameters()
        pass
    
    def reset_parameters(self):
        std = 1.0 / math.sqrt(self.hidden_size)
        for w in self.parameters():
            w.data.uniform_(-std, std)
        pass

    def forward(self, x, hidden):

        hx, cx = hidden
        x = x.view(-1, x.size(1))
        gates = self.x2h(x) + self.h2h(hx)
        forget_gate, input_gate, cell_gate, out_gate = gates.chunk(4, 1)
        
        forget_gate = torch.sigmoid(forget_gate)
        input_gate = torch.sigmoid(input_gate)
        cell_gate = torch.tanh(cell_gate)
        out_gate = torch.sigmoid(out_gate)

        cell_gate = forget_gate * cx + input_gate * cell_gate
        hx = out_gate * torch.tanh(cell_gate)
        
        return (hx, cell_gate)

class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, layer_dim, output_dim, bias=True):
        super(LSTMModel, self).__init__()
        # Hidden dimensions
        self.hidden_dim = hidden_dim
         
        # Number of hidden layers
        self.layer_dim = layer_dim
               
        self.lstm = LSTMCell(input_dim, hidden_dim, layer_dim)  
        
        self.fc = nn.Linear(hidden_dim, output_dim)
     
    
    
    def forward(self, x):
        
        # Initialize hidden state with zeros
        #######################
        #  USE GPU FOR MODEL  #
        #######################
        #print(x.shape,"x.shape")100, 28, 28
        if torch.cuda.is_available():
            h0 = Tensor(torch.zeros(self.layer_dim, x.size(0), self.hidden_dim).cuda())
        else:
            h0 = Tensor(torch.zeros(self.layer_dim, x.size(0), self.hidden_dim))

        # Initialize cell state
        if torch.cuda.is_available():
            c0 = Tensor(torch.zeros(self.layer_dim, x.size(0), self.hidden_dim).cuda())
        else:
            c0 = Tensor(torch.zeros(self.layer_dim, x.size(0), self.hidden_dim))

                    
       
        outs = []
        
        cn = c0[0,:,:]
        hn = h0[0,:,:]
        
        for seq in range(x.size(1)):
            hn, cn = self.lstm(x[:,seq,:], (hn,cn)) 
            outs.append(hn)
            
    
        out = outs[-1].squeeze()
        
        out = self.fc(out) 
        # out.size() --> 100, 10
        return out