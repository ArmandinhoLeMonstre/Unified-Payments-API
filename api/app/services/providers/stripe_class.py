from app.services.providers.providers import PaymentProvider
import stripe
from datetime import datetime, timezone
import time as time_module
import calendar

class StripeProvider(PaymentProvider):
    def __init__(self, api_key, last_synced_at):
        self.last_synced_at = last_synced_at
        stripe.api_key = api_key # Make it a try catch

    def list_payments(self):

        final_query = self.query_builder()
        # final_query = "created >= 0"
        pi = stripe.PaymentIntent.search(query=final_query, limit=10)

        has_more = True

        all_payments = []

        while has_more:
            data = pi.get("data")

            if data:
                self.extract_payment_data(data, all_payments)

            has_more = pi.get("has_more")

            if has_more:
                next_page = pi.get("next_page")
                pi = stripe.PaymentIntent.search(query=final_query, limit=10, page=next_page)

        return(all_payments)

    def query_builder(self):

        query = ""
        if self.last_synced_at:
            unix_str = str(self.datetime_to_unix(self.last_synced_at))
            query += "created >'"
            query += unix_str
            query += "' AND "
        query += "created<'"
        timestamp = str(int(time_module.time()))
        query += timestamp
        query += "'"
        print(query)
        return (query)
    
    def datetime_to_unix(self, date):
        unix_ts = int(date.replace(tzinfo=timezone.utc).timestamp())

        return (unix_ts)

    def extract_payment_data(self, data, all_payments):
        for payment in data:
            payment_id = payment.get("id")
            amount = payment.get("amount")
            currency = payment.get("currency")
            time = payment.get("created")
            d = datetime.fromtimestamp(time, tz=timezone.utc)
            status = payment.get("status")
            unified_status = self.convert_status(status)

            row = {"id": payment_id,
                    "amount": amount,
                    "currency": currency,
                    "date": d,
                    "status": unified_status}

            all_payments.append(row)

        return (0)
    def convert_status(self, status):
        statuses = {
            "processing": "pending",
            "requires_action": "pending",
            "requires_capture": "pending",
            "requires_confirmation": "pending",
            "requires_payment_method": "pending",
            "succeeded": "succeeded",
            "canceled": "failed",
        }

        unified_status = statuses.get(status, "unknown")

        return(unified_status)