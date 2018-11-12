# encoding: utf-8
# pylint: disable=bad-continuation
"""
RESTful API Payments resources
--------------------------
"""

import logging

from flask_login import current_user
from flask_restplus_patched import Resource
from flask_restplus._http import HTTPStatus

from app.extensions import db
from app.extensions.api import Namespace, abort
from app.extensions.api.parameters import PaginationParameters


from . import parameters, schemas
from .models import Payment


log = logging.getLogger(__name__)  # pylint: disable=invalid-name
api = Namespace('payments', description="Payments")  # pylint: disable=invalid-name


@api.route('/')
class Payments(Resource):
    """
    Manipulations with Payments.
    """

    @api.parameters(PaginationParameters())
    @api.response(schemas.BasePaymentSchema(many=True))
    def get(self, args):
        """
        List of Payment.

        Returns a list of Payment starting from ``offset`` limited by ``limit``
        parameter.
        """
        return Payment.query.offset(args['offset']).limit(args['limit'])

    @api.parameters(parameters.CreatePaymentParameters())
    @api.response(schemas.DetailedPaymentSchema())
    @api.response(code=HTTPStatus.CONFLICT)
    def post(self, args):
        """
        Create a new instance of Payment.
        """
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to create a new Payment"
            ):
            payment = Payment(**args)
            db.session.add(payment)
        return payment


@api.route('/<payment_id>')
@api.response(
    code=HTTPStatus.NOT_FOUND,
    description="Payment not found.",
)
@api.resolve_object_by_model(Payment, 'payment')
class PaymentByID(Resource):
    """
    Manipulations with a specific Payment.
    """

    @api.response(schemas.DetailedPaymentSchema())
    def get(self, payment):
        """
        Get Payment details by ID.
        """
        return payment

    @api.parameters(parameters.PatchPaymentDetailsParameters())
    @api.response(schemas.DetailedPaymentSchema())
    @api.response(code=HTTPStatus.CONFLICT)
    def patch(self, args, payment):
        """
        Patch Payment details by ID.
        """
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to update Payment details."
            ):
            parameters.PatchPaymentDetailsParameters.perform_patch(args, obj=payment)
            db.session.merge(payment)
        return payment

    @api.response(code=HTTPStatus.CONFLICT)
    @api.response(code=HTTPStatus.NO_CONTENT)
    def delete(self, payment):
        """
        Delete a Payment by ID.
        """
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to delete the Payment."
            ):
            db.session.delete(payment)
        return None
