from pydantic import BaseSettings, Field, root_validator, AnyHttpUrl


class Settings(BaseSettings):
    APP_HOST: str = Field("127.0.0.1")
    APP_PORT: int = Field(3000)
    APP_CORS_ORIGINS: list[AnyHttpUrl] = Field(["http://localhost"])
    APP_SECRET_KEY: str = Field("d93bf836fe1b9ef571a55af686080dac3b0b571ae5ab59f2b890bfbd86b4fc1e")
    APP_DEFAULT_USER: str = Field("Admin")
    APP_DEFAULT_PASSWORD: str = Field("P@ssword")

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
            values["APP_PORT"] = values["APP_PORT"] + 1
            values["POSTGRES_DATABASE"] = f"{values['POSTGRES_DATABASE']}_test"
        if values["POSTGRES_URL"] is None:
            values["POSTGRES_URL"] = f"postgresql://{values['POSTGRES_USER']}:{values['POSTGRES_PASSWORD']}" \
                                     f"@{values['POSTGRES_HOST']}:{values['POSTGRES_PORT']}" \
                                     f"/{values['POSTGRES_DATABASE']}"
        return values

    class Config:
        env_file = ".env"


settings = Settings()
