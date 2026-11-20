import json
import urllib.request
import urllib.error

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Meeting, Transcript, MeetingSummary
from app.schemas import MeetingSummaryResponse

router = APIRouter(prefix="/meetings", tags=["AI Summary"])

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_summary(transcript_text: str):
    prompt = f"""
You are an expert meeting assistant.

Analyze the following meeting transcript.

Return ONLY valid JSON with exactly these three keys:
- summary: A concise meeting summary.
- decisions: Important decisions made during the meeting.
- action_items: Tasks, responsible persons, and deadlines if mentioned.

Write all three values in simple Marathi using Devanagari script.
Do not invent information. If something is not mentioned, write "उल्लेख नाही".

Transcript:
{transcript_text}
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))

        generated_text = result.get("response", "")
        parsed_result = json.loads(generated_text)

        required_keys = {"summary", "decisions", "action_items"}

        if not required_keys.issubset(parsed_result):
            raise ValueError("AI response is missing required fields.")

        return {
            "summary": str(parsed_result["summary"]),
            "decisions": str(parsed_result["decisions"]),
            "action_items": str(parsed_result["action_items"]),
        }

    except (urllib.error.URLError, TimeoutError) as exc:
        raise HTTPException(
            status_code=503,
            detail="Local AI service is unavailable or timed out.",
        ) from exc
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=502,
            detail="AI returned an invalid summary response.",
        ) from exc


@router.post(
    "/{meeting_id}/transcripts/{transcript_id}/summarize",
    response_model=MeetingSummaryResponse,
    status_code=201,
)
def create_meeting_summary(
    meeting_id: int,
    transcript_id: int,
    db: Session = Depends(get_db),
):
    meeting = db.get(Meeting, meeting_id)

    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found.")

    transcript = db.get(Transcript, transcript_id)

    if transcript is None or transcript.meeting_id != meeting_id:
        raise HTTPException(status_code=404, detail="Transcript not found.")

    if transcript.status != "completed" or not transcript.full_text.strip():
        raise HTTPException(
            status_code=400,
            detail="A completed, non-empty transcript is required.",
        )

    existing_summary = (
        db.query(MeetingSummary)
        .filter(MeetingSummary.transcript_id == transcript_id)
        .first()
    )

    if existing_summary:
        return existing_summary

    ai_result = generate_summary(transcript.full_text)

    summary_record = MeetingSummary(
        meeting_id=meeting_id,
        transcript_id=transcript_id,
        summary=ai_result["summary"],
        decisions=ai_result["decisions"],
        action_items=ai_result["action_items"],
    )

    try:
        db.add(summary_record)
        db.commit()
        db.refresh(summary_record)
        return summary_record
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save meeting summary.",
        )
        