# -*- coding: utf-8 -*-
"""linear regression using pytorch

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fGwTIytNLYTInu6-BHUSwoYcuCDiMFiF
"""

import numpy as np
import torch

# inputs given for the  (a,b,c)
inputs = np.array([[73,24,45],
                  [23,34,56],
                  [12,13,25],
                  [35,65,75],
                  [67,87,98]], dtype='float32')

#output (c,d)
outputs = np.array([[24,35],
            [34,45],
            [45,56],
            [21,26],
            [65,43]],dtype='float32')

inputs = torch.from_numpy(inputs)
targets = torch.from_numpy(outputs)
print(inputs)
print(targets)

# to built linear regression from scratch first assume with initial values of W and b
w = torch.randn(2,3,requires_grad=True)
b = torch.randn(2,requires_grad=True)
print(w)
print(b)

#DEFIN THE FUNCTION
def model(x):
  return x@w.t()+b

preds = model(inputs)
print(preds)

#our targets
print(targets)

# mse function to find out the losses
def mse(t1,t2):
  diff = t1-t2
  return torch.sum(diff*diff)/diff.numel()

loss = mse(preds, targets)
print(loss)

# to minimise the losses we have to take gradient of the loss function
loss.backward()

# variable is w
print(w)
print(w.grad)

with torch.no_grad():
  w -= w.grad * 10e-5
  b -= b.grad * 10e-5

print(w)
print(b)

loss = mse(preds, targets)
print(loss)

#before procide we have to zero the gradient
w.grad.zero_()
b.grad.zero_()

print(w.grad)
print(b.grad)

print(w)

# training and use the updated wieght
preds = model (inputs)
print(preds)

loss = mse(preds, targets)
print(loss)

loss.backward()

print(w.grad)
print(b.grad)

with torch.no_grad():
  w -= w.grad * 10e-5
  b -= b.grad * 10e-5
  w.grad.zero_()
  b.grad.zero_()

print(w)
print(b)

preds = model(inputs)

loss = mse(preds,targets)
print(loss)
#loss.backward()

# now i am training for the multiple epochs(100)
for i in range(100):
  preds = model(inputs)
  loss = mse(preds,targets)
  print(loss)
  loss.backward()
  with torch.no_grad():
    w -= w.grad * 10e-5
    b -= b.grad * 10e-5
    w.grad.zero_()
    b.grad.zero_()

# now take look on loss function

preds = model(inputs)
loss = mse(preds, targets)
print(loss)

preds

targets

#linear regression using pytorch built in functon
import torch.nn as nn

inputs = np.array([[73, 67, 43], 
                   [91, 88, 64], 
                   [87, 134, 58], 
                   [102, 43, 37], 
                   [69, 96, 70], 
                   [74, 66, 43], 
                   [91, 87, 65], 
                   [88, 134, 59], 
                   [101, 44, 37], 
                   [68, 96, 71], 
                   [73, 66, 44], 
                   [92, 87, 64], 
                   [87, 135, 57], 
                   [103, 43, 36], 
                   [68, 97, 70]], 
                  dtype='float32')

targets = np.array([[56, 70], 
                    [81, 101], 
                    [119, 133], 
                    [22, 37], 
                    [103, 119],
                    [57, 69], 
                    [80, 102], 
                    [118, 132], 
                    [21, 38], 
                    [104, 118], 
                    [57, 69], 
                    [82, 100], 
                    [118, 134], 
                    [20, 38], 
                    [102, 120]], 
                   dtype='float32')

inputs = torch.from_numpy(inputs)
targets = torch.from_numpy(targets)

?TensorDataset

from torch.utils.data import TensorDataset

train = TensorDataset(inputs,targets)
train[0:3]

?DataLoader

from torch.utils.data import DataLoader

# Define data loader
batch_size = 5
train = DataLoader(train, batch_size, shuffle=False)

for xb,yb in train:
  print(xb)
  print(yb)
  break

?nn.Linear

model = nn.Linear(3,2)
print(model.weight)
print(model.bias)

preds = model(inputs)
print(preds)

import torch.nn.functional as f

loss_fn = f.mse_loss

loss = loss_fn(preds,targets)
print(loss)

#define optimiser
opt = torch.optim.SGD(model.parameters(), lr=1e-5)

def fit (epochs, model, loss_fn,opt,train):
  for epoch in range(epochs):
    for xb,yb in train:
      pred = model(xb)
      loss = loss_fn(pred,yb)
      loss.backward()
      opt.step()
      opt.zero_grad()
    if (epoch+1) % 10 == 0:
            print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch+1, epochs, loss.item()))

fit(100,model,loss_fn,opt,train)

preds = model(inputs)

print(preds)

targets

