import argparse
from pathlib import Path
import logging
import urllib

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

if __name__ == '__main__':

    images_dir.mkdir(parents=True, exist_ok=True)

    images = Image.select().where(Image.category_id == 8)

    print('count:', images.count())

    for image in images:

        filename = str(image.identity) + '.jpg'

        filename, header = urllib.request.urlretrieve(image.image_url, filename=str(images_dir / filename))

        image.is_downloaded = True
        image.image_filename = filename

        time.sleep(args.interval)
