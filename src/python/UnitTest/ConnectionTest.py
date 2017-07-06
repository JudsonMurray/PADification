#!usr/bin/env Python3
#
#
#       NAME: WILLIAM GALE
#       DATE: 2017-07-04
#       PURPOSE: TestCase for Connection Testing in PADification Database
#
#

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
    unittest.main()