# 🧠 MindSpace: A Mindful Companion  
*A Streamlit-based AI Mental Health Support System powered by OpenRouter AI*

---

## 🌿 Overview

**MindSpace** is an AI-driven **mental health companion** designed to provide empathetic, supportive, and non-judgmental conversations to users dealing with stress, anxiety, or emotional distress.  
Built using **Streamlit** and **OpenRouter AI**, it offers **mood tracking**, **coping strategies**, and **mental wellness guidance** through a clean, responsive web interface.

This project was developed as part of the **IBM SkillsBuild Internship Program (Capstone Project)** under **Saveetha Engineering College** (ECE Department).

---

## 💡 Problem Statement

Increased academic pressure, social isolation, and limited access to mental health professionals have left many students and young adults struggling with their emotional well-being.  
Traditional counseling systems are often stigmatized or unavailable.

**MindSpace** aims to bridge this gap by offering an **accessible, private, and always-available digital companion** that provides:
- Safe and empathetic AI conversations  
- Mood and emotion tracking  
- Coping tools and self-help strategies  
- Crisis detection and immediate help resources  

---

---

## 🧩 Features

✅ **AI-powered support** – empathetic, natural, and non-judgmental dialogue  
📊 **Mood tracking** – log emotions with intensity and optional notes  
💡 **Coping strategies** – guided exercises and mindfulness prompts  
🚨 **Crisis detection** – auto-detects distress keywords and shows helpline info  
🧘 **Wellness tools** – quick mood-boosting and grounding tips  
🔒 **Privacy-focused** – no personal data stored; uses secure HTTPS API calls  
📱 **Responsive UI** – Streamlit interface works on desktop and mobile  

---

## 🧠 Core Components

| File | Description |
|------|--------------|
| `app.py` | Streamlit UI – chat interface, sidebar tools, and layout |
| `openrouter_client.py` | Handles API communication with OpenRouter securely |
| `prompts.py` | Contains coping strategies, mindfulness tips, and prompt templates |
| `safety.py` | Detects crisis-related keywords and validates inputs |
| `requirements.txt` | Project dependencies |
| `.streamlit/secrets.toml` | Stores API key securely on Streamlit Cloud |

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **AI Model:** Mistral 7B via OpenRouter API  
- **Visualization:** Plotly / Pandas  
- **Deployment:** Streamlit Cloud  
- **Version Control:** GitHub  

---

## 🚀 Setup Instructions (Run Locally)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/MindSpace--A-Mindful-Companion.git
cd MindSpace--A-Mindful-Companion
pip install -r requirements.txt
OPENROUTER_API_KEY = "your_api_key_here"
streamlit run app.py
```
