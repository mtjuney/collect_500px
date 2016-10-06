import argparse
from pathlib import Path
import logging

# from urllib import request
import requests
import json
import peewee as pw
import datetime
import time
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', default='out', type=str)
parser.add_argument('--keys', '-k', default='keys.json', type=str)
parser.add_argument('--interval', '-i', default=10, type=int)
parser.add_argument('--logfile', '-l', default='default.log', type=str)
args = parser.parse_args()


output_dir = Path(args.output)
db_path = output_dir / 'metadata.db'
images_dir = output_dir / 'images'
log_path = output_dir / args.logfile
keys = json.load(Path(args.keys).open())

logging.basicConfig(filename=str(log_path), level=logging.DEBUG, format='%(asctime)s\n%(message)s')


# url_api = 'https://api.500px.com/v1/photos'
# params_ = {
#     'feature': 'created_at',
#     'consumer_key': keys['ckey'],
#     'rpp': 100
# }

url_api = 'https://api.500px.com/v1/photos/search'







class Image(pw.Model):
    identity = pw.IntegerField(primary_key=True)
    image_url = pw.TextField()
    rating = pw.FloatField()
    user_id = pw.TextField()
    times_viewed = pw.IntegerField()
    category_id = pw.IntegerField(null=True)
    taken_at = pw.DateField(null=True)
    width = pw.IntegerField()
    height = pw.IntegerField()
    votes_count = pw.IntegerField()
    favorites_count = pw.IntegerField()
    comments_count = pw.IntegerField()
    sales_count = pw.IntegerField()
    collections_count = pw.IntegerField()
    positive_votes_count = pw.IntegerField()
    image_format = pw.TextField(null=True)
    iso = pw.TextField(null=True)
    lens = pw.TextField(null=True)
    location = pw.TextField(null=True)
    country = pw.TextField(null=True)
    shutter_speed = pw.TextField(null=True)
    camera = pw.TextField(null=True)
    aperture = pw.TextField(null=True)
    created_at = pw.DateField()
    is_downloaded = pw.BooleanField(default=False)
    image_filename = pw.TextField(null=True)
    timestamp = pw.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = pw.SqliteDatabase(str(db_path))


def insert_photo(photo):
    created_at = photo['created_at']
    if created_at is not None:
        created_at = created_at.split('T')[0].split('-')
        created_at = list(map(int, created_at))
        created_at = datetime.date(created_at[0], created_at[1], created_at[2])

    taken_at = photo['taken_at']
    if taken_at is not None:
        try:
            taken_at = taken_at.split('T')[0].split('-')
            taken_at = list(map(int, taken_at))
            taken_at = datetime.date(taken_at[0], taken_at[1], taken_at[2])
        except:
            taken_at = None

    country = None
    try:
        country = photo['location_details']['country'][0]
    except:
        country = None


    image, is_created = Image.create_or_get(
        identity=photo['id'],
        image_url=photo['image_url'],
        rating=photo['rating'],
        user_id=photo['user']['id'],
        times_viewed=photo['times_viewed'],
        category_id=photo['category'],
        width=photo['width'],
        height=photo['height'],
        votes_count=photo['votes_count'],
        favorites_count=photo['favorites_count'],
        comments_count=photo['comments_count'],
        sales_count=photo['sales_count'],
        collections_count=photo['collections_count'],
        positive_votes_count=photo['positive_votes_count'],
        image_format=photo['image_format'],
        iso=photo['iso'],
        lens=photo['lens'],
        location=photo['location'],
        country=country,
        shutter_speed=photo['shutter_speed'],
        camera=photo['camera'],
        aperture=photo['aperture'],
        taken_at=taken_at,
        created_at=created_at
    )

    if not is_created:
        image = Image(
            identity=photo['id'],
            image_url=photo['image_url'],
            rating=photo['rating'],
            user_id=photo['user']['id'],
            times_viewed=photo['times_viewed'],
            category_id=photo['category'],
            width=photo['width'],
            height=photo['height'],
            votes_count=photo['votes_count'],
            favorites_count=photo['favorites_count'],
            comments_count=photo['comments_count'],
            sales_count=photo['sales_count'],
            collections_count=photo['collections_count'],
            positive_votes_count=photo['positive_votes_count'],
            image_format=photo['image_format'],
            iso=photo['iso'],
            lens=photo['lens'],
            location=photo['location'],
            country=photo['location_details']['country'][0] if len(photo['location_details']['country'])>0 else None,
            shutter_speed=photo['shutter_speed'],
            camera=photo['camera'],
            aperture=photo['aperture'],
            taken_at=taken_at,
            created_at=created_at
        )
        image.save()

    return is_created


if __name__ == '__main__':

    output_dir.mkdir(parents=True, exist_ok=True)

    if not db_path.is_file():
        Image.create_table()

    params_ = {
        'geo': '36.1158,140.1179,10000km',
        'consumer_key': keys['ckey'],
        'sort': 'created_at',
        'rpp':100
    }

    r = requests.get(url_api, params=params_)
    print(r.url)
    data = json.loads(r.text)

    total_items = data['total_items']
    total_pages = data['total_pages']

    for page in tqdm(range(total_pages)):

        params = params_.copy()
        params['page'] = page

        r = requests.get(url_api, params=params)
        data = json.loads(r.text)
        try:
            photos = data['photos']
        except Exception as e:
            logging.warning(str(e) + '\n' + str(data))
            continue

        for photo in photos:
            insert_photo(photo)

        time.sleep(args.interval)
