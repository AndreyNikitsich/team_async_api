from .models.film import Film, PersonsFilm
from .models.genre import Genre
from .models.person import Person

FAKE_FILMS = [
    Film(id="b8ecd337-f378-460a-9337-c14f143e3093", title="The Shawshank Redemption"),
    Film(id="adbd0f4e-e933-45c6-a7dc-807c2ea7ba10", title="The Godfather"),
    Film(id="312e3916-9b73-4a07-afa0-874f0a6157bd", title="12 Angry Men"),
]

FAKE_PERSONS_FILMS = [
    PersonsFilm(id="b8ecd337-f378-460a-9337-c14f143e3093", title="The Shawshank Redemption", roles=["actor"]),
    PersonsFilm(id="adbd0f4e-e933-45c6-a7dc-807c2ea7ba10", title="The Godfather", roles=["director"]),
    PersonsFilm(id="312e3916-9b73-4a07-afa0-874f0a6157bd", title="12 Angry Men", roles=["writer"]),
]

FAKE_ACTORS = [
    Person(id="a09dc4df-a03d-4a9a-8f75-e12e733d1ad8", name="Morgan Freeman"),
    Person(id="88503d79-b058-483b-be6b-77a8742617b5", name="Bob Gunton"),
    Person(id="7ed7530c-1aff-4d67-9df0-e418b1c624eb", name="Al Pacino"),
    Person(id="10bf5591-f38e-478f-9a46-577a2783d98f", name="Henry Fonda"),
]

FAKE_WRITERS = [
    Person(id="3cb47fe3-3856-45d9-a66b-e8aa21d233b3", name="Stephen King"),
    Person(id="38c78240-f978-4e06-9a03-3ebbf8b7240a", name="Mario Puzo"),
    Person(id="bc540510-3f00-47fe-ba53-fc0122f14417", name="Sidney Lumet"),
]

FAKE_DIRECTORS = [
    Person(id="dc7acf00-01e8-4c16-9f4b-0ee560332628", name="Frank Darabont"),
    Person(id="37d0a908-7f19-476f-a4c3-1c6b46134b23", name="Francis Ford Coppola"),
    Person(id="5af72cbe-2428-48eb-9851-61ce8610ea51", name="Sidney Lumet"),
]

FAKE_GENRES = [
    Genre(id="181a827f-d6f1-40ff-b72b-7b893c1cef61", name="crime"),
    Genre(id="09ae0dea-53a4-43d7-9c3a-ea5fc1edb0a9", name="drama"),
    Genre(id="cf64debe-429c-473e-980b-ba283b285843", name="romance"),
]

FAKE_PERSONS = [*FAKE_ACTORS, *FAKE_WRITERS, *FAKE_DIRECTORS]
