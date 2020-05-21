# CS162 Spring 2019: Retail estate database application
#### Wei-Ting Yap

# Instructions to run

Run the following to install all required packages:

`python3.6 -m venv .venv`

`source .venv/bin/activate`

`pip3 install -r requirements.txt`

## Declaring models and creating the database

Run the following to declare models and create the database, a sqlite file 'database.db' in the same directory:

`python3 create.py`

Models created: Agents, Offices, AgentsOffices, ZipcodeOffices, Houses, Sellers, Buyers, Sales

## Inserting data

Run the following to insert dummy data to test the database application:

`python3 insert_data.py`

Two scenarios requiring insertion/updating of data have been coded:
- When a new house is listed
- When a house is sold

## Querying the data

Run the following to query the database:
`python3 query_data.py`

The queries print results corresponding to the following for the month of June 2025:

- top 5 offices with the most sales
- top 5 estate agents who have sold the most
- commission that each estate agent must receive
- average number of days that a sold house was on the market
- average selling price of sold houses
- zip codes with the top 5 average sales prices

These queries can be used to generate monthly results by changing the `salesmonth` variable.

# Data normalization

Most tables are in third normalized form, which adds complexity (see the number of join statements in `query_data.py`), but prevents database anomalies when modifications are made. A key application of data normalization: the table `agents` and `offices` have an intersection table `agentsoffices` with a composite multi-field primary key. The intersection table transforms the many-to-many relationship between agents and retail offices into one-to-many and many-to-one, so that there is no need for duplication of information (many rows in `agents` or `offices`) and each table corresponds to a clear conceptual idea.

# Indexing

Some columns for some tables have been indexed for faster queries. For example, `salemonth` in the `Sales` table has been indexed. The author anticipates this choice of indexing will speed up the generation of monthly reports significantly as the database scales. Monthly reports are largely concerned with houses sold in a particular month, so all queries (see `query_data.py`) filter by `Sales.salemonth`. Indexing reduces the lookup time for rows with the desired salemonth with the use of dictionary key-value pairs.

# Transactions

In `inserting_data.py`, transactions have been used to illustrate the insertion of data when a house is listed, and when a house is sold. Transactions are helpful because they prevent database anomalies in the case of a an interrupted transaction. For example, if the `status` of a listing is set to `sold` but an interruption stops the sale from recording in the `Sales` table. This scenario violates the integrity of the database.

Another use of transactions is in an additional file, `test_app.py`. Although the author did not code many unit tests for the database application, the author recognises that transactions can be especially helpful for database testing. With SQL Alchemy, the tester can use a single database engine for the entire test case, but start a new transaction for each test and roll back the commits to the database before the next test.

# Languages used

This project uses SQL Alchemy as an Object Relational Mapper as well as a lightweight SQLite database in the same directory. Installation of the `sqlalchemy` module is required.
