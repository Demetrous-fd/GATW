from socket import gethostbyname

from pydantic import BaseSettings, Field, root_validator, AnyHttpUrl, validator, IPvAnyAddressError, IPvAnyAddress


class Settings(BaseSettings):
    APP_HOST: str = Field("127.0.0.1")
    APP_PORT: int = Field(3000)
    APP_CORS_ORIGINS: list[AnyHttpUrl] = Field(["http://localhost"])

    POSTGRES_HOST: str = Field("127.0.0.1")
    POSTGRES_PORT: int = Field(5432)
    POSTGRES_DATABASE: str = Field("postgres")
    POSTGRES_USER: str = Field("postgres")
    POSTGRES_PASSWORD: str = Field("postgres")
    POSTGRES_URL: str | None = Field(None)

    MINIO_HOST: str = Field("127.0.0.1")
    MINIO_API_PORT: int = Field(9001)
    MINIO_SECURE: bool = Field(False)
    MINIO_ACCESS_KEY: str = Field("None")
    MINIO_SECRET_KEY: str = Field("None")

    TESTING: bool = Field(False)

    @root_validator()
    def root_validation(cls, values):
        if values["TESTING"]:
            values['POSTGRES_DATABASE'] = f"{values['POSTGRES_DATABASE']}_test"
        if values["POSTGRES_URL"] is None:
            values["POSTGRES_URL"] = f"postgresql://{values['POSTGRES_USER']}:{values['POSTGRES_PASSWORD']}" \
                                     f"@{values['POSTGRES_HOST']}:{values['POSTGRES_PORT']}" \
                                     f"/{values['POSTGRES_DATABASE']}"
        return values

    class Config:
        env_file = ".env"


settings = Settings()
