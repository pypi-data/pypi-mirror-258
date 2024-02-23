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
#print(f"Using {device} device")

class Build_Data(Dataset):
    # Constructor
    def __init__(self):
        self.base_fn = '/Users/mlandis/projects/phyddle/workspace/format/Rev_GeoSSE/'
        self.tree_width = 500
        self.tree_rows = 3
        self.char_rows = 7
        self.total_rows = self.tree_rows + self.char_rows

        self.labels_fn  = self.base_fn + 'train.nt500.labels.csv'
        self.phy_dat_fn = self.base_fn + 'train.nt500.phy_data.csv'
        self.aux_dat_fn = self.base_fn + 'train.nt500.aux_data.csv'

        self.labels     = pd.read_csv(self.labels_fn, sep=',').to_numpy(dtype='float32')
        self.phy_data   = pd.read_csv(self.phy_dat_fn, sep=',', header=None).to_numpy(dtype='float32')
        self.aux_data   = pd.read_csv(self.aux_dat_fn, sep=',').to_numpy(dtype='float32')

        self.len        = self.labels.shape[0]
        self.phy_data.shape = (self.len, self.total_rows, self.tree_width)


    # Getting the dataq
    def __getitem__(self, index):
        return self.phy_data[index], self.aux_data[index], self.labels[index]

    # Getting length of the data
    def __len__(self):
        return self.len



class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()

        self.num_tree_rows = 3
        self.num_data_rows = 7
        self.num_total_rows = self.num_tree_rows + self.num_data_rows
        self.num_aux_data_col = 20
        self.num_labels = 4
        input_channels = 1
        input_size = 320 # concat width???


        # Phylogenetic Tensor layers
        # Standard convolution layers
        self.conv_std1 = nn.Conv1d(in_channels=self.num_total_rows, out_channels=64, kernel_size=3, padding='same')
        self.conv_std2 = nn.Conv1d(in_channels=64, out_channels=96, kernel_size=5, padding='same')
        self.conv_std3 = nn.Conv1d(in_channels=96, out_channels=128, kernel_size=7, padding='same')
        self.pool_std = nn.AdaptiveAvgPool1d(1)

        # Stride convolution layers
        self.conv_stride1 = nn.Conv1d(in_channels=self.num_total_rows, out_channels=64, kernel_size=7, stride=3)
        self.conv_stride2 = nn.Conv1d(in_channels=64, out_channels=96, kernel_size=9, stride=6)
        self.pool_stride = nn.AdaptiveAvgPool1d(1)

        # Dilated convolution layers
        self.conv_dilate1 = nn.Conv1d(in_channels=self.num_total_rows, out_channels=32, kernel_size=3, dilation=2, padding='same')
        self.conv_dilate2 = nn.Conv1d(in_channels=32, out_channels=64, kernel_size=5, dilation=4, padding='same')
        self.pool_dilate = nn.AdaptiveAvgPool1d(1)

        # self.conv_std1.float()
        # self.conv_stride1.float()
        # self.conv_dilate1.float()

        # Auxiliary Data layers
        self.aux_ffnn_1 = nn.Linear(self.num_aux_data_col, 128)
        self.aux_ffnn_2 = nn.Linear(128, 64)
        self.aux_ffnn_3 = nn.Linear(64, 32)

        # Label Value layers
        self.point_ffnn1 = nn.Linear(input_size, 128)
        self.point_ffnn2 = nn.Linear(128, 64)
        self.point_ffnn3 = nn.Linear(64, 32)
        self.point_ffnn4 = nn.Linear(32, self.num_labels)

        # Label Lower layers
        self.lower_ffnn1 = nn.Linear(input_size, 128)
        self.lower_ffnn2 = nn.Linear(128, 64)
        self.lower_ffnn3 = nn.Linear(64, 32)
        self.lower_ffnn4 = nn.Linear(32, self.num_labels)

        # Label Upper layers
        self.upper_ffnn1 = nn.Linear(input_size, 128)
        self.upper_ffnn2 = nn.Linear(128, 64)
        self.upper_ffnn3 = nn.Linear(64, 32)
        self.upper_ffnn4 = nn.Linear(32, self.num_labels)

    def forward(self, phy_dat, aux_dat):

        # Phylogenetic Tensor forwarding
        # Standard convolutions
        phy_dat = phy_dat.float()
        aux_dat = aux_dat.float()
        x_std = nn.ReLU()(self.conv_std1(phy_dat))
        x_std = nn.ReLU()(self.conv_std2(x_std))
        x_std = nn.ReLU()(self.conv_std3(x_std))
        x_std = self.pool_std(x_std)

        # Stride convolutions
        x_stride = nn.ReLU()(self.conv_stride1(phy_dat))
        x_stride = nn.ReLU()(self.conv_stride2(x_stride))
        x_stride = self.pool_stride(x_stride)

        # Dilated convolutions
        x_dilated = nn.ReLU()(self.conv_dilate1(phy_dat))
        x_dilated = nn.ReLU()(self.conv_dilate2(x_dilated))
        x_dilated = self.pool_dilate(x_dilated)

        # Auxiliary Data Tensor forwarding
        x_aux_ffnn = F.relu(self.aux_ffnn_1(aux_dat))
        x_aux_ffnn = F.relu(self.aux_ffnn_2(x_aux_ffnn))
        x_aux_ffnn = F.relu(self.aux_ffnn_3(x_aux_ffnn))

        # Concatenate phylo and aux layers
        x_cat = torch.cat((x_std, x_stride, x_dilated, x_aux_ffnn.unsqueeze(dim=2)), dim=1).squeeze()

        # Point estimate path
        x_point_est = F.relu(self.point_ffnn1(x_cat))
        x_point_est = F.relu(self.point_ffnn2(x_point_est))
        x_point_est = F.relu(self.point_ffnn3(x_point_est))
        x_point_est = self.point_ffnn4(x_point_est)

        # Lower quantile path
        x_lower_quantile = F.relu(self.lower_ffnn1(x_cat))
        x_lower_quantile = F.relu(self.lower_ffnn2(x_lower_quantile))
        x_lower_quantile = F.relu(self.lower_ffnn3(x_lower_quantile))
        x_lower_quantile = self.lower_ffnn4(x_lower_quantile)

        # Upper quantile path
        x_upper_quantile = F.relu(self.upper_ffnn1(x_cat))
        x_upper_quantile = F.relu(self.upper_ffnn2(x_upper_quantile))
        x_upper_quantile = F.relu(self.upper_ffnn3(x_upper_quantile))
        x_upper_quantile = self.upper_ffnn4(x_upper_quantile)

        # https://medium.com/the-artificial-impostor/quantile-regression-part-2-6fdbc26b2629
        # return loss
        return (x_point_est, x_lower_quantile, x_upper_quantile)


# analysis settings
num_iter = 5
batch_size = 1024
num_cores = 14

# dataset
data_set = Build_Data()
trainloader = DataLoader(dataset=data_set, batch_size=batch_size)

# model stuff
torch.set_num_threads(num_cores)
model = NeuralNetwork()
#model.to(device)
loss_value_func = torch.nn.MSELoss()
q_width = 0.95
q_tail = (1.0 - q_width) / 2
q_lower = 1.0 - q_tail
q_upper = q_tail
qloss_lower_func = QuantileLoss(q=q_lower)
qloss_upper_func = QuantileLoss(q=q_upper)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)


# test one iteration of training
#phy_dat, aux_dat, lbls = list(trainloader)[0]
#lbls_hat = model(phy_dat, aux_dat)

# training
#loss_Adam = []
running_loss = 0
for i in range(num_iter):
    print(i)
    for phy_dat, aux_dat, lbls in trainloader:
        # making a prediction in forward pass
        lbls_hat = model(phy_dat, aux_dat)
        # calculating the loss between original and predicted data points
        loss_value = loss_value_func(lbls_hat[0], lbls)
        loss_lower = qloss_lower_func(lbls_hat[1], lbls)
        loss_upper = qloss_upper_func(lbls_hat[2], lbls)
        #loss_lower = loss_pinball(lbls_hat, lbls)
        #loss_upper = loss_pinball(lbls_hat, lbls)
        # ... different loss functions for lower/upper pinball loss
        # store loss into list
        #loss_Adam.append(loss_value.item())
        # zeroing gradients after each iteration
        optimizer.zero_grad()
        # backward pass for computing the gradients of the loss w.r.t to learnable parameters
        loss = loss_value + loss_lower + loss_upper
        loss.backward()
        # updateing the parameters after each iteration
        optimizer.step()



idx = 0
y_value = lbls_hat[0][:,idx].detach().numpy()
y_lower = lbls_hat[1][:,idx].detach().numpy()
y_upper = lbls_hat[2][:,idx].detach().numpy()
y_true = lbls[:,idx].detach().numpy()

coverage = sum( np.logical_and(y_lower < y_true, y_upper > y_true) ) / len(y_true)

plt.scatter( y_true, y_value, color='blue' )
plt.plot([y_true,y_true],
         [y_lower,y_upper],
          color='blue' )
plt.axline(xy1=[0,0], slope=1, color='black')
plt.savefig(f'example_{idx}.pdf', format='pdf', dpi=300, bbox_inches='tight')
#plt.show()
#plt.close()


# plt.scatter(lbl_true[stat_not_cover], lbl_est[stat_not_cover],
#             alpha=alpha, c='red', zorder=5, s=3)
# # not covered bars
# plt.plot([lbl_true[stat_not_cover], lbl_true[stat_not_cover]],
#             [lbl_lower[stat_not_cover], lbl_upper[stat_not_cover]],
#             color='red', alpha=alpha, linestyle="-", marker='_',
#             linewidth=0.5, zorder=4 )

#lbls_hat = model(phy_dat, aux_dat)

#print(model)

print(lbls_hat)
print(lbls)






# #-----------------_#

# # Creating our dataset class
# class Build_Data2(Dataset):
#     # Constructor
#     def __init__(self):
#         self.x = torch.arange(-5, 5, 0.1).view(-1, 1)
#         self.func = -5 * self.x + 1
#         self.y = self.func + 0.4 * torch.randn(self.x.size())
#         self.len = self.x.shape[0]
#     # Getting the data
#     def __getitem__(self, index):
#         return self.x[index], self.y[index]
#     # Getting length of the data
#     def __len__(self):
#         return self.len

# # Create dataset object
# data_set = Build_Data()

# # Creating Dataloader object
# trainloader = DataLoader(dataset = data_set, batch_size=1)
# n_iter = 100

# model = torch.nn.Linear(1, 1)

# loss_Adam = []
# for i in range(n_iter):
#     for x, y in trainloader:
#         # making a pridiction in forward pass
#         y_hat = model(x)
#         # calculating the loss between original and predicted data points
#         loss = loss_fn(y_hat, y)
#         # store loss into list
#         loss_Adam.append(loss.item())
#         # zeroing gradients after each iteration
#         optimizer.zero_grad()
#         # backward pass for computing the gradients of the loss w.r.t to learnable parameters
#         loss.backward()
#         # updateing the parameters after each iteration
#         optimizer.step()


# print(model)

#     #     w_conv = layers.Conv1D(64, 3, activation = 'relu', padding = 'same', name='conv_std1')(input_data_tensor)
#     #     w_conv = layers.Conv1D(96, 5, activation = 'relu', padding = 'same', name='conv_std2')(w_conv)
#     #     w_conv = layers.Conv1D(128, 7, activation = 'relu', padding = 'same', name='conv_std3')(w_conv)
#     #     w_conv_gavg = layers.GlobalAveragePooling1D(name='pool_std')(w_conv)

#     #     # stride layers (skip sizes during slide)
#     #     w_stride = layers.Conv1D(64, 7, strides = 3, activation = 'relu',padding = 'same', name='conv_stride1')(input_data_tensor)
#     #     w_stride = layers.Conv1D(96, 9, strides = 6, activation = 'relu', padding = 'same', name='conv_stride2')(w_stride)
#     #     w_stride_gavg = layers.GlobalAveragePooling1D(name = 'pool_stride')(w_stride)

#     #     # dilation layers (spacing among grid elements)
#     #     w_dilated = layers.Conv1D(32, 3, dilation_rate = 2, activation = 'relu', padding = 'same', name='conv_dilate1')(input_data_tensor)
#     #     w_dilated = layers.Conv1D(64, 5, dilation_rate = 4, activation = 'relu', padding = 'same', name='conv_dilate2')(w_dilated)
#     #     w_dilated_gavg = layers.GlobalAveragePooling1D(name = 'pool_dilate')(w_dilated)

