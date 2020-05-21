from create import Agents, Offices, AgentsOffices, ZipcodeOffices, Sellers, Buyers, Tiers, Houses, Sales
from create import init_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from datetime import datetime

engine = init_db('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

def addAgent(id,firstname,surname,email,phone):
    session.add(Agents(id=id,firstname=firstname,surname=surname,email=email,phone=phone))

def addSeller(id,firstname,surname,email,phone):
    session.add(Sellers(id=id,firstname=firstname,surname=surname,email=email,phone=phone))

def addBuyer(id,firstname,surname,email,phone):
    session.add(Buyers(id=id,firstname=firstname,surname=surname,email=email,phone=phone))

def addListing(id,zipcode,nbedrms,nbathrms,listingdate,listingmonth,listingprice,sellerid,agentid,status="unsold"):
    session.add(Houses(id=id,zipcode=zipcode,nbedrms=nbedrms,nbathrms=nbathrms,listingdate=listingdate,listingmonth=listingmonth,listingprice=listingprice,sellerid=sellerid,agentid=agentid,status=status))

def updateAgentsOffices(zipcode,agentid):
    """
    When a house is listed, update to list association between agent and office.
    """
    # Find office responsible for house (by area/zipcode)
    officeid = session.query(ZipcodeOffices.officeid).filter(ZipcodeOffices.zipcode==zipcode).first()[0]
    # Check if agent-office relationship has already been recorded
    res = session.query(AgentsOffices.agentid).filter(AgentsOffices.officeid == officeid, AgentsOffices.agentid==agentid).all()
    if(res==[]): # Agent not yet associated with office
        session.add(AgentsOffices(agentid=agentid,officeid=officeid))

def updateHousetoSold(houseid):
    """
    Updates status of house to 'sold'.
    """
    session.query(Houses).filter(Houses.id==houseid).update({"status":"sold"})

#Agents example data from CS162 Spring 2020 8.2 bankloans example
addAgent(2001,"Kathy","Mc","kathy@mc.com","(251) 546-9460")
addAgent(2002,"Avatar","Aang","avatar@nic.com","999")
addAgent(2003,"Avatar","Kora","avatar2@nick.com","888")
session.add(Agents(id=2004, firstname = 'Robert', surname = 'Warren', email = 'RobertDWarren@teleworm.us', phone = '(251) 546-9442'))
session.add(Agents(id=2005, firstname = 'Vincent', surname = 'Brown', email = 'VincentHBrown@rhyta.com', phone = '(125) 546-4478'))
session.add(Agents(id=2006, firstname = 'Janet', surname = 'Prettyman', email = 'JanetTPrettyman@teleworm.us', phone = '(949) 569-4371'))
session.add(Agents(id=2007, firstname = 'Martina', surname = 'Kershner', email = 'MartinaMKershner@rhyta.com', phone = '(630) 446-8851'))

print(session.query(Agents).all())

session.add(Offices(id=1001,name='San Francisco'))
session.add(Offices(id=1002,name='Berkeley'))
session.add(Offices(id=1003,name='Office3'))
session.add(Offices(id=1004,name='Office4'))
session.add(Offices(id=1005,name='Office5'))
session.add(Offices(id=1006,name='Office6'))
session.add(Offices(id=1007,name='Office7'))

session.add(ZipcodeOffices(zipcode=94102,officeid=1001))
session.add(ZipcodeOffices(zipcode=94704,officeid=1002))
session.add(ZipcodeOffices(zipcode=94706,officeid=1002))
session.add(ZipcodeOffices(zipcode=33333,officeid=1003))
session.add(ZipcodeOffices(zipcode=44444,officeid=1004))
session.add(ZipcodeOffices(zipcode=55555,officeid=1005))
session.add(ZipcodeOffices(zipcode=66666,officeid=1006))
session.add(ZipcodeOffices(zipcode=77777,officeid=1007))
session.add(ZipcodeOffices(zipcode=94105,officeid=1008))

session.add(AgentsOffices(agentid=2001,officeid=1002))
session.add(AgentsOffices(agentid=2003,officeid=1002))


"""From assignment instructions:
For houses sold below $100,000 the commission is 10%
For houses between $100,000 and $200,000 the commission is 7.5%
For houses between $200,000 and $500,000 the commission is 6%
For houses between $500,000 and $1,000,000 the commission is 5%
For houses above $1,000,000 the commission is 4%"""

session.add(Tiers(uppbound=100000,lowbound=0,rate=10))
session.add(Tiers(uppbound=200000,lowbound=100001,rate=7.5))
session.add(Tiers(uppbound=500000,lowbound=200001,rate=6))
session.add(Tiers(uppbound=1000000,lowbound=500001,rate=5))
session.add(Tiers(uppbound=1*10^16,lowbound=1000001,rate=4))

session.commit()

### When a house is listed:
# All the relevant details of that house need to be captured,
#ie. at least: seller details, # of bedrooms, # of bathrooms,
#listing price, zip code, date of listing, the listing estate agent,
#and the appropriate office.

# Add new seller
# session.add(Sellers(id=3001,firstname="Seller1",surname="Tan",email="seller1@tan.net",phone="(444)3213211"))
addSeller(3001,"Seller1","Tan","seller1@tan.net","(444)3213211")

# Add new house listing
# session.add(Houses(id=5001,zipcode=94704,nbedrms=3,nbathrms=2,listingdate=datetime(2025,1,1),listingmonth="202501",listingprice=150000,sellerid=3001,agentid=2001))
addListing(5001,94704,3,2,datetime(2025,1,1),202501,150000,3001,2001)

# Update association between agent and office (if not yet listed)
zipcode = 94704
agentid = 2001
updateAgentsOffices(94704,2001)

print(session.query(Houses).all())
print(session.query(AgentsOffices).all())

session.commit()

### When a house is sold

# Add new buyer
# session.add(Buyers(id=4001,firstname="Santa",surname="Claus",email="santa@northpole.com",phone="(000)1112223333"))
addBuyer(4001,"Santa","Claus","santa@northpole.com","(000)1112223333")

# Change status of house to sold
houseid = 5001
updateHousetoSold(houseid)
print(session.query(Houses).all())

# Calculate commission rate
listingprice = session.query(Houses.listingprice).filter(Houses.id==houseid).first()[0]
rate = session.query(Tiers.rate).filter(listingprice >= Tiers.lowbound,listingprice <= Tiers.uppbound).first()[0]
print(rate)
commission = rate*listingprice
saleprice = listingprice + commission

# Update sale price of house and capture details of sale
session.add(Sales(id=9001,houseid=houseid,commission=commission,saledate=datetime(2025,6,23),salemonth=202506,saleprice=saleprice,buyerid=4001))
print(session.query(Sales).all())

session.commit()

addSeller(3002,"Lazy","Cat","lazy@cat.com","(222)3334444")
addSeller(3003,"Happyy","Dogg","happy@dog.com","(333)4445555")
addSeller(3004,"Lazyy","Catt","lazy2@cat.com","(222)3334447")
addSeller(3005,"Happyyy","Doggg","happy3@dog.com","(333)4445557")
addSeller(3006,"Lazyyyyy","Cattttt","lazy5@cat.com","(222)3334449")
addSeller(3007,"Happyyyyy","Doggggg","happy5@dog.com","(333)4445559")
print(session.query(Sellers).all())

addListing(5002,94102,2,2,datetime(2025,3,22),202503,250000,3002,2003)
updateAgentsOffices(94102,2003)
addListing(5003,94102,2,2,datetime(2025,2,23),202503,302000,3003,2003)
updateAgentsOffices(94102,2003)
addListing(5004,94105,2,2,datetime(2025,1,24),202503,260000,3004,2007)
updateAgentsOffices(94105,2007)
addListing(5005,94704,2,2,datetime(2024,3,25),202403,270000,3005,2007)
updateAgentsOffices(94704,2007)
addListing(5006,94706,2,2,datetime(2024,3,26),202403,350000,3006,2001)
updateAgentsOffices(94706,2001)
addListing(5007,44444,2,2,datetime(2024,3,27),202403,550000,3007,2004)
updateAgentsOffices(44444,2004)

print(session.query(AgentsOffices).all())

for i in range(5002,5008):
    updateHousetoSold(i)
    # Calculate commission rate
    listingprice = session.query(Houses.listingprice).filter(Houses.id==i).first()[0]
    rate = session.query(Tiers.rate).filter(listingprice >= Tiers.lowbound,listingprice <= Tiers.uppbound).first()[0]
    commission = rate*listingprice
    saleprice = listingprice + commission

    # Update sale price of house and capture details of sale
    session.add(Sales(id=i+4000,houseid=i,commission=commission,saledate=datetime(2025,6,23),salemonth=202506,saleprice=saleprice,buyerid=4002))

print(session.query(Sales).all())

session.commit()
