# 🧥 MultiLabel FashionNet

A web application that classifies fashion images into four attributes:  
<ul>
<li>👕 <b>Article Type</b></li>
<li>🎨 <b>Base Colour</b> </li>
<li>🌦️ <b>Season</b> </li>
<li>🧑‍🤝‍🧑 <b>Gender</b> </li> 
</ul>
— using a fine-tuned <b>Vision Transformer (ViT)</b> model served via <b>FastAPI</b>.

## 🚀 Tech Stack

### 🧠 Model & Training
- **PyTorch** for model development and training
- **timm** library for pretrained ViT (`vit_base_patch16_224`)
- **Fine-tuned** on a custom fashion dataset using multi-task learning
- Four separate classification heads for:
  - Article Type
  - Base Colour
  - Season
  - Gender

### 🧩 Frontend
- **HTML + CSS + JavaScript**
- Simple and responsive interface for image upload
- Image preview and structured prediction display

### 🖥️ Backend
- **FastAPI** for serving inference endpoints
- **PIL (Pillow)** for image preprocessing
- **Scikit-learn** LabelEncoders for decoding predictions
- RESTful `POST /predict` API for model inference

---

## ✨ Features

- ✅ Multi-label predictions in a single inference pass
- ✅ Fine-tuned transformer backbone (ViT)
- ✅ Mobile/web image upload support
- ✅ Lightweight and easy to deploy locally

---

## 📦 How to Use

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
