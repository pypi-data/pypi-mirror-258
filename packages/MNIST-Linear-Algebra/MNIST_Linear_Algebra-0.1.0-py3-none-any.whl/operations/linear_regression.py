# mnist_svd_project/svd_mnist/eigen_VV.py

import torch
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def load_and_preprocess_mnist():
    transform = transforms.Compose([transforms.ToTensor(),
                                    transforms.Normalize((0.5,), (0.5,))])
    train_data = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    train_loader = torch.utils.data.DataLoader(train_data, batch_size=len(train_data), shuffle=True)
    data_iter = iter(train_loader)
    images, labels = next(data_iter)
    images_flat = images.view(images.shape[0], -1).numpy()  # Flatten images
    return images_flat, labels

def compute_pca_and_predict_intensity(images_flat):
    # Calculate pixel intensity sums as the target variable
    pixel_intensity_sums = np.sum(images_flat, axis=1)

    # Apply PCA to reduce dimensionality
    pca = PCA(n_components=0.50)  # Retain 95% of variance
    pca_features = pca.fit_transform(images_flat)

    # Split the dataset for training and testing
    X_train, X_test, y_train, y_test = train_test_split(pca_features, pixel_intensity_sums, test_size=0.2, random_state=42)

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict pixel intensity sums on the test set
    predicted_sums = model.predict(X_test)

    # Return the model, actual and predicted sums for evaluation
    return model, y_test, predicted_sums

def plot_predictions(y_test, predicted_sums, sample_size=10):
    # Select a subset for clearer visualization
    indices = np.arange(sample_size)  # Adjust sample_size if needed
    actual_sums_sample = y_test[:sample_size]
    predicted_sums_sample = predicted_sums[:sample_size]
    
    # Setting up the bar chart
    plt.figure(figsize=(12, 6))
    bar_width = 0.35  # Width of the bars
    plt.bar(indices, actual_sums_sample, bar_width, color='blue', label='Actual Sums', alpha=0.6)
    plt.bar(indices + bar_width, predicted_sums_sample, bar_width, color='red', label='Predicted Sums', alpha=0.6)
    
    plt.xlabel('Image Index')
    plt.ylabel('Pixel Intensity Sum')
    plt.title('Actual vs. Predicted Pixel Intensity Sums - Bar Chart')
    plt.xticks(indices + bar_width / 2, indices)  # Positioning the x-axis ticks
    plt.legend()
    plt.tight_layout()
    plt.show()
