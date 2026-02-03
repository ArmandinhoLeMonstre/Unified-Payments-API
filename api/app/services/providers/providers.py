from abc import ABC, abstractmethod

class PaymentProvider(ABC):

    @abstractmethod
    def list_payments(self):
        pass
