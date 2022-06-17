import minio

from backend.config import settings

client = minio.Minio(
    f"{settings.MINIO_HOST}:{settings.MINIO_API_PORT}",
    settings.MINIO_ACCESS_KEY,
    settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)

MIN_PART_SIZE = 8 * 1024 * 1024 * 5


def get_storage() -> minio.Minio:
    return client
