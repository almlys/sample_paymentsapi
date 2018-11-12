# encoding: utf-8
# pylint: disable=missing-docstring

import simplejson as json
import copy
import logging

log = logging.getLogger(__name__)


def create_new_payment(flask_app_client):
    """
    Test creation of a new payment
    :param flask_app_client:
    :return:
    """
    create_new_payment.payment_json_body = {
        "type": "Payment",
        "version": 0,
        "organisation_id": "743d5b63-8e6f-432e-a8fa-c5d8d2ee5fcb",
        "attributes": {
            "amount": 100.21,
            "beneficiary_party": {
                "account_name": "W Owens",
                "account_number": "31926819",
                "account_number_code": "BBAN",
                "account_type": 0,
                "address": "1 The Beneficiary Localtown SE2",
                "bank_id": "403000",
                "bank_id_code": "GBDSC",
                "name": "Wilfred Jeremiah Owens"
            },
            "charges_information": {
                "bearer_code": "SHAR",
                "sender_charges": [
                    {
                        "amount": 5.00,
                        "currency": "GBP"
                    },
                    {
                        "amount": 10.00,
                        "currency": "USD"
                    }
                ],
                "receiver_charges_amount": 1.00,
                "receiver_charges_currency": "USD"
            },
            "currency": "GBP",
            "debtor_party": {
                "account_name": "EJ Brown Black",
                "account_number": "GB29XABC10161234567801",
                "account_number_code": "IBAN",
                "address": "10 Debtor Crescent Sourcetown NE1",
                "bank_id": "203301",
                "bank_id_code": "GBDSC",
                "name": "Emelia Jane Brown"
            },
            "end_to_end_reference": "Wil piano Jan",
            "fx": {
                "contract_reference": "FX123",
                "exchange_rate": 2.00000,
                "original_amount": 200.42,
                "original_currency": "USD"
            },
            "numeric_reference": "1002001",
            "payment_id": "123456789012345678",
            "payment_purpose": "Paying for goods/services",
            "payment_scheme": "FPS",
            "payment_type": "Credit",
            "processing_date": "2017-01-18",
            "reference": "Payment for Em's piano lessons",
            "scheme_payment_sub_type": "InternetBanking",
            "scheme_payment_type": "ImmediatePayment",
            "sponsor_party": {
                "account_number": "56781234",
                "bank_id": "123123",
                "bank_id_code": "GBDSC"
            }
        }
    }

    response = flask_app_client.post(
        '/api/v1/payments/',
        content_type='application/json',
        data=json.dumps(create_new_payment.payment_json_body)
    )
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    payment_id = response.json['id']
    # Remove id as them will be different
    # Also remove other keys not present in the original request
    for key in ('id', 'updated', 'created'):
        del response.json[key]
    assert response.json == create_new_payment.payment_json_body
    return payment_id


def test_new_payment_creation(flask_app_client, db):
    """
    Tests payment has been correctly created within the DB.
    :param flask_app_client:
    :param db:
    :return:
    """

    payment_id = create_new_payment(flask_app_client)

    from app.modules.payments.models import Payment
    from app.modules.payments.schemas import BasePaymentSchema
    lookup_payment = Payment.query.get(payment_id)

    # Pass to json as original request is not coded using BigDecimal
    payment_test = json.loads(BasePaymentSchema().dumps(lookup_payment).data)
    del payment_test['id']
    assert create_new_payment.payment_json_body == payment_test


def test_update_existing_payment(flask_app_client, db):
    payment_id = create_new_payment(flask_app_client)

    response = flask_app_client.patch(
        '/api/v1/payments/%s' % (payment_id,),
        content_type='application/json',
        data=json.dumps([
            {
                'op': 'replace',
                'path': '/attributes/amount',
                'value': 200.0
            }
        ])
    )

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    assert response.json['id'] == payment_id

    check_original_payment = copy.deepcopy(create_new_payment.payment_json_body)
    check_original_payment['attributes']['amount'] = 200.0
    check_original_payment['id'] = payment_id

    # Also remove other keys not present in the original request
    for key in ('updated', 'created'):
        del response.json[key]

    assert check_original_payment == response.json

    # Now check against the DB
    from app.modules.payments.models import Payment
    from app.modules.payments.schemas import BasePaymentSchema
    lookup_payment = Payment.query.get(payment_id)

    # Pass to json as original request is not coded using BigDecimal
    payment_test = json.loads(BasePaymentSchema().dumps(lookup_payment).data)
    assert check_original_payment == payment_test



def test_remove_existing_payment(flask_app_client, db):
    payment_id = create_new_payment(flask_app_client)

    response = flask_app_client.delete(
        '/api/v1/payments/%s' % (payment_id,),
    )

    log.debug(response)
