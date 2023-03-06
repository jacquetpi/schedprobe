# schedprobe

Expose scheduler stats (as delta) in a csv format

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements
```

## Usage

```bash
source venv/bin/activate
python3 schedprobe.py --name={hostname} --delay={delay_in_ms} --output={output}
```

A notebook is present for example purposes

## Background usage

```bash
loginctl enable-linger pierre
mkdir -p ~/.config/systemd/user
vmname="vmname"
delay="60000"
output="schedstat"
location=$( pwd )
cat misc/schedprobe.service | sed "s/#location#/$location/g" | sed "s/#vmname#/$vmname/g" | sed "s/#delay#/$delay/g" | sed "s/#output#/$output/g" >> ~/.config/systemd/user/schedprobe.service
systemctl --user daemon-reload
systemctl --user start schedprobe
systemctl --user status schedprobe
sleep {duration}
systemctl --user stop schedprobe
```