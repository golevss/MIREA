import sys, os
sys.path.append(os.path.dirname(__file__))

import unittest
from marketpalce import Marketplace


class TestMarketplace(unittest.TestCase):
    def setUp(self):
        self.m = Marketplace()

    def test_add_and_get_listing(self):
        l = self.m.add_listing("Phone", "Used phone, good", 99.99, "seller1")
        self.assertIsNotNone(l.id)
        fetched = self.m.get_listing(l.id)
        self.assertEqual(fetched.title, "Phone")
        self.assertEqual(fetched.price, 99.99)

    def test_search_found_and_not_found(self):
        self.m.add_listing("Red Bike", "Mountain bike", 150, "s1")
        self.m.add_listing("Blue Helmet", "Safety helmet", 20, "s2")
        res = self.m.search_listings("bike")
        self.assertEqual(len(res), 1)
        self.assertIn("Red Bike", res[0]["title"])
        res_all = self.m.search_listings("")  # empty -> all
        self.assertGreaterEqual(len(res_all), 2)

    def test_send_message_and_history(self):
        l = self.m.add_listing("Lamp", "Desk lamp", 15, "sellerX")
        self.m.send_message(l.id, "buyer1", "Is it available?")
        self.m.send_message(l.id, "sellerX", "Yes, still available")
        listing = self.m.get_listing(l.id)
        self.assertEqual(len(listing.messages), 2)
        self.assertEqual(listing.messages[0]["from"], "buyer1")
        self.assertEqual(listing.messages[1]["from"], "sellerX")

    def test_update_delivery_status(self):
        l = self.m.add_listing("Book", "Novel", 5, "s")
        self.assertEqual(l.delivery_status, "pending")
        self.m.update_delivery_status(l.id, "shipped")
        self.assertEqual(self.m.get_listing(l.id).delivery_status, "shipped")
        with self.assertRaises(ValueError):
            self.m.update_delivery_status(l.id, "unknown_status")

    def test_errors(self):
        with self.assertRaises(ValueError):
            self.m.add_listing("", "no title", 10, "s")
        with self.assertRaises(KeyError):
            self.m.send_message(9999, "u", "hi")
        with self.assertRaises(KeyError):
            self.m.update_delivery_status(9999, "shipped")

if __name__ == "__main__":
    unittest.main()
