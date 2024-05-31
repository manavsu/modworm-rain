import os
import signal
import psutil

def find_pids_by_name(process_name):
    this_pid = os.getpid()
    return [proc.info['pid'] for proc in psutil.process_iter(['pid', 'name']) if proc.info['name'] == process_name and proc.info['pid'] != this_pid]

def kill(process_name):
    print(os.getpid())
    pids = find_pids_by_name(process_name)
    for pid in pids:
        try:
            if os.name == 'nt':
                p = psutil.Process(pid)
                p.terminate()
                print(f"Killed '{process_name}' --> PID {pid}")
            else:
                os.kill(pid, signal.SIGTERM)
                print(f"Killed '{process_name}' --> PID {pid}")
        except psutil.NoSuchProcess:
            print(f"Process '{process_name}' with PID {pid} does not exist.")
        except psutil.AccessDenied:
            print(f"Permission denied to kill process '{process_name}' with PID {pid}.")
        except Exception as e:
            print(f"An error occurred: {e}")
