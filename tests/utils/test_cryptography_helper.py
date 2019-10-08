import unittest
from mockito import unstub
from src.scraper.utils.cryptography_helper import CryptographyHelper


class TestCryptographyHelper(unittest.TestCase):

    def setUp(self):
        pass

    def test_no_password(self):
        self.assertIsNone(CryptographyHelper.decrypt(None))

    def test_encrypted_pasword(self):
        encrypted_password = 'gAAAAABdnEVcJYKGTxRsDG3mP0QFK9TH3oWMhlOZpdvDX_d5PEdXwrZah5XFsWgr8BV3uACb6oaleXdARvca_G7NtovOZ-4zvg=='
        decrypted_password = CryptographyHelper.decrypt(encrypted_password)
        self.assertEqual('justpassword', decrypted_password)

    def tearDown(self):
        unstub()
