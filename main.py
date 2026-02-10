import json, pyaudio, struct, os, wave
from vosk import Model, KaldiRecognizer
import pvporcupine
from piper import PiperVoice
from tts import PiperTTS
from llm import Llm
from functions import Functions

tts = PiperTTS()
llm = Llm()
f = Functions()

voice = PiperVoice.load("Piper/ru_RU-irina-medium.onnx")

handle = pvporcupine.create(
  access_key='Glmpe54BqlaSmAxo4poGyCAN3nr35DxFmaptKSjsa/tS+D6quTaefg==',
  keyword_paths=['Porcupine\ミワア_ja_windows_v4_0_0.ppn'],
  model_path='Porcupine\porcupine_params_ja.pv'
)

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer = handle.frame_length)

modelVosk = Model('Vosk/RusSmallModel')
rec = KaldiRecognizer(modelVosk,16000)
stream.start_stream()

def terminate():
    handle.delete()
    stream.stop_stream()
    stream.close()
    audio.terminate()
    quit()

def listen():
    while True:
        data = stream.read(8000,exception_on_overflow=False)
        if(rec.AcceptWaveform(data)and len(data) >0):
            answer = json.loads(rec.Result())
            if(answer['text']):
                yield answer['text']

def speak(text):
    with wave.open("tts.wav", "wb") as f:
        voice.synthesize(text, f)
    

print('started')
while True:
    pcm = stream.read(handle.frame_length, exception_on_overflow=False)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)
    keyword_index = handle.process(pcm)
    if keyword_index >= 0:
        print('detected')
        for text in listen():
            print("Ты: " + text)

            if(text == 'пока ассистент'):
                terminate()
            
            answer = llm.ask_llm(text)
            print("Ассистент: ", answer)

            command = f.CheckForCommand(answer)
            if(command != None):
                print("Результат команды: ", command)
                answer = llm.ask_llm("Результат команды: " + command)
                print("Ассистент: ", answer)

            tts.say(answer, pitch=1.3,speed=1)
            break
        pass