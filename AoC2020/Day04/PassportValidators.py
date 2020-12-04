from typing import Dict, Callable


def __byr(text: str):
    try:
        return 1920 <= int(text) <= 2020
    except ValueError:
        pass
    return False


def __iyr(text: str):
    try:
        return 2010 <= int(text) <= 2020
    except ValueError:
        pass
    return False


def __eyr(text: str):
    try:
        return 2020 <= int(text) <= 2030
    except ValueError:
        pass
    return False


def __hgt(text: str):
    try:
        if text.endswith("cm"):
            return 150 <= int(text[:-2]) <= 193
        if text.endswith("in"):
            return 59 <= int(text[:-2]) <= 76
    except ValueError:
        pass
    return False


def __hcl(text: str):
    try:
        if text.startswith("#"):
            int(text[1:], base=16)
            return len(text) == 7
    except ValueError:
        pass
    return False


def __ecl(text: str):
    return text in ["amb", "blu", "brn", "gry", "hzl", "grn", "oth"]


def __pid(text: str):
    try:
        int(text, base=10)
        return len(text) == 9
    except ValueError:
        pass
    return False


def __cid(text: str):
    return True


KEYS = {
    "byr": "(Birth Year)",
    "iyr": "(Issue Year)",
    "eyr": "(Expiration Year)",
    "hgt": "(Height)",
    "hcl": "(Hair Color)",
    "ecl": "(Eye Color)",
    "pid": "(Passport ID)",
    "cid": "(Country ID)"
}

VALIDATORS_REQUIRED: Dict[str, Callable[[str], bool]] = {
    "byr": __byr,
    "iyr": __iyr,
    "eyr": __eyr,
    "hgt": __hgt,
    "hcl": __hcl,
    "ecl": __ecl,
    "pid": __pid
}

VALIDATORS_OPTIONAL: Dict[str, Callable[[str], bool]] = {
    "cid": __cid
}
