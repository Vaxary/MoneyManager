"""Entry class containing necessary data for the other functions"""


class Entry:
    """Entry object that contains
     the "wallet" where the change happened,
     "amount" of change, amount "before" and "after" the change,
     what was the "date" of the change
     and what was the "reason" for the change"""
    def __init__(self, params):
        """Initialize entry object with tuple containing parameters"""
        self._wallet = params[0]
        self._amount = params[1]
        self._before = params[2]
        self._after = params[3]
        self._date = params[4]
        self._reason = params[5]

    @property
    def amount(self):
        """amount field getter"""
        return self._amount

    @amount.setter
    def amount(self, value):
        """amount field setter"""
        self._amount = value

    @property
    def before(self):
        """before field getter"""
        return self._before

    @before.setter
    def before(self, value):
        """before field setter"""
        self._before = value

    @property
    def after(self):
        """after field getter"""
        return self._after

    @after.setter
    def after(self, value):
        """after field setter"""
        self._after = value

    @property
    def wallet(self):
        """wallet field getter"""
        return self._wallet

    @wallet.setter
    def wallet(self, value):
        """wallet field setter"""
        self._wallet = value

    @property
    def date(self):
        """date field getter"""
        return self._date

    @date.setter
    def date(self, value):
        """date field setter"""
        self._date = value

    @property
    def reason(self):
        """reason field getter"""
        return self._reason

    @reason.setter
    def reason(self, value):
        """reason field setter"""
        self._reason = value
