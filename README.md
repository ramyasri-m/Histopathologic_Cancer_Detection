# Image Classifier Application

This is a full-stack image classifier application that detects cancerous cells in uploaded images. It consists of a Django-based backend and a React-based frontend.

## Table of Contents

-   [Backend](#backend)
-   [Frontend](#frontend)
-   [Setup](#setup)
-   [Usage](#usage)

## Backend

The backend is built using Django and PyTorch. It handles image uploads, processes the images using a Convolutional Neural Network (CNN) model, and returns predictions.

### Backend Features

-   Accepts `.tif` images for cancer detection.
-   Processes images using a PyTorch CNN model.
-   Returns a JSON response with the classification result and confidence score.

### Requirements

-   Python 3.x
-   Django
-   PyTorch
-   Pillow (for image processing)
-   Torchvision (for transformations)

### Backend Installation

1. **Clone the repository**:

    ```bash
    git clone <repository-url>
    cd <backend-folder>
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the Django project**:

    Update your `settings.py` file with the correct database, media root, and static settings.

4. **Prepare the database**:

    ```bash
    python manage.py migrate
    ```

5. **Run the server**:

    ```bash
    python manage.py runserver
    ```

### Backend API Endpoints

-   **POST** `/upload/` - Uploads an image and returns a classification result (Cancerous/Non-cancerous).

#### Example request

```bash
curl -X POST -F 'image=@path_to_image.tif' http://127.0.0.1:8000/upload/
```

#### Example response

```json
{
    "is_cancerous": true,
    "confidence": 0.85
}
```

## Frontend

The frontend is built with React and Material-UI, providing an interface for users to upload images and view predictions.

### Frontend Features

-   Allows users to upload images for classification.
-   Displays the prediction result and confidence score.
-   Responsive design with navigation between different pages (Home, Upload, About).

### Frontend Installation

1. **Navigate to the frontend folder**:

    ```bash
    cd <frontend-folder>
    ```

2. **Install dependencies**:

    ```bash
    npm install
    ```

3. **Start the development server**:

    ```bash
    npm start
    ```

    The frontend will be served at `http://localhost:3000`.

### Available Pages

-   **Home**: A welcome page.
-   **Upload**: A page for uploading images and viewing prediction results.
-   **About**: Information about the application.

## Setup

### Backend Setup

1. Make sure your Python environment is set up correctly.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Start the Django development server using `python manage.py runserver`.

### Frontend Setup

1. Install Node.js dependencies by running `npm install`.
2. Start the frontend by running `npm start`.

## Usage

1. Start the Django backend server.
2. Start the React frontend.
3. Open `http://localhost:3000` in your browser.
4. Navigate to the "Upload" page, choose a `.tif` image, and submit it.
5. View the prediction result and confidence score on the same page.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
