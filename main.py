import os
import subprocess
import time

def run_command_no_console(command, **kwargs):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.run(command, startupinfo=startupinfo, **kwargs)

def is_wsl_running(timeout=5):
    try:
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            wsl_check = run_command_no_console(['wsl.exe', '--list', '--running'], text=True, capture_output=True, timeout=timeout)
            if "No running instances" not in wsl_check.stdout:
                return True
            time.sleep(1)
        return False
    except subprocess.TimeoutExpired:
        print(f"Timeout of {timeout} seconds reached.")
        return False

def restart_wsl():
    run_command_no_console(['wsl.exe', '--terminate'])
    run_command_no_console(['wsl.exe'])
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
