from requests import get
import json


def get_chatid(bot_token: str, name = None):
    url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    response = get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data['result']) > 0:
            if name:
                for i in data['result']:
                    if i['message']['from']['first_name'].lower() == name:
                        return i['message']['chat']['id']
            else:
                return data['result'][-1]['message']['chat']['id']


if __name__ == '__main__':
    print(get_chatid('a'))
