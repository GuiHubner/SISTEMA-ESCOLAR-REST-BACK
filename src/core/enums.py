from enum import Enum

class UserType(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    COORDINATOR = "coordinator"