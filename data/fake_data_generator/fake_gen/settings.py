from faker import Faker

from .providers.genre import GenreProvider
from .providers.roles import RoleProvider

CHUNK_SIZE = 1024


fake = Faker('ru_RU')
fake.add_provider(GenreProvider)
fake.add_provider(RoleProvider)
