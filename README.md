conda create -p "D:\All_project\gradelab\gimini OCR\giminiOcr" python=3.10 -y
conda activate "D:\All_project\gradelab\gimini OCR\giminiOcr"


python -m pip install -r backend/requirements.txt

# treminal 1
conda activate "D:\All_project\gradelab\gimini OCR\giminiOcr"
python backend/main.py

## terminal 2
conda activate "D:\All_project\gradelab\gimini OCR\giminiOcr"
cd "D:\All_project\gradelab\gimini OCR\frontend"
$env:Path="C:\Program Files\nodejs;" + $env:Path
npm run dev

# 🚀 OCR Document Analysis - Multi-Model AI Comparison

A production-ready full-stack application that extracts text from images and PDFs using three different Google Gemini AI models, compares their performance, and automatically determines the best model for your document.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Security](#security)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Core Functionality
- **Multi-Format Support**: Upload JPG, PNG, or PDF files
- **PDF Intelligence**: Automatically detects text-based vs scanned PDFs
- **Triple AI Analysis**: Simultaneous text extraction using:
  - Gemini 2.0 Flash (Fast & Efficient)
  - Gemini 1.5 Pro (High Accuracy)
  - Gemini 1.5 Flash 8B (Lightweight)
- **Smart Comparison**: Automatic model performance evaluation
- **Real-time Processing**: Concurrent API calls for faster results

### User Experience
- **Drag & Drop Upload**: Intuitive file upload interface
- **Side-by-Side Comparison**: View all three model outputs simultaneously
- **Performance Metrics**: 
  - Accuracy scores with visual progress bars
  - Response time tracking
  - Best model highlighting with badges
- **Output Options**:
  - Toggle between raw and cleaned text
  - Download individual model outputs (TXT)
  - Export complete analysis (JSON)
- **Beautiful UI**: Modern gradient design with Tailwind CSS

### Technical Features
- **Text Normalization**: Automatic noise removal and formatting
- **Evaluation Metrics**:
  - Text completeness (length analysis)
  - Semantic similarity (TF-IDF + cosine similarity)
  - Response clarity scoring
- **Error Handling**: Graceful degradation with detailed error messages
- **CORS Security**: Configured for secure cross-origin requests

---

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **AI Models**: Google Generative AI (Gemini)
- **PDF Processing**: PyMuPDF (fitz)
- **Image Processing**: Pillow
- **ML Analysis**: scikit-learn, numpy
- **Server**: Uvicorn with async support

### Frontend
- **Framework**: Next.js 14.1.0 (React 18)
- **Styling**: Tailwind CSS 3.3
- **HTTP Client**: Axios
- **File Upload**: react-dropzone
- **Icons**: lucide-react
- **Language**: TypeScript

---

## 🏗 Architecture

### Design Principles
1. **Separation of Concerns**: Clear separation between frontend, backend, and AI services
2. **Modularity**: Reusable components and services
3. **Async Processing**: Non-blocking concurrent API calls
4. **Security First**: API keys stored server-side only
5. **Scalability**: Stateless design for horizontal scaling

### System Flow
```
User Upload → Frontend (Next.js)
    ↓
File Validation → Backend (FastAPI)
    ↓
PDF Detection → Image Conversion (if needed)
    ↓
Parallel Processing → 3 Gemini Models
    ↓
Text Extraction → Normalization
    ↓
Comparison Engine → Scoring Algorithm
    ↓
Results → Frontend Display
```

---

## 📦 Prerequisites

### Required Software
- **Python**: 3.9 or higher
- **Node.js**: 18.0 or higher
- **npm** or **yarn**: Latest version
- **pip**: Python package manager

### API Keys
You need three Google Gemini API keys (provided):
- Gemini Flash Key
- Gemini Pro Key  
- Gemini Lite Key

---

## 🔧 Installation

### Step 1: Clone or Extract Project
```bash
# If using git
git clone <repository-url>
cd ocr-document-analysis

# Or extract the provided files to a directory
```

### Step 2: Backend Setup

#### 2.1 Navigate to Backend Directory
```bash
cd backend
```

#### 2.2 Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies Installed**:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-multipart` - File upload support
- `google-generativeai` - Gemini AI SDK
- `Pillow` - Image processing
- `PyMuPDF` - PDF handling
- `scikit-learn` - ML metrics
- `numpy` - Numerical operations
- `python-dotenv` - Environment variables

#### 2.4 Configure Environment Variables
The `.env` file is already created with your API keys:
```env
GEMINI_FLASH_KEY=AIzaSyDOULXCMFMKLXAII8v_FeIEXAfyuicWvrk
GEMINI_PRO_KEY=AIzaSyAUCXvB5uh6ShgS1n4nVBmMl2LxQ6DPp0s
GEMINI_LITE_KEY=AIzaSyCWnqmImcaUHbuAMWLVAOCSoIF8LCqlJMw
```

**⚠️ SECURITY NOTE**: Never commit `.env` to version control!

### Step 3: Frontend Setup

#### 3.1 Navigate to Frontend Directory
```bash
cd ../frontend
```

#### 3.2 Install Node Dependencies
```bash
npm install
# or
yarn install
```

**Dependencies Installed**:
- `next` - React framework
- `react` & `react-dom` - UI library
- `axios` - HTTP client
- `react-dropzone` - File upload
- `lucide-react` - Icon library
- `tailwindcss` - CSS framework
- `typescript` - Type safety

---

## 🚀 Running the Application

### Method 1: Run Both Services Separately

#### Terminal 1 - Backend Server
```bash
cd backend
# Activate virtual environment if not already active
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

python main.py
```

**Backend will start on**: `http://localhost:8000`

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Terminal 2 - Frontend Server
```bash
cd frontend
npm run dev
# or
yarn dev
```

**Frontend will start on**: `http://localhost:3000`

You should see:
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- event compiled client and server successfully
```

### Method 2: Production Build

#### Backend (Production)
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend (Production)
```bash
cd frontend
npm run build
npm start
```

---

## 🌐 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response**:
```json
{
  "message": "OCR Document Analysis API",
  "status": "running"
}
```

#### 2. Analyze Document
```http
POST /api/analyze
Content-Type: multipart/form-data
```

**Request**:
- `file`: File upload (JPG, PNG, or PDF)

**Response**:
```json
{
  "success": true,
  "model_outputs": {
    "flash": "Extracted text from Flash model...",
    "pro": "Extracted text from Pro model...",
    "lite": "Extracted text from Lite model..."
  },
  "raw_outputs": {
    "flash": "Raw unprocessed text...",
    "pro": "Raw unprocessed text...",
    "lite": "Raw unprocessed text..."
  },
  "scores": {
    "flash": 0.85,
    "pro": 0.92,
    "lite": 0.78
  },
  "response_times": {
    "flash": 1.23,
    "pro": 2.45,
    "lite": 0.98
  },
  "best_model": "Gemini 1.5 Pro",
  "model_names": {
    "flash": "Gemini 2.0 Flash",
    "pro": "Gemini 1.5 Pro",
    "lite": "Gemini 1.5 Flash 8B"
  },
  "errors": null
}
```

**Error Response**:
```json
{
  "detail": "Error message here"
}
```

### Interactive API Docs
FastAPI provides automatic interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📁 Project Structure

```
ocr-document-analysis/
├── backend/
│   ├── main.py                 # FastAPI application & core logic
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (API keys)
│   └── .env.example           # Template for environment variables
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx         # Root layout component
│   │   ├── page.tsx           # Main application page
│   │   └── globals.css        # Global styles
│   ├── package.json           # Node dependencies
│   ├── tsconfig.json          # TypeScript configuration
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   ├── postcss.config.js      # PostCSS configuration
│   └── next.config.js         # Next.js configuration
│
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## 🔍 How It Works

### 1. File Upload & Processing

**Frontend**:
- User drags/drops or selects a file
- `react-dropzone` validates file type (JPG, PNG, PDF)
- File is stored in component state

**Backend**:
- Receives file via multipart/form-data
- Detects file type by extension
- For PDFs: Converts pages to images using PyMuPDF
- For images: Loads directly with Pillow

### 2. Text Extraction

**Parallel Processing**:
```python
tasks = [
    extract_text_with_gemini(image, "flash"),
    extract_text_with_gemini(image, "pro"),
    extract_text_with_gemini(image, "lite")
]
results = await asyncio.gather(*tasks)
```

**Each Model**:
1. Configures Gemini API with specific key
2. Sends image + extraction prompt
3. Receives text response
4. Tracks response time
5. Handles errors gracefully

### 3. Text Normalization

**Cleaning Process**:
```python
def normalize_text(text: str) -> str:
    lines = [line.strip() for line in text.split('\n')]
    lines = [line for line in lines if line]
    return '\n'.join(lines)
```

- Removes leading/trailing whitespace
- Eliminates empty lines
- Preserves structure

### 4. Model Comparison

**Scoring Algorithm**:

**A. Length Score (30% weight)**:
- Measures text completeness
- Normalized against longest output
- Formula: `length / max_length`

**B. Similarity Score (40% weight)**:
- Uses TF-IDF vectorization
- Calculates cosine similarity between outputs
- Measures semantic consistency

**C. Clarity Score (30% weight)**:
- Analyzes word count and line structure
- Formula: `(words/100) * 0.5 + (lines/20) * 0.5`
- Caps at 1.0

**Final Score**:
```python
score = length_score * 0.3 + similarity_score * 0.4 + clarity_score * 0.3
```

### 5. Results Display

**Frontend Rendering**:
- Three-column grid layout
- Color-coded score bars:
  - Green: ≥80% (Excellent)
  - Yellow: 60-79% (Good)
  - Red: <60% (Needs improvement)
- Best model highlighted with yellow border
- Response times displayed with clock icon

---

## 🔒 Security

### API Key Protection
✅ **Implemented**:
- API keys stored in backend `.env` file only
- Never exposed to frontend or client
- `.env` excluded from version control via `.gitignore`

❌ **Never Do**:
- Hardcode API keys in frontend code
- Commit `.env` to Git
- Share API keys in public repositories

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Restrict to frontend only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production**: Update `allow_origins` to your production domain.

### File Upload Security
- File type validation (whitelist approach)
- Size limits enforced by FastAPI
- Temporary file handling (no persistent storage)

---

## 🐛 Troubleshooting

### Backend Issues

#### Problem: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

#### Problem: `google.api_core.exceptions.InvalidArgument: 400 API key not valid`
**Solution**:
- Verify API keys in `backend/.env`
- Check for extra spaces or quotes
- Ensure keys are active in Google Cloud Console

#### Problem: `OSError: cannot identify image file`
**Solution**:
- Ensure uploaded file is valid JPG/PNG/PDF
- Check file isn't corrupted
- Try re-uploading

#### Problem: Port 8000 already in use
**Solution**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

#### Problem: `Error: Cannot find module 'next'`
**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### Problem: `Network Error` when uploading
**Solution**:
- Ensure backend is running on port 8000
- Check CORS configuration
- Verify `http://localhost:8000` is accessible

#### Problem: Port 3000 already in use
**Solution**:
```bash
# Use different port
PORT=3001 npm run dev
```

#### Problem: Tailwind styles not loading
**Solution**:
```bash
npm run dev  # Restart dev server
# Clear browser cache
```

### PDF Processing Issues

#### Problem: `fitz.fitz.FileDataError: cannot open document`
**Solution**:
- Ensure PDF isn't password-protected
- Check PDF isn't corrupted
- Try converting PDF to images manually first

#### Problem: Slow PDF processing
**Solution**:
- Large PDFs take longer to convert
- Currently processes first page only
- Consider implementing pagination for multi-page PDFs

### API Rate Limiting

#### Problem: `429 Too Many Requests`
**Solution**:
- Gemini API has rate limits
- Wait before retrying
- Consider implementing request queuing
- Check quota in Google Cloud Console

---

## 📊 Performance Optimization

### Backend
- **Async Processing**: All model calls run concurrently
- **Connection Pooling**: Reuse HTTP connections
- **Caching**: Consider adding Redis for repeated documents

### Frontend
- **Code Splitting**: Next.js automatic code splitting
- **Image Optimization**: Next.js Image component (if needed)
- **Lazy Loading**: Components load on demand

---

## 🚀 Deployment

### Backend Deployment (Example: Railway/Render)
1. Create new service
2. Connect repository
3. Set environment variables (API keys)
4. Deploy command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment (Example: Vercel)
1. Connect repository
2. Framework preset: Next.js
3. Build command: `npm run build`
4. Update API URL in `page.tsx` to production backend URL

---

## 📝 Usage Examples

### Example 1: Analyze Receipt
1. Upload receipt image (JPG/PNG)
2. Click "Analyze Document"
3. Compare extracted text from all models
4. Download best result as TXT

### Example 2: Process Scanned PDF
1. Upload scanned PDF document
2. System converts to images automatically
3. All three models extract text
4. View side-by-side comparison
5. Export complete analysis as JSON

### Example 3: Compare Model Performance
1. Upload same document multiple times
2. Note which model consistently scores highest
3. Use that model's output for production
4. Track response times for optimization

---

## 🔄 Future Enhancements

### Planned Features
- [ ] Multi-page PDF support with pagination
- [ ] Batch processing (multiple files)
- [ ] User authentication & history
- [ ] Custom model selection
- [ ] Language detection & translation
- [ ] OCR confidence scores per word
- [ ] Export to multiple formats (DOCX, CSV)
- [ ] Real-time progress tracking
- [ ] Model fine-tuning options
- [ ] Database storage for results

### Performance Improvements
- [ ] Redis caching for repeated documents
- [ ] WebSocket for real-time updates
- [ ] CDN integration for static assets
- [ ] Database connection pooling
- [ ] Request rate limiting
- [ ] Image compression before upload

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 🤝 Support

### Common Questions

**Q: Can I use different Gemini models?**
A: Yes! Update the model names in `backend/main.py` MODELS dictionary.

**Q: How do I add more models?**
A: Add new entries to MODELS dict, update frontend to display 4+ columns.

**Q: Can I process multiple pages?**
A: Currently processes first page only. Loop through `pdf_to_images()` results for multi-page.

**Q: What's the file size limit?**
A: Default FastAPI limit is 16MB. Adjust with `app.add_middleware(RequestSizeLimitMiddleware)`.

**Q: How accurate is the scoring?**
A: Scoring is heuristic-based. For production, consider human validation or ground truth comparison.

---

## 🎯 Quick Start Summary

```bash
# 1. Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py

# 2. Frontend (new terminal)
cd frontend
npm install
npm run dev

# 3. Open browser
http://localhost:3000
```

---

## ✅ Verification Checklist

Before first use, verify:
- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] API keys configured in `backend/.env`
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Can upload test image
- [ ] All three models return results

---

**🎉 You're all set! Upload a document and watch the AI magic happen!**

For issues or questions, check the Troubleshooting section above.
