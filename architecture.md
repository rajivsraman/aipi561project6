# Architecture Overview

This document describes the full-stack architecture of the Conversational AI Assistant application, which integrates Streamlit (frontend), FastAPI (backend), and Amazon Bedrock’s Titan model for LLM inference. It supports secure login, real-time messaging, logging, and live monitoring.

---

## System Design

The system is composed of three tightly integrated layers:

### 1. Frontend: `Streamlit`
- Handles login and chat UI.
- Stores JWT token securely via session state.
- Sends authenticated POST requests to backend endpoints (`/login`, `/chat`).
- Renders chat messages and live metrics.

### 2. Backend: `FastAPI`
- Validates user credentials and returns JWTs.
- Secures the `/chat` route with JWT verification.
- Forwards user input to Amazon Bedrock's Titan model.
- Captures metadata such as latency, request volume, and timestamps.

### 3. Inference: `Amazon Bedrock (Titan)`
- Handles inference using the `amazon.titan-tg1-large` model.
- Accepts raw JSON requests and returns text completions.
- Fully managed on AWS; invoked securely from backend.

---

## Component Diagram (built with ChatGPT)

```plaintext
+---------------------+        +---------------------+        +-----------------------------+
|   Streamlit Frontend|<------>|   FastAPI Backend   |<------>|  Amazon Bedrock Titan Model |
+---------------------+        +---------------------+        +-----------------------------+
| - Login form        |        | - /login, /chat API |        | - amazon.titan-tg1-large    |
| - JWT in session    |        | - JWT validation    |        | - Text-to-text LLM          |
| - Chat UI           |        | - Monitoring store  |        |                             |
+---------------------+        +---------------------+        +-----------------------------+
