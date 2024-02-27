# mnist_svd_project/svd_mnist/eigen_VV.py

import torch
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets, transforms

def load_mnist():
    transform = transforms.Compose([transforms.ToTensor(),
                                    transforms.Normalize((0.5,), (0.5,))])
    train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    train_loader = torch.utils.data.DataLoader(train_data, batch_size=len(train_data), shuffle=True)
    data_iter = iter(train_loader)
    images, labels = next(data_iter)
    return images.view(images.shape[0], -1), labels  # Flatten images

def compute_PCA(data):
    # Centering the data
    mean = torch.mean(data, 0)
    data_centered = data - mean
    
    # Compute covariance matrix
    covariance_matrix = torch.matmul(data_centered.T, data_centered) / (data_centered.shape[0] - 1)
    
    # Compute eigenvalues and eigenvectors
    eigenvalues, eigenvectors = torch.linalg.eigh(covariance_matrix)
    
    # Sort eigenvalues and eigenvectors
    sorted_indices = torch.argsort(eigenvalues, descending=True)
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]
    
    return sorted_eigenvalues, sorted_eigenvectors

def plot_eigenfaces(eigenvectors, k=9):
    fig, axes = plt.subplots(1, k, figsize=(10, 2))
    for i, ax in enumerate(axes):
        ax.imshow(eigenvectors[:, i].reshape(28, 28).numpy(), cmap='gray')
        ax.axis('off')
    plt.show()
