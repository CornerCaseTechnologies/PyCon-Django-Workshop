from django.db.models.enums import Choices


class ChoicesEnum(Choices):
    @classmethod
    def get_choices(cls) -> list:
        choices = []
        for prop in cls:
            choices.append((prop.value, prop.name))
        return choices


class ExampleEnum(ChoicesEnum):
        ChoiceA = "a"
        ChoiceB = "b"