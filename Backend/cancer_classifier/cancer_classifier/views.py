import os
import logging
from PIL import Image
import numpy as np
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # <-- Add this import
from tensorflow.keras.models import load_model as keras_load_model
from django.conf import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the .h5 model using Keras
def load_model():
    model_path = os.path.join(settings.BASE_DIR, 'HCD.h5')  # Update to your actual path
    logger.info(f"Loading Keras model from: {model_path}")
    
    if not os.path.exists(model_path):
        logger.error(f"Model file not found at {model_path}")
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    try:
        # Load the .h5 model
        model = keras_load_model(model_path)
        logger.info("Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

# Preprocess image for model prediction
def preprocess_image(image):
    logger.info("Preprocessing image")
    try:
        img = image.resize((96, 96))  # Adjust size to match model input (96x96)
        img = np.array(img)  # Convert PIL image to NumPy array
        img = img / 255.0  # Normalize pixel values to range [0, 1]
        img = np.expand_dims(img, axis=0)  # Add batch dimension: (1, 96, 96, 3)
        logger.info("Image preprocessed successfully")
        return img
    except Exception as e:
        logger.error(f"Error during image preprocessing: {e}")
        raise

# Predict cancer using the model
def predict_cancer(image, model):
    logger.info("Making cancer prediction")
    try:
        # Preprocess the image
        preprocessed_image = preprocess_image(image)
        
        # Make prediction using the Keras model
        prediction = model.predict(preprocessed_image)
        logger.info(f"Prediction made successfully: {prediction}")
        
        return prediction[0][0]  # Assuming a single probability output
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise

# Load the model once at the start (to avoid reloading on every request)
logger.info("Loading model at startup")
model = load_model()

@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        logger.info(f"Received image: {image.name}")
        
        try:
            # Open the image directly
            img = Image.open(image)

            # Make sure the image is in RGB mode
            img = img.convert('RGB')

            # Pass the image to the model for prediction
            cancer_prediction = predict_cancer(img, model)
            logger.info(f"Cancer prediction: {cancer_prediction}")

            # Return the prediction result in the response
            return JsonResponse({
                'message': 'Image processed successfully',
                'cancer_prediction': float(cancer_prediction),  # Convert NumPy float to standard float
            })
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return JsonResponse({'error': 'Prediction failed.'}, status=500)

    logger.error('No image uploaded.')
    return JsonResponse({'error': 'No image uploaded.'}, status=400)
