import soundfile as sf
import sounddevice as sd
from pathlib import Path


def play_wav(wav_path_str: str):
    data, samplerate = sf.read(wav_path_str, dtype="float32")
    sd.play(data, samplerate)
    sd.wait()


def __main__():
    script_path = Path(__file__).resolve()
    parent_directory = script_path.parent.parent
    config_file_path = parent_directory / "resources/zundamon_test.wav"
    config_path_str = str(config_file_path)

    play_wav(config_path_str)


if __name__=="__main__":
    __main__()