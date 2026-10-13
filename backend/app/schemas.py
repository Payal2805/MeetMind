
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MeetingCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None


class MeetingResponse(BaseModel):
    id: int
    title: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    

class MeetingUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    
    

class AudioFileResponse(BaseModel):
    id: int
    meeting_id: int
    original_filename: str
    file_path: str
    source: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TranscriptResponse(BaseModel):
    id: int
    meeting_id: int
    audio_file_id: int
    full_text: str
    language: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MeetingSummaryResponse(BaseModel):
    id: int
    meeting_id: int
    transcript_id: int
    summary: str
    decisions: str
    action_items: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    