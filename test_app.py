import unittest
from create import init_db, Offices
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func

engine=init_db('sqlite:///:memory:')
Session = sessionmaker()

"""
setUp, tearDown and test functions are based on template
taken from https://docs.sqlalchemy.org/en/13/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites.

"""

class testDBapp(unittest.TestCase):

    def setUp(self):
        # connect to the database
        self.connection = engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)

    def tearDown(self):
        self.session.close()

        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        self.trans.rollback()

        # return connection to the Engine
        self.connection.close()

    def test_Offices(self):
        """Test set-up of db and Offices table"""
        self.setUp()
        self.session.add(Offices(id=1,name='San Francisco'))
        self.session.commit()
        print(self.session.query(Offices).filter_by(id=1).all())
        self.assertEqual(self.session.query(func.count(Offices.id),1))
        self.tearDown()

    def test_ZipcodeOffices(self):
        """Test ZipcodeOffices table"""
        self.setUp()
        self.session.add(Offices(id=1,name='San Francisco'))
        self.session.add(ZipcodeOffices(zipcode=94704,officeid=1))
        print(self.session.query(ZipcodeOffices).join('offices').all())
        self.session.commit()
        self.tearDown()

if __name__ == '__main__':
    unittest.main()
