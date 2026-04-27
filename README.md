# AI Math Assistant

AI Math Assistant is a full-stack web application that solves math problems using a Python backend powered by LangChain, OpenRouter, and SymPy. The frontend is built with HTML, CSS, and JavaScript, and connects to a FastAPI backend for live responses.

## Preview

![AI Math Assistant Screenshot](Assets/Screenshot%202026-04-27%20042647.png)

## Demo Video

[Watch Demo Video](Assets/AI%20Math%20Assistant.mp4)

## Features

- Natural language math queries
- Basic arithmetic
- Algebraic simplification
- Expression expansion
- Factorization
- Equation solving
- Derivatives
- Indefinite integrals
- Definite integrals
- Limits
- Trigonometric evaluation
- Trigonometric simplification
- Matrix determinant
- Matrix inverse
- Matrix multiplication
- Matrix eigenvalues
- Dark-themed frontend interface
- FastAPI backend integration

## Tech Stack

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- FastAPI
- LangChain
- OpenRouter
- SymPy
- Uvicorn

## Project Structure

```text
AI-Math-Assistant/
├── Assets/
│   ├── AI Math Assistant.mp4
│   └── Screenshot 2026-04-27 042647.png
├── api.py
├── main.py
├── index.html
├── styles.css
├── script.js
├── pyproject.toml
├── uv.lock
├── .gitignore
└── README.md


### Run the backend

- uv run uvicorn api:app --reload --host 127.0.0.1 --port 8000
- Backend URL: http://127.0.0.1:8000


### Run the frontend

- python -m http.server 3000
- Frontend URL: http://127.0.0.1:3000
