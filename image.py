from pathlib import Path
import peewee as pw
import datetime

output_dir = Path('out')
# db_path = output_dir / 'metadata.db'

db_path = output_dir / 'landscape.db'

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


if not db_path.is_file():
    Image.create_table()
