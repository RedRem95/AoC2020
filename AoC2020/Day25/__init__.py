from typing import Tuple

from AoC.Day import Day, StarTask


class Day25(Day):
    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        content = [int(x.strip()) for x in str(raw_input, "utf-8").strip().split("\n") if len(x) > 0]
        return {"card_public_key": content[0], "door_public_key": content[1]}

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run(**self.get_input(task=task), **self.get_day_config())
        if task is not None:
            return "Simply pay", None
        return "", None

    @staticmethod
    def _iterate_value(s: int, v: int, d: int):
        return (s * v) % d

    @staticmethod
    def _run(card_public_key: int, door_public_key: int, subject_number: int, divisor: int) -> Tuple[str, object]:
        log = [
            ("Cards public key", card_public_key),
            ("Doors public key", door_public_key),
            ("Subject number", subject_number),
            ("Divisor of encryption", divisor)
        ]
        value = 1
        loop_size = 1
        while True:

            value = Day25._iterate_value(s=subject_number, v=value, d=divisor)

            if value == card_public_key:
                subject_number = door_public_key
                log.append(("Needed loop size", loop_size))
                log.append(("Found key", "Card"))
                break
            if value == door_public_key:
                subject_number = card_public_key
                log.append(("Needed loop size", loop_size))
                log.append(("Found key", "Door"))
                break

            loop_size += 1

        value = 1
        for _ in range(loop_size):
            value = Day25._iterate_value(s=subject_number, v=value, d=divisor)

        log.append(("Encryption key", value))

        template = "{key:%ss} {value}" % (max(len(x[0]) for x in log) + 1)

        return "\n".join(template.format(key=f"{key}:", value=value) for key, value in log), value
