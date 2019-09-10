import csv
from .models import db, Talk, User
from datetime import datetime


def load_talks_command(file):
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:

            print(row)
            datetime_object = datetime.strptime(row['talk_dt'], '%Y-%m-%d %H:%M:%S')
            t = Talk(
                id=int(row['id']),
                title=row['title'],
                presenters=row['presenters'],
                description=row['description'],
                location=row['location'],
                talk_dt=datetime_object,
                year=row['year'],
            )
            db.session.merge(t, load=True)
            db.session.commit()


def createsuperuser_command(username, password):
    u = User(username=username)
    u.set_password(password)
    db.session.merge(u, load=True)
    db.session.commit()
