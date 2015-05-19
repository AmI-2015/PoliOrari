'''
'politoschedule' module for querying Politecnico di Torino's time tables

:module: politoschedule
'''

import requests
# uses HTTP request library from http://www.python-requests.org/en/latest/

import datetime
# standard library for handling dates and times
# see https://docs.python.org/2/library/datetime.html#

import re

__author__ = 'Fulvio'

_baseURL = "http://www.swas.polito.it/dotnet/orari_lezione_pub/mobile/ws_orari_mobile.asmx/"


class Course:
    """
    Information about a single course
    """

    def __init__(self, json_dict):
        """
        Create a new Course object

        :rtype: Course
        :param json_dict: the dictionary describing a course, returned by Json parsing
        """

        self.key = json_dict['chiave']
        '''Unique key'''

        self.topic = json_dict['materia']
        '''Topic (course name)'''

        self.pd = json_dict['pd']
        '''Periodo Didattico (Semester)'''

        self.teacher = json_dict['docente']
        '''Teacher name'''

        self.alpha_range = json_dict['alfabetica']
        '''Alphabetical sub-group'''


class Event:
    """
    Information about a single scheduled event (class or exam)
    """

    def __init__(self, json_dict):
        """
        Create a new Event object.

        Beware: the JSON information is parsed into meaningful fields. The parsing code is extremely
        fragile, and may break if slight modification are made to the JSON content.

        :rtype: Event
        :param json_dict: the dictionary describing a scheduled event, returned by Json parsing
        """

        self.id = json_dict['id']
        '''Unique key'''

        self.text = json_dict['text']
        '''full description of the event (includes HTML)'''

        self.start_str = json_dict['start']
        '''start time, as a string'''

        self.start = datetime.datetime.strptime(self.start_str, "%Y-%m-%dT%H:%M:%S")
        '''start time, as a datetime object'''

        self.end_str = json_dict['end']
        '''end time, as a string'''

        self.end = datetime.datetime.strptime(self.end_str, "%Y-%m-%dT%H:%M:%S")
        '''end time, as a datetime object'''

        # Parse and split the text into more useful fields
        # Tecniche di programmazione<p style="margin:0"></p><p style="margin:0">SQUADRA 1</p><p style="margin:0">CORNO</p><p style="margin:0">Aula LEP A (DIGEP)</p>
        words = re.split("<[^>]+>", self.text)
        self.topic = words[0]
        '''Course name'''

        self.dontknow = words[1]
        '''???? (always empty???)'''

        self.notes = words[3]
        '''Notes (e.g, SQUADRA)'''

        self.teacher = words[5]
        '''Teacher (last name only)'''

        self.room = words[7]
        '''Full room description (e.g., 'Aula 3')'''

        self.roomname = self.room[self.room.find(' ') + 1:]
        '''Room name (e.g., '3')'''


class Room():
    """
    Information about a single classroom
    """

    def __init__(self, json_dict):
        """
        Create a new Room object

        :rtype: Room
        :param json_dict: the dictionary describing a classroom, returned by Json parsing
        """
        self.name = json_dict['aula']
        self.campus = json_dict['sede']
        self.building = json_dict['sito']
        self.seats = int(json_dict['posti'])
        self.type = json_dict['tipo']
        self.lat = float(json_dict['lat'].replace(',', '.'))
        self.lon = float(json_dict['lon'].replace(',', '.'))


def find_courses_by_text(text):
    """
    Searches the full list of available courses and returns the ones
    whose description, or whose teacher name, matches the parameter 'text'.

    :param text: string to search (in course name, and teacher name)
    :type text: str

    :return: the list of matching courses
    :rtype: list[Course]
    """
    url = _baseURL + "get_elenco_materie"
    params = {'txt': text}

    r = requests.post(url, json=params)
    courses = r.json()
    r.close()
    return [Course(c) for c in courses['d']]


def find_events_by_courses(courses, date):
    """
    Searches the full list of events for a list of specified courses. The events are bound to
    one week before and two weeks later than the specified date.

    :param courses: a list of course IDs (taken from the field "chiave" in the find_courses_by_text result)
    :type courses: list[str]
    :param date: the date around which the events are extracted (suggestion: datetime.date.today())
    :type date: datetime.date
    :return: a list of events describing all the classes (in future, also exams) for anyof the courses
    :rtype: list[event]
    """
    url = _baseURL + "get_orario"
    params = {'listachiavimaterie': ','.join(courses), 'datarif': str(date)}

    r = requests.post(url, json=params)
    events = r.json()
    r.close()
    return [Event(e) for e in events['d']]


def find_events_by_room(room, date):
    """
    Searches the full list of events for a list of specified courses. The events are bound to
    one week before and two weeks later than the specified date.

    :param room: the name of the classroom (taken from Room.name)
    :type room: str
    :param date: the date around which the events are extracted (suggestion: datetime.date.today())
    :type date: datetime.date
    :return: a list of events describing all the classes (in future, also exams) for the room
    :rtype: list[Event]
    """
    url = _baseURL + "get_orario_aula"
    params = {'aula': room, 'datarif': str(date)}

    r = requests.post(url, json=params)
    events = r.json()
    r.close()
    return [Event(e) for e in events['d']]


def get_all_classrooms():
    """
    Searches the full list of classrooms.

    :return: a complete(?) list of classrooms all the classes in Politecnico
    :rtype: list[Room]
    """

    url = _baseURL + "get_elenco_aule"
    params = {}

    r = requests.post(url, json=params)
    rooms = r.json()
    r.close()
    return [Room(e) for e in rooms['d']]
