import requests
LIVESTREAM_API_BASE_URL = 'https://api.new.livestream.com'
CHUNK_SIZE = 1024**2

def get_video_download_url(livestream_url_data):
    params = 'secure=true&player=true'
    api_token_url = f'{LIVESTREAM_API_BASE_URL}/{livestream_url_data}/media?{params}'

    response = requests.get(api_token_url).json()
    return response["m3u8"]

def get_video(livestream_url_data):
    video_url = get_video_download_url(livestream_url_data)
    response = requests.get(video_url, stream=True)
    file_name = ''.join(video_url.replace('.','-').split('/')[3:7]) + 'secure.mp3'
    print(file_name)
    with open(file_name,'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
                f.flush()
    return response.status_code


def main():
    livestream_url = input("provide a livestream.com url: ")
    livestream_url_data = '/'.join(livestream_url.split('/')[3:])
    get_video(livestream_url_data)


if __name__ == "__main__":
    main()