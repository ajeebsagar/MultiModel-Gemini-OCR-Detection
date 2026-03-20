import os
from dotenv import load_dotenv
import time
import asyncio
import requests
import base64
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import google.generativeai as genai
from PIL import Image
import io
import fitz
from typing import Dict, List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load environment variables from backend/.env
load_dotenv()

app = FastAPI(title="OCR Document Analysis API")

# Allow local dev ports for the Next.js app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Model Configuration (Gemini 3 previews)
MODELS = {
    "flash": {
        "name": "gemini-3.0-flash-preview",
        "api_key": os.getenv("GEMINI_FLASH_KEY"),
        "display_name": "Gemini 3 Flash Preview"
    },
    "pro": {
        "name": "gemini-3.1-pro-preview",
        "api_key": os.getenv("GEMINI_PRO_KEY"),
        "display_name": "Gemini 3.1 Pro Preview"
    },
    "lite": {
        "name": "gemini-3.1-flash-lite-preview",
        "api_key": os.getenv("GEMINI_LITE_KEY"),
        "display_name": "Gemini 3.1 Flash Lite Preview"
    }
}


class OCRProcessor:
    @staticmethod
    def ensure_api_keys_present():
        missing = [key for key, cfg in MODELS.items() if not cfg["api_key"]]
        if missing:
            raise HTTPException(
                status_code=500,
                detail=f"Missing API key(s) for: {', '.join(missing)}. Check backend/.env."
            )

    @staticmethod
    def image_to_part(image: Image.Image) -> Dict:
        """Convert PIL image to Gemini content part."""
        buf = io.BytesIO()
        # use PNG to preserve quality; Gemini accepts common formats
        image.save(buf, format="PNG")
        return {
            "mime_type": "image/png",
            "data": buf.getvalue()
        }
    @staticmethod
    def normalize_text(text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]
        return '\n'.join(lines)

    @staticmethod
    def is_pdf_text_based(pdf_path: str) -> bool:
        """Check if PDF contains extractable text"""
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                if page.get_text().strip():
                    return True
            return False
        except Exception:
            return False

    @staticmethod
    def pdf_to_images(pdf_bytes: bytes, scale: float = 2.0) -> List[Image.Image]:
        """Convert PDF pages to images. Scale controls render quality."""
        images = []
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
            img_bytes = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_bytes))
            images.append(img)
        
        return images

    @staticmethod
    def image_to_base64(image: Image.Image) -> str:
        """Convert PIL image to base64 string"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    @staticmethod
    async def extract_text_with_gemini_rest(
        image: Image.Image,
        model_key: str,
        temperature: float
    ) -> Dict:
        """Extract text using Gemini REST API (more reliable)"""
        start_time = time.time()
        
        model_config = MODELS[model_key]
        api_key = model_config["api_key"]
        
        # Convert image to base64
        image_base64 = OCRProcessor.image_to_base64(image)
        
        # Models to try - prioritize Gemini 3 previews, then fall back to older IDs
        model_names = [
            model_config["name"],  # Try configured model first
            # Variants of Gemini 3 preview IDs (with and without models/ prefix)
            "models/gemini-3.0-flash-preview",
            "models/gemini-3.1-pro-preview",
            "models/gemini-3.1-flash-lite-preview",
            "gemini-3.0-flash-preview",
            "gemini-3.1-pro-preview",
            "gemini-3.1-flash-lite-preview",
            # Older fallbacks
            "gemini-2.0-flash-exp",
            "gemini-exp-1206",
            "gemini-2.0-flash-lite-exp",
            "gemini-pro",
            "gemini-1.5-flash",
        ]
        
        # Enhanced OCR prompt
        prompt = """Perform OCR (Optical Character Recognition) on this image.

CRITICAL INSTRUCTIONS:
1. Extract ALL visible text from the image word-by-word
2. Maintain the EXACT original layout, structure, and formatting
3. Preserve all line breaks, spacing, indentation, and alignment
4. Include every single word, number, symbol, and punctuation mark
5. If text is in columns, read left-to-right, top-to-bottom
6. If text is rotated or at an angle, still extract it
7. Preserve capitalization exactly as shown
8. Do NOT add explanations, interpretations, or commentary
9. Do NOT translate or modify the text
10. Return ONLY the raw extracted text

Begin OCR extraction:"""
        
        last_error = None
        
        for model_name in model_names:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": "image/png",
                                    "data": image_base64
                                }
                            }
                        ]
                    }],
                    "generationConfig": {
                        "temperature": temperature,
                        "topP": 0.95,
                        "topK": 40,
                        "maxOutputTokens": 8192,
                    }
                }
                
                response = await asyncio.to_thread(
                    requests.post,
                    url,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if 'candidates' in data and len(data['candidates']) > 0:
                        text = data['candidates'][0]['content']['parts'][0]['text']
                        response_time = time.time() - start_time
                        
                        return {
                            "text": text,
                            "response_time": round(response_time, 2),
                            "success": True,
                            "error": None,
                            "model_used": model_name
                        }
                else:
                    error_data = response.json() if response.text else {}
                    last_error = error_data.get('error', {}).get('message', f'HTTP {response.status_code}')
                    
            except Exception as e:
                last_error = str(e)
                continue
        
        # All attempts failed
        error_msg = last_error if last_error else "Unknown error"
        
        if "API key not valid" in error_msg or "invalid" in error_msg.lower() or "403" in error_msg:
            error_msg = f"Invalid API key for {model_config['display_name']}. Get new key at: https://aistudio.google.com/app/apikey"
        elif "404" in error_msg or "not found" in error_msg.lower():
            error_msg = f"Models not available. Enable API at: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com"
        elif "billing" in error_msg.lower():
            error_msg = f"Billing not enabled. Enable at: https://console.cloud.google.com/billing"
        elif "quota" in error_msg.lower() or "429" in error_msg:
            error_msg = f"API quota exceeded for {model_config['display_name']}"
        
        return {
            "text": "",
            "response_time": round(time.time() - start_time, 2),
            "success": False,
            "error": error_msg
        }

    @staticmethod
    async def extract_text_with_gemini(
        image: Image.Image,
        model_key: str,
        temperature: float,
        thinking_level: str,
    ) -> Dict:
        """Extract text using specific Gemini model - tries SDK first, then REST API"""
        # Try REST API directly (more reliable)
        return await OCRProcessor.extract_text_with_gemini_rest(image, model_key, temperature)


class ModelComparator:
    @staticmethod
    def calculate_scores(outputs: Dict[str, str]) -> Dict[str, float]:
        """Calculate comparison scores for each model"""
        scores = {}
        
        # Filter out failed outputs
        valid_outputs = {k: v for k, v in outputs.items() if v.strip()}
        
        if not valid_outputs:
            return {k: 0.0 for k in outputs.keys()}
        
        # Text length score (normalized)
        lengths = {k: len(v) for k, v in valid_outputs.items()}
        max_length = max(lengths.values()) if lengths else 1
        length_scores = {k: v / max_length for k, v in lengths.items()}
        
        # Semantic similarity score
        if len(valid_outputs) > 1:
            vectorizer = TfidfVectorizer()
            try:
                tfidf_matrix = vectorizer.fit_transform(valid_outputs.values())
                similarity_matrix = cosine_similarity(tfidf_matrix)
                avg_similarities = similarity_matrix.mean(axis=1)
                
                similarity_scores = {}
                for idx, key in enumerate(valid_outputs.keys()):
                    similarity_scores[key] = float(avg_similarities[idx])
            except:
                similarity_scores = {k: 0.5 for k in valid_outputs.keys()}
        else:
            similarity_scores = {k: 1.0 for k in valid_outputs.keys()}
        
        # Clarity score (based on word count and structure)
        clarity_scores = {}
        for key, text in valid_outputs.items():
            words = text.split()
            lines = text.split('\n')
            clarity = min(1.0, (len(words) / 100) * 0.5 + (len(lines) / 20) * 0.5)
            clarity_scores[key] = clarity
        
        # Combined score
        for key in outputs.keys():
            if key in valid_outputs:
                scores[key] = round(
                    length_scores.get(key, 0) * 0.3 +
                    similarity_scores.get(key, 0) * 0.4 +
                    clarity_scores.get(key, 0) * 0.3,
                    2
                )
            else:
                scores[key] = 0.0
        
        return scores

    @staticmethod
    def determine_best_model(scores: Dict[str, float]) -> str:
        """Determine the best performing model"""
        if not scores:
            return "None"
        best_key = max(scores, key=scores.get)
        # If everything is zero, signal no winner so frontend can show clearly
        if scores[best_key] == 0:
            return "None"
        return MODELS[best_key]["display_name"]


@app.get("/")
async def root():
    return {"message": "OCR Document Analysis API", "status": "running"}


@app.post("/api/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    temperature: float = Form(0.7),
    media_resolution: str = Form("default"),
    thinking_level: str = Form("minimal"),
):
    """Main endpoint for document analysis"""
    try:
        OCRProcessor.ensure_api_keys_present()

        # Read file
        file_bytes = await file.read()
        file_extension = file.filename.split('.')[-1].lower()
        # Resolve render scale for PDFs based on requested media resolution
        render_scale = 2.0
        if media_resolution.lower() == "high":
            render_scale = 3.0
        elif media_resolution.lower() == "low":
            render_scale = 1.5
        
        # Process based on file type
        if file_extension == 'pdf':
            images = OCRProcessor.pdf_to_images(pdf_bytes=file_bytes, scale=render_scale)
            # Use first page for analysis
            image = images[0] if images else None
            if not image:
                raise HTTPException(status_code=400, detail="Could not process PDF")
        elif file_extension in ['jpg', 'jpeg', 'png', 'jfif']:
            image = Image.open(io.BytesIO(file_bytes))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Extract text with all three models concurrently
        tasks = [
            OCRProcessor.extract_text_with_gemini(image, "flash", temperature, thinking_level),
            OCRProcessor.extract_text_with_gemini(image, "pro", temperature, thinking_level),
            OCRProcessor.extract_text_with_gemini(image, "lite", temperature, thinking_level)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Organize results
        model_outputs = {}
        raw_outputs = {}
        response_times = {}
        errors = {}
        
        for idx, model_key in enumerate(["flash", "pro", "lite"]):
            result = results[idx]
            raw_text = result["text"]
            normalized_text = OCRProcessor.normalize_text(raw_text)
            
            model_outputs[model_key] = normalized_text
            raw_outputs[model_key] = raw_text
            response_times[model_key] = result["response_time"]
            
            if not result["success"]:
                errors[model_key] = result["error"]
        
        # Calculate scores and determine best model
        scores = ModelComparator.calculate_scores(model_outputs)
        best_model = ModelComparator.determine_best_model(scores)
        
        return JSONResponse({
            "success": True,
            "model_outputs": {
                "flash": model_outputs["flash"],
                "pro": model_outputs["pro"],
                "lite": model_outputs["lite"]
            },
            "raw_outputs": {
                "flash": raw_outputs["flash"],
                "pro": raw_outputs["pro"],
                "lite": raw_outputs["lite"]
            },
            "scores": scores,
            "response_times": response_times,
            "best_model": best_model,
            "model_names": {
                "flash": MODELS["flash"]["display_name"],
                "pro": MODELS["pro"]["display_name"],
                "lite": MODELS["lite"]["display_name"]
            },
            "errors": errors if errors else None
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
