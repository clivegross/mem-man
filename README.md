# mem-man
Python 3 script for managing memory on a Linux based development server. Use as a fallback to automatically kill processes on remote dev servers that are eating memory and killing your connection. For example, [this issue with VS Code Remote SSH](https://github.com/microsoft/vscode/issues/175830)

Start the program by executing:

    python mem-man.py

### Requirements

Ensure `python3` is installed.
Install python module `psutils` for root:

```
sudo pip3 install psutils
```

### Configuration

The program checks if the system memory has exceeded a threshold (%) `MEM_THRESHOLD_PERCENT` is exceeded, then excecutes any commands provided. Set `MEM_THRESHOLD_PERCENT` in `mem-man.py`.

Provide the commands to execute in the `COMMANDS` list in `mem-man.py`, eg:

```
COMMANDS = [
    "pm2 stop all",
    "killall node",
    "pkill -f pm2"
]
```

### Run as a systemd service using systemctl

1. Download this repo into `/usr/local/bin/mem-man` (or wherever you like)
1. Edit `mem-man.service` if required. Configured to run script from `/usr/local/bin/mem-man`
1. Copy the systemd unit file to systemd: `sudo cp mem-man.service /etc/systemd/system/`
1. Then run it with:

```
sudo systemctl start mem-man    # Runs the script now
sudo systemctl enable mem-man   # Sets the script to run every boot
journalctl -u mem-man.service   # Check systemd journal for errors
```

To disable the service:

```
sudo systemctl disable mem-man  # Sets the script to not run
```

To stop the service:

```
sudo systemctl stop mem-man    # Stops the script now
```

To reload the service after changing, eg `MEM_THRESHOLD_PERCENT` adjustment:

```
sudo systemctl stop mem-man
sudo systemctl daemon-reload
sudo systemctl start mem-man
journalctl -u mem-man.service
```

### Troubleshooting

Ensure `psutils` is installed for root (ie `sudo pip3 install psutils`) and not just local user or the systemd service will fail:

```
$ journalctl -u mem-man.service
systemd[1]: Started mem-man.service - Python 3 script for managing memory on a Linux based development server..
python3[11478]: Traceback (most recent call last):
python3[11478]:   File "/usr/local/bin/mem-man/mem-man.py", line 4, in <module>
python3[11478]:     import psutil
python3[11478]: ModuleNotFoundError: No module named 'psutil'
systemd[1]: mem-man.service: Main process exited, code=exited, status=1/FAILURE
systemd[1]: mem-man.service: Failed with result 'exit-code'.
```
