import unittest
from pathlib import Path

import werkzeug.datastructures
from api import app
from flask import current_app
import werkzeug
from io import BytesIO
from bll import select_all_bll
class TestBasicAPI(unittest.TestCase):
    client = app.test_client()

    @classmethod
    def setUpClass(cls):
        app.testing = True

    def test_get_cart(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1  # או כל id שמתאים למערכת שלך

        response = self.client.get("/cart/")
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        user_id = 1
        with self.client.session_transaction() as sess:
            sess['user_id'] = user_id
        product_name = 'Milk'
        empty = werkzeug.datastructures.FileStorage(
        stream=BytesIO(),  # Empty content
        filename="",  # Empty filename
        
    )
        self.client.post("/", data = {'product': product_name})
        get_products_list = select_all_bll(user_id)
        print(get_products_list)
        
        
        
        self.assertEqual(get_products_list[0][2], product_name)

        
        
        