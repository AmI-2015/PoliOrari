'''
'orari' module for querying Politecnico di Torino's
'''

import requests
# uses HTTP request library from http://www.python-requests.org/en/latest/


__author__ = 'Fulvio'

_baseURL = "http://www.swas.polito.it/dotnet/orari_lezione_pub/mobile/ws_orari_mobile.asmx/"

def find_courses_by_text(text):
    """
    Searches the full list of available courses and returns the ones
    whose description, or whose teacher name, matches the parameter

    :param text: string to search (in course name, and teacher name)
    :type text: str

    :return: the list of matching courses
    :rtype: list[dict]
    """
    url = _baseURL+"get_elenco_materie"
    params = { 'txt': text }

    r = requests.post(url,json=params)
    courses = r.json()
    return courses['d']

