# encoding: utf-8
"""
Payments database models
--------------------
"""

import uuid
from sqlalchemy_utils import types as column_types, Timestamp

from app.extensions import db


class Payment(db.Model, Timestamp):
    """
    Defines Payment Database Model within the ORM
    """

    type = "Payment"
    id = db.Column(column_types.UUIDType(binary=False), default=uuid.uuid4,
                   primary_key=True)  # pylint: disable=invalid-name
    version = 0
    organisation_id = db.Column(column_types.UUIDType(binary=False), index=True, unique=False)
    attributes = db.relationship(
        'PaymentAttributes',
        uselist=False,
        cascade="save-update, merge, "
                "delete, delete-orphan"
    )

    def __repr__(self):
        return (
            "<{class_name}("
            "id='{self.id}'"
            "version={self.version}"
            "organisation_id='{self.organisation_id}'"
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )


class PaymentAttributes(db.Model):
    """
    Defines list of attributes linked to a Payment resource
    """
    id = db.Column(column_types.UUIDType(binary=False), db.ForeignKey('payment.id'), primary_key=True)

    amount = db.Column(db.DECIMAL, nullable=False)

    beneficiary_party_id = db.Column(db.Integer, db.ForeignKey(
        'bank_account.id'
    ), index=True, unique=False)
    beneficiary_party = db.relationship(
        'BankAccount',
        foreign_keys=[beneficiary_party_id]
    )

    charges_information_id = db.Column(db.Integer, db.ForeignKey(
        'charges_information.id'
    ))
    charges_information = db.relationship(
        'ChargesInformation'
    )

    currency = db.Column(db.String)

    debtor_party_id = db.Column(db.Integer, db.ForeignKey(
        'bank_account.id'
    ), index=True, unique=False)
    debtor_party = db.relationship(
        'BankAccount',
        foreign_keys=[debtor_party_id]
    )

    end_to_end_reference = db.Column(db.String)

    fx_id = db.Column(db.Integer, db.ForeignKey(
        'fx.id'
    ), index=True, unique=False)
    fx = db.relationship(
        'FX'
    )

    numeric_reference = db.Column(db.String)
    payment_id = db.Column(db.String)
    payment_purpose = db.Column(db.String)
    payment_scheme = db.Column(db.String)
    payment_type = db.Column(db.String)
    processing_date = db.Column(db.String)
    reference = db.Column(db.String)
    scheme_payment_sub_type = db.Column(db.String)
    scheme_payment_type = db.Column(db.String)

    sponsor_party_id = db.Column(db.Integer, db.ForeignKey(
        'bank_account.id'
    ), index=True, unique=False)
    sponsor_party = db.relationship(
        'BankAccount',
        foreign_keys=[sponsor_party_id]
    )


class BankAccount(db.Model):
    """
    Defines the BeneficiaryParty model.
    """
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(100), index=True, unique=False)
    account_number = db.Column(db.String(100), index=True, unique=False)
    account_number_code = db.Column(db.String(100), index=True, unique=False)
    account_type = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(100), index=True, unique=False)
    bank_id = db.Column(db.String(100), index=True, unique=False)
    bank_id_code = db.Column(db.String(100), index=True, unique=False)
    name = db.Column(db.String(100), index=True, unique=False)

    def __repr__(self):
        return (
            "<{class_name}("
            "id='{self.id}'"
            "account_name={self.account_name}"
            "account_number='{self.account_number}'"
            "account_number_code={self.account_number_code}"
            "account_type='{self.account_type}'"
            "address={self.address}"
            "bank_id='{self.bank_id}'"
            "bank_id_code='{self.bank_id_code}'"
            "name='{self.name}'"
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )


class ChargesInformation(db.Model):
    """
    Contains the diferent charges.
    """
    id = db.Column(db.Integer, primary_key=True)
    bearer_code = db.Column(db.String())

    sender_charges = db.relationship(
        'Charge'
    )

    receiver_charges_amount = db.Column(db.DECIMAL)
    receiver_charges_currency = db.Column(db.String)

    def __repr__(self):
        return (
            "<{class_name}("
            "id='{self.id}'"
            "bearer_code={self.bearer_code}"
            "sender_charges='{self.sender_charges}'"
            "receiver_charges_amount={self.receiver_charges_amount}"
            "receiver_charges_currency='{self.receiver_charges_currency}'"
            ")>".format(
                class_name=self.__class__.__name__,
                self=self
            )
        )


class Charge(db.Model):
    """
    The Charge
    """
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('charges_information.id'))

    amount = db.Column(db.DECIMAL)
    currency = db.Column(db.String)


class FX(db.Model):
    """
    Exchange Rate
    """
    __tablename__ = 'fx'
    id = db.Column(db.Integer, primary_key=True)
    contract_reference = db.Column(db.String)
    exchange_rate = db.Column(db.DECIMAL)
    original_amount = db.Column(db.DECIMAL)
    original_currency = db.Column(db.String)
