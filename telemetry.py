# wthud - Head-up Display for War Thunder
# Copyright (C) 2020 wysiwyng
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Telemetry requests from War Thunder localhost server. Adapted from
# https://github.com/PowerBroker2/WarThunder

import requests
import socket

IP_ADDRESS     = '127.0.0.1' #socket.gethostbyname(socket.gethostname())
URL_INDICATORS = 'http://{}:8111/indicators'.format(IP_ADDRESS)
URL_STATE      = 'http://{}:8111/state'.format(IP_ADDRESS)
URL_COMMENTS   = 'http://{}:8111/gamechat?lastId={}'
URL_EVENTS     = 'http://{}:8111/hudmsg?lastEvt=-1&lastDmg={}'
URL_MAP_IMG    = 'http://{}:8111/map.img'.format(IP_ADDRESS)
URL_MAP_OBJ    = 'http://{}:8111/map_obj.json'.format(IP_ADDRESS)
URL_MAP_INFO   = 'http://{}:8111/map_info.json'.format(IP_ADDRESS)
FT_TO_M        = 0.3048
IN_FLIGHT      = 0
IN_MENU        = -1
NO_MISSION     = -2
WT_NOT_RUNNING = -3
OTHER_ERROR    = -4
METRICS_PLANES = ['p-', 'f-', 'f2', 'f3', 'f4', 'f6', 'f7', 'f8', 'f9', 'os',
                  'sb', 'tb', 'a-', 'pb', 'am', 'ad', 'fj', 'b-', 'xp', 'bt',
                  'xa', 'xf', 'sp', 'hu', 'ty', 'fi', 'gl', 'ni', 'fu', 'fu',
                  'se', 'bl', 'be', 'su', 'te', 'st', 'mo', 'we', 'ha']

_s = requests.Session()

def find_altitude(indicators):
    name = indicators['type']

    # account for freedom units in US and UK planes
    if name[:2] in METRICS_PLANES:
        if 'altitude_10k' in indicators.keys():
            return indicators['altitude_10k'] * FT_TO_M
        elif 'altitude_hour' in indicators.keys():
            return indicators['altitude_hour'] * FT_TO_M
        elif 'altitude_min' in indicators.keys():
            return indicators['altitude_min'] * FT_TO_M
        else:
            return 0
    else:
        if 'altitude_10k' in indicators.keys():
            return indicators['altitude_10k']
        elif 'altitude_hour' in indicators.keys():
            return indicators['altitude_hour']
        elif 'altitude_min' in indicators.keys():
            return indicators['altitude_min']
        else:
            return 0

def get_indicators():
    try:
        obj = _s.get(URL_INDICATORS, timeout=0.1).json()

        if obj['valid']:
            obj['aviahorizon_pitch'] = -obj['aviahorizon_pitch'] if 'aviahorizon_pitch' in obj else None
            obj['aviahorizon_roll'] = -obj['aviahorizon_roll'] if 'aviahorizon_roll' in obj else None

            obj['alt_m'] = find_altitude(obj)

            return obj
    except:
        return None

def get_state():
    try:
        obj = _s.get(URL_STATE, timeout=0.1).json()

        if obj['valid']:
            return obj
    except:
        return None

def get_map_obj():
    try:
        obj = _s.get(URL_MAP_OBJ, timeout=0.1).json()

        if obj['valid']:
            return obj
    except:
        return None

def get_map_info():
    try:
        obj = _s.get(URL_MAP_INFO, timeout=0.1).json()

        if obj['valid']:
            return obj
    except:
        return None

def get_flight_data():
    try:
        ind = get_indicators()
        state = get_state()

        if ind['valid'] and state['valid']:
            obj = {}

            obj.update(ind)
            obj.update(state)

            return obj
    except:
        return None

def calc_additional_data(obj):
    # get speed for further calculations
    speed = obj.get('speed')
    if not speed:
        speed = obj.get('speed')

if __name__ == "__main__":
    while True:
        ind = get_indicators()
        state = get_state()
        pass