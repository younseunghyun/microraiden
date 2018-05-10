from microraiden.proxy.resources import Expensive
from flask import request
import logging
from microraiden.paying.PayManager import PayManagerFactory

log = logging.getLogger(__name__)


class BuyableExpensive(Expensive):
    def __init__(self, **kwargs):
        print(kwargs)
        super(BuyableExpensive, self).__init__(**kwargs)
        self.pay_manager = PayManagerFactory.get_instance()

    def price(self) -> int:
        if self.is_already_buyed():
            return 0
        else:
            return super(BuyableExpensive, self).price()

    def is_already_buyed(self) -> bool:
        content_id = request.path
        if 'RDN-Sender-Address' not in request.cookies.keys():
            return False
        address = request.cookies['RDN-Sender-Address']
        return self.pay_manager.is_paid(address, content_id)

