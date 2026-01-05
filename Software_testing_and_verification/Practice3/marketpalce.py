import itertools
from typing import List, Dict

_id_gen = itertools.count(1)

class Listing:
    def __init__(self, title: str, description: str, price: float, seller_id: str):
        self.id = next(_id_gen)
        self.title = title
        self.description = description
        self.price = float(price)
        self.seller_id = seller_id
        self.delivery_status = "pending"  # pending / shipped / delivered / cancelled
        self.messages = []  # list of dicts: {from, text}

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "seller_id": self.seller_id,
            "delivery_status": self.delivery_status,
            "messages": list(self.messages),
        }

class Marketplace:
    def __init__(self):
        self._listings: Dict[int, Listing] = {}

    def add_listing(self, title: str, description: str, price: float, seller_id: str) -> Listing:
        if not title or price is None:
            raise ValueError("title and price required")
        listing = Listing(title, description, price, seller_id)
        self._listings[listing.id] = listing
        return listing

    def get_listing(self, listing_id: int) -> Listing:
        return self._listings.get(listing_id)

    def list_all(self) -> List[Dict]:
        return [l.to_dict() for l in self._listings.values()]

    def search_listings(self, query: str) -> List[Dict]:
        q = (query or "").lower()
        if not q:
            return self.list_all()
        res = []
        for l in self._listings.values():
            if q in l.title.lower() or q in l.description.lower():
                res.append(l.to_dict())
        return res

    def send_message(self, listing_id: int, from_user: str, text: str) -> None:
        l = self.get_listing(listing_id)
        if l is None:
            raise KeyError("listing not found")
        if not text:
            raise ValueError("text required")
        l.messages.append({"from": from_user, "text": text})

    def update_delivery_status(self, listing_id: int, status: str) -> None:
        allowed = {"pending", "shipped", "delivered", "cancelled"}
        if status not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        l = self.get_listing(listing_id)
        if l is None:
            raise KeyError("listing not found")
        l.delivery_status = status
