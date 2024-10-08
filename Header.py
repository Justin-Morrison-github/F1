from enum import StrEnum
from colorama import Fore


class Header(StrEnum):
    POS = f"{'Pos':<5}"
    NAME = f"{'Name':<20}"
    CONSTRUCTOR = f"{'Constructor':<20}"
    TEAM = f"{'Team':<20}"
    EMPTY = ""
    NATIONALITY = f"{'Nationality':<15}"
    POINTS = f"{'Points':<10}"
    WINS = f"{'Wins':<15}"


class Season_Header(StrEnum):
    ROUND = f"{'Round':<8}"
    RACE_NAME = f"{'Race Name':<30}"
    CIRCUIT_NAME = f"{'Circuit Name':<40}"
    CITY = f"{'City':<15}"
    COUNTRY = f"{'Country':<15}"
    DATE = f"{'Date':<12}"
    TIME = f"{'Time':<12}"
    HEADER = Fore.YELLOW + ROUND + RACE_NAME + CIRCUIT_NAME + CITY + COUNTRY + DATE + TIME + Fore.RESET


class RaceResultHeader(StrEnum):
    POS = f"{'Pos':<5}"
    NUMBER = f"{'Number':<7}"
    NAME = f"{'Name':<20}"
    TEAM = f"{'Team':<20}"
    FINISH = f"{'Time':<15}"
    POINTS = f"{'Points':<10}"
    LAPS_COMPLETED = f"{'Laps':<10}"
    POS_CHANGE = f"{'Pos Change':<15}"
    HEADER = Fore.CYAN + POS + NUMBER + NAME + TEAM + FINISH + POINTS + LAPS_COMPLETED + POS_CHANGE + Fore.RESET
