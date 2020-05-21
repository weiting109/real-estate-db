from create import Agents, Offices, AgentsOffices, ZipcodeOffices, Sellers, Buyers, Tiers, Houses, Sales
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, create_engine

engine = create_engine('sqlite:///database.db')
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

print(session.query(Houses).all())
print(session.query(Sales).all())

salemonth = 202506

# Find the top 5 offices with the most sales for that month.
q = session.query(Offices.name,Offices.id,func.sum(Sales.saleprice).label('total')).join(Sales.houses
                        ).join(Houses.zipcodeoffices).join(ZipcodeOffices.offices
                        ).filter(Sales.salemonth==salemonth
                        ).group_by(Offices.id).limit(5).all()

print(q)

# Find the top 5 estate agents who have sold the most (include their contact details and their sales details
q = session.query(Agents.firstname,Agents.surname,Agents.email,Agents.phone,func.sum(Sales.saleprice)
                        ).join(Sales.houses).join(Houses.agents).filter(Sales.salemonth==salemonth
                        ).group_by(Agents.id).limit(5).all()
print(q)

# Calculate the commission that each estate agent must receive and store the results in a separate table.
q = session.query(Agents.id,func.sum(Sales.commission)).join(Sales.houses).join(Houses.agents
                        ).filter(Sales.salemonth==salemonth).group_by(Agents.id).all()
print(q)

# For all houses that were sold that month, calculate the average number of days
# that a house was on the market.
q = session.query(func.avg(Sales.saledate - Houses.listingdate)).join(Sales.houses
                        ).filter(Sales.salemonth==salemonth).first()
print(q)

# For all houses that were sold that month, calculate the average selling price
q = session.query(func.avg(Sales.saleprice)).join(Sales.houses
                        ).filter(Sales.salemonth==salemonth).first()
print(q)

# Find the zip codes with the top 5 average sales prices
q = session.query(Houses.zipcode, func.avg(Sales.saleprice)).join(Sales.houses
                        ).filter(Sales.salemonth==salemonth).group_by(Houses.zipcode
                        ).limit(5).all()

print(q)
