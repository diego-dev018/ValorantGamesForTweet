from time import sleep
from datetime import datetime, timedelta
from os import system
from platform import platform
from get_twitter_api import get_api_main
from make_tweet import make_tweet_main
from get_times import get_sleep_time
from send_getcode_exportcode import get_code
from send_noti_telegrambot import send_telegram_main

telegram_codes = get_code('telegram_api.pkl') # {'bot_token': bot_token, 'chat_id': chat_id}


def main():
    oauth = get_api_main()
    send_telegram_main('SCRIPT \"VALORANG_GAMES_FOR_TWEET\" INICIADO CON EXITO!', telegram_codes['bot_token'], telegram_codes['chat_id'])
    system('cls' if 'windows' in platform().lower() else 'clear')
    while True:
        games_time = get_sleep_time(day=datetime.now().day+1, hour=1)
        msg = f'Esperando tiempo para CREAR el tweet... Se CREARA el {datetime.now() + timedelta(0, games_time)}!\n' if games_time else 'NO HAY PARTIDOS EL DIA DE HOY :('
        print(msg)
        send_telegram_main(msg, telegram_codes['bot_token'], telegram_codes['chat_id'])
        # sleep(games_time)

        tweet = make_tweet_main(datetime.now().day)
        print(f'TWEET CREADO\n{tweet}\n')

        tweet_time = get_sleep_time(day=datetime.now().day, hour=11)
        msg = f'\nEsperando tiempo para SUBIR el tweet... Se SUBIRA el {datetime.now() + timedelta(0, tweet_time)}!\n' if tweet else 'NO HAY PARTIDOS EL DIA DE HOY :('
        print(msg)
        send_telegram_main(f'TWEET CREADO EXITOSAMENTE\n\n{tweet}\n{msg}', telegram_codes['bot_token'], telegram_codes['chat_id'])
        # sleep(tweet_time)

        if tweet:
            response = oauth.post(
                "https://api.twitter.com/2/tweets",
                json={'text': tweet},
            )
            if response.status_code != 201:
                raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
            else:
                print("Response code: ", response.status_code)
                print("Tweet hecho con exito")
                send_telegram_main('TWEET PUBLICADO EXITOSAMENTE', telegram_codes['bot_token'], telegram_codes['chat_id'])

        else:
            print('No hay juegos hoy :(')

        break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nAdios!')
    except Exception as e:
        print(f'Ah ocurrido un error en el script!\n{e}')
        send_telegram_main(f'Ah ocurrido un error en el script!\n\nERROR:\n{e}', telegram_codes['bot_token'], telegram_codes['chat_id'])
