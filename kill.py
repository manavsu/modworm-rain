import os
import signal
import psutil
import platform

process_name = 'modworm'

def find_pid_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

# Signal name as a string (for Unix-like systems)
signal_name = 'SIGKILL'

# Find the PID
pid = find_pid_by_name(process_name)

if pid:
    try:
        if platform.system() == 'Windows':
            # Windows specific process termination
            p = psutil.Process(pid)
            p.terminate()  # or p.kill() for forceful termination
            print(f"Successfully terminated process '{process_name}' (PID: {pid}) on Windows")
        else:
            # Unix-like system signal sending
            signal_number = getattr(signal, signal_name)
            os.kill(pid, signal_number)
            print(f"Successfully sent {signal_name} to process '{process_name}' (PID: {pid})")
    except psutil.NoSuchProcess:
        print(f"Process '{process_name}' with PID {pid} does not exist.")
    except psutil.AccessDenied:
        print(f"Permission denied to kill process '{process_name}' with PID {pid}.")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print(f"No process named '{process_name}' found.")
