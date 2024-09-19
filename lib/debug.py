#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie, FreebieAlreadyGivenError, FreebieNotMineToGiveError

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # 1. Freebie.company - return the Company instance for a Freebie object
    freebie = session.query(Freebie).first()
    print('1. Freebie.company:', freebie.company)

    # 2. Company.freebies - returns a collection of all freebies for the company
    company = session.query(Company).first()
    print('2. Company.freebies: ', company.freebies)

    # 3. Company.give_freebie - associate a freebie with a dev
    print('3. Company.give_freebie')
    company = session.query(Company).first()
    dev = session.query(Dev).first()
    first_freebie_not_in_company = session.query(Freebie).filter(
        Freebie.id != company.id).first()
    # Test for FreebieNotMineToGiveError
    first_freebie_not_owned_by_company = session.query(Freebie).filter(
        Freebie.company_id != company.id).first()
    try:
        company.give_freebie(dev, first_freebie_not_owned_by_company)
    except FreebieNotMineToGiveError as e:
        print(f"3(b). Test for FreebieNotMineToGiveError passed")
    # Test for give_freebie
    freebie_in_company = company.freebies[0]
    company.give_freebie(dev, freebie_in_company)
    print('3(c). Test for give_freebie {freebie.dev}: ',
          freebie_in_company.dev)

    session.close()
    import ipdb
    ipdb.set_trace()
