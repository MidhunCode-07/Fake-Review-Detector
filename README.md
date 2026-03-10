# 🛡️ ReviewGuard — AI Fake Review Detector

> Unmask fake product reviews in real-time using AI, NLP, and 
> reviewer behavior analysis.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![AI](https://img.shields.io/badge/AI-Claude%20Sonnet%204-purple)
![Domain](https://img.shields.io/badge/Domain-Retail-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 🚀 About The Project

ReviewGuard is a full-stack AI web application built for the 
**retail domain** that automatically detects fake product reviews. 
With 42% of online reviews estimated to be fake, this system 
helps customers make informed purchase decisions and helps 
e-commerce platforms maintain review integrity.

The system analyzes reviews using three powerful layers:
- 🔬 **NLP Text Analysis** — 11 linguistic fraud signals
- 👤 **Reviewer Behavior Profiling** — 7 behavioral red flags
- 🤖 **Claude Vision AI** — Product identification from image

---

## ✨ Features

- 📝 **Text Review Analysis** — Paste any review and get an 
  instant fraud score with detailed signal breakdown
- 📦 **Product Image Scan** — Upload a product photo, AI 
  identifies it and analyzes its reviews automatically
- 👤 **Reviewer Behavior Analysis** — Detect suspicious patterns 
  from a reviewer's past review history
- 🔬 **Full Combined Analysis** — 60% text + 40% behavior = 
  unified fraud score
- 📦 **Bulk Analysis** — Analyze up to 20 reviews at once
- 📊 **Trust Score Dashboard** — Visual breakdown of 
  Genuine / Suspicious / Fake reviews per product

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python 3.x, Flask, Flask-CORS     |
| Frontend   | HTML5, CSS3, Vanilla JavaScript   |
| AI Model   | Claude Sonnet 4 (Anthropic API)   |
| Database   | MySQL (proposed for production)   |
| Fonts      | Outfit + JetBrains Mono           |

---

## 📁 Project Structure
```
reviewguard/
├── backend/
│   ├── app.py              # Flask REST API
│   └── requirements.txt    # Python dependencies
└── frontend/
    └── index.html          # Complete UI (no build needed)
```

---

## ⚙️ How To Run

### Step 1 — Clone the Repository
```bash
git clone https://github.com/yourusername/reviewguard.git
cd reviewguard
```

### Step 2 — Start the Backend
```bash
cd backend
pip install flask flask-cors
python app.py
```
Server runs at `http://localhost:5000`

### Step 3 — Open the Frontend
Just open `frontend/index.html` in any browser.
No build step needed.

---

## 🔌 API Endpoints

| Method | Endpoint               | Description                    |
|--------|------------------------|--------------------------------|
| GET    | `/api/health`          | Check server status            |
| POST   | `/api/analyze`         | Analyze single review          |
| POST   | `/api/bulk-analyze`    | Analyze up to 20 reviews       |
| POST   | `/api/reviewer-behavior` | Reviewer behavior profiling  |
| POST   | `/api/full-analysis`   | Combined text + behavior score |

---

## 🧠 How It Works
```
User uploads product image
         ↓
Claude Vision AI identifies product
(name, brand, category, features)
         ↓
AI generates realistic review samples
(genuine + suspicious + fake mix)
         ↓
Flask backend scores each review
using 11 NLP fraud signals
         ↓
Results displayed with Trust Score,
color-coded review cards & signal drilldown
```

---

## 📊 Fraud Detection Signals

### Text Signals (11)
- Word count & sentence length
- Exclamation mark density
- CAPS ratio
- Lexical diversity (repetition)
- Spam keyword detection
- Generic phrase detection
- Sentiment extremity
- Verified purchase status
- Reviewer account history
- Extreme rating pattern
- Generic phrase count

### Behavioral Signals (7)
- Extreme rating pattern (85%+ one-star or five-star)
- Zero rating variance across reviews
- Copy-paste text similarity
- Review burst detection (same-day posting)
- All 5-star or all 1-star history
- Very short review pattern
- Unnatural product category spread

---

## 🎯 Verdict Thresholds

| Score Range | Verdict     |
|-------------|-------------|
| 0% – 39%    | ✅ Genuine  |
| 40% – 64%   | ⚠️ Suspicious |
| 65% – 100%  | 🚨 Fake     |

---

## 👥 Team

| Member   | Responsibility                        |
|----------|---------------------------------------|
| Member 1 | Backend — Python Flask API & Scoring  |
| Member 2 | Frontend — UI/UX HTML CSS JavaScript  |
| Member 3 | AI Integration — Claude Vision & Testing |

---

## 📌 Domain
**Retail / E-Commerce** — Final Year Academic Project

---

## 🔮 Future Scope

- [ ] Integrate MySQL database for persistent storage
- [ ] Train ML model on Yelp/Amazon fake review datasets
- [ ] Add multilingual review support
- [ ] Build browser extension for Amazon & Flipkart
- [ ] Real-time review monitoring dashboard
- [ ] Email alerts for coordinated fake review attacks

---

## 📜 License
This project is for academic purposes.

---

## 🙏 Acknowledgements
- [Anthropic Claude AI](https://anthropic.com) for Vision API
- [Flask](https://flask.palletsprojects.com) for backend framework
- Retail fake review research papers for domain knowledge

---

⭐ If you found this project helpful, please give it a star!
```

---

## 🏷️ GitHub Topics / Tags to Add
```
fake-review-detection, nlp, python, flask, retail, 
e-commerce, machine-learning, claude-ai, review-analysis, 
fraud-detection, html-css-javascript, final-year-project,
anthropic, sentiment-analysis, reviewer-behavior
