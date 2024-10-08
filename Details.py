from bs4 import BeautifulSoup
from XML_Keys import XML


class Location():
    def __init__(self, location_xml: BeautifulSoup):
        self.city = location_xml.find("Locality").text
        self.country = location_xml.find("Country").text
        self.lat = float(location_xml.find("Location")["lat"])
        self.long = float(location_xml.find("Location")["long"])

    def __repr__(self) -> str:
        city = f"{self.city:<15}"
        country = f"{self.country:<15}"

        return city + country


class Date():
    def __init__(self, date_xml: BeautifulSoup) -> None:
        self.date = date_xml.find(XML.DATE).text
        self.time = None

    def __repr__(self) -> str:
        return f"{self.date}"


class Date_Time():
    def __init__(self, session_xml: BeautifulSoup) -> None:
        self.date = session_xml.find(XML.DATE).text
        self.time = session_xml.find(XML.TIME).text

    def __repr__(self) -> str:
        return f"{self.date} at {self.time}"


class WeekendDetails():
    def __init__(self, xml: BeautifulSoup, season: int):
        if season > 2021:  # Seasons after 2021 have both session dates and times
            self.practice_1_date = Date_Time(xml.find(XML.FIRST_PRACTICE))
            self.practice_2_date = Date_Time(xml.find(XML.SECOND_PRACTICE))

            if xml.find(XML.THIRD_PRACTICE):
                self.practice_3_date = Date_Time(xml.find(XML.THIRD_PRACTICE))
                self.sprint = None
            else:
                self.practice_3_date = None
                self.sprint = Date_Time(xml.find(XML.SPRINT))

            self.qualy_date = Date_Time(xml.find(XML.QUALYFING))

        elif season == 2021:  # 2021 races have session dates but not times
            self.practice_1_date = Date(xml.find(XML.FIRST_PRACTICE))
            self.practice_2_date = Date(xml.find(XML.SECOND_PRACTICE))

            if xml.find(XML.THIRD_PRACTICE):
                self.practice_3_date = Date(xml.find(XML.THIRD_PRACTICE))
                self.sprint = None
            else:
                self.practice_3_date = None
                self.sprint = Date(xml.find(XML.SPRINT))

            self.qualy_date = Date(xml.find(XML.QUALYFING))
        else:  # Seasons before 2021 only had main race date and time, no other session info
            self.practice_1_date = None
            self.practice_2_date = None
            self.practice_3_date = None
            self.qualy_date = None
            self.sprint = None
