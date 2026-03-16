import psutil
import subprocess
import os

def is_running(exe_name: str) -> bool:
    for proc in psutil.process_iter(["name"]):
        try:
            if exe_name.lower() in proc.info["name"].lower():
                print(f"[INFO]{exe_name} is already running.")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def run_program(exe_path: str):
    try:
        subprocess.Popen([exe_path])
        print(f"[INFO]{exe_path} has been executed.")
    except Exception as e:
        raise e


def delete_file(file_path_str: str):
    try:
        os.remove(file_path_str)
        print(f"[INFO]{file_path_str} has been removed successfully.")
    except Exception as e:
        print(f"[Error]{file_path_str} could not be deleted.")



def __main__():
    PROGRAM_NAME: str = "VOICEVOX.exe"

    if not is_running(PROGRAM_NAME):
        run_program("C:\\Users\\Owner\\AppData\\Local\\Programs\\VOICEVOX\\VOICEVOX.exe")


if __name__ == "__main__":
    __main__()