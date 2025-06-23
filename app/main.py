from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from torchvision import transforms
from PIL import Image
import torch
import joblib
import io
import os
from app.model import FashionNet  


app = FastAPI()

# Static and template paths
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


le_color = joblib.load("models/le_color.pkl")
le_type = joblib.load("models/le_type.pkl")
le_season = joblib.load("models/le_season.pkl")
le_gender = joblib.load("models/le_gender.pkl")

# Load model and encoders
model = FashionNet(
    num_colors=len(le_color.classes_),
    num_article_types=len(le_type.classes_),
    num_seasons=len(le_season.classes_),
    num_genders=len(le_gender.classes_)
)

model.load_state_dict(torch.load("models/fashion_model.pth", map_location=torch.device('cpu')))
model.eval()  # Set model to evaluation mode

# Transform (same as used during training)
transform = torch.load("models/transform.pt")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:5500"] for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return FileResponse("static/templates/index.html")


@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):
    try:
        # Read image
        image = Image.open(io.BytesIO(await file.read())).convert("RGB")
        img_tensor = transform(image).unsqueeze(0)  # [1, 3, 224, 224]

        with torch.no_grad():
            outputs = model(img_tensor)

        # Get predictions
        color_pred = outputs["color"].argmax(1).item()
        type_pred = outputs["article_type"].argmax(1).item()
        season_pred = outputs["season"].argmax(1).item()
        gender_pred = outputs["gender"].argmax(1).item()

        # Convert to label names using LabelEncoders
        prediction = {
            "articleType": le_type.inverse_transform([type_pred])[0],
            "baseColour": le_color.inverse_transform([color_pred])[0],
            "season": le_season.inverse_transform([season_pred])[0],
            "gender": le_gender.inverse_transform([gender_pred])[0]
        }

        return JSONResponse(content={"prediction": prediction})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
