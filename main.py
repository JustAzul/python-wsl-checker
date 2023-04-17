import logging
import subprocess
import time

logging.basicConfig(level=logging.INFO)

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
        logging.warning(f"Timeout of {timeout} seconds reached.")
        return False

def restart_wsl(retries=3):
    for attempt in range(retries):
        logging.info(f"Attempt {attempt + 1} to terminate WSL...")
        terminate_result = run_command_no_console(['wsl.exe', '--terminate'], capture_output=True, text=True)
        
        if terminate_result.returncode != 0:
            logging.error(f"Error terminating WSL: {terminate_result.stderr}")
            time.sleep(2)
            continue

        logging.info("WSL terminated. Starting WSL...")
        start_result = run_command_no_console(['wsl.exe'], capture_output=True, text=True)

        if start_result.returncode != 0:
            logging.error(f"Error starting WSL: {start_result.stderr}")
            time.sleep(2)
            continue

        logging.info("WSL restarted successfully.")
        return

    logging.error("Failed to restart WSL after multiple attempts.")

def main():
    timeout = 10  # Adjust this value as needed
    if not is_wsl_running(timeout):
        logging.warning("WSL not running. Restarting...")
        restart_wsl()
    else:
        logging.info("WSL is running.")

if __name__ == "__main__":
    main()
