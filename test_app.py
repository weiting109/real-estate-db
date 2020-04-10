import unittest

class testDBapp(unittest.TestCase):

    def setUpClass(cls): 2
        dal.db_init('sqlite:///:memory:')
