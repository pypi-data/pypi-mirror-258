
![Logo](https://scontent.flyn1-1.fna.fbcdn.net/v/t39.30808-6/424961189_3486299574847394_336702687462440976_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=3635dc&_nc_ohc=V1iiqvdoY-kAX9eXJNW&_nc_ht=scontent.flyn1-1.fna&oh=00_AfCxRBprigIdFmTkH0ZsHmz45bCzlpwhE4JF-Tv_GAAIZw&oe=65DD5417)


# Linear Algebra
## Introduction

This project explores the application of Singular Value Decomposition (SVD), Principal Component Analysis (PCA), and Pixel Intensity Sum (PIS) on the MNIST dataset. SVD and PCA are utilized for dimensionality reduction, providing insights into data compression and feature extraction. The project demonstrates how these techniques can significantly reduce the complexity of data while retaining essential features necessary for tasks like image reconstruction and classification. Additionally, PIS predictions via linear regression showcase the relationship between reduced dimensions and image characteristics. This comprehensive analysis not only highlights the effectiveness of SVD and PCA in handling high-dimensional data but also underscores the potential of simple linear models in making meaningful predictions from complex datasets.

Below is the directory structure:


![App Screenshot](https://scontent.flyn1-1.fna.fbcdn.net/v/t39.30808-6/424932863_3486299951514023_1451982105073225357_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=3635dc&_nc_ohc=VvN-FfIzijcAX_ICvnS&_nc_oc=AQlf_m5bTRuWB-t2c-ci4572U0NXZTXmYcgg5g712hy00ZNWixUa268zKv3XvI23hNIcrEPAgAlh1NABdJmUiKwK&_nc_ht=scontent.flyn1-1.fna&oh=00_AfASzE6Lc4QRKJh7TkWMcK9QGQJx3sXsHGPQ-6oGMueZvA&oe=65DDD40A)


### Singular Value Decomposition (SVD)

The code from svd.py performs the following operations:

1.  Loads the MNIST Dataset: Utilizes PyTorch's datasets and transforms to load the MNIST dataset, normalizing the images.

2.  Applies Singular Value Decomposition (SVD): Converts images to NumPy arrays, centers them by subtracting the mean, and then applies SVD to decompose the images, retaining only the top k components for dimensionality reduction.

3.  Reconstructs Images: Uses the top k components from SVD to reconstruct images.

4.  Visual Comparison: Plots and compares the first original image from the MNIST dataset against its reconstructed version after applying SVD, facilitating a visual assessment of the reconstruction quality.

### Principal value Decomposition (PCA)

The code from eigen_VV.py performs the following operations:
1.  Loads the MNIST dataset, normalizing and flattening the images for processing.

2.  Computes PCA to center the data, calculate the covariance matrix, and determine the eigenvalues and eigenvectors, which are then sorted by the magnitude of eigenvalues.

3.  Plots the first few eigenfaces by reshaping and displaying the leading eigenvectors as images, illustrating the principal components that capture the most variance in the dataset.

### pixel intensity Sum (PIS)
The code from linear_regression.py performs the following operations:
1.  Loads and preprocesses the MNIST dataset, normalizing images and flattening them into vectors.

2.  Calculates pixel intensity sums for each image as a target variable for regression.

3.  Applies PCA to reduce the dimensionality of the dataset, retaining 50% of the variance.

4.  Splits the dataset into training and testing sets for model validation.

5.  Trains a linear regression model to predict pixel intensity sums based on PCA-reduced features.

6.   Visualizes predictions using a bar chart to compare actual vs. predicted pixel intensity sums for a subset of images.

## The Main Function
The main.py script orchestrates the application of Singular Value Decomposition (SVD), Principal Component Analysis (PCA), and Pixel Intensity Sum prediction (PIS) on the MNIST dataset.

1.  SVD Operation (run_svd): Loads MNIST images, applies SVD to decompose and then reconstruct the images, and visualizes the original vs. reconstructed images.

2.  PCA Operation (run_pca): Loads MNIST images, computes PCA to extract eigenvalues and eigenvectors (principal components), prints the first 10 eigenvalues, and visualizes the "eigenfaces."

3.  Pixel Intensity Sum Prediction (run_pis): Preprocesses MNIST images by flattening, applies PCA for dimensionality reduction, uses linear regression to predict the total pixel intensity sums, and plots the actual vs. predicted sums.

4.   Argument Parsing: Enables the user to specify which operation to perform (svd, pca, or pis) via command-line arguments.

This structure allows for modular exploration of different machine learning techniques on image data, demonstrating dimensionality reduction, reconstruction, and regression analysis within a unified framework.

## Run Locally

Clone the project

```bash
  git clone https://github.com/SammyIJ/WASORIA.git
```

Go to the project directory

```bash
  cd WASORIA/MNIST_Linear_Algebra
```

Run the main and make sure to parse other arguments
```bash
  python main.py --run svd
  python main.py --run pca
  python main.py --run pis
  ```


