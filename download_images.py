import argparse
from pathlib import Path
import logging
import urllib
from urllib.error import HTTPError
import logging

# from urllib import request
import requests
import json
import peewee as pw
import datetime
import time
from tqdm import tqdm

from image import Image

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', default='out', type=str)
parser.add_argument('--interval', '-i', default=10, type=int)
parser.add_argument('--logfile', '-l', default='download.log', type=str)
args = parser.parse_args()


output_dir = Path(args.output)
images_dir = output_dir / 'images'
log_path = output_dir / args.logfile

logging.basicConfig(filename=str(log_path), level=logging.WARNING, format='%(asctime)s\n%(message)s')


if __name__ == '__main__':

    images_dir.mkdir(parents=True, exist_ok=True)

    images = Image.select().where(Image.category_id == 8).where(Image.is_downloaded == False)

    print('count:', images.count())

    for image in tqdm(images):

        filename = str(image.identity) + '.jpg'

        try:
            filename, header = urllib.request.urlretrieve(image.image_url, filename=str(images_dir / filename))
        except HTTPError as e:
            logging.warning(str(e.code) + ':' + e.reason + '\n' + image.image_url)
            continue
        except Exception as e:
            logging.warning(str(e))
            continue

        image.is_downloaded = True
        image.image_filename = filename
        image.save()

        time.sleep(args.interval)
