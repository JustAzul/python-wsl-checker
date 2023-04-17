import os
import subprocess
import time

def is_wsl_running(timeout=5):
    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            wsl_check = subprocess.run(['wsl.exe', '--list', '--running'], capture_output=True, text=True, timeout=timeout)
            if "No running instances" not in wsl_check.stdout:
                return True
            time.sleep(1)
        return False
    except subprocess.TimeoutExpired:
        print(f"Timeout of {timeout} seconds reached.")
        return False

def restart_wsl():
    subprocess.run(['wsl.exe', '--terminate'], capture_output=True)
    subprocess.run(['wsl.exe'], capture_output=True)
    print("WSL restarted.")

def main():
    timeout = 10  # Adjust this value as needed
    if not is_wsl_running(timeout):
        print("WSL not running. Restarting...")
        restart_wsl()
    else:
        print("WSL is running.")

if __name__ == "__main__":
    main()
