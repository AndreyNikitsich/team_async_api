from datetime import datetime


class TimestampedMixin:

    @classmethod
    def created(cls):
        return datetime.now()

    @classmethod
    def modified(cls):
        return datetime.now()
