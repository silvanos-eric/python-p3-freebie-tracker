#!/usr/bin/env python3

# This is a script to generate some fake swag data to be used in the
# freebies database.

# We import Faker, a Python package that generates fake data.
from faker import Faker
from datetime import datetime

# We import random to generate random numbers.
import random

# We import the required classes from sqlalchemy.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# We import the model classes from the models module.
from models import Freebie, Company, Dev

if __name__ == '__main__':
    # Create an engine object that represents the core interface to
    # the database.
    engine = create_engine('sqlite:///freebies.db')

    # Create a sessionmaker object that creates new Session objects
    # bound to the engine object.
    Session = sessionmaker(bind=engine)

    # Create a new session object from the sessionmaker.
    session = Session()

    # Delete all the freebies in the database.
    session.query(Freebie).delete()
    session.query(Company).delete()
    session.query(Dev).delete()

    # Create a fake object that can be used to generate fake data.
    fake = Faker()

    # Create a list to hold all the dev objects that we create
    devs = []

    # Create 5 devs
    for _ in range(5):
        # Create a dev object
        dev = Dev(name=fake.unique.name())

        # Add the dev object to the devs list
        devs.append(dev)

    # Add the devs to the session at once
    session.bulk_save_objects(devs)

    # Create a list to hold all the Company objects that we create
    companies = []

    # Define the range for a random year
    start_date = datetime.strptime('1860-01-01', "%Y-%m-%d")
    end_date = datetime.now()

    for _ in range(5):
        # Generate a random date
        random_date = fake.date_between(start_date=start_date,
                                        end_date=end_date)
        company = Company(name=fake.unique.name(), founding_year=random_date)
        companies.append(company)

        # Add and commit individually to get IDs back
        session.add(company)
        session.commit()

        companies.append(company)

    # Create a list to hold all the Freebie objects that we create.
    freebies = []

    # Create a list of swag items that we can randomly select from.
    swag_items = [
        "T-shirt", "Hoodie", "Sticker", "Notebook", "Pen", "USB Drive",
        "Water Bottle", "Keychain", "Mouse Pad", "Lanyard", "Tote Bag",
        "Sunglass", "Stress Ball", "Phone Stand", "Charging Cable",
        "Power Bank", "Laptop Sleeve", "Coffee Mug", "Earbud", "Hat",
        "Wristband", "Post-it Note", "Screen Cleaner", "Bottle Opener",
        "Phone Grip", "Badge", "Button", "Puzzle", "Flashlight", "Umbrella"
    ]

    # Loop 30 times to create 30 freebie objects.
    for _ in range(30):
        # Create a new freebie object with a random swag item and a
        # value between 1 and 3000, and a random company id.
        freebie = Freebie(item_name=random.choice(swag_items),
                          value=random.randint(1, 3000),
                          company_id=random.randint(1, len(companies)))
        # Append the freebie object to the list of freebies.
        freebies.append(freebie)

    # Add the freebies to the session.
    session.bulk_save_objects(freebies)

    # Commit the session.
    session.commit()

    # Close the session.
    session.close()
