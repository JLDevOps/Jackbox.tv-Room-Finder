# Jackbox.TV Room Finder

*Never Play Jackbox Games Alone.*

This script will find all the available rooms that are online on Jackbox.TV.

This script can also output a list of the rooms and their corresponding statuses via a csv.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. 

### Installations

The following steps go through installing Python dependencies.
1. Install the Python modules for this tool
    ```
    $ pip install -r requirements.txt
    ```

### Usage

#### Using the Script via Terminal/Command Line
You can also run the room_finder.py file by itself, and provide arguments to what functionality you would like to use.

```bash
    $ python room_finder.py -c {_csv_filename__} -r {___room_code__}
```

Command Line / Terminal Arguments:
- -c (CSV Filename (ex. test.csv))
- -r (room code (ex. AAAA))


** You can also run the script without arguments, which will output via cmdline/terminal the list of room codes and their status

Sample command without arguments: 
```
    $ python room_finder.py
```

Sample command to find only one room's availability: 
```
    $ python room_finder.py -r AALJ
```

Sample command to output the room/status to a csv:
```
    $ python room_finder.py -c test.csv
```

Here is a sample output:
    ```
    {'roomid': 'AALJ', 'apptag': 'bombintern', 'appid': 'CCJhi8No2mKeADbC474Zn81Vstm7WyBP', 'nu
     mPlayers': 2, 'numAudience': 0, 'joinAs': 'full', 'locked': True}
    ```
    
## Built With

* Python 3.6

## Authors

* **Jimmy Le** - [Jldevops](https://github.com/jldevops)


## License

Licensed under the [MIT License](LICENSE)

