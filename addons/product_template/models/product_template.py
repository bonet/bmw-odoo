from odoo import models, fields, api
import os
import requests
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    usd_sales_price = fields.Float(
        string="Sales Price (USD)", 
        compute='_compute_usd_sales_price', 
        store=True,
        readonly=True
    )

    @api.depends('list_price')
    def _compute_usd_sales_price(self):
        _logger.info('Computing sales price in USD')
        for product in self:
            currency_api_param = {
                'apikey': os.getenv('CURRENCY_API_KEY'),
                'currencies': 'USD',
                'base_currency': 'IDR'
            }
            currency_api_url = os.getenv('CURRENCY_API_URL')
            currency_api_response = requests.get(currency_api_url, params=currency_api_param).json()
            currency_usd = currency_api_response['data']['USD']['value']
            product.usd_sales_price = product.list_price * currency_usd
