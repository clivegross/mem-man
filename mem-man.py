import os
import sys
import time
import psutil

# Set the threshold for memory usage
MEM_THRESHOLD_PERCENT = 94 # %
# Set the frequency of checking memory usage
CHECK_INTERVAL = 60 # seconds
# Set the commands to execute when memory usage exceeds the threshold
COMMANDS = [
    "pkill -f pm2"
]

def get_memory_usage():
    # Get the current memory usage percentage
    return psutil.virtual_memory().percent

while True:
    # Check if memory usage exceeds the threshold
    memory_usage = get_memory_usage()
    if memory_usage > MEM_THRESHOLD_PERCENT:
        print("mem-man: memory usage at %2.1f%% exceeds threshold of %2.1f%%, executing provided commands..." % (memory_usage, MEM_THRESHOLD_PERCENT), file=sys.stderr)
        for command in COMMANDS:
            os.system(command)
    else:
        print("mem-man: memory usage at %2.1f%% does not exceed threshold of %2.1f%%, nothing to do." % (memory_usage, MEM_THRESHOLD_PERCENT), file=sys.stderr)
    time.sleep(CHECK_INTERVAL)

