import random
from encrypter import AESCipher
from datetime import datetime
import requests
from uuid import uuid4
import time

p = 2 ** 255 - 19
g = 9
URL = 'http://176.37.97.117:8000/api/messages/'

user_id = str(uuid4())

last_timestamp = int(time.time())


def send_msg(content):
    requests.post(URL,
                  json={'content': str(content), 'timestamp': int(time.time()), 'userId': user_id})


def get_msg():
    msgs = requests.get(URL, params={'timestamp': last_timestamp})
    try:
        ret = msgs.json()
    except Exception as ex:
        return []
    return ret


if __name__ == '__main__':
    a = random.randint(0, 100)
    send_msg(f'INIT {pow(g, a, p)}')
    real_key = None
    other_id = None
    while real_key is None:
        msgs = get_msg()
        for msg in msgs:
            try:
                content = msg['content']
                if content.startswith('INIT'):
                    other_id = msg['userId']
                    _, other_key = content.split()
                    if other_id != user_id:
                        gp = int(other_key)
                        real_key = pow(gp, a, p)
                        send_msg(f'INIT {pow(g, a, p)}')
            except Exception as ex:
                print(ex)

        time.sleep(1)

    print(f'Connected to {other_id} with key {real_key}.')

    encrypter = AESCipher(real_key)

    while True:
        last_timestamp = int(time.time())
        msg = input('What do you want to send?\n>> ')
        if msg == 'exit()':
            break
        send_msg(encrypter.encrypt(msg))

        msgs = get_msg()
        msgs_filtered = []
        for msg in msgs:
            try:
                if msg['userId'] == other_id:
                    msgs_filtered.append((msg['timestamp'], encrypter.decrypt(msg['content'])))
            except Exception as ex:
                print(ex)

        print(f'You got {len(msgs_filtered)} messages from {other_id}')
        for timestamp, msg in msgs_filtered:
            print(f'{other_id} at {datetime.fromtimestamp(timestamp).isoformat()}: {msg}')
