#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from app import app
from models import db, Message

fake = Faker()

usernames = [fake.first_name() for i in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")

def make_messages():
    print("Deleting old data...")
    Message.query.delete()

    print("Creating new messages...") 
    messages = [
        Message(
            body=fake.sentence(),
            username=rc(usernames),
        )
        for _ in range(20)
    ]

    db.session.add_all(messages)
    db.session.commit()
    print(f"Added {len(messages)} messages.")      

if __name__ == '__main__':
    with app.app_context():
        make_messages()
