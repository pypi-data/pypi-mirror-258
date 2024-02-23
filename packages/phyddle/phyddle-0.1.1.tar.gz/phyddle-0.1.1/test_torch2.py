import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torch.utils.data import Dataset, DataLoader
from neuralforecast import NeuralForecast #QuantileLoss
from neuralforecast.losses.pytorch import MQLoss, QuantileLoss
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np

import torch.nn.functional as F
import pandas as pd

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
my_device = torch.device(device)  # NEEDED TO USE ALL AVAIL CPU/THREADS
print(f'Using {my_device}')

# Creating our dataset class
class Build_Data2(Dataset):
    # Constructor
    def __init__(self):
        self.x = torch.arange(-5, 5, 0.001).view(-1, 1)
        self.func = -5 * self.x + 1
        self.y = self.func + 0.4 * torch.randn(self.x.size())
        self.len = self.x.shape[0]
    # Getting the data
    def __getitem__(self, index):
        return self.x[index], self.y[index]
    # Getting length of the data
    def __len__(self):
        return self.len

# # Create dataset object
data_set = Build_Data2()

# # Creating Dataloader object
trainloader = DataLoader(dataset = data_set, batch_size=100)
n_iter = 1000

loss_fn = torch.nn.MSELoss()
model = torch.nn.Linear(1, 1)
model.to(my_device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)


loss_Adam = []
for i in range(n_iter):
    if i % 10 == 0:
        print(f'Iteration {i}')
    for x, y in trainloader:
        # making a prediction in forward pass
        x = x.to(my_device)
        y = y.to(my_device)
        y_hat = model(x)
        # calculating the loss between original and predicted data points
        loss = loss_fn(y_hat, y)
        # store loss into list
        loss_Adam.append(loss.item())
        # zeroing gradients after each iteration
        optimizer.zero_grad()
        # backward pass for computing the gradients of the loss w.r.t to learnable parameters
        loss.backward()
        # updateing the parameters after each iteration
        optimizer.step()


print(model)

