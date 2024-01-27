from faker import Faker

from .providers.accessibility import AccessibilityProvider
from .providers.definitions import DefinitionProvider
from .providers.genre import GenreProvider
from .providers.mpaa_rating import MPAARatingProvider
from .providers.roles import RoleProvider

CHUNK_SIZE = 1024


fake = Faker('ru_RU')
fake.add_provider(AccessibilityProvider)
fake.add_provider(DefinitionProvider)
fake.add_provider(GenreProvider)
fake.add_provider(MPAARatingProvider)
fake.add_provider(RoleProvider)
