from piper import PiperVoice
import numpy as np
import sounddevice as sd
from scipy.io import wavfile

class PiperTTS:
    def __init__(self, model_path="Piper/ru_RU-irina-medium.onnx",
                 config_path="Piper/ru_RU-irina-medium.onnx.json"):
        self.voice = PiperVoice.load(model_path, config_path)

    def _change_pitch(self, audio, factor):
        new_length = int(len(audio) / factor)
        x_old = np.linspace(0, 1, len(audio))
        x_new = np.linspace(0, 1, new_length)
        return np.interp(x_new, x_old, audio)
    
    def PlaySound(self, path):
        samplerate, data = wavfile.read(path)
        sd.play(data, samplerate)

    def say(self, text, pitch=1, speed = 1):
        chunks = list(self.voice.synthesize(text))
        if not chunks:
            return
        
        audio = np.concatenate([c.audio_float_array for c in chunks])
        original_sr = chunks[0].sample_rate

        # Изменяем pitch (тон) через изменение скорости с пересэмплированием
        if pitch != 1.0:
            # Для изменения pitch без изменения скорости
            # используем преобразование Фурье (phase vocoder)
            audio = self._change_pitch(audio, pitch)
        
        # Изменяем скорость
        if speed != 1.0:
            # Просто меняем скорость воспроизведения
            new_sr = int(original_sr * speed)
            # Пересэмплируем для изменения скорости
            num_samples = int(len(audio) / speed)
            indices = np.linspace(0, len(audio), num_samples)
            audio = np.interp(indices, np.arange(len(audio)), audio)
            sr = new_sr
        else:
            sr = original_sr
        
        sd.play(audio, sr)
        sd.wait()