from api import app
from dal import init_db
import unittest
from tests.unit_tests import TestBasicAPI

if __name__ == "__main__":
    init_db()
    app.run(debug= True)
    # ts = unittest.defaultTestLoader.loadTestsFromTestCase(TestBasicAPI)
    # unittest.TextTestRunner().run(ts)