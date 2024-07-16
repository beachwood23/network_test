# ping-chart.py
A simple tool to ping a remote server for a period of time, and generate a graph of the connection times. It uses your computer's built-in `ping` tool.

## Requirements
- `ping`
- Python 3.9+
- installing all `Python` dependencies with `python3 -m pip install -r requirements.txt`.

## Usage
First, download script and install dependencies:
```
git clone https://github.com/beachwood23/ping-chart.git
python3 -m pip install -r requirements.txt
```

Then, you can do:
```
$ python3 ping_chart.py -h
usage: ping_chart.py [-h] -d DURATION -n NAME -t TARGET [--nochart NOCHART]

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
python ping_chart.py -d 60 -n my-mac -t www.github.com 
```
We then see a progress bar during the test:

![Progress](https://github.com/beachwood23/ping-chart/blob/main/screenshots/progress.png?raw=true)

Then, after the test has completed, we will see a full chart:

![Chart](https://github.com/beachwood23/ping-chart/blob/main/screenshots/chart.png?raw=true)

