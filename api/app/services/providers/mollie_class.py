from app.services.providers.providers import PaymentProvider
from mollie.api.client import Client
from datetime import datetime, timezone
from decimal import Decimal

class MollieProvider(PaymentProvider):

    def __init__(self, api_key, last_sync):
        self.client = Client()
        self.api_key = api_key
        self.last_sync = last_sync

    def list_payments(self):
        self.client.set_api_key(self.api_key)
        payments_list = self.client.payments.list(sort="desc")

        data = payments_list.get("_embedded")
        data2 = data.get("payments")
        
        start_date = None

        if self.last_sync is not None:
            start_date = self.last_sync.replace(tzinfo=timezone.utc)
            print(f"{start_date} is the start date")

        all_payments = []

        for p in data2:

            date = p.get("createdAt")
            dt = datetime.fromisoformat(date)
            if start_date:
                if dt < start_date: # the elder the datetime is, the "bigger it is"
                    break 

            p_id = p.get("id")
            amount = p.get("amount")
            amount_value = amount.get("value")
            int_value = self.convert_amount(amount_value)
            currency = amount.get("currency").lower()
            status = p.get("status")
            unified_status = self.convert_status(status)

            payment = {
                "id": p_id,
                "amount": int_value,
                "currency": currency,
                "date": dt,
                "status": unified_status
            }

            all_payments.append(payment)

        return(all_payments)

    def convert_status(self, status):
        statuses = {
            "open": "requires_action",
            "pending": "pending",
            "authorized": "pending",
            "paid": "succeeded",
            "canceled": "failed",
            "expired": "failed",
            "failed": "failed"
        }

        unified_status = statuses.get(status, "unknown")
        return(unified_status)
    # succeeded
    # pending
    # requires_action
    # failed

    def convert_amount(self, amount_value):
        decimal_value = Decimal(amount_value)
        unified_value = decimal_value * 100
        int_value = int(unified_value)

        return(int_value)