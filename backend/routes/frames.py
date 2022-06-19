import uuid

import minio
from pydantic import conlist
from fastapi import APIRouter, UploadFile, Depends, status, HTTPException

from backend.database import get_session, get_async_session, Session, AsyncSession
from backend.utils import validate_upload_files, get_date_isoformat
from backend.schemes import FramesCreate, FramesResult, FrameRead
from backend.storage import get_storage, MIN_PART_SIZE
from backend.security import current_active_user
from backend.crud import CRUDFrame

router = APIRouter(
    prefix="/frames",
    tags=["Frames"],
    dependencies=[Depends(current_active_user)]
)


@router.get(
    "/{request_code}",
    response_model=list[FrameRead],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."},
        status.HTTP_404_NOT_FOUND: {"description": "The frames does not exist."}
    }
)
async def get_frames(request_code: uuid.UUID,
                     db: AsyncSession = Depends(get_async_session)):
    frames = await CRUDFrame.async_read(db, request_code)
    if frames:
        return frames

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    "",
    response_model=FramesResult,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."},
        status.HTTP_400_BAD_REQUEST: {"description": "Only jpeg images are accepted"}
    }
)
def upload_frames(frames: conlist(UploadFile, min_items=1, max_items=15),
                  request_code: uuid.UUID = Depends(uuid.uuid4),
                  storage: minio.Minio = Depends(get_storage),
                  db: Session = Depends(get_session)):
    if not validate_upload_files(frames):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only jpeg images are accepted"
        )

    bucket = get_date_isoformat()
    if not storage.bucket_exists(bucket):
        storage.make_bucket(bucket)

    frames_filename = []
    for frame in frames:
        image = storage.put_object(
            bucket,
            f"{uuid.uuid4()}.jpg",
            data=frame.file,
            length=-1,
            part_size=MIN_PART_SIZE
        )
        frames_filename.append(image.object_name)

    return CRUDFrame.create(
        db,
        FramesCreate(request_code=request_code, filenames=frames_filename)
    )


@router.delete(
    "/{request_code}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."},
        status.HTTP_404_NOT_FOUND: {"description": "The frames does not exist."}
    }
)
def delete_frames(request_code: uuid.UUID,
                  storage: minio.Minio = Depends(get_storage),
                  db: Session = Depends(get_session)):
    frames = CRUDFrame.read(db, request_code)
    if not frames:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    bucket = get_date_isoformat(frames[0].create_at)

    for frame in frames:
        storage.remove_object(bucket, frame.filename)

    CRUDFrame.delete(db, request_code)
