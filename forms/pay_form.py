from flask_wtf import Form
from wtforms import SubmitField, HiddenField


class PayForm(Form):
    amount = HiddenField()
    currency = HiddenField()
    shop_id = HiddenField()
    sign = HiddenField()
    shop_order_id = HiddenField()
    description = HiddenField()

    submit = SubmitField("Оплатить")
