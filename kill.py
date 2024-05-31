import os
import signal
import psutil

def find_pids_by_name(process_name):
    current_pid = os.getpid()
    bootstrap_pid = psutil.Process(current_pid).parent().pid

    return [proc.info['pid'] for proc in psutil.process_iter(['pid', 'name']) if proc.info['name'] == process_name and proc.info['pid'] != current_pid and proc.info['pid'] != bootstrap_pid]

def kill(process_name):
    pids = find_pids_by_name(process_name)
    for pid in pids:
        try:
            if os.name == 'nt':
                p = psutil.Process(pid)
                p.terminate()
                print(f"Killing '{process_name}' --> PID {pid}")
            else:
                os.kill(pid, signal.SIGTERM)
                print(f"Killing '{process_name}' --> PID {pid}")
        except psutil.NoSuchProcess:
            print(f"Process '{process_name}' with PID {pid} does not exist.")
        except psutil.AccessDenied:
            print(f"Permission denied to kill process '{process_name}' with PID {pid}.")
        except Exception as e:
            print(f"An error occurred: {e}")
