from enum import StrEnum, auto


class Request():
    def __init__(self, limit, offset):
        self.limit = limit
        self.offset = offset

    def advance(self):
        self.offset += self.limit


class Request_Type(StrEnum):
    GET_STANDINGS = auto()
    GET_RACE_RESULTS = auto()


class Url():
    def __init__(self, request_type: Request_Type, year, query=None, request: Request = None):
        if request_type == Request_Type.GET_STANDINGS:
            self.URL = f"https://ergast.com/api/f1/{year}/{query}"
        elif request_type == Request_Type.GET_RACE_RESULTS:
            self.URL = f"https://ergast.com/api/f1/{year}/results/?limit={request.limit}&offset={request.offset}"
