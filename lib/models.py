from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

engine = create_engine('sqlite:///freebies.db')
Base = declarative_base(metadata=metadata)
Session = sessionmaker(bind=engine)
session = Session()

companies_devs = Table('companies_devs',
                       Base.metadata,
                       Column('company_id',
                              ForeignKey('companies.id'),
                              primary_key=True),
                       Column('dev_id',
                              ForeignKey('devs.id'),
                              primary_key=True),
                       extend_existing=True)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # Python mapping of relationships
    freebies = relationship('Freebie', backref="company")
    devs = relationship('Dev',
                        secondary=companies_devs,
                        back_populates='companies')

    def __repr__(self):
        """Return a string representation of Company object."""
        return f'<Company {self.name}>'

    @classmethod
    def oldest_company(cls):
        """Return the oldest company in the database."""
        return session.query(cls).order_by(cls.founding_year).first()

    def give_freebie(self, dev, freebie):
        """Associates the freebie with the dev."""
        if not isinstance(dev, Dev):
            raise TypeError('dev argument is not of type Dev.')
        if not isinstance(freebie, Freebie):
            raise TypeError('freebie argument is not of type freebie.')

    @classmethod
    def oldest_company(cls):
        """
        Return the oldest company in the database.

        The oldest company is determined by the founding year of the company.
        """
        return session.query(cls).order_by(cls.founding_year).first()

    def give_freebie(self, dev, freebie):
        """
        Associate a freebie with a dev.

        :param dev: the dev to associate the freebie with
        :type dev: models.Dev
        :param freebie: the freebie to associate with the dev
        :type freebie: models.Freebie
        :raises TypeError: if dev is not of type models.Dev or freebie is not of type models.Freebie
        :raises FreebieAlreadyGivenError: if the freebie has already been given to another dev
        :raises FreebieNotMineToGiveError: if the freebie does not belong to the company
        """
        if not isinstance(dev, Dev):
            raise TypeError('dev argument is not of type models.Dev.')
        if not isinstance(freebie, Freebie):
            raise TypeError('freebie argument is not of type models.Freebie.')
        if freebie.dev_id:
            raise FreebieAlreadyGivenError
        if freebie not in self.freebies:
            raise FreebieNotMineToGiveError
        else:
            # Add the freebie to the dev's freebies
            dev.freebies.append(freebie)


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # Python mapping of relationships
    freebies = relationship('Freebie', backref="dev")
    companies = relationship('Company',
                             secondary=companies_devs,
                             back_populates="devs")

    def __repr__(self):
        """
        Return a string representation of the Dev object.
        """
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        """
        Returns True if any of the freebies associated with the dev has the given
        item_name, otherwise returns False.

        :param item_name: the item_name to look for in the freebies
        :type item_name: str
        :return: whether the item_name was found in the freebies
        :rtype: bool
        """
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        """
        Changes the freebie's dev to be the given dev; your code should only
        make the change if the freebie belongs to the dev who's giving it away.

        :param dev: the dev to associate the freebie with
        :type dev: models.Dev
        :param freebie: the freebie to associate with the dev
        :type freebie: models.Freebie
        :raises TypeError: if dev is not of type models.Dev or freebie is not of type models.Freebie
        :raises FreebieNotMineToGiveError: if the freebie does not belong to the dev
        """
        if not isinstance(dev, Dev):
            raise TypeError("dev argument must be of type Dev")
        if not isinstance(freebie, Freebie):
            raise TypeError("freebie argument must be of type Freebie")
        if freebie not in self.freebies:
            raise FreebieNotMineToGiveError

    def received_one(self, item_name):
        """
        Returns True if any of the freebies associated with the dev has the given
        item_name, otherwise returns False.

        :param item_name: the item_name to look for in the freebies
        :type item_name: str
        :return: whether the item_name was found in the freebies
        :rtype: bool
        """
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        """
        Changes the freebie's dev to be the given dev; your code should only
        make the change if the freebie belongs to the dev who's giving it away.

        :param dev: the dev to associate the freebie with
        :type dev: models.Dev
        :param freebie: the freebie to associate with the dev
        :type freebie: models.Freebie
        :raises TypeError: if dev is not of type models.Dev or freebie is not of type models.Freebie
        :raises FreebieNotMineToGiveError: if the freebie does not belong to the dev
        """
        # Check the type of the arguments
        if not isinstance(dev, Dev):
            raise TypeError("dev argument must be of type Dev")
        if not isinstance(freebie, Freebie):
            raise TypeError("freebie argument must be of type Freebie")

        # Check if the freebie is in the dev's freebies
        if freebie not in self.freebies:
            raise FreebieNotMineToGiveError
        else:
            # Change the freebie's dev to the given dev
            freebie.dev = dev
            # Commit the changes to the database
            session.commit()


class Freebie(Base):
    # Mapped table name at the database level
    __tablename__ = 'freebies'

    # Column definitions
    id = Column(Integer(), primary_key=True)
    item_name = Column(String(), nullable=False)
    value = Column(Integer(), nullable=False)

    # Foreign Keys definitions (relationships at the database level)
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'), nullable=False)

    def __repr__(self):
        """Return a string representation of Freebie object."""
        return f"Freebie(item-name={self.item_name}, " + \
            f"value={self.value})"

    def print_details(self):
        """
        Prints a nicely formatted string with details about the freebie.

        :return: None
        """
        # Print the freebie details
        print(f"{self.dev} owns a {self.item_name} "
              f"from {self.company.name}")


class FreebieAlreadyGivenError(Exception):
    pass


class FreebieNotMineToGiveError(Exception):
    pass
