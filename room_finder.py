import requests
import json
from itertools import product
from concurrent.futures import ThreadPoolExecutor, as_completed, thread
import time
import threading
import argparse
import csv
import signal
from multiprocessing import Pool

base_url = "https://blobcast.jackboxgames.com/room/"
exitFlag = 0
csv_writer_lock = threading.Lock()


def initializer():
    signal.signal(SIGINT, SIG_IGN)


pool = Pool(initializer=initializer)


def test_room_code(code, csv_file):
    try:
        jackbox_url = base_url + str(code)
        r = requests.get(url=jackbox_url)
        data = r.json()
        if r.status_code != 404:
            print(data)
            try:
                server = data['server']
            except Exception as e:
                server = ''

            try:
                locked = data['locked']
            except Exception as e:
                locked = 'False'

            room_row = str(data['roomid']) + ',' + server + ',' + data['apptag'] + ',' + data[
                'appid'] + ',' + str(data['numPlayers']) + ',' + str(data['numAudience']) + ',' + data[
                           'joinAs'] + ',' + str(locked) + ','
            with csv_writer_lock:
                with open(csv_file, 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([str(room_row)])
            return room_row
    except Exception as e:
        print("Error: " + str(e))


def generate_room_codes(length):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code_list = [''.join(i) for i in product(chars, repeat=length)]
    return code_list


def create_csv(filename):
    header = ['RoomId', 'Server', 'Game', 'AppID', 'NumPlayers', 'NumAudience', 'JoinAs', 'Locked']
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
    csv_file.close()


def main():
    st = time.time()
    parser = argparse.ArgumentParser(description='Checks if there are any available room in Jackbox.Tv')
    parser.add_argument('-c', '--csv', help='Output CSV file', required=False)
    args = vars(parser.parse_args())
    csv_filename = args['csv']

    code_list = generate_room_codes(4)

    if csv_filename:
        print("Csv created")
        create_csv(csv_filename)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(test_room_code, code, csv_filename) for code in code_list]
        try:
            for future in as_completed(futures):
                future.result()
        except KeyboardInterrupt as e:
            executor._threads.clear()
            thread._threads_queues.clear()

    print("total time: %s" % (time.time() - st))


if __name__ == "__main__":
    main()
