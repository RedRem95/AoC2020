from abc import ABC, abstractmethod
from enum import IntEnum
from typing import List, Set, Optional, Iterable


class CodeLine:

    def __init__(self, instruction: str, value: float):
        self._instruction = str(instruction)
        self._value = value

    @classmethod
    def parse(cls, line: str):
        line = line.split(" ")
        if len(line) != 2:
            raise KeyError("Line has contain exactly the instruction and the value separated by a space")
        return CodeLine(line[0], float(line[1]))

    def get_instruction(self) -> str:
        return self._instruction

    def get_value(self) -> float:
        return self._value

    def __str__(self):
        return f"{self.get_instruction()} {self.get_value()}"


class Instruction(ABC):

    @classmethod
    @abstractmethod
    def instruction_key(cls) -> str:
        pass

    @abstractmethod
    def apply_instruction(self, line: CodeLine, instruction_pointer: int) -> int:
        pass

    def __str__(self):
        return f"Generic instruction {self.instruction_key()}"

    def __repr__(self):
        return f"Instruction<key:{self.instruction_key()}>"


class SimpleKeyInstruction(Instruction, ABC):

    @classmethod
    def instruction_key(cls) -> str:
        return cls.__name__.lower()


class SimpleNextInstruction(Instruction, ABC):
    def apply_instruction(self, line: CodeLine, instruction_pointer: int) -> int:
        self.simple_apply(line=line)
        return instruction_pointer + self.step_size()

    @abstractmethod
    def simple_apply(self, line: CodeLine):
        pass

    @staticmethod
    def step_size() -> int:
        return 1


class InstructionMachine:

    def __init__(self, machine_code: Iterable[CodeLine], registered_instructions: Iterable[Instruction]):

        self._registered_instructions = {}
        self.__machine_code_raw: List[CodeLine] = []
        self._instruction_pointer: int = 0
        self._machine_code: List[CodeLine] = []
        self._detect_loops = True
        self._visited: Set[int] = set()

        self.register_instructions(registered_instructions=registered_instructions)
        self.insert_new_code(machine_code=machine_code)
        self.reset_machine_code()
        self.reset_instruction_pointer()
        self.detect_loops()

    def reset_instruction_pointer(self, value: int = 0) -> "InstructionMachine":
        self._instruction_pointer = value
        return self

    def reset_machine_code(self) -> "InstructionMachine":
        self._machine_code = [x for x in self.__machine_code_raw]
        return self

    def insert_new_code(self, machine_code: Iterable[CodeLine], also_reset: bool = True):
        self.__machine_code_raw = [x for x in machine_code]
        if also_reset:
            self.reset_machine_code()

    def detect_loops(self, detect_loops: bool = True) -> "InstructionMachine":
        self._detect_loops = detect_loops
        return self

    def visit(self, instruction_pointer: int):
        if instruction_pointer in self._visited:
            return True
        self._visited.add(instruction_pointer)
        return False

    def register_instructions(self, registered_instructions: Iterable[Instruction]):
        for key, instruction in ((ri.instruction_key(), ri) for ri in registered_instructions):
            if key in self._registered_instructions:
                raise KeyError(f"Cant register {instruction}. Instruction with key {key} "
                               f"has already been registered as {self._registered_instructions[key]}")
            self._registered_instructions[key] = instruction

    def remove_instruction(self, instruction: Instruction):
        self._registered_instructions.pop(instruction.instruction_key())

    def run(self, *args, **kwargs) -> "ExitCodes":
        while True:
            if self._instruction_pointer >= len(self._machine_code):
                return ExitCodes.Good
            if self._detect_loops:
                if self.visit(instruction_pointer=self._instruction_pointer):
                    return ExitCodes.Loop
            line = self._machine_code[self._instruction_pointer]
            if line.get_instruction() not in self._registered_instructions:
                raise MachineError(line=line, instruction=None, machine=self)
            instruction = self._registered_instructions[line.get_instruction()]
            self._instruction_pointer = instruction.apply_instruction(line=line,
                                                                      instruction_pointer=self._instruction_pointer)


class ExitCodes(IntEnum):
    Good = 0,
    Loop = 1


class MachineError(Exception):
    def __init__(self, line: Optional[CodeLine], instruction: Optional[Instruction],
                 machine: Optional[InstructionMachine] = None):
        self._machine = machine
        self._current_line = line
        self._current_instruction = instruction

    def __repr__(self) -> str:
        return f"Machine error<line: {repr(self._current_line)}, instruction{repr(self._current_instruction)}>"

    def __str__(self) -> str:
        return f"There has been a machine error: {self._current_line} executed on {self._current_instruction}"


class JMP(SimpleKeyInstruction):
    def apply_instruction(self, line: CodeLine, instruction_pointer: int) -> int:
        return int(instruction_pointer + line.get_value())


class NOP(SimpleKeyInstruction, SimpleNextInstruction):
    def simple_apply(self, line: CodeLine):
        pass


class ACC(SimpleKeyInstruction, SimpleNextInstruction):
    def simple_apply(self, line: CodeLine):
        self._acc += line.get_value()

    def __init__(self, acc_init: int = 0) -> None:
        super().__init__()
        self._acc = acc_init

    def get_value(self):
        return self._acc
