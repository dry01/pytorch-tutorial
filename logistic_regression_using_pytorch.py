# -*- coding: utf-8 -*-
"""logistic regression using pytorch

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fGwTIytNLYTInu6-BHUSwoYcuCDiMFiF
"""

import torch

import torchvision

from torchvision.datasets import MNIST

datasets = MNIST(root='data/',download= True)

len(datasets)

test_datasets = MNIST(root='data/',train=False)
len(test_datasets)

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
# %matplotlib inline

image,label = datasets[1]
plt.imshow(image,cmap='gray')
print('labels:', label)

print(type(image))

import torchvision.transforms as transforms

datasets = MNIST(root='data/',train = True,transform=transforms.ToTensor())

datasets[0]

image_tensor, label = datasets[0]
print(image_tensor.shape, label)

"""The image is now converted to a 1x28x28 tensor. The first dimension tracks color channels. The second and third dimensions represent pixels along the height and width of the image, respectively. Since images in the MNIST dataset are grayscale, there's just one channel. Other datasets have images with color, in which case there are three channels: red, green, and blue (RGB).

"""

print(torch.max(image_tensor),torch.min(image_tensor))
print(image_tensor[0,5:10,5:10])
plt.imshow(image_tensor[0,5:10,5:10],cmap='gray')

from torch.utils.data import random_split

train_ds, val_ds = random_split(datasets,[50000,10000])
#print(train_ds,test_ds)

len(train_ds),len(val_ds)

from torch.utils.data import DataLoader
batch_size =128
train_loader = DataLoader(train_ds,batch_size, shuffle=True)
val_loader = DataLoader(val_ds,batch_size)

import torch.nn as nn
input_size = 784
num_classes = 10
model = nn.Linear(input_size, num_classes)

print(model.weight.shape)

print(model.bias.shape)
model.bias

for images, labels in train_loader:
    print(labels)
    print(images.shape)
    outputs = model(images)
    print(outputs)
    break

print(images)
images.shape

images.shape

images.reshape(128,784).shape

images.shape

class MNISTmodel(nn.Module):
  def __init__(self):
    super().__init__()
    self.Linear = nn.Linear(input_size,num_classes)
  def forward(self,xb):
    xb = xb.reshape(-1,784)
    out = self.Linear(xb)
    return out

model = MNISTmodel()

print(model)

model.Linear

print(model.Linear.weight.shape, model.Linear.bias.shape)
list(model.parameters())

for images, labels in train_loader:
    print(images.shape)
    outputs = model(images)
    break

print('outputs.shape : ', outputs.shape)
print('Sample outputs :\n', outputs[:2].data)

import torch.nn.functional as F

probs = F.softmax(outputs,dim=1)
print(probs[:5].data)
print(torch.sum(probs[0]).item())

"""now we predict value as label which has the highest probability in overall


"""

max_probs , preds = torch.max(probs,dim=1)
print(preds)
print(max_probs)

labels

torch.sum(preds == labels)

def accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))

accuracy(outputs, labels)

loss_fn = F.cross_entropy

loss = loss_fn(outputs, labels)
print(loss)

def fit(epochs, lr, model, train_loader, val_loader, opt_func=torch.optim.SGD):
    optimizer = opt_func(model.parameters(), lr)
    history = [] # for recording epoch-wise results
    
    for epoch in range(epochs):
        
        # Training Phase 
        for batch in train_loader:
            loss = model.training_step(batch)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        
        # Validation phase
        result = evaluate(model, val_loader)
        model.epoch_end(epoch, result)
        history.append(result)

    return history

def evaluate(model, val_loader):
    outputs = [model.validation_step(batch) for batch in val_loader]
    return model.validation_epoch_end(outputs)

class MnistModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(input_size, num_classes)
        
    def forward(self, xb):
        xb = xb.reshape(-1, 784)
        out = self.linear(xb)
        return out
    
    def training_step(self, batch):
        images, labels = batch 
        out = self(images)                  # Generate predictions
        loss = F.cross_entropy(out, labels) # Calculate loss
        return loss
    
    def validation_step(self, batch):
        images, labels = batch 
        out = self(images)                    # Generate predictions
        loss = F.cross_entropy(out, labels)   # Calculate loss
        acc = accuracy(out, labels)           # Calculate accuracy
        return {'val_loss': loss, 'val_acc': acc}
        
    def validation_epoch_end(self, outputs):
        batch_losses = [x['val_loss'] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()   # Combine losses
        batch_accs = [x['val_acc'] for x in outputs]
        epoch_acc = torch.stack(batch_accs).mean()      # Combine accuracies
        return {'val_loss': epoch_loss.item(), 'val_acc': epoch_acc.item()}
    
    def epoch_end(self, epoch, result):
        print("Epoch [{}], val_loss: {:.4f}, val_acc: {:.4f}".format(epoch, result['val_loss'], result['val_acc']))
    
model = MnistModel()

result0 = evaluate(model, val_loader)
result0

history1 = fit(5, 0.001, model, train_loader, val_loader)

history2 = fit(5, 0.001, model, train_loader, val_loader)

history3 = fit(5, 0.001, model, train_loader, val_loader)

history4 = fit(5, 0.001, model, train_loader, val_loader)

history = [result0] + history1 + history2 + history3 + history4
accuracies = [result['val_acc'] for result in history]
plt.plot(accuracies, '-x')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.title('Accuracy vs. No. of epochs');

test_dataset = MNIST(root='data/', 
                     train=False,
                     transform=transforms.ToTensor())

img, label = test_dataset[0]
plt.imshow(img[0], cmap='gray')
print('Shape:', img.shape)
print('Label:', label)

def predict_image(img, model):
    xb = img.unsqueeze(0)
    yb = model(xb)
    _, preds = torch.max(yb, dim=1)
    return preds[0].item()

model

img, label = test_dataset[123]
plt.imshow(img[0], cmap='gray')
print('Label:', label, ', Predicted:', predict_image(img, model))

test_loader = DataLoader(test_dataset, batch_size=256)
result = evaluate(model, test_loader)
result

"""save the model

"""

torch.save(model.state_dict(), 'mnist-logistic.pth')

model.state_dict()

model2 = MnistModel()

model2.state_dict()

evaluate(model2, test_loader)

model2.load_state_dict(torch.load('mnist-logistic.pth'))
model2.state_dict()

test_loader = DataLoader(test_dataset, batch_size=256)
result = evaluate(model2, test_loader)
result

