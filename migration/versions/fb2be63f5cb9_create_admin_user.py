"""create admin user

Revision ID: fb2be63f5cb9
Revises: b91b0987b75d
Create Date: 2022-06-17 20:31:36.898695

"""
from fastapi_users.password import PasswordHelper

from backend.schemes import UserCreate
from backend.config import settings
from backend.models import User
from backend.database import SessionLocal


# revision identifiers, used by Alembic.
revision = 'fb2be63f5cb9'
down_revision = 'b91b0987b75d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    create_user = UserCreate.parse_obj({
        "username": settings.APP_DEFAULT_USER,
        "password": "",
        "is_superuser": True
    }).dict()
    create_user.pop("password")
    create_user["hashed_password"] = PasswordHelper().hash(settings.APP_DEFAULT_PASSWORD)
    with SessionLocal() as session:
        session.add(User(**create_user))
        session.commit()


def downgrade() -> None:
    pass
