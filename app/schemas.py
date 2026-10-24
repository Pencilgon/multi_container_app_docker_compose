from typing import Literal

from pydantic import BaseModel, Field


MediaType = Literal[
    "film",
    "television",
    "video_game",
    "music",
    "book",
    "other",
]

RecoveryStatus = Literal[
    "lost",
    "partially_recovered",
    "found",
    "under_investigation",
]


class MediaCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    media_type: MediaType
    release_year: int | None = Field(
        default=None,
        ge=1800,
        le=2100,
    )
    recovery_status: RecoveryStatus = "lost"
    description: str | None = None
    source_url: str | None = Field(
        default=None,
        max_length=500,
    )


class MediaUpdate(BaseModel):
    recovery_status: RecoveryStatus


class MediaResponse(BaseModel):
    id: int
    title: str
    media_type: str
    release_year: int | None
    recovery_status: str
    description: str | None
    source_url: str | None