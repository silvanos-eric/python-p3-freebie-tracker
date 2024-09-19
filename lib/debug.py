#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # 1. Freebie.company - return the Company instance for a Freebie object
    freebie = session.query(Freebie).first()
    print('1. Company name for the first freebie:', freebie.company)

    # 2. Company.freebies - returns a collection of all freebies for the company
    company = session.query(Company).first()
    print('2. Collection of all freebies for first company', company.freebies)

    session.close()
    import ipdb
    ipdb.set_trace()
