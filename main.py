import requests
import os
from pydub import AudioSegment
import speech_recognition as sr

LIVESTREAM_API_BASE_URL = 'https://api.new.livestream.com'
CHUNK_SIZE = 1024**2

def get_video_download_url(livestream_url_data):
    params = 'secure=true&player=true'
    api_token_url = f'{LIVESTREAM_API_BASE_URL}/{livestream_url_data}/media?{params}'

    response = requests.get(api_token_url).json()
    return response["m3u8"]

def convert_m3u8_to_mp3(file):
    command = ''.join([
        'ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto  -loglevel error -i ', 
        file, ' "', file.replace('.m3u8', '.wav').replace('tmp_',''), '"'])
    print('Running command ' + command)
    os.system(command)
    os.remove(file)

def get_mp3(livestream_url_data):
    video_url = get_video_download_url(livestream_url_data)
    response = requests.get(video_url, stream=True)
    file_name = 'tmp_' + ''.join(video_url.replace('.','-').split('/')[3:7]) + '.wav'
    with open(file_name,'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
                f.flush()

    convert_m3u8_to_mp3(file_name)
    return file_name.replace(".m3u8",".wav").replace('tmp_','')


def get_time_in_ms(formatted_time):
    minutes, seconds = map(int,formatted_time.split(':'))
    return (minutes*60 + seconds) * 1000

def trim_audio(mp3_file, start, end):
    audio = AudioSegment.from_mp3(mp3_file)
    trimmed_audio = audio[start:end]
    trimmed_audio.export(mp3_file, format="wav")



def main():
    livestream_url = input("provide a livestream.com url: ")
    start_trim_time = input("when does the chapel begin(mm:ss): ")
    end_trim_time = input("when does the chapel end(mm:ss): ")

    livestream_url_data = '/'.join(livestream_url.split('/')[3:])
    audio_file_name = get_mp3(livestream_url_data)
    trim_audio(audio_file_name, get_time_in_ms(start_trim_time), get_time_in_ms(end_trim_time))
    recognition_engine = sr.Recognizer()
    with sr.AudioFile('Recording.wav') as source:
        recognition_engine.adjust_for_ambient_noise(source, duration=0)
        audio = recognition_engine.record(source, duration=None,offset=None)
    try:
        print("Google Speech Recognition thinks you said " + recognition_engine.recognize_google(audio_data = audio, language = 'en-US'))
    
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    main()