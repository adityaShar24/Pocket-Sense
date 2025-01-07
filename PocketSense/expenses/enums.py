from enum import Enum


class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)

    @classmethod
    def help(cls):
        return ", ".join([f"{i.name} -> {i.value}" for i in cls])

    @classmethod
    def values(cls):
        return [i.value for i in cls]


class PaymentStatusEnum(ChoiceEnum):
    Pending = 1
    Completed = 2
    Failed = 3
    
class PaymentMethodEnum(ChoiceEnum):
    Bank_Transfer = 1
    UPI = 2
    Cheque = 3