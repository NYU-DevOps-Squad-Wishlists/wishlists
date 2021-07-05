"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Wishlist, Item


class WishlistFactory(factory.Factory):
    """Creates fake wishlists that you don't have to feed"""

    class Meta:
        model = Wishlist

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    customer_id = factory.Sequence(lambda n: n)

class ItemFactory(factory.Factory):
    """Creates fake items that you don't have to feed"""

    class Meta:
        model = Item

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    wishlist_id = factory.Sequence(lambda n: n)
