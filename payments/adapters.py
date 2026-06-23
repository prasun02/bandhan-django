class PaymentAdapter:
    provider = "base"

    def create_attempt(self, payment):
        raise NotImplementedError

    def verify_callback(self, payload):
        raise NotImplementedError


class CashOnDeliveryAdapter(PaymentAdapter):
    provider = "cod"

    def create_attempt(self, payment):
        payment.status = "cod_pending"
        payment.save(update_fields=["status", "updated_at"])
        return {"status": payment.status}

    def verify_callback(self, payload):
        return False


class BKashAdapter(PaymentAdapter):
    provider = "bkash"

    def create_attempt(self, payment):
        return {"status": "credential_required"}

    def verify_callback(self, payload):
        return False


class CardGatewayAdapter(PaymentAdapter):
    provider = "card"

    def create_attempt(self, payment):
        return {"status": "credential_required"}

    def verify_callback(self, payload):
        return False
