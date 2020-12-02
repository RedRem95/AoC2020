from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    def get_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def validate(self, v1: int, v2: int, character: str, password: str) -> bool:
        pass


class Toboggan(Validator):

    def get_name(self) -> str:
        return "Official Toboggan Policy"

    def validate(self, v1: int, v2: int, c: str, pw: str) -> bool:
        return (pw[v1] == c and pw[v2] != c) or (pw[v1] != c and pw[v2] == c)


class SledRental(Validator):

    def get_name(self) -> str:
        return "Sled Rental Down The Street Policy"

    def validate(self, v1: int, v2: int, character: str, password: str) -> bool:
        return v1 <= len([x for x in password if x == character]) <= v2
