from enum import StrEnum, auto


class XML(StrEnum):
    NUMBER = auto()
    POSITION = auto()
    POINTS = auto()
    DRIVER = "Driver"
    CODE = auto()
    DOB = "DateOfBirth"
    GRID = "Grid"
    LAPS_COMPLETED = "Laps"
    STATUS = "Status"
    FASTEST_LAP = "FastestLap"
    WINS = auto()
    RANK = auto()
    LAP = auto()
    AVERAGE_SPEED = "AverageSpeed"
    NATIONALITY = "Nationality"
    CONSTRUCTOR = "Constructor"
    CONSTRUCTOR_ID = "constructorId"
    GIVENNAME = "GivenName"
    NAME = "Name"
    FAMILYNAME = "FamilyName"
    DATE = "Date"
    TIME = "Time"
    FIRST_PRACTICE = "FirstPractice"
    SECOND_PRACTICE = "SecondPractice"
    THIRD_PRACTICE = "ThirdPractice"
    QUALYFING = "Qualifying"
    SPRINT = "Sprint"
    SEASON = auto()
    ROUND = auto()
    RACE_NAME = "RaceName"
    CIRCUIT = "Circuit"
    CIRCUIT_ID = "circuitId"
    CIRCUIT_NAME = "CircuitName"
    RESULT = "Result"
