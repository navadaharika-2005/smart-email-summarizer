# 📧 Smart Email Summarizer


## 🚀 Live Demo

[Open the Smart Email Summarizer](https://smart-email-summarizer-8k5cs3ltg3qsqern3c8kw2.streamlit.app/)
An AI-powered email analyzer that connects to Gmail, extracts email content, and generates simple summaries.

## 🚀 Features

- 🔐 Gmail authentication
- 📩 Fetch emails directly from Gmail
- 📄 Display email content
- 🤖 AI-powered email summarization
- ✂️ Choose summary length
- ⚡ Streamlit web interface

## 🛠️ Technologies Used

- Python
- Streamlit
- Hugging Face Transformers
- PyTorch
- Gmail API
- Google OAuth 2.0
- BeautifulSoup

## 🧠 How It Works

1. Authenticate with Gmail.
2. Fetch emails from the user's inbox.
3. Select an email.
4. Load and display its content.
5. Choose the desired summary length.
6. The AI model generates a concise summary.

## 📂 Project Structure

```text
smart-email-summarizer/
│
├── app.py
├── summarizer.py
├── gmail_service.py
├── test_gmail.py
├── requirements.txt
├── .gitignore
└── README.md