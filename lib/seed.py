#!/usr/bin/env python3

# This is a script to generate some fake swag data to be used in the
# freebies database.

# We import Faker, a Python package that generates fake data.
from faker import Faker

# We import random to generate random numbers.
import random

# We import the required classes from sqlalchemy.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# We import the Freebie class from the models module.
from models import Freebie

if __name__ == '__main__':
    # We create an engine object that represents the core interface to
    # the database.
    engine = create_engine('sqlite:///freebies.db')

    # We create a sessionmaker object that creates new Session objects
    # bound to the engine object.
    Session = sessionmaker(bind=engine)

    # We create a new session object from the sessionmaker.
    session = Session()

    # We delete all the freebies in the database.
    session.query(Freebie).delete()

    # We create a fake object that can be used to generate fake data.
    fake = Faker()

    # We create a list of swag items that we can randomly select from.
    swag_items = [
        "T-shirt", "Hoodie", "Sticker", "Notebook", "Pen", "USB Drive",
        "Water Bottle", "Keychain", "Mouse Pad", "Lanyard", "Tote Bag",
        "Sunglass", "Stress Ball", "Phone Stand", "Charging Cable",
        "Power Bank", "Laptop Sleeve", "Coffee Mug", "Earbud", "Hat",
        "Wristband", "Post-it Note", "Screen Cleaner", "Bottle Opener",
        "Phone Grip", "Badge", "Button", "Puzzle", "Flashlight", "Umbrella"
    ]

    # We create a list to hold all the freebie objects that we create.
    freebies = []

    # We loop 30 times to create 30 freebie objects.
    for _ in range(30):
        # We create a new freebie object with a random swag item and a
        # value between 1 and 3000.
        freebie = Freebie(item_name=random.choice(swag_items),
                          value=random.randint(1, 3000))
        # We append the freebie object to the list of freebies.
        freebies.append(freebie)

    # We add the freebies to the session.
    session.bulk_save_objects(freebies)

    # We commit the session.
    session.commit()

    # We close the session.
    session.close()
