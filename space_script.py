import os.path
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, unquote
import requests
from dotenv import load_dotenv

Path(f'{Path.cwd()}\images').mkdir(parents=True, exist_ok=True)
load_dotenv()


def download_image(image_url, filename):
    response = requests.get(image_url)
    response.raise_for_status()

    with open(f'images/{filename}', 'wb') as file:
        file.write(response.content)


filename = "hubble.jpeg"
url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
download_image(url, filename)


def fetch_spacex_last_launch(launch_id):
    launch_url = f'https://api.spacexdata.com/v3/launches/{launch_id}'
    response = requests.get(url=launch_url)
    response.raise_for_status()
    launch_images = response.json()['links']['flickr_images']
    for image_number, image_url in enumerate(launch_images, start=0):
        download_image(image_url, f'spacex_{image_number}.jpeg')


def fetch_nasa_apod(images_to_download):
    apod_url = "https://api.nasa.gov/planetary/apod"
    params = {'api_key': os.environ.get('API_KEY'), 'count': images_to_download}
    response = requests.get(url=apod_url, params=params)
    response.raise_for_status()
    for apod in response.json():
        download_image(apod['url'], get_file_name(apod['url']))


def get_file_name(random_url):
    parsed_url = urlparse(random_url)
    unquoted = unquote(parsed_url.path)
    path, downloaded_filename = os.path.split(unquoted)
    return downloaded_filename


def fetch_nasa_epic(date):
    endpoint = f'https://api.nasa.gov/EPIC/api/natural/date/{date}'
    params = {'api_key': os.environ.get('API_KEY')}
    response = requests.get(url=endpoint, params=params)
    for photo in response.json():
        photo_date = datetime.strptime(photo['date'], '%Y-%m-%d %H:%M:%S')
        photo_name = photo['image']
        photo_url = f'https://api.nasa.gov/EPIC/archive/natural/' \
                    f'{photo_date.year}/{photo_date.month}/{photo_date.day}/png/{photo_name}.png'
        download_image(photo_url, f'{photo_name}.png')

