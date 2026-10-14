from enum import StrEnum
import antigravity


class Program(StrEnum):
    CS = "COMPUTER SCIENCE"
    CB = "CYBER SECURITY"
    IS = "INFORMATION SYSTEM"

class Student:
    def __init__(self, name: str,
               program: Program):
        self.name = name

        self.__program = program
        self.__gpa = 0.0

        self.__is_expelled = False
        self.__is_grant = True

    @property
    def gpa(self):
        return self.__gpa


    def set_gpa(self, value: float):
        if 0.0 < value > 4.0:
            raise ValueError("GPA должен находится в диапазоне от 0 до 4")

        self.__gpa = value

        if self.__gpa < 2.0:
            self.__is_grant = False
        else:
            self.__is_grant = True

        if self.__gpa < 1.0:
            self.__is_expelled = True
        else:
            self.__is_expelled = False

    def transfer(self, program: Program):
        if self.__is_expelled:
            raise ValueError("Невозможно перевести отчисленного студента")

        self.__program = program

    def __str__(self) -> str:
        return f"""Студент: {self.name}
        \tОбразовательная программа: {self.__program.value}
        \tТекущий годвоой GPA: {self.__gpa}
        \tУчится {"на бесплатном" if self.__is_grant else "на платном"} отделении
        \tОтчислен: {"ДА" if self.__is_expelled else "НЕТ"}
        """

stud1 = Student(
    name="Андрей",
    program=Program.CS
)

stud1.set_gpa(3.8)
print(stud1)

stud1.transfer(
    program=Program.CB
)
stud1.set_gpa(1.6)
print(stud1)

stud1.set_gpa(0.67)
print(stud1)

stud1.set_gpa(5)
