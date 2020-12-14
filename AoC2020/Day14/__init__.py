import itertools
from typing import Tuple, List, Dict

from AoC.Day import Day, StarTask


class Day14(Day):

    def convert_input(self, raw_input: bytes, task: StarTask) -> object:
        raw_data = [x for x in str(raw_input, "utf-8").split("\n") if len(x) > 0]
        ret = []
        for line in raw_data:
            ret.append(line)
        return ret

    def run(self, task: StarTask) -> Tuple[str, object]:
        if task == StarTask.Task01:
            return self._run(data=self.get_input(task=StarTask.Task01), mask_address=False, mask_value=True)
        if task == StarTask.Task02:
            return self._run(data=self.get_input(task=StarTask.Task02), mask_address=True, mask_value=False)
        return "", None

    def _run(self, data: List[str], mask_address: bool, mask_value: bool):
        memory: Dict[int, int] = {}
        target_bits = int(self.get_day_config()["bit_length"])
        binary_format = "{0:0%sb}" % target_bits
        current_mask: List[str] = ["X"] * target_bits
        mask_changes = 0
        memory_access = 0

        for line in data:
            if line.startswith("mask = "):
                current_mask = list(line[len("mask = "):])
                current_mask = ["X"] * max(0, target_bits - len(current_mask)) + current_mask
                mask_changes += 1
            if line.startswith("mem["):
                address = list(binary_format.format(int(line.split("[")[1].split("]")[0])))
                floating_pos = []

                if mask_address:
                    for i in range(1, target_bits + 1, 1):
                        if current_mask[-i] != "0":
                            address[-i] = current_mask[-i]
                        if current_mask[-i] == "X":
                            floating_pos.append(-i)

                if len(floating_pos) > 0:
                    addresses = []
                    for combination in itertools.product([0, 1], repeat=len(floating_pos)):
                        for f, i in enumerate(combination):
                            address[floating_pos[f]] = i
                        addresses.append(int("".join(str(x) for x in address), 2))
                else:
                    addresses = [int("".join(address), 2)]

                value = list(binary_format.format(int(line.split("=")[1].strip())))
                if mask_value:
                    for i in range(1, target_bits + 1, 1):
                        if current_mask[-i] != "X":
                            value[-i] = current_mask[-i]
                value = int("".join(value), 2)

                for address in addresses:
                    memory[address] = value
                    memory_access += 1

        log = [
            f"       Used memory: {len(memory)}",
            f"  Access to memory: {memory_access}",
            f"         New Masks: {mask_changes}",
            f"Min memory address: {min(memory.keys())}",
            f"Max memory address: {max(memory.keys())}",
            f" Sum stored memory: {sum(memory.values())}",
        ]
        return "\n".join(str(x) for x in log), sum(memory.values())

    def get__file__(self) -> str:
        return __file__
