import os
import torch
from torchvision import transforms
from PIL import Image
import torch.nn as nn
from django.conf import settings

# Updated Custom CNN model architecture (with 5 convolutional layers)
class CustomCNN(nn.Module):
    def __init__(self):
        super(CustomCNN, self).__init__()
        # First convolutional block
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.leakyrelu1 = nn.LeakyReLU(0.1)
        self.maxpool1 = nn.MaxPool2d(2, 2)
        self.dropout1 = nn.Dropout2d(p=0.2)

        # Second convolutional block
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.leakyrelu2 = nn.LeakyReLU(0.1)
        self.maxpool2 = nn.MaxPool2d(2, 2)
        self.dropout2 = nn.Dropout2d(p=0.2)

        # Third convolutional block
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.leakyrelu3 = nn.LeakyReLU(0.1)
        self.maxpool3 = nn.MaxPool2d(2, 2)
        self.dropout3 = nn.Dropout2d(p=0.2)

        # Fourth convolutional block
        self.conv4 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(256)
        self.leakyrelu4 = nn.LeakyReLU(0.1)
        self.maxpool4 = nn.MaxPool2d(2, 2)
        self.dropout4 = nn.Dropout2d(p=0.2)

        # Fifth convolutional block
        self.conv5 = nn.Conv2d(256, 512, kernel_size=3, padding=1)
        self.bn5 = nn.BatchNorm2d(512)
        self.leakyrelu5 = nn.LeakyReLU(0.1)
        self.maxpool5 = nn.MaxPool2d(2, 2)
        self.dropout5 = nn.Dropout2d(p=0.2)

        # Fully connected layers
        self.fc1 = nn.Linear(512 * 1 * 1, 512)
        self.leakyrelu6 = nn.LeakyReLU(0.1)
        self.dropout6 = nn.Dropout(p=0.5)
        self.fc2 = nn.Linear(512, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.leakyrelu1(self.bn1(self.conv1(x)))
        x = self.maxpool1(x)
        x = self.dropout1(x)

        x = self.leakyrelu2(self.bn2(self.conv2(x)))
        x = self.maxpool2(x)
        x = self.dropout2(x)

        x = self.leakyrelu3(self.bn3(self.conv3(x)))
        x = self.maxpool3(x)
        x = self.dropout3(x)

        x = self.leakyrelu4(self.bn4(self.conv4(x)))
        x = self.maxpool4(x)
        x = self.dropout4(x)

        x = self.leakyrelu5(self.bn5(self.conv5(x)))
        x = self.maxpool5(x)
        x = self.dropout5(x)

        x = x.view(x.size(0), -1)
        x = self.leakyrelu6(self.fc1(x))
        x = self.dropout6(x)
        x = self.fc2(x)
        x = self.sigmoid(x)
        return x

# Instantiate the model and load weights
model = CustomCNN()
model_path = 'model.pth'  # Replace with your model path
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

# Define the image transformation
transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
])

# Function to predict if an image is cancerous or not
def predict_image(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        output = model(image)
        print(output,"$$$$$$$$$$$$$$$$$$$")
        probability = output.item()
    return "Cancerous" if probability > 0.5 else "Non-cancerous"

# Path to the image
# Create the media temp directory if it doesn't exist
temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')


image_file = os.listdir(temp_dir)[0]  # Get the first image from temp_media
image_path = os.path.join(temp_dir, image_file)

# Predict for the single image
prediction = predict_image(image_path)
print(f"Prediction for the image '{image_file}': {prediction}")
