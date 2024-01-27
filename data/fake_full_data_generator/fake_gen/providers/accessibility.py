from faker.providers import BaseProvider

from ..models.accessibility import Accessibility


class AccessibilityProvider(BaseProvider):
    accessibility_collection = list(Accessibility)

    weights_of_number_of_combinations = [0.5, 0.3, 0.2]

    def accessibility(self) -> set[Accessibility]:
        number_of_combinations = self.generator.random.choices(
            [1, 2, 3],
            weights=self.weights_of_number_of_combinations,
            k=1,
        )[0]
        return set(self.generator.random.choices(
            self.accessibility_collection,
            k=number_of_combinations,
        ))
