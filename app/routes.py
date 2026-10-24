from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .models import MediaEntry
from .schemas import MediaCreate, MediaUpdate, MediaResponse


router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post(
    "/media",
    response_model=MediaResponse,
    status_code=201,
)
def create_media(
    data: MediaCreate,
    db: Session = Depends(get_db),
):
    entry = MediaEntry(**data.model_dump())

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return entry


@router.get(
    "/media",
    response_model=list[MediaResponse],
)
def get_media(db: Session = Depends(get_db)):
    statement = select(MediaEntry).order_by(MediaEntry.id)

    return list(db.scalars(statement).all())


@router.get(
    "/media/{media_id}",
    response_model=MediaResponse,
)
def get_media_by_id(
    media_id: int,
    db: Session = Depends(get_db),
):
    entry = db.get(MediaEntry, media_id)

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Media entry not found",
        )

    return entry


@router.patch(
    "/media/{media_id}",
    response_model=MediaResponse,
)
def update_media(
    media_id: int,
    data: MediaUpdate,
    db: Session = Depends(get_db),
):
    entry = db.get(MediaEntry, media_id)

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Media entry not found",
        )

    entry.recovery_status = data.recovery_status

    db.commit()
    db.refresh(entry)

    return entry


@router.delete(
    "/media/{media_id}",
    status_code=204,
)
def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
):
    entry = db.get(MediaEntry, media_id)

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Media entry not found",
        )

    db.delete(entry)
    db.commit()

    return Response(status_code=204)