import sqlalchemy
from sqlalchemy import create_engine, Column, Text, String, Integer, DateTime, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Agents(Base):
	__tablename__="agents"
	id = Column(Integer, primary_key=True, index=True) #indexed for faster queries (monthly reports by employee)
	firstname=Column(Text)
	surname=Column(Text)
	email=Column(Text)
	phone=Column(String(20))

	def __repr__(self):
		return "Agents(id={},firstname={},surname={},email={},phonenum={})\n".format(self.id,self.firstname,self.surname,self.email,self.phone)

class Offices(Base):
	__tablename__="offices"
	id = Column(Integer, primary_key=True, index=True) #indexed for faster queries (monthly reports by month)
	name = Column(Text)

	def __repr__(self):
		return "Office(id={},name={})\n".format(self.id,self.name)

class AgentsOffices(Base):
	"""
	Intersection table for many-to-many relationship between agents and offices.
	Composite primary key from agentid and officeid.
	"""
	__tablename__="agentsoffices"
	agentid = Column(Integer, ForeignKey('agents.id'),primary_key=True)
	officeid = Column(Integer, ForeignKey('offices.id'), primary_key=True)

	offices = relationship(Offices)
	agents = relationship(Agents)

	def __repr__(self):
		return "AgentsOffices(agentid={},officeid={})\n".format(self.agentid,self.officeid)

class ZipcodeOffices(Base):
	__tablename__="zipcodeoffices"
	zipcode = Column(Integer,primary_key=True, index=True) #indexed for faster queries (monthly reports - by zipcode)
	officeid = Column(Integer, ForeignKey('offices.id'), index=True) #indexed for faster queries (monthly reports - by office)
	offices = relationship(Offices)
	def __repr__(self):
		return "ZipcodeOffices(zipcode={},officeid={})\n".format(self.zipcode,self.officeid)

class Sellers(Base):
	__tablename__="sellers"
	id = Column(Integer,primary_key=True)
	firstname = Column(String(100))
	surname = Column(String(100))
	email = Column(Text)
	phone = Column(String(20))

	def __repr__(self):
		return "Sellers(id={},firstname={},surname={},email={},phonenum={})\n".format(self.id,self.firstname,self.surname,self.email,self.phone)

class Buyers(Base):
	__tablename__="buyers"
	id = Column(Integer,primary_key=True)
	firstname = Column(String(100))
	surname = Column(String(100))
	email = Column(Text)
	phone = Column(String(20))

	def __repr__(self):
		return "Buyers(id={},firstname={},surname={},email={},phonenum={})\n".format(self.id,self.firstname,self.surname,self.email,self.phone)

class Tiers(Base):
	"""Commission tiers and rates"""
	__tablename__="tiers"
	uppbound = Column(Numeric(precision=2), primary_key=True, index=True)
	lowbound = Column(Numeric(precision=2))
	rate = Column(Numeric(precision=1))

class Houses(Base):
	__tablename__="houses"
	id = Column(Integer,primary_key=True)
	zipcode = Column(Integer,ForeignKey('zipcodeoffices.zipcode'), index=True) #indexed for faster queries (monthly reports))
	nbedrms = Column(Integer)
	nbathrms = Column(Integer)
	listingdate = Column(DateTime)
	listingmonth = Column(Integer, index=True)
	listingprice = Column(Numeric(precision=2))
	sellerid = Column(Integer,ForeignKey('sellers.id'))
	agentid = Column(Integer,ForeignKey('agents.id'), index=True) #indexed for faster queries (monthly reports))
	status = Column(String,default="unsold")

	zipcodeoffices=relationship(ZipcodeOffices)
	sellers=relationship(Sellers)
	agents=relationship(Agents)

	def __repr__(self):
		return """Houses(id={},zipcode={},nbedrms={},nbathrms={},listingdate={},listingmonth={},listingprice={},
sellerid={},agentid={},status={})\n""".format(self.id,self.zipcode,self.nbedrms,self.nbathrms,
							self.listingdate,self.listingmonth,self.listingprice,
							self.sellerid,self.agentid,self.status)

class Sales(Base):
	__tablename__="sales"
	id = Column(Integer,primary_key=True)
	houseid = Column(Integer,ForeignKey('houses.id'),index=True)
	commission = Column(Numeric(precision=2))
	saledate = Column(DateTime)
	salemonth = Column(Integer,index=True) #indexed for faster queries (monthly reports)
	saleprice = Column(Numeric(precision=2))
	buyerid = Column(Integer,ForeignKey('buyers.id'))

	houses = relationship(Houses)
	buyers= relationship(Buyers)

	def __repr__(self):
		return """Sales(id={},houseid={},commission={},saledate={},
salemonth={},saleprice={},buyerid={})\n""".format(self.id,self.houseid,self.commission,self.saledate,
							self.salemonth,self.saleprice,self.buyerid)

def init_db(url='sqlite:///database.db'):
	engine = create_engine(url)
	engine.connect()
	Base.metadata.create_all(bind=engine)
	return engine

if __name__ == "__main__":
	engine = init_db()
