from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from backend.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
