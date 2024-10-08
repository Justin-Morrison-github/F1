
import unittest
from parameterized import parameterized

from XML_Keys import XML


class Test_XML_Keys(unittest.TestCase):
    @parameterized.expand([
        ("Number", XML.NUMBER, "number"),
        ("Position", XML.POSITION, "position"),
        ("Points", XML.POINTS, "points"),
        ("Driver", XML.DRIVER, "Driver"),
        ("Code", XML.CODE, "code"),
        ("Date Of Birth", XML.DOB, "DateOfBirth"),
        ("Grid", XML.GRID, "Grid"),
        ("Laps Completed", XML.LAPS_COMPLETED, "Laps"),
        ("Status", XML.STATUS, "Status"),
        ("Fastest Lap", XML.FASTEST_LAP, "FastestLap"),
        ("Wins", XML.WINS, "wins"),
        ("Rank", XML.RANK, "rank"),
        ("Lap", XML.LAP, "lap"),
        ("Average Speed", XML.AVERAGE_SPEED, "AverageSpeed"),
        ("Nationality", XML.NATIONALITY, "Nationality"),
        ("Constructor", XML.CONSTRUCTOR, "Constructor"),
        ("Constructor ID", XML.CONSTRUCTOR_ID, "constructorId"),
        ("Given Name", XML.GIVENNAME, "GivenName"),
        ("Name", XML.NAME, "Name"),
        ("Family Name", XML.FAMILYNAME, "FamilyName"),
        ("Date", XML.DATE, "Date"),
        ("Time", XML.TIME, "Time"),
        ("First Practice", XML.FIRST_PRACTICE, "FirstPractice"),
        ("Second Practice", XML.SECOND_PRACTICE, "SecondPractice"),
        ("Third Practice", XML.THIRD_PRACTICE, "ThirdPractice"),
        ("Qualifying", XML.QUALYFING, "Qualifying"),
        ("Sprint", XML.SPRINT, "Sprint"),
        ("Season", XML.SEASON, "season"),
        ("Round", XML.ROUND, "round"),
        ("Race Name", XML.RACE_NAME, "RaceName"),
        ("Circuit", XML.CIRCUIT, "Circuit"),
        ("Circuit ID", XML.CIRCUIT_ID, "circuitId"),
        ("Circuit Name", XML.CIRCUIT_NAME, "CircuitName"),
        ("Result", XML.RESULT, "Result"),
    ])
    def test_values(self, name, input, expected):
        self.assertEqual(input, expected)


if __name__ == '__main__':
    unittest.main()
