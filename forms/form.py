from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField, TextAreaField, ValidationError, IntegerField
from wtforms import validators


class ShopForm(Form):
    def amount_validate(form, field):
        if field.data < 0:
            raise ValidationError('Сумма должна быть больше 0.')

    def currency_validate(form, field):
        if field.data.upper() not in ["EUR", "USD", "RUB"]:
            raise ValidationError('Валюта должна быть EUR, USD или RUB.')

    payment_amount_first = IntegerField("Сумма оплаты: ", [
        validators.DataRequired("Пожалуйста введите сумму оплаты."),
        amount_validate
    ])

    currency_first = StringField("Валюта: ", [
        validators.DataRequired("Пожалуйста введите валюту."),
        currency_validate
    ])

    payment_amount_second = IntegerField("Сумма оплаты: ", [
        validators.DataRequired("Пожалуйста введите сумму оплаты."),
        amount_validate
    ])

    currency_second = SelectField("Валюта оплаты: ", [
        validators.DataRequired("Пожалуйста выберете валюту оплаты.")],
                                  choices=[
                                      (978, "EUR"),
                                      (840, "USD"),
                                      (643, "RUB")])

    product_description = TextAreaField("Описание товара: ", [
        validators.DataRequired("Пожалуйста введите описание товара."),
    ])

    submit = SubmitField("Оплатить")
