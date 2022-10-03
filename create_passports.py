import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import requests
from time import sleep

CREDENTIALS_FILE = 'token.json'
spreadsheet_id = '1FEiT0ikzJ8H9ltG952MigfZ1-nI8loecoggFbJ9U1MM'
height = 20
offset = 3

login = "agereth@gmail.com"
password = "juice87"
projectid = 1046

field_id_dict = {42208: 'is_cultivator', 42371: 'lead', 42374: 'abilities', 42375: 'hit_points', 42377: 'true_name',
                 42396: 'alco', 42414: 'features', 42416: 'study', 42443: 'slots', 42444: 'free_slots',
                 42445: 'techniques', 42446: 'death_words'}

if __name__ == '__main__':
    # init googlesheets api auth
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    http_auth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http=http_auth)

    # Авторизация на джойне
    r = requests.post('https://joinrpg.ru/x-api/token',
                      data={'grant_type': 'password', 'username': login, 'password': password})
    token = r.json()['access_token']

    # Получаем список персонажей
    r = requests.get('https://joinrpg.ru/x-game-api/{0}/characters'.format(projectid),
                     headers={"Authorization": "Bearer {0}".format(token)})
    characters = r.json()

    # получить данные персонажа с джойна
    char_dict = dict()
    for char in characters:
        characterid = char['characterId']
        r = requests.get('https://joinrpg.ru/x-game-api/{0}/characters/{1}'.format(projectid, characterid),
                         headers={"Authorization": "Bearer {0}".format(token)})

        char_data = r.json()['fields']
        print(char_data)
        char_name = char_data[0]['value']
        char_dict[char_name] = dict()
        for field in char_data[1:]:
            if field['projectFieldId'] in field_id_dict.keys():
                char_dict[char_name][field_id_dict[field['projectFieldId']]] = field['displayString']

    # пишем данные в таблицу

    for i, char in enumerate(char_dict.keys()):
        sleep(15)
        name = [char]
        request_body = {"valueInputOption": "RAW", "data": [
            {"range": 'b%i:b%i' % (i * height + offset, i * height + offset), "values": [name]}]}
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        _ = request.execute()

        name = char
        print(name)
        cult_data = ['Заклинатель', char_dict[name]['is_cultivator']]
        request_body = {"valueInputOption": "RAW", "data": [
            {"range": 'b%i:c%i' % (i * height + offset + 2, i * height + offset + 2), "values": [cult_data]}]}
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        _ = request.execute()

        lead_data = ['Инициатива', char_dict[name]['lead'], 'Смерть-слова']
        request_body = {"valueInputOption": "RAW", "data": [
            {"range": 'b%i:d%i' % (i * height + offset + 3, i * height + offset + 3), "values": [lead_data]}]}
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        _ = request.execute()

        hit_data = ['Хиты', char_dict[name]['hit_points'], char_dict[name]['death_words']]
        request_body = {"valueInputOption": "RAW", "data": [
            {"range": 'b%i:d%i' % (i * height + offset + 4, i * height + offset + 4), "values": [hit_data]}]}
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        _ = request.execute()

        alco_data = ['Алкоголь', char_dict[name]['alco'], 'Слоты']
        request_body = {"valueInputOption": "RAW", "data": [
            {"range": 'b%i:d%i' % (i * height + offset + 5, i * height + offset + 5), "values": [alco_data]}]}
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        _ = request.execute()

        techniques = char_dict[name]['techniques'].strip().split(', ')
        abilities = char_dict[name]['abilities'].replace("(готово)", "").strip().split(', ')
        techniques.extend(abilities)

        data = ['Общее число слотов', char_dict[name]['slots'], '1', techniques.pop(0)]
        request_body = {"valueInputOption": "RAW", "data": [
            {"range": 'b%i:e%i' % (i * height + offset + 6, i * height + offset + 6), "values": [data]}]}
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        _ = request.execute()

        data = ['Свободно слотов', char_dict[name]['free_slots'], '2', techniques.pop(0)]
        request_body = {"valueInputOption": "RAW", "data": [
            {"range": 'b%i:e%i' % (i * height + offset + 7, i * height + offset + 7), "values": [data]}]}
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        _ = request.execute()

        data = ['Особенности', "", '3', techniques.pop(0)]
        request_body = {"valueInputOption": "RAW", "data": [
            {"range": 'b%i:e%i' % (i * height + offset + 8, i * height + offset + 8), "values": [data]}]}
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        _ = request.execute()

        data = [char_dict[name]['features'], '', '4', techniques.pop(0)]
        request_body = {"valueInputOption": "RAW", "data": [
            {"range": 'b%i:e%i' % (i * height + offset + 9, i * height + offset + 9), "values": [data]}]}
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        _ = request.execute()

        for j in range(5, 7):
            slot = techniques.pop(0) if techniques else ""
            data = [' ', " ", j, slot]
            request_body = {"valueInputOption": "RAW", "data": [
                {"range": 'b%i:e%i' % (i * height + offset + 5 + j, i * height + offset + 5 + j), "values": [data]}]}
            request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
            _ = request.execute()

        slot = techniques.pop(0) if techniques else ""
        data = ['Обучение', " ", 7, slot]
        request_body = {"valueInputOption": "RAW", "data": [
                {"range": 'b%i:e%i' % (i * height + offset + 12, i * height + offset + 12), "values": [data]}]}
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        _ = request.execute()

        slot = techniques.pop(0) if techniques else ""
        data = [char_dict[name]['study'], "", 8, slot]
        request_body = {"valueInputOption": "RAW", "data": [
                {"range": 'b%i:e%i' % (i * height + offset + 13, i * height + offset + 13), "values": [data]}]}
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        _ = request.execute()

        data = ['Дополнительно']
        request_body = {"valueInputOption": "RAW", "data": [
                {"range": 'b%i:b%i' % (i * height + offset + 14, i * height + offset + 14),
                 "values": [data]}]}
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
        _ = request.execute()

        data = [""]
        if 'true_name' in char_dict[name].keys():
            data = [char_dict[name]['true_name']]
        if techniques:
            data = [data[0] + ' ' + ', '.join(techniques)]
        if data:
            request_body = {"valueInputOption": "RAW", "data": [
                {"range": 'b%i:b%i' % (i * height + offset + 15, i * height + offset + 15), "values": [data]}]}
            request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body)
            _ = request.execute()
