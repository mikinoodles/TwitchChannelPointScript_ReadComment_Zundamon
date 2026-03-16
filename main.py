import os
import queue
import threading
from pathlib import Path
import time
from scripts import config, zundamon, twitch_web_socket


config_dict: dict = config.get_config_as_dict()
ng_word_list: list = config.get_ng_word_list()

tts_queue = queue.Queue()

stop_event = threading.Event()



def tts_worker(stop_event: threading.Event):
    while not stop_event.is_set():
        try:
            text = tts_queue.get(timeout=0.5)
        except queue.Empty:
            continue

        try:
            print("[TTS] speaking: ", text)
            zundamon.speak_zundamon_blocking(text, 
                                             config_dict["voicevox_settings"]["voicevox_url"],
                                             config_dict["voicevox_settings"]["zundamon_id"], 
                                             ng_word_list)
            print("[TTS] done: ", text)
        except Exception as e:
            print("[TTS ERROR] ", e)
        finally:
            tts_queue.task_done()
    
    print("[TTS WORKDER] Exiting.")


def remove_generated_wav_files():
    wav_audio_folder_str: str = "./_generated"

    for item in os.listdir(wav_audio_folder_str):
        full_path: str = os.path.join(wav_audio_folder_str, item)
        if os.path.isfile(full_path):
            try:
                os.remove(full_path)
                print(f"[INFO] {full_path} has been removed successfully.")
            except Exception as e:
                print(f"[ERROR] {full_path} could not be deleted: {str(e)}")





def __main__():
    zundamon.open_voicevox(config_dict["voicevox_settings"]["voicevox_path"])

    worker = threading.Thread(target=tts_worker, args=(stop_event,), daemon=False)
    worker.start()

    try:
        while not stop_event.is_set():
            twitch_web_socket.create_connection(config_dict["twitch_settings"]["client_id"],
                                                config_dict["twitch_settings"]["user_access_token"],
                                                config_dict["twitch_settings"]["broadcaster_user_id"],
                                                config_dict["twitch_settings"]["reward_id"],
                                                tts_queue)
    except KeyboardInterrupt as e:
        print("[INFO] Keyboard interruption detected.")
        stop_event.set()

    except Exception as e:
        print("[MAIN ERROR]", e)
        print("Retrying in 3sec...")
        time.sleep(3)
    
    finally:
        print("[INFO] Shutting down worker thread...")
        stop_event.set()

        worker.join(timeout=5)

        if config_dict["delete_wavs_on_program_complete"]:
            print("[INFO] Deleting all generated wav files per config settings.")
            remove_generated_wav_files()
        
        print("[INFO] Main process finished.")


if __name__ == "__main__":
    __main__()