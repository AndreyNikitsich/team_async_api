import uuid
from dataclasses import InitVar, dataclass, field
from datetime import datetime


@dataclass
class UUIDMixin:
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class TimeStampedMixin:
    created: datetime = field(init=False, default=None)
    modified: datetime = field(init=False, default=None)

    created_at: InitVar[datetime] = None
    updated_at: InitVar[datetime] = None

    def __post_init__(self, created_at, updated_at):
        if self.created is None and created_at is not None:
            self.created = created_at
        if self.modified is None and updated_at is not None:
            self.modified = updated_at


@dataclass
class FilmWork(UUIDMixin, TimeStampedMixin):
    title: str = None
    description: str = None
    creation_date: datetime = None
    type: str = None
    rating: float = field(default=0.0)

    file_path: InitVar[str] = None

    def __post_init__(self, created_at, updated_at, file_path):
        super().__post_init__(created_at, updated_at)


@dataclass
class Genre(UUIDMixin, TimeStampedMixin):
    name: str = None
    description: str = None


@dataclass
class Person(UUIDMixin, TimeStampedMixin):
    full_name: str = None


@dataclass
class GenreFilmWork(UUIDMixin):
    film_work_id: uuid.UUID = None
    genre_id: uuid.UUID = None
    created: datetime = field(init=False, default=None)

    created_at: InitVar[datetime] = None

    def __post_init__(self, created_at):
        if self.created is None and created_at is not None:
            self.created = created_at


@dataclass
class PersonFilmWork(UUIDMixin):
    film_work_id: uuid.UUID = None
    person_id: uuid.UUID = None
    role: str = None
    created: datetime = field(init=False, default=None)

    created_at: InitVar[datetime] = None

    def __post_init__(self, created_at):
        if self.created is None and created_at is not None:
            self.created = created_at
