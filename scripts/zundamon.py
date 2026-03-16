from scripts import file_utils, audio_utils
import requests
import uuid
import traceback
from pathlib import Path


def open_voicevox(voicevox_exe_path: str):
    try:
        exe_file_name: str = Path(voicevox_exe_path).name
        is_voicevox_open: bool = file_utils.is_running(exe_file_name)
        if not is_voicevox_open:
            file_utils.run_program(voicevox_exe_path)
    except Exception as e:
        raise e
    

def modify_text(text: str, ng_words: list):
    # Limit text length to 80 characters for safety
    # Add suffix "(以下略" in case any text is cut off
    if len(text) > 80:
        text = text[:80] + "(以下略"
    # Replace NG words with "ホニャララ"
    for word in ng_words:
        text = text.replace(word, "ホニャララ")
    
    return text
    

def speak_zundamon_blocking(text: str, voicevox_url: str, 
                            speaker_id: int, ng_words: list):
    text_mod = modify_text(text, ng_words)

    try:
        # Create audio query
        audio_query_req = requests.post(
            f"{voicevox_url}/audio_query", 
            params={"text": text_mod, "speaker": speaker_id},
            timeout=10
            )
        audio_query_req.raise_for_status()
        query = audio_query_req.json()
        
        # Synthesize audio
        audio_req = requests.post(
            f"{voicevox_url}/synthesis",
            params={"speaker": speaker_id},
            json=query,
            timeout=30
            )
        audio_req.raise_for_status()
        
        # Save audio to file and play
        wav_path_str = f"_generated/output_{uuid.uuid4().hex}.wav"
        wav_path = Path(wav_path_str)
        wav_path.write_bytes(audio_req.content)
        
        audio_utils.play_wav(wav_path_str)
    except Exception as e:
        print("[VOICEVOX ERROR]", repr(e))
        traceback.print_exc()




def __main__():
    import file_utils, audio_utils

    speak_zundamon_blocking("Zundamon.py内部からのテストなのだ", "http://127.0.0.1:50021", 3, ["shit"])


if __name__ == "__main__":
    __main__()