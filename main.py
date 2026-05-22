from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# โหลด AI Model (RAM 16GB รับไหวสบายๆ)
reader = easyocr.Reader(['th', 'en'])

@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = reader.readtext(temp_file_path, detail=0)
    
    os.remove(temp_file_path)
    
    joined_text = " ".join(result)
    return {"status": "success", "text": joined_text}
