from pydantic import BaseModel, Field


class Genre(BaseModel):
    id: str
    name: str
    description: str | None = Field("")
