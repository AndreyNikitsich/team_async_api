from pydantic import BaseModel


class ESGenre(BaseModel):
    """Модель данных жанров для индексации в Elasticsearch."""

    id: str
    name: str
    description: str | None = None
