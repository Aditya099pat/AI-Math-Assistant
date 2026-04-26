from dotenv import load_dotenv
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from main import (
    calculator,
    say_hello,
    simplify_expression,
    expand_expression,
    factor_expression,
    derivative,
    integral,
    definite_integral,
    compute_limit,
    solve_equation,
    evaluate_trig_function,
    trig_simplify,
    create_matrix,
    matrix_determinant,
    matrix_inverse,
    matrix_multiply,
    matrix_eigenvalues,
)

load_dotenv()

app = FastAPI(title="AI Math Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SolveRequest(BaseModel):
    question: str


def build_agent():
    model = ChatOpenAI(
        model="openrouter/auto",
        temperature=0,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:3000",
            "X-OpenRouter-Title": "My First AI Project",
        },
    )

    tools = [
        calculator,
        say_hello,
        simplify_expression,
        expand_expression,
        factor_expression,
        derivative,
        integral,
        definite_integral,
        compute_limit,
        solve_equation,
        evaluate_trig_function,
        trig_simplify,
        create_matrix,
        matrix_determinant,
        matrix_inverse,
        matrix_multiply,
        matrix_eigenvalues,
    ]

    return create_agent(model=model, tools=tools)


agent = build_agent()


@app.get("/")
def health_check():
    return {"status": "API is running"}


@app.post("/api/solve")
def solve(request: SolveRequest):
    try:
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request.question,
                    }
                ]
            }
        )

        answer_parts = []

        for message in result["messages"]:
            if getattr(message, "type", "") == "ai" and message.content:
                answer_parts.append(message.content)

        answer = "\n".join(answer_parts).strip()

        return {
            "success": True,
            "answer": answer or "No answer generated.",
        }

    except Exception as e:
        return {
            "success": False,
            "answer": str(e),
        }