import datetime
import hashlib
import logging

import requests
from flask import Flask, render_template, request, redirect

from forms.form import ShopForm
from forms.invoice_form import InvoiceForm
from forms.pay_form import PayForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_string'

shop_id = 5
secretKey = "SecretKey01"
payway = "advcash_rub"  # (для invoice)
shop_order_id = 101


def sign_generation(*args):
    items = list(map(lambda x: str(x), args))
    sha_str = ":".join(items) + secretKey
    hex_str = hashlib.sha256(bytes(sha_str, encoding='utf-8')).hexdigest()
    return hex_str


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ShopForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('shop_form.html', form=form, form_name="Новая оплата", action="",
                                   participant=None)

        if form.currency_second.data == "978":  # EUR
            logging.info("currency - {}, amount - {}, time - {}, "
                         "description - {}".format(form.currency_second.data,
                                                   form.payment_amount_second.data,
                                                   datetime.datetime.now().strftime("%H:%M:%S"),
                                                   form.product_description.data
                                                   ))
            payment_amount = "%.2f" % form.payment_amount_second.data
            sign = sign_generation(payment_amount, form.currency_second.data, shop_id, shop_order_id)
            pay_form = PayForm()
            pay_form.amount.data = payment_amount
            pay_form.currency.data = form.currency_second.data
            pay_form.shop_id.data = shop_id
            pay_form.sign.data = sign
            pay_form.shop_order_id.data = shop_order_id
            pay_form.description.data = form.product_description.data

            return render_template('pay_form.html', form=pay_form, form_name="Подтверждание оплаты",
                                   action="https://pay.piastrix.com/ru/pay")

        elif form.currency_second.data == "840":  # USD
            payment_amount = "%.2f" % form.payment_amount_second.data
            sign = sign_generation(form.currency_second.data, payment_amount, form.currency_second.data, shop_id,
                                   shop_order_id,
                                   )
            request_params = {
                "description": form.product_description.data,
                "payer_currency": form.currency_second.data,
                "shop_amount": payment_amount,
                "shop_currency": form.currency_second.data,
                "shop_id": shop_id,
                "shop_order_id": shop_order_id,
                "sign": sign
            }
            answ = requests.post('https://core.piastrix.com/bill/create', json=request_params).json()

            if answ['error_code'] == 0:
                logging.info("currency - {}, amount - {}, time - {}, "
                             "description - {}".format(form.currency_second.data,
                                                       form.payment_amount_second.data,
                                                       datetime.datetime.now().strftime("%H:%M:%S"),
                                                       form.product_description.data
                                                       ))
                return redirect(answ["data"]["url"])
            else:
                logging.warning("currency - {}, amount - {}, time - {}, "
                                "description - {}, message".format(form.currency_second.data,
                                                                   form.payment_amount_second.data,
                                                                   datetime.datetime.now().strftime("%H:%M:%S"),
                                                                   form.product_description.data,
                                                                   answ['message']
                                                                   ))

        else:  # RUB
            payment_amount = "%.2f" % form.payment_amount_second.data
            sign = sign_generation(payment_amount, form.currency_second.data, payway, shop_id, shop_order_id)

            request_params = {
                "currency": form.currency_second.data,
                "sign": sign,
                "payway": payway,
                "amount": payment_amount,
                "shop_id": shop_id,
                "shop_order_id": shop_order_id,
            }
            answ = requests.post('https://core.piastrix.com/invoice/create', json=request_params).json()

            if answ['error_code'] == 0:
                logging.info("currency - {}, amount - {}, time - {}, "
                             "description - {}".format(form.currency_second.data,
                                                       form.payment_amount_second.data,
                                                       datetime.datetime.now().strftime("%H:%M:%S"),
                                                       form.product_description.data
                                                       ))
                invoice_form = InvoiceForm()
                invoice_form.ac_account_email.data = answ["data"]["data"]["ac_account_email"]
                invoice_form.ac_amount.data = answ["data"]["data"]["ac_amount"]
                invoice_form.ac_currency.data = answ["data"]["data"]["ac_currency"]
                invoice_form.ac_fail_url.data = answ["data"]["data"]["ac_fail_url"]
                invoice_form.ac_order_id.data = answ["data"]["data"]["ac_order_id"]
                invoice_form.ac_ps.data = answ["data"]["data"]["ac_ps"]
                invoice_form.ac_sci_name.data = answ["data"]["data"]["ac_sci_name"]
                invoice_form.ac_sign.data = answ["data"]["data"]["ac_sign"]
                invoice_form.ac_sub_merchant_url.data = answ["data"]["data"]["ac_sub_merchant_url"]
                invoice_form.ac_success_url.data = answ["data"]["data"]["ac_success_url"]

                return render_template('pay_form.html', form=invoice_form, form_name="Подтверждание оплаты",
                                       action=answ["data"]["url"])
            else:
                logging.warning("currency - {}, amount - {}, time - {}, "
                                "description - {}, message".format(form.currency_second.data,
                                                                   form.payment_amount_second.data,
                                                                   datetime.datetime.now().strftime("%H:%M:%S"),
                                                                   form.product_description.data,
                                                                   answ['message']
                                                                   ))

    return render_template('shop_form.html', form=form, form_name="Новая оплата", action="")


if __name__ == '__main__':
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True
    logging.basicConfig(filename=f'logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    app.run()
