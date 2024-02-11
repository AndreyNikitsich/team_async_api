import abc
import json
from typing import Any

from redis import Redis

ALLOWED_VTYPES = (str, bytes, float, int)


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния.

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, state: dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""

    @abc.abstractmethod
    def retrieve_state(self) -> dict[str, Any]:
        """Получить состояние из хранилища."""


class JsonFileStorage(BaseStorage):
    """
    Реализация хранилища, использующего локальный файл.
    Формат хранения: JSON
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self._state = self.retrieve_state()

    def save_state(self, state: dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        self._state.update(state)
        with open(self.file_path, "w") as file:
            json.dump(self._state, file)

    def retrieve_state(self) -> dict[str, Any]:
        """Получить состояние из хранилища."""
        result = {}
        try:
            with open(self.file_path, "r") as file:
                result = json.load(file)
        finally:
            return result


class RedisStorage(BaseStorage):
    """
    Реализация хранилища, использующего Redis.
    Формат хранения: JSON
    """

    def __init__(self, redis_adapter: Redis):
        self.redis_adapter = redis_adapter
        self._state = self.retrieve_state()

    def save_state(self, state: dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        self._state.update(state)
        self.redis_adapter.set("data", json.dumps(self._state))

    def retrieve_state(self) -> dict[str, Any]:
        """Получить состояние из хранилища."""
        res_bytes = self.redis_adapter.get("data")

        if isinstance(res_bytes, ALLOWED_VTYPES):
            return json.loads(res_bytes)

        return {}


class State:
    """Класс для работы с состояниями."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage
        self._dict = {}

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        self._dict[key] = value
        self.storage.save_state(self._dict)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        self._dict = self.storage.retrieve_state()
        return self._dict.get(key)
