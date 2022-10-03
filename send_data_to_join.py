import json
import requests

import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'token.json'
source_sheet_id = '1OMD-80UCEvbLwuBtZwtSL3ObKXKk2xKHJdpYmsrOzcA'
start = 'a2'
end = 'p45'

login = "agereth@gmail.com"
password = "juice87"
projectid = 1046

if __name__ == '__main__':

    # init googlesheets api auth
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    http_auth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http=http_auth)
    character_dict = dict()
    answer = service.spreadsheets().values().get(spreadsheetId=source_sheet_id,
                                                 range='%s:%s' % (start, end)).execute()
    for row in answer['values']:
        if len(row) >= 10:
            print(row[0])
            tech_num = int(row[3])
            tech_list = list()
            if tech_num > 0:
                for i in range(11, 11 + tech_num):
                    tech_list.append(row[i])
                tech_str = ', '.join(tech_list)
            else:
                tech_str = ""
            character_dict[row[0].lower()] = {'slots': int(row[8]),
                                              'free_slots': int(row[7]),
                                              'death_words': row[10],
                                              'techniques': tech_str}
    print(character_dict)

    # Авторизация на джойне
    r = requests.post('https://joinrpg.ru/x-api/token',
                      data={'grant_type': 'password', 'username': login, 'password': password})
    token = r.json()['access_token']

    # Получаем список персонажей
    r = requests.get('https://joinrpg.ru/x-game-api/{0}/characters'.format(projectid),
                     headers={"Authorization": "Bearer {0}".format(token)})
    characters = r.json()

    for char in characters:
        characterid = char['characterId']
        r = requests.get('https://joinrpg.ru/x-game-api/{0}/characters/{1}'.format(projectid, characterid),
                         headers={"Authorization": "Bearer {0}".format(token)})
        char_name = r.json()['fields'][0]['value']
        print(char_name)
        if char_name.lower() in character_dict.keys():
            current_char = character_dict[char_name.lower()]
            payload = {42443: str(current_char['slots']),
                       42444: str(current_char['free_slots']),
                       42446: current_char['death_words'],
                       42445: current_char['techniques']}

            url = 'https://joinrpg.ru/x-game-api/{0}/characters/{1}/fields'.format(projectid, characterid)
            r = requests.post(url, headers={"Authorization": "Bearer {0}".format(token),
                                            'Content-Type': 'application/json'}, json=payload)
        else:
            print("error: %s" % char_name)

'''
# простановка поля
data = {42443: "3"}
url = 'https://joinrpg.ru/x-game-api/{0}/characters/{1}/fields'.format(projectid, characterid)
r = requests.post(url, headers={"Authorization": "Bearer {0}".format(token),
                               'Content-Type': 'application/json'},
                 json=data)
print(r.status_code)
print(r.text)
'''

# for item in character['fields']:
#     print(item)

# полный дамп персонажей
'''char_dict = dict()
for char in characters:
    characterid = char['characterId']
    r = requests.get('https://joinrpg.ru/x-game-api/{0}/characters/{1}'.format(projectid, characterid), headers={"Authorization": "Bearer {0}".format(token)})
    character = r.json()
    char_dict[characterid] = character

with open("characters.txt", "w", encoding='utf-8') as f:
    f.write(json.dumps(char_dict, ensure_ascii=False))'''
