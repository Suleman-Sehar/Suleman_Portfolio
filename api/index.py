import os
import re

import resend
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


PORTFOLIO_CONTACT_EMAIL = os.environ.get(
    "PORTFOLIO_CONTACT_EMAIL",
    "solemanseher@gmail.com",
)


class ContactForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    email: str = Field(..., min_length=3, max_length=254)
    message: str = Field(..., min_length=1, max_length=5000)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://suleman-portfolio-six.vercel.app",
        "https://suleman-portfolio.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/")
@app.post("/contact")
@app.post("/api/contact")
async def contact(payload: ContactForm) -> dict[str, str | bool]:
    email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    if not re.fullmatch(email_pattern, payload.email):
        raise HTTPException(status_code=422, detail={"message": "Invalid email address."})

    try:
        resend.api_key = os.environ["RESEND_API_KEY"]
        resend.Emails.send(
            {
                "from": "Portfolio Contact <onboarding@resend.dev>",
                "to": [PORTFOLIO_CONTACT_EMAIL],
                "subject": f"New message from {payload.name}",
                "html": f"""
                <h2>New portfolio message</h2>
                <p><strong>Name:</strong> {payload.name}</p>
                <p><strong>Email:</strong> {payload.email}</p>
                <p><strong>Message:</strong></p>
                <p>{payload.message}</p>
                """,
            }
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=500,
            detail={"message": "Missing RESEND_API_KEY environment variable."},
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={"message": "Failed to send message. Please try again later."},
        ) from exc

    return {"success": True, "message": "Message sent successfully."}
