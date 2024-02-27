import datetime
import os

import requests


class OutscraperClient:
    def __init__(self):
        self.environment = os.environ.get("ENV", "Staging")
        self.base_url = "https://api.app.outscraper.com"

    @property
    def headers(self):
        common_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        auth_token = {
            "Staging": "MWM5ZDg3MTdlNTE2NGIwMjgzNzRkNTVmNDhhMTQ0MzV8MzhhOWRmYjk3Mg",
            "Prod": "MWM5ZDg3MTdlNTE2NGIwMjgzNzRkNTVmNDhhMTQ0MzV8MzhhOWRmYjk3Mg",
        }.get(self.environment)

        return {**common_headers, "X-API-KEY": auth_token}

    def search_google_maps_reviews(self, google_place_id: str, start_from: int):
        resp = requests.post(
            f"{self.base_url}/maps/reviews-v3",
            headers=self.headers,
            params={"query": google_place_id, "webhook": "asd", "start": start_from},
        )
        return resp

    def stripe_create_customer(self, user_id):
        resp = requests.post(
            f"{self.base_url}/stripe/user/{user_id}/customer",
            headers=self.headers,
        )
        return resp

    def stripe_create_booking_guarantee(self, business_id, booking_price):
        resp = requests.post(
            f"{self.base_url}/stripe/business/{business_id}/booking-guarantee/",
            headers=self.headers,
            params={"booking_price": booking_price},
        )
        return resp

    def stripe_get_customer(self, user_id):
        resp = requests.get(
            f"{self.base_url}/stripe/user/{user_id}/customer",
            headers=self.headers,
        )
        return resp

    def stripe_get_cards(self, user_id):
        resp = requests.get(
            f"{self.base_url}/stripe/user/{user_id}/cards", headers=self.headers
        )
        return resp

    def stripe_set_default_payment_method(self, user_id: int, default_payment_method):
        resp = requests.patch(
            f"{self.base_url}/stripe/user/{user_id}/default_payment/{default_payment_method}",
            headers=self.headers,
        )
        return resp

    def stripe_create_setup_intent(self, user_id: int):
        resp = requests.post(
            f"{self.base_url}/stripe/user/{user_id}/setup_intent",
            headers=self.headers,
        )
        return resp

    def stripe_delete_payment_method(self, payment_method: str):
        resp = requests.delete(
            f"{self.base_url}/stripe/payment_method/{payment_method}",
            headers=self.headers,
        )
        return resp

    def stripe_cancel_subscription(self, business_id: int):
        resp = requests.delete(
            f"{self.base_url}/stripe/business/{business_id}",
            headers=self.headers,
        )
        return resp

    def twilio_create_business_phone_number(self, business_id=None):
        resp = requests.post(
            f"{self.base_url}/twilio/create-business-phone-number",
            headers=self.headers,
            params={
                "business_id": business_id,
            },
        )
        return resp

    def twilio_remove_phone_number(
        self, business_id=None, phone_number=None, remove_from_db=False
    ):
        resp = requests.delete(
            f"{self.base_url}/twilio/remove-phone-number",
            headers=self.headers,
            params={
                "business_id": business_id,
                "phone_number": phone_number,
                "remove_from_db": remove_from_db,
            },
        )
        return resp

    def twilio_manage_toll_free_verification_review(
        self, business_id=None, phone_number=None
    ):
        resp = requests.post(
            f"{self.base_url}/twilio/manage-toll-free-verification-review",
            headers=self.headers,
            params={
                "business_id": business_id,
                "phone_number": phone_number,
            },
        )
        return resp

    def twilio_business_phone_details(self, business_id=None, phone_number=None):
        resp = requests.get(
            f"{self.base_url}/twilio/business-phone-details",
            headers=self.headers,
            params={
                "business_id": business_id,
                "phone_number": phone_number,
            },
        )
        return resp


#
# api_gateway = ReachApiGatewayV2()
# stripe_customer = api_gateway.stripe_create_customer(
#     user_id=1,
#     description="wilson",
#     name="teste",
#     email="teste@gmail.com",
#     phone=None,
# )
