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
        return f'<Company {self.name}>'

    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year).first()

    def give_freebie(dev, freebie):
        if not isinstance(dev, Dev):
            raise TypeError('dev argument is not of type Dev.')
        if not isinstance(freebie, Freebie):
            raise TypeError('freebie argument is not of type freebie.')
        if freebie.dev_id:
            raise FreebieAlreadyGivenError
        else:
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
        return f'<Dev {self.name}>'


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
        return f"Freebie(item-name={self.item_name}, " + \
            f"value={self.value})"

    def print_details(self):
        print(f"{self.dev} owns a {self.item_name} from {self.company.name}")


class FreebieAlreadyGivenError(Exception):
    pass
