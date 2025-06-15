# Titan-Powered Full-Stack AI Chat Application

## Overview
This application is a secure, full-stack AI assistant that integrates Amazon Bedrock's Titan language model. Built using FastAPI (backend) and Streamlit (frontend), it supports authenticated chat interactions, performance monitoring, and model analytics.

## Features
- Full JWT-based user authentication
- Streamlit frontend with two tabs: Chat and Monitoring
- Real-time model latency tracking and request count display
- Amazon Titan model integration through Bedrock Runtime API
- Secure environment variable handling
- Easy-to-run locally with deployment-ready structure

## Technologies Used
- FastAPI (Python backend)
- Streamlit (Python frontend)
- Amazon Bedrock (Titan model)
- JWT for authentication (via PyJWT)
- boto3 for AWS interaction
- Python-dotenv for managing credentials

## Project Structure
```
project9_bedrock_app/
├── backend/
│   ├── app.py
│   ├── auth.py
│   ├── bedrock_client.py
│   └── monitor.py
├── frontend/
│   └── streamlit_chat.py
├── .env
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- An active AWS account with Bedrock access enabled for `amazon.titan-tg1-large`
- AWS CLI installed and configured

### Install Dependencies
```
pip install -r requirements.txt
```

### Configure Environment Variables
Create a `.env` file in the root directory:
```
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
AWS_REGION=us-east-1
JWT_SECRET=your_custom_jwt_secret
BEDROCK_MODEL_ID=amazon.titan-tg1-large
```

### Start Backend
```
PYTHONPATH=. uvicorn backend.app:app --reload
```

### Start Frontend
```
streamlit run frontend/streamlit_chat.py
```

## Usage
1. Open Streamlit in your browser (http://localhost:8501)
2. Log in with:
   - Username: `admin`
   - Password: `admin`
3. Use the Chat tab to interact with Titan
4. Use the Monitor tab to view:
   - Model name
   - Request count
   - Last response latency

## API Endpoints
- `POST /login`: Authenticates a user
- `POST /chat`: Sends prompt and returns model output
- `GET /metrics`: Returns request count, latency, and model ID

## Notes
- Titan model requests are made using `inputText` in Bedrock Runtime
- Metrics are stored in `app.state` for persistence across requests
- Monitoring is purely local and resets on backend restart

## License
This project is provided for educational and demonstration purposes only.

## Authors
Developed by Rajiv Raman