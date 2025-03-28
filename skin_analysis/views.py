import os
import torch
import torchvision.transforms as transforms
import numpy as np
from PIL import Image
from io import BytesIO
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import SkinAnalysis
from .utils import get_skin_disease_labels  # Ensure this file contains get_skin_disease_labels()

# Device setup
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
THRESHOLD = 0.1

# Define model path
MODEL_PATH = os.path.join(settings.MEDIA_ROOT, "model.bin")
MODEL_URL = "https://your-cloud-storage-link.com/model.bin"  # Replace with actual URL

# Ensure model file exists
if not os.path.exists(MODEL_PATH):
    print("Downloading model file...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(response.content)

# Load model
try:
    model = torch.load(MODEL_PATH, map_location=torch.device("cpu")).to(DEVICE)
    model.eval()
    skin_disease_labels = get_skin_disease_labels()
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    skin_disease_labels = []

# Image preprocessing function
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224), interpolation=transforms.InterpolationMode.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0).to(DEVICE)  # Add batch dimension

class SkinAnalysisView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # 1️⃣ Get uploaded image
        image_file = request.FILES.get("image")
        if not image_file:
            return Response({"error": "No image uploaded"}, status=400)

        # 2️⃣ Save image to database
        image_instance = SkinAnalysis.objects.create(user=request.user, image=image_file)

        # 3️⃣ Ensure model is loaded
        if model is None:
            return Response({"error": "Model file not found"}, status=500)

        # 4️⃣ Construct the absolute image URL
        image_url = request.build_absolute_uri(image_instance.image.url)

        try:
            response = requests.get(image_url)
            if response.status_code != 200:
                return Response({"error": "Failed to download image"}, status=500)

            image = Image.open(BytesIO(response.content)).convert("RGB")
        except Exception as e:
            return Response({"error": f"Failed to process image: {str(e)}"}, status=500)

        # 5️⃣ Preprocess image
        image_tensor = preprocess_image(image)

        # 6️⃣ Make prediction
        with torch.no_grad():
            model_output = torch.sigmoid(model(image_tensor)).cpu().numpy()
            binary_output = (model_output > THRESHOLD).astype(int).squeeze()

        # 7️⃣ Map results to conditions
        top_index = np.argmax(model_output[0])  # Get index of highest probability
        top_condition = skin_disease_labels[top_index]  # Map index to label
        top_confidence = float(model_output[0][top_index])  # Get probability as a float

        # Save and return the top condition with confidence
        image_instance.result = f"{top_condition} ({top_confidence:.2%})"  # Store as "Condition (Confidence%)"
        image_instance.save()

        return Response({"condition": top_condition, "confidence": round(top_confidence * 100, 2)})
