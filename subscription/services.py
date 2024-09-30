import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_products(name):
    stripe.Product.create(name=name)


def create_price(summ):
    return stripe.Price.create(
        currency="rub",
        unit_amount=summ * 100,
        product_data={"name": "Gold Plan"},
    )


def create_session(price):
    session = stripe.checkout.Session.create(
        success_url="https://localhost:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
