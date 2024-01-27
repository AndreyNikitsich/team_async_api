from faker.providers import BaseProvider

from ..models.mpaa_rating import MPAARating


class MPAARatingProvider(BaseProvider):
    mpaa_rating_collection = list(MPAARating)

    weights_of_collection = [0.15, 0.15, 0.2, 0.3, 0.15, 0.05]

    def mpaa_rating(self) -> MPAARating:
        return self.generator.random.choices(
            self.mpaa_rating_collection,
            self.weights_of_collection,
            k=1,
        )[0]
