#!usr/bin/env Python3
#
#
#       NAME: WILLIAM GALE
#       DATE: 2017-07-04
#       PURPOSE: TestCases for PADification Account Creation and Login.

import unittest
import PADSQL
from PADMonster import *

class TC2(unittest.TestCase):
    """Tests Creation of an account, Then Login """

    def __init__(self, methodName = 'runTest'):
        self.padsql = PADSQL.PADSQL()
        return super().__init__(methodName)

    def test_Signup_Valid_Information(self):
        """Test account signup, Ensure Information Does not Exist in Database"""
        self.padsql.signup(['Username','Password','TestEmail1@test.test', 300000000])

    def test_Signup_Duplicate_Information(self):
        """Test Fails to sign up duplicate account"""
        with self.assertRaises(PADSQL.pypyodbc.IntegrityError):
            self.padsql.signup(['Usertest1','PassTest1','TestEmail1@test.test', 300000000])
    
    @unittest.skip("No Rules set up to Test yet.")
    def test_Signup_Invalid_Information(self):
        """No rules set up to test yet"""
        self.assertTrue(False,"No rules set up to test yet")

    def test_login(self):
        """Valid Username and Password sign in"""
        self.padsql.login('Username', 'Password')
        self.assertTrue(self.padsql.signedIn)

    def test_login_invalid(self):
        """Invalid Username and Password sign in"""
        self.padsql.login('User', 'Pass')
        self.assertFalse(self.padsql.signedIn)

    def test_login_Casesensitivity(self):
        self.padsql.login('USERNAME', 'PASSWORD')
        self.assertFalse(self.padsql.signedIn, "Case Sensitivity is not functioning")

    def test_login_Empty(self):
        self.padsql.login('', '')
        self.assertFalse(self.padsql.signedIn, "Login with no credentials what?")

if __name__ == '__main__':
    unittest.main(verbosity=2)