import unittest
from parameterized import parameterized
from bs4 import BeautifulSoup

from Details import Date, Date_Time, WeekendDetails, Location


class Test_XML_Keys(unittest.TestCase):

    @classmethod
    def setUpClass(self) -> None:
        self.file = open("test_Details.xml", 'r')
        self.xml = BeautifulSoup(self.file, features='xml')
        self.Location = Location(self.xml)
        self.Date = Date(self.xml)
        self.DateTime = Date_Time(self.xml)

    def test_Location(self):
        self.assertEqual(self.Location.city, "Sakhir")
        self.assertEqual(self.Location.country, "Bahrain")
        self.assertAlmostEqual(self.Location.lat, 26.0325, 5)
        self.assertAlmostEqual(self.Location.long, 50.5106, 5)
        self.assertEqual(repr(self.Location), f"{'Sakhir':<15}" + f"{'Bahrain':<15}")

    def test_Date(self):
        self.assertEqual(self.Date.date, "2024-03-02")
        self.assertEqual(self.Date.time, None)
        self.assertEqual(repr(self.Date), "2024-03-02")

    def test_Date_Time(self):
        self.assertEqual(self.DateTime.date, "2024-03-02")
        self.assertEqual(self.DateTime.time, "15:00:00Z")
        self.assertEqual(repr(self.DateTime), "2024-03-02 at 15:00:00Z")

    @classmethod
    def tearDownClass(self) -> None:
        self.file.close()
        return super().tearDownClass()


if __name__ == '__main__':
    unittest.main()
