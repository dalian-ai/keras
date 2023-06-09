# flake8: noqa
import os

# Set backend env to torch
os.environ["KERAS_BACKEND"] = "torch"

import torch
import torch.nn as nn
import torch.optim as optim
from keras_core import layers
import keras_core
import numpy as np


# Model / data parameters
num_classes = 10
input_shape = (28, 28, 1)
learning_rate = 0.01
batch_size = 128
num_epochs = 1

# Load the data and split it between train and test sets
(x_train, y_train), (x_test, y_test) = keras_core.datasets.mnist.load_data()

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255
# Make sure images have shape (28, 28, 1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
print("x_train shape:", x_train.shape)
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")

# Create the Keras model
model = keras_core.Sequential(
    [
        layers.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(num_classes),
    ]
)

#################################################################
######## Writing a torch training loop for a Keras model ########
#################################################################

def get_keras_model():
    pass

model = get_keras_model()

# Instantiate the torch optimizer
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Instantiate the torch loss function
loss_fn = nn.CrossEntropyLoss()

def train_step(data):
    x, y = data
    y_pred = model(x)
    loss = loss_fn(y_pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss

# Create a TensorDataset
dataset = torch.utils.data.TensorDataset(
    torch.from_numpy(x_train), torch.from_numpy(y_train)
)

for data in dataset:
    loss = train_step(data)
    print("Loss:", float(loss))


def train(model, train_loader, num_epochs, optimizer, loss_fn):
    for epoch in range(num_epochs):
        running_loss = 0.0
        for batch_idx, (inputs, targets) in enumerate(train_loader):
            # Forward pass
            outputs = model(inputs)
            loss = loss_fn(outputs, targets)

            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            # Print loss statistics
            if (batch_idx + 1) % 10 == 0:
                print(
                    f"Epoch [{epoch+1}/{num_epochs}], "
                    f"Batch [{batch_idx+1}/{len(train_loader)}], "
                    f"Loss: {running_loss / 10}"
                )
                running_loss = 0.0


# Create a TensorDataset
dataset = torch.utils.data.TensorDataset(
    torch.from_numpy(x_train), torch.from_numpy(y_train)
)

# Create a DataLoader
train_loader = torch.utils.data.DataLoader(
    dataset, batch_size=batch_size, shuffle=False
)

train(model, train_loader, num_epochs, optimizer, loss_fn)


################################################################
######## Using a Keras model or layer in a torch Module ########
################################################################

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = keras_core.Sequential(
            [
                layers.Input(shape=(28, 28, 1)),
                layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Flatten(),
                layers.Dropout(0.5),
                layers.Dense(num_classes),
            ]
        )

    def forward(self, x):
        return self.model(x)


torch_module = MyModel()

# Instantiate the torch optimizer
print("Num params:", len(list(torch_module.parameters())))
optimizer = optim.Adam(torch_module.parameters(), lr=learning_rate)

# Instantiate the torch loss function
loss_fn = nn.CrossEntropyLoss()

train(torch_module, train_loader, num_epochs, optimizer, loss_fn)
