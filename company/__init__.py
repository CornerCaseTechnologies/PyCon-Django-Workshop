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


class Positions(ChoicesEnum):
    MANAGER = "manager"
    SENIOR_DEVELOPER = "senior_developer"
    DEVELOPER = "developer"
    JUNIOR_DEVELOPER = "junior_developer"
    DESIGNER = "designer"
    TESTER = "tester"
