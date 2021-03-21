from flask_wtf import Form
from wtforms import SubmitField, HiddenField


class InvoiceForm(Form):
    ac_account_email = HiddenField()
    ac_amount = HiddenField()
    ac_currency = HiddenField()
    ac_fail_url = HiddenField()
    ac_order_id = HiddenField()
    ac_ps = HiddenField()
    ac_sci_name = HiddenField()
    ac_sign = HiddenField()
    ac_sub_merchant_url = HiddenField()
    ac_success_url = HiddenField()

    submit = SubmitField("Оплатить")
