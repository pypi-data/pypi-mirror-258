# svd_mnist/svd.py

import torch
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets, transforms

def load_mnist():
    transform = transforms.Compose([transforms.ToTensor(),
                                    transforms.Normalize((0.5,), (0.5,))])
    train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    train_loader = torch.utils.data.DataLoader(train_data, batch_size=len(train_data), shuffle=True)
    return next(iter(train_loader))

def apply_svd(images, k=9):
    # Ensure images is a NumPy array first
    images_np = images.numpy().reshape(images.shape[0], -1)
    images_mean = np.mean(images_np, axis=1, keepdims=True)
    images_np = images_np - images_mean
    
    U, S, Vt = np.linalg.svd(images_np, full_matrices=False)
    return U[:, :k], np.diag(S[:k]), Vt[:k, :]

def reconstruct_images(U_k, S_k, Vt_k):
    return np.dot(U_k, np.dot(S_k, Vt_k))

def plot_images(original_images, reconstructed_images):
    plt.figure(figsize=(10, 4))
    
    # Plot the first original image
    plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
    # Ensure the image is a numpy array and reshape it
    if not isinstance(original_images, np.ndarray):
        original_images = original_images.numpy()  # Convert PyTorch tensor to NumPy array if necessary
    plt.imshow(original_images[0].reshape(28, 28), cmap='gray')
    plt.title('Original Image')
    plt.axis('off')
 
    # Plot the first reconstructed image
    plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
    # Ensure the image is a numpy array and reshape it
    if not isinstance(reconstructed_images, np.ndarray):
        reconstructed_images = reconstructed_images.numpy()  # Convert PyTorch tensor to NumPy array if necessary
    plt.imshow(reconstructed_images[0].reshape(28, 28), cmap='gray')  # Assuming reconstructed_images can be reshaped back
    plt.title('Reconstructed Image')
    plt.axis('off')

    
    plt.show()
