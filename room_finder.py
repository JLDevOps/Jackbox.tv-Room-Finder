import requests
from itertools import product

base_url = "https://blobcast.jackboxgames.com/room/"
exitFlag = 0

def test_room_code(code):
    try:
        jackbox_url = base_url + str(code)
        r = requests.get(url=jackbox_url)
        data = r.json()
        if r.status_code != 404:
            print(data)
    except Exception as e:
        print("Error: " + str(e))


def generate_room_codes(length):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code_list = [''.join(i) for i in product(chars, repeat=length)]
    return code_list


def main():
    code_list = generate_room_codes(4)
    for code in code_list:
        test_room_code(code)


if __name__ == "__main__":
    main()
