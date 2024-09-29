import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
import torch
from torchvision import transforms
from .script import CustomCNN

# Initialize the model
model = CustomCNN()
model_path = 'model.pth'  # Path to your model
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()  # Set model to evaluation mode

# Define the image transformation (you may already have this in script.py)
transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
])

@csrf_exempt  # Use this if you're not sending a CSRF token from React
def upload_image(request):
    if request.method == 'POST':
        # Check if the image file is in the request
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image uploaded'}, status=400)

        # Get the uploaded image
        image_file = request.FILES['image']
        
        # Check if the file extension is '.tif'
        if not image_file.name.endswith('.tif'):
            return JsonResponse({'error': 'Only .tif files are accepted'}, status=400)

        # Ensure the temp directory exists
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        # Save the file temporarily
        temp_image_path = os.path.join(temp_dir, image_file.name)
        with default_storage.open(temp_image_path, 'wb') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # Open the image using PIL
        image = Image.open(temp_image_path).convert('RGB')

        # Transform the image
        image_tensor = transform(image).unsqueeze(0)  # Add batch dimension

        # Make prediction
        with torch.no_grad():
            output = model(image_tensor)
            probability = torch.sigmoid(output).item()  # Use sigmoid for binary classification
            prediction = "Cancerous" if probability > 0.5 else "Non-cancerous"

        # Delete the temporary image file after processing
        default_storage.delete(temp_image_path)

        # Return the prediction as a JSON response
        return JsonResponse({
            'is_cancerous': prediction == "Cancerous",
            'confidence': probability,
        }, status=200)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
