import argparse
import csv
import datetime
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product

import requests

base_url = "https://blobcast.jackboxgames.com/room/"
csv_writer_lock = threading.Lock()


def test_room_code(code, csv_file=None):
    try:
        jackbox_url = base_url + str(code)
        r = requests.get(url=jackbox_url)
        data = r.json()
        if r.status_code == 200:
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
                           'joinAs'] + ',' + str(locked) + ',' + str(
                datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')) + ','
        else:
            room_row = str(code) + ',,,,,,,,' + str(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')) + ','

        if csv_file:
            with csv_writer_lock:
                with open(csv_file, 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([str(room_row)])
        else:
            print(room_row)
            return room_row

    except Exception as e:
        print("Error: " + str(e))


def generate_room_codes(length):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code_list = [''.join(i) for i in product(chars, repeat=length)]
    return code_list


def create_csv(filename):
    header = ['RoomId', 'Server', 'Game', 'AppID', 'NumPlayers', 'NumAudience', 'JoinAs', 'Locked', 'Last_Checked']
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
    csv_file.close()


def main():
    st = time.time()
    parser = argparse.ArgumentParser(description='Checks if there are any available room in Jackbox.Tv')
    parser.add_argument('-c', '--csv', help='Output CSV file', required=False)
    parser.add_argument('-r', '--room', help='Room Code', required=False)

    args = vars(parser.parse_args())
    csv_filename = args['csv']
    room_code = args['room']
    code_list = generate_room_codes(4)

    if csv_filename:
        create_csv(csv_filename)

    if room_code:
        room_status = test_room_code(room_code, csv_filename)
        print(room_status)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(test_room_code, code, csv_filename) for code in code_list]
        try:
            for future in as_completed(futures):
                future.result()
        except KeyboardInterrupt as e:
            raise
            # executor._threads.clear()
            # thread._threads_queues.clear()

    print("total time: %s" % (time.time() - st))


if __name__ == "__main__":
    main()
