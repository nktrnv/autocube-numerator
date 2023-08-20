from src.config import ADMIN_PASSWORD
from src.exceptions import IncorrectNumber, WrongPassword
from src.model import Model


class Controller:
    def __init__(self, model: Model):
        self.model = model

    def get_next_number(self):
        return self.model.get_next_number()

    def set_number(self, password: str, number: str):
        try:
            number = int(number)
        except ValueError:
            raise IncorrectNumber

        if password != ADMIN_PASSWORD:
            raise WrongPassword

        self.model.set_number(number)
