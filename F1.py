# Program that gathers F1 data from the Ergast API: http://ergast.com/mrd

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back
from enum import StrEnum, auto

from XML_Keys import XML
from Header import Header, Season_Header, RaceResultHeader
from Details import Location, Date_Time, Date
from Request import Request, Request_Type, Url
from Symbols import Symbols


def main():
    year = 2024
    races = 5
    lines_per_race = 20
    offset = 0

    request = Request(races * lines_per_race, offset)
    url = Url(Request_Type.GET_RACE_RESULTS, year=year, request=request)
    url_text = requests.get(url.URL).text
    soup = BeautifulSoup(url_text, features="xml")

    season = Season(soup)
    print(f"{Fore.GREEN}First {races} Races of the {year} F1 Season:{Fore.RESET}")
    print(season)
    print(f"{Fore.GREEN}Constructor Standings for {year} F1 Season:{Fore.RESET}")
    print(season.results.team_standings)
    print(f"{Fore.GREEN}Driver Standings for {year} F1 Season:{Fore.RESET}")
    print(season.results.driver_standings)

    print(f"\n{Fore.GREEN}Race Results for First {races} Races of {year} F1 Season:{Fore.RESET}\n")

    for race in season:
        print(Season_Header.HEADER)
        print(race)
        print(race.results)


class Season():
    def __init__(self, season_xml: BeautifulSoup):
        xml_races = season_xml.find_all("Race")
        self.race_count = len(xml_races)
        self.races = [Race(race) for race in xml_races]

        year = int(season_xml.find("RaceTable")[XML.SEASON])
        self.results = Season_Results(year)
        print()

    def __repr__(self) -> str:
        string = f"\n{Season_Header.HEADER}\n"

        for race in self.races:
            string += str(race) + "\n"

        return string

    def __iter__(self):
        for race in self.races:
            yield race


class Race():
    def __init__(self, xml: BeautifulSoup):
        self.season = int(xml[XML.SEASON])
        self.round = int(xml[XML.ROUND])
        self.race_name = xml.find(XML.RACE_NAME).text
        self.circuit_Id = xml.find(XML.CIRCUIT)[XML.CIRCUIT_ID]
        self.circuit_name = xml.find(XML.CIRCUIT_NAME).text
        self.location = Location(xml)
        self.date = Date_Time(xml)
        # self.weekend_details = WeekendDetails(xml, self.season)
        self.results = RaceResultList(xml)

    def __repr__(self) -> str:

        round = f"{self.round:<8}"
        race_name = f"{self.race_name:<30}"
        circ_name = f"{self.circuit_name:<40}"
        date = f"{self.date.date:<12}"
        time = f"{self.date.time:<12}"

        return round + race_name + circ_name + str(self.location) + date + time


class RaceResultList():
    def __init__(self, soup: BeautifulSoup):
        self.results = [RaceResult(result) for result in soup.find_all(XML.RESULT)]

    def __len__(self):
        return len(self.results)

    def __repr__(self) -> str:
        string = f"\n{RaceResultHeader.HEADER}\n"

        for result in self.results:
            string += f"{result}"

        return string

    def get_winner(self):
        return self.results[0]


class RaceResult():
    def __init__(self, result_xml: BeautifulSoup):
        self.number = check(result_xml[XML.NUMBER])
        self.finish_pos = int(check(result_xml[XML.POSITION]))
        self.points = int(check(result_xml[XML.POINTS]))
        self.driver_abrv = check(result_xml.find(XML.DRIVER)[XML.CODE])

        self.name = check(result_xml.find(XML.GIVENNAME).text) + " " + check(result_xml.find(XML.FAMILYNAME).text)
        self.dob = check(result_xml.find(XML.DOB).text)
        self.nationality = check(result_xml.find(XML.NATIONALITY).text)

        self.team = Team(check(result_xml.find(XML.CONSTRUCTOR)[XML.CONSTRUCTOR_ID]),
                         check(result_xml.find(XML.CONSTRUCTOR).find(XML.NAME).text),
                         check(result_xml.find(XML.CONSTRUCTOR).find(XML.NATIONALITY).text))

        self.start_pos = int(check(result_xml.find(XML.GRID).text))
        self.laps_completed = int(check(result_xml.find(XML.LAPS_COMPLETED).text))
        self.status = check(result_xml.find(XML.STATUS).text)

        if self.status == "Finished":
            self.finish_delta = check(result_xml.find(XML.TIME).text)
        else:
            self.finish_delta = None

        if self.laps_completed > 1:

            self.fl = FastestLap(check(result_xml.find(XML.FASTEST_LAP)))

            if self.fl.fl_rank == 1:
                self.fastest = True
            else:
                self.fastest = False

        else:
            self.fl = None
            self.fastest = None

        if self.start_pos != 0:
            self.pos_change = self.start_pos - self.finish_pos
        else:
            self.pos_change = 20 - self.finish_pos

    def __repr__(self) -> str:
        pos = f"{self.finish_pos:<5}"
        number = f"{self.number:<7}"
        name = f"{self.name:<20}"
        team = f"{self.team.team_name:<20}"
        finish = f"{(self.finish_delta if self.status == 'Finished' else self.status):<15}"
        if self.fastest:
            points = f"{(Back.MAGENTA + str(self.points) + Back.RESET):<20}"
        else:
            points = f"{self.points:<10}"

        laps = f"{self.laps_completed:<10}"
        if self.pos_change > 0:
            pos_change = f"{(Fore.GREEN + Symbols.GAINED + ' ' + str(self.pos_change) + Fore.RESET):<15}"
        elif self.pos_change < 0:
            pos_change = f"{(Fore.RED + Symbols.LOST + ' ' + str(abs(self.pos_change)) + Fore.RESET):<15}"
        else:
            pos_change = f"{('- ' + str(self.pos_change)):<15}"

        return pos + number + name + team + finish + points + laps + pos_change + "\n"


class Team():
    def __init__(self, team_id, team_name, team_nat):
        self.team_id = team_id
        self.team_name = team_name
        self.team_nat = team_nat

    def __repr__(self) -> str:
        return f"{self.team_name}"


class FastestLap():
    def __init__(self, fastest_lap_xml: BeautifulSoup):
        if fastest_lap_xml:
            self.fl_rank = int(fastest_lap_xml[XML.RANK])
            self.fl_lap_number = int(fastest_lap_xml[XML.LAP])
            self.fl_time = fastest_lap_xml.find(XML.TIME).text
            self.fastest_average_speed_kph = float(fastest_lap_xml.find(XML.AVERAGE_SPEED).text)
        else:
            self.fl_rank = None
            self.fl_lap_number = None
            self.fl_time = None
            self.fastest_average_speed_kph = None

    def __repr__(self) -> str:
        return f'{self.fl_rank}{"th" if int(self.fl_rank) > 2 else "nd" if int(self.fl_rank)==2 else "st"} Fastest Lap: {self.fl_time} on lap {self.fl_lap_number}'


class Query(StrEnum):
    CONSTRUCTOR_STANDINGS = "constructorStandings"
    DRIVER_STANDINGS = "driverStandings"


class Tag(StrEnum):
    CONSTRUCTOR_STANDING = "ConstructorStanding"
    DRIVER_STANDING = "DriverStanding"


class Option(StrEnum):
    CONSTRUCTOR = auto()
    DRIVER = auto()
    BOTH = auto()


class Packet():
    def __init__(self, option: Option):
        if option == Option.CONSTRUCTOR:
            self.query = Query.CONSTRUCTOR_STANDINGS
            self.tag = Tag.CONSTRUCTOR_STANDING
            self.option = option
        elif option == Option.DRIVER:
            self.query = Query.DRIVER_STANDINGS
            self.tag = Tag.DRIVER_STANDING
            self.option = option
        else:
            self.query = None
            self.tag = None
            self.option = None

    def __repr__(self) -> str:
        return str(self.__dict__)


class Season_Results():
    def __init__(self, year):
        self.year = year

        self.constructor_xml = self.get_year_results_xml(self.year, Packet(Option.CONSTRUCTOR))
        self.driver_xml = self.get_year_results_xml(self.year, Packet(Option.DRIVER))

        self.team_standings = Standing_List(self.constructor_xml, Packet(Option.CONSTRUCTOR))
        self.driver_standings = Standing_List(self.driver_xml, Packet(Option.DRIVER))

    def get_year_results_xml(self, year, packet: Packet) -> BeautifulSoup:
        url = Url(Request_Type.GET_STANDINGS, year, packet.query)
        return BeautifulSoup(requests.get(url.URL).text, features="xml")

    def __repr__(self) -> str:
        return f"{self.team_standings}\n{self.driver_standings}"


class Standing_List():
    def __init__(self, soup: BeautifulSoup, packet: Packet):
        self.members = []

        if packet.tag == Tag.CONSTRUCTOR_STANDING:
            self.driver = False
        elif packet.tag == Tag.DRIVER_STANDING:
            self.driver = True

        xml_standings = soup.find_all(packet.tag)
        for xml_standing in xml_standings:
            self.add(Standing(xml_standing, packet.option))

    def __len__(self):
        return len(self.members)

    def add(self, standing):
        self.members.append(standing)

    def __repr__(self) -> str:
        string = f"\n{Fore.YELLOW}{Header.POS}{Header.NAME if self.driver else Header.CONSTRUCTOR}{Header.TEAM if self.driver else Header.EMPTY}{Header.NATIONALITY}{Header.POINTS}{Header.WINS}{Fore.RESET}\n"

        for member in self.members:
            string += f"{member}\n"

        return string

    def get_winner(self):
        return self.members[0]


class Standing():
    def __init__(self, xml: BeautifulSoup, option: Option):
        self.pos = int(xml[XML.POSITION])
        self.points = int(xml[XML.POINTS])
        self.wins = int(xml[XML.WINS])
        self.nat = xml.find(XML.NATIONALITY).text

        if option == Option.DRIVER:
            self.team = xml.find(XML.CONSTRUCTOR).find(XML.NAME).text
            self.name = xml.find(XML.GIVENNAME).text + " " + xml.find(XML.FAMILYNAME).text
        elif option == Option.CONSTRUCTOR:
            self.team = None
            self.name = xml.find(XML.CONSTRUCTOR).find(XML.NAME).text

    def __repr__(self) -> str:
        return f"{self.pos:<5}{self.name:<20}{(f'{self.team:<20}' if self.team else '')}{self.nat:<15}{self.points:<10}{self.wins:<5}"


def check(value):
    try:
        if value:
            return value
        else:
            return None
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()
