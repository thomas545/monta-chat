# Chat Appliacation - Monta AI
Chat application using Genimi & Python, which is a powerful and flexible open-source App to chat with AI models

## Installation

- Clone the PR

- Create Python ENV
  - python3 -m venv `env_name`
  - source  env_name/bin/activate
  - pip install -r requirements.txt
  - Add `.env` file with  your secret keys


- Run project
  - Run: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`


## API Documentation

- [Local Docs](http://127.0.0.1:8000/docs)
- [Live Docs](https://monta-chat.onrender.com/docs)

## Tech Stack
- Python 3.10+
- FastAPI
- Langchain
- Google Gemini
- MongoDB
- uvicorn

## ENV Keys
- MONGO_URI="xxxxxxxx"
- SECRET_KEY="xxxxxxxx"
- ALGORITHM="xxxxxxxx"
- ACCESS_TOKEN_EXPIRE_DAYS="xxxxxxxx"
- GOOGLE_API_KEY="xxxxxxxx"
