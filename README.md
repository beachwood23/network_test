# network_test
A simple tool to ping a remote server for a period of time, and generate a graph of the connection times. It uses your computer's built-in `ping` tool.

## Requirements
- `ping`
- Python 3.9+
- installing all `Python` dependencies with `python3 -m pip install -r requirements.txt`.

## Usage
```
$ python network_test.py -h
usage: network_test.py [-h] -d DURATION -n NAME -t TARGET [--nochart NOCHART]

Creates charts from output of network pings.

options:
  -h, --help            show this help message and exit
  -d DURATION, --duration DURATION
                        The duration, in seconds, to run the network test for.
  -n NAME, --name NAME  The name of this host running the network test.
  -t TARGET, --target TARGET
                        The target host of the ping connections. Either IP or FQDN.
  --nochart NOCHART     If this flag is set, no chart will be generated.
```

Example:
```
python network_test.py -d 60 -n my-mac -t www.github.com 
```
