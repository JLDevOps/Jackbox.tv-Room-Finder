import requests
from itertools import product
import time
from random import randint
import threading
import os, sys

base_url = "https://blobcast.jackboxgames.com/room/"
exitFlag = 0

class roomThread(threading.Thread):
    def __init__(self, code, room_name):
        threading.Thread.__init__(self)
        self.code = code
        self.room_name = room_name
        self.kill_received = False

    def run(self):
        print("Starting " + self.room_name)
        while not self.kill_received:
            test_room_code(self.code)
        print("Exiting " + self.room_name)


def test_room_code(code):
    # seconds = randint(1, 5)
    seconds = 5
    try:
        jackbox_url = base_url + str(code)
        r = requests.get(url=jackbox_url)
        data = r.json()
        print(str(data))
    except Exception as e:
        print("Error: " + str(e))
    time.sleep(seconds)


def generate_room_codes(length):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code_list = [''.join(i) for i in product(chars, repeat=length)]
    return code_list


def main():
    threads = []
    code_list = generate_room_codes(4)
    # for code in code_list[:10]:
    #     rm_thread = roomThread(code, str(code))
    #     threads.append(rm_thread)
    #     rm_thread.start()
    #
    # while len(threads) > 0:
    #     try:
    #         threads = [t.join(1) for t in threads if t is not None and t.isAlive()]
    #     except KeyboardInterrupt:
    #         for t in threads:
    #             t.kill_received = True

    for code in code_list:
        seconds = randint(1, 20)
        test_room_code(code)
        time.sleep(seconds)


if __name__ == "__main__":
    main()
