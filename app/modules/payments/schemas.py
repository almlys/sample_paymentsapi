# encoding: utf-8
"""
Serialization schemas for Payments resources RESTful API
----------------------------------------------------
"""

import simplejson

from flask_marshmallow import base_fields
from flask_restplus_patched import ModelSchema

from .models import Payment, PaymentAttributes, BankAccount, Charge, ChargesInformation, FX


class BaseSponsorPartySchema(ModelSchema):
    class Meta:
        model = BankAccount
        fields = (
            BankAccount.account_number.key,
            BankAccount.bank_id.key,
            BankAccount.bank_id_code.key,
        )


class BaseDebtorPartySchema(BaseSponsorPartySchema):
    class Meta:
        model = BankAccount
        fields = BaseSponsorPartySchema.Meta.fields + (
            BankAccount.account_name.key,
            BankAccount.account_number_code.key,
            BankAccount.address.key,
            BankAccount.name.key
        )


class BaseBeneficiaryPartySchema(BaseDebtorPartySchema):
    class Meta:
        model = BankAccount
        fields = BaseDebtorPartySchema.Meta.fields + (
            BankAccount.account_type.key,
        )


class BaseChargeSchema(ModelSchema):
    amount = base_fields.Decimal(places=2)

    class Meta:
        model = Charge
        fields = (
            Charge.amount.key,
            Charge.currency.key
        )


class BaseChargesInformationSchema(ModelSchema):
    sender_charges = base_fields.Nested(BaseChargeSchema, many=True)
    receiver_charges_amount = base_fields.Decimal(places=2)

    class Meta:
        model = ChargesInformation
        fields = (
            ChargesInformation.bearer_code.key,
            ChargesInformation.sender_charges.key,
            ChargesInformation.receiver_charges_amount.key,
            ChargesInformation.receiver_charges_currency.key
        )


class BaseFXSchema(ModelSchema):
    original_amount = base_fields.Decimal(places=2)
    exchange_rate = base_fields.Decimal(places=2)

    class Meta:
        model = FX
        fields = (
            FX.contract_reference.key,
            FX.exchange_rate.key,
            FX.original_amount.key,
            FX.original_currency.key
        )


class BasePaymentAttributesSchema(ModelSchema):
    """
    Attributes
    """
    amount = base_fields.Decimal(places=2)
    beneficiary_party = base_fields.Nested(BaseBeneficiaryPartySchema)
    charges_information = base_fields.Nested(BaseChargesInformationSchema)
    debtor_party = base_fields.Nested(BaseDebtorPartySchema)
    fx = base_fields.Nested(BaseFXSchema)
    sponsor_party = base_fields.Nested(BaseSponsorPartySchema)

    class Meta:
        model = PaymentAttributes
        fields = (
            PaymentAttributes.amount.key,
            PaymentAttributes.beneficiary_party.key,
            PaymentAttributes.charges_information.key,
            PaymentAttributes.currency.key,
            PaymentAttributes.debtor_party.key,
            PaymentAttributes.end_to_end_reference.key,
            PaymentAttributes.fx.key,
            PaymentAttributes.numeric_reference.key,
            PaymentAttributes.payment_id.key,
            PaymentAttributes.payment_purpose.key,
            PaymentAttributes.payment_scheme.key,
            PaymentAttributes.payment_type.key,
            PaymentAttributes.processing_date.key,
            PaymentAttributes.reference.key,
            PaymentAttributes.scheme_payment_sub_type.key,
            PaymentAttributes.scheme_payment_type.key,
            PaymentAttributes.sponsor_party.key
        )
        dump_only = (
            PaymentAttributes.id.key,
        )


class BasePaymentSchema(ModelSchema):
    """
    Base Payment schema exposes only the most general fields.
    """
    attributes = base_fields.Nested(BasePaymentAttributesSchema)

    class Meta:
        # pylint: disable=missing-docstring
        json_module = simplejson
        model = Payment
        fields = (
            'type',
            Payment.id.key,
            'version',
            Payment.organisation_id.key,
            Payment.attributes.key
        )
        dump_only = (
            'type',
            Payment.id.key,
            'version'
        )


class DetailedPaymentSchema(BasePaymentSchema):
    """
    Detailed Payment schema exposes all useful fields.
    """

    class Meta(BasePaymentSchema.Meta):
        fields = BasePaymentSchema.Meta.fields + (
            Payment.created.key,
            Payment.updated.key,
        )
        dump_only = BasePaymentSchema.Meta.dump_only + (
            Payment.created.key,
            Payment.updated.key,
        )
