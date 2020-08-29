from unittest import TestCase

from CmClient import CmClient
from tests.test_data.TestDataProvider import TestDataProvider


class TestCmClient(TestCase):

    def setUp(self):
        test_data = TestDataProvider()
        self.uut = CmClient(test_data.provide_config(), test_data.provide_confidential_config())
        self.product_id = 27

    def test_get_account_articles(self):
        resp, _, _ = self.uut.get_account_articles()
        self.assertTrue(resp)

    def test_get_account_stock(self):
        resp, _, _ = self.uut.get_account_stock()
        self.assertTrue(resp)

    def test_get_account_data(self):
        resp, _, _ = self.uut.get_account_data()
        self.assertTrue(resp)

    def test_get_card_info(self):
        resp, _, _ = self.uut.get_card_info(self.product_id)
        self.assertTrue(resp)

    def test_get_card_listing(self):
        resp, _, _ = self.uut.get_card_listing(self.product_id)
        self.assertTrue(resp)

    def test_put_card_price(self):
        example_card = {
            "article":
                {'idArticle': 593000831, 'idProduct': 27, 'language': {'idLanguage': 1, 'languageName': 'English'}, 'comments': '', 'price': 0.40, 'idCurrency': 1, 'currencyCode': 'EUR', 'count': 1, 'inShoppingCart': False, 'lastEdited': '2020-06-11T13:51:42+0200', 'product': {'idGame': 1, 'image': '//static.cardmarket.com/img/6058ee20479ba5c80d41447a9b1625fc/items/1/MRD/27.jpg', 'enName': 'Taj-Nar Swordsmith', 'locName': 'Taj-Nar Swordsmith', 'expansion': 'Mirrodin', 'nr': '27', 'expIcon': 43, 'rarity': 'Uncommon'}, 'condition': 'EX', 'isFoil': False, 'isSigned': False, 'isPlayset': False, 'isAltered': False}
        }
        resp, _, _ = self.uut.put_card_price(example_card)
        self.assertTrue(resp)
