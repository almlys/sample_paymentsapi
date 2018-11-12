# encoding: utf-8
"""
Input arguments (Parameters) for Payments resources RESTful API
-----------------------------------------------------------
"""

from flask_marshmallow import base_fields
from marshmallow import validate, validates_schema, ValidationError
from flask_restplus_patched import Parameters, PostFormParameters, PatchJSONParameters

import logging

from . import schemas
from .models import Payment, PaymentAttributes

log = logging.getLogger(__name__)


class CreatePaymentParameters(Parameters, schemas.DetailedPaymentSchema):
    class Meta(schemas.DetailedPaymentSchema.Meta):
        pass


class PatchPaymentDetailsParameters(PatchJSONParameters):
    # pylint: disable=abstract-method,missing-docstring
    OPERATION_CHOICES = (
        PatchJSONParameters.OP_REPLACE,
    )

    PATH_CHOICES = tuple(
        [
            '/%s' % field for field in
            (
                Payment.__table__.columns._data.keys()
            )
        ]
        +
        [
            '/attributes/%s' % field for field in
            (
                PaymentAttributes.__table__.columns._data.keys()
            )
        ]
    )

    @classmethod
    def replace(cls, obj, field, value, state):
        """
        Traverse the entity tree and update those values as required.
        :param obj:
        :param field:
        :param value:
        :param state:
        :return:
        """

        root = obj
        fields = field.split('/')

        while len(fields[:-1]) != 0:
            field = fields.pop(0)

            if not hasattr(root, field):
                raise ValidationError("Field '%s' does not exist, so it cannot be patched" % field)
            root = getattr(root, field)

        field = fields[-1]
        if not hasattr(root, field):
            raise ValidationError("Field '%s' does not exist, so it cannot be patched" % field)
        setattr(root, field, value)
        return True
