from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from torchvision import transforms
from PIL import Image
import torch
import joblib
import os

app = FastAPI()

# Static and template paths
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load model and encoders
model = torch.load("model/model.pt", map_location=torch.device("cpu"))
model.eval()

le_color = joblib.load("model/le_color.pkl")
le_type = joblib.load("model/le_type.pkl")
le_season = joblib.load("model/le_season.pkl")
le_gender = joblib.load("model/le_gender.pkl")

# Transform (same as used during training)
transform = torch.load("model/transforms.pt")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/predict", response_class=HTMLResponse)
# async def predict(request: Request, file: UploadFile = File(...)):
#     image = Image.open(await file.read()).convert("RGB")
#     img_tensor = transform(image).unsqueeze(0)  # Add batch dimension

#     with torch.no_grad():
#         outputs = model(img_tensor)
#         type_pred, color_pred, season_pred, gender_pred = [out.argmax(1).item() for out in outputs]

#     prediction = {
#         "articleType": le_type.inverse_transform([type_pred])[0],
#         "baseColour": le_color.inverse_transform([color_pred])[0],
#         "season": le_season.inverse_transform([season_pred])[0],
#         "gender": le_gender.inverse_transform([gender_pred])[0]
#     }

#     return templates.TemplateResponse("index.html", {
#         "request": request,
#         "prediction": prediction
#     })

@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(...)):
    try:
        image = Image.open(await file.read()).convert("RGB")
        img_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = model(img_tensor)
            type_pred, color_pred, season_pred, gender_pred = [out.argmax(1).item() for out in outputs]

        prediction = {
            "articleType": le_type.inverse_transform([type_pred])[0],
            "baseColour": le_color.inverse_transform([color_pred])[0],
            "season": le_season.inverse_transform([season_pred])[0],
            "gender": le_gender.inverse_transform([gender_pred])[0]
        }

        return JSONResponse(content={"prediction": prediction})

    except Exception as e:
        import traceback
        traceback.print_exc()  # Show full error in terminal
        return JSONResponse(status_code=500, content={"error": str(e)})

