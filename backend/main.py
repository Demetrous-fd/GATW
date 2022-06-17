import sys
from pathlib import Path

sys.path.extend([str(Path(__file__).absolute().parent.parent), str(Path(__file__).absolute().parent)])
from backend.app import app

if __name__ == "__main__":
    import uvicorn
    from config import settings

    uvicorn.run(
        "app:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level="info",
        reload=True
    )
