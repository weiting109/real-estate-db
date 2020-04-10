import sqlalchemy
from sqlalchemy import create_engine, Column, Text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///database.db')
engine.connect()

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key = True)
	name = Column(Text)
	insurance_id = Column(Integer)

	def __repr__(self):
		return "<User(id={0}, name={1}, insurance_id={2})>".format(self.id, self.name, self.insurance_id)

class Insurance(Base):
	__tablename__ = 'insurance'
	id = Column(Integer, ForeignKey('users.insurance_id'), primary_key = True)
	claim_id = Column(Integer)
	users = relationship(User)

	def __repr__(self):
		return "<Insurance(id={0}, claim_id={1}>".format(self.id, self.claim_id)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

session.add(User(id = 1, name = "What's His Name", insurance_id = 1))
session.add(Insurance(id = 1, claim_id = 1))
session.commit()

print(session.query(User).all())

"""You should see something like:

<User(id=1, name=What's His Name, insurance_id=1)>
"""

print(session.query(Insurance).filter_by(claim_id = 1).all())

"""
Here, you should see something like:
<Insurance(id=1, claim_id=1>
"""
