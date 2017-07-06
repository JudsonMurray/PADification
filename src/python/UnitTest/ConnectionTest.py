#!usr/bin/env Python3
#
#
#       NAME: WILLIAM GALE
#       DATE: 2017-07-04
#       PURPOSE: TestCase for Connection Testing in PADification Database
#
#
import datetime
import unittest
import PADSQL
from PADMonster import *

class TC1(unittest.TestCase):
    """Connection Tests"""

    def __init__(self, methodName = 'runTest'):
        self.padsql = PADSQL.PADSQL()
        self.padsql.connect()
        return super().__init__(methodName)

    def test_is_istantiated(self):
        """PADSQL pypyodbc Instantiation"""
        self.assertIsInstance(self.padsql, PADSQL.PADSQL)

    def test_connection(self):
        """MsSQL Server Connected"""
        self.assertTrue(self.padsql.connection.connected)

    def test_disconnect(self):
        """MsSQL Server Disonnect"""
        self.padsql.closeConnection()
        self.assertFalse(self.padsql.connection.connected)

if __name__ == '__main__':
    log_file = 'Connection_Test_log_' + '{:%Y-%m-%d %H-%M-%S}'.format(datetime.datetime.now()) + '.txt'
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f,verbosity = 2)
    unittest.main(testRunner=runner,verbosity=2,exit=False)
    f.close()

f = open(log_file, "r")
print(f.read())
f.close()