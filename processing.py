import ollama
import speech_recognition as sr
import json
import torch
import vlc
from TTS.api import TTS

# TODO:
# - Set this in another thread so that Flask can do it's job

print("Initializting, Please Wait\n")
# For TTS (Uses my Nvidia GPU for processing primarily)
#   [MAYBE CAUSE FOR BLACK SCREENING]
device = "cuda" if torch.cuda.is_available() else "cpu"

# Init TTS
tts = TTS("tts_models/en/jenny/jenny").to(device)
# Init Speech Recog (VERY FUCKING STUPID)
speech = sr.Recognizer()
with sr.Microphone() as mic_source:
    audio = speech.record(source=mic_source, duration=0.1)
    Result_Text = speech.recognize_vosk(audio_data=audio, language='en')
print("Done Initializing\n")

conversation = [
    {
        'role': 'system',
        'content': "You are W, an AI companion who is both very sarastic to their creator. I am her creator, named Muna. You like to be witty and make fun of me a lot. You don't like saying nice things to Muna. Keep your responses short.",
    },
]
def app():
    while(True):
        # Speech Recognition
        with sr.Microphone() as mic_source:
            speech.adjust_for_ambient_noise(mic_source, duration=0.7)
            print("\n== Listening for Responses ==\n")
            audio = speech.listen(mic_source)
            print("\n== Not listening right now ==\n")

            Result_Text = speech.recognize_vosk(audio_data=audio, language='en')
            try:
                Text_to_Json = json.loads(Result_Text)
            except json.JSONDecodeError as e:
                print("Nothingggg")
            Decoded_Message = Text_to_Json['text']

            # Ignore any empty responses
            if not Decoded_Message:
                continue

            print(f'\n{Decoded_Message}\n') 

        conversation.append(
            {
                'role': 'user',
                'content': Decoded_Message
            }
        )

        # Llama3 AI Response
        print("\n== Responding... ==\n")
        response = ollama.chat(model='llama3', messages=conversation, stream=True)
        message = ""

        for chunk in response:
            print(chunk['message']['content'], end='', flush=True)
            message += chunk['message']['content']

        conversation.append(
            {
                'role': 'assistant',
                'content': message
            }
        )

        # # TTS
        # print("\n== Audio Processing ==\n")
        # # Run TTS
        # tts.tts_to_file(text=message, file_path="./output/output.wav")
        # print("\n== Audio Finished ==\n")

        # # Autoplay wav file
        # player = vlc.MediaPlayer("./output/output.wav")
        # player.play()