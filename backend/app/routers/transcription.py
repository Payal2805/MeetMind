
import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import AudioFile, Meeting, Transcript
from app.schemas import TranscriptResponse

router = APIRouter(prefix="/meetings", tags=["Transcription"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/{meeting_id}/audio/{audio_id}/transcribe",
    response_model=TranscriptResponse,
)
def transcribe_audio(
    meeting_id: int,
    audio_id: int,
    db: Session = Depends(get_db),
):
    meeting = db.get(Meeting, meeting_id)
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found.")

    audio = db.get(AudioFile, audio_id)
    if audio is None or audio.meeting_id != meeting_id:
        raise HTTPException(status_code=404, detail="Audio file not found.")

    if not os.path.isfile(audio.file_path):
        raise HTTPException(
            status_code=404,
            detail="Audio file is missing from the server.",
        )

    existing_transcript = (
        db.query(Transcript)
        .filter(Transcript.audio_file_id == audio_id)
        .order_by(Transcript.id.desc())
        .first()
    )

    if existing_transcript and existing_transcript.status == "completed":
        return existing_transcript

    if existing_transcript:
        transcript_record = existing_transcript
    else:
        transcript_record = Transcript(
            meeting_id=meeting_id,
            audio_file_id=audio_id,
            full_text="",
            language=None,
            status="processing",
        )
        db.add(transcript_record)
        db.commit()
        db.refresh(transcript_record)

    try:
        import whisper

        model = whisper.load_model("tiny")
        result = model.transcribe(audio.file_path)

        transcript_record.full_text = result.get("text", "").strip()
        transcript_record.language = result.get("language")
        transcript_record.status = "completed"

        audio.status = "transcribed"
        db.commit()
        db.refresh(transcript_record)

        return transcript_record

    except Exception as exc:
        db.rollback()
        transcript_record = db.get(Transcript, transcript_record.id)
        if transcript_record is not None:
            transcript_record.status = "failed"
            db.commit()

        raise HTTPException(
            status_code=500,
            detail="Transcription failed. Check the backend terminal logs.",
        ) from exc


@router.get(
    "/{meeting_id}/transcripts/{transcript_id}",
    response_model=TranscriptResponse,
)
def get_transcript(
    meeting_id: int,
    transcript_id: int,
    db: Session = Depends(get_db),
):
    meeting = db.get(Meeting, meeting_id)
    if meeting is None:
        raise HTTPException(
            status_code=404,
            detail="Meeting not found.",
        )

    transcript = db.get(Transcript, transcript_id)

    if transcript is None or transcript.meeting_id != meeting_id:
        raise HTTPException(
            status_code=404,
            detail="Transcript not found.",
        )

    return transcript
