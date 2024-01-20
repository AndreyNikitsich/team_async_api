from faker.providers import BaseProvider

from ..models.roles import Roles


class RoleProvider(BaseProvider):

    roles_collection = list(Roles)

    weights_of_number_of_combinations = [
        0.7,
        0.2,
        0.1,
    ]

    weights_of_collection = [
        0.8,
        0.15,
        0.05,
    ]

    def roles(self) -> set[Roles]:
        number_of_combinations = self.generator.random.choices(
            [1, 2, 3],
            weights=self.weights_of_number_of_combinations,
            k=1,
        )[0]
        return set(self.generator.random.choices(
            self.roles_collection,
            weights=self.weights_of_collection,
            k=number_of_combinations,
        ))
