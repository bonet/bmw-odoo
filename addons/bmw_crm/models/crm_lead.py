from odoo import models, fields, api
import os
import requests
import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    linkedin_url = fields.Char(string="LinkedIn URL")
    linkedin_results = fields.One2many(
        'bmw.crm.linkedin.result', 'lead_id', string="LinkedIn Results"
    )

    def reload_linkedin_results(self):
        _logger.info("Reloading LinkedIn results")
        for record in self:
            if not record.partner_id:
                _logger.warning("No customer associated with this lead.")
                continue

            user_name = record.partner_id.name
            scraping_google_api_param = {
                'api_key': os.getenv('SCRAPING_GOOGLE_API_KEY'),
                'query': f'site:linkedin.com/in intitle:"{user_name}"',
                'results': 10,
                'country': 'us',
                'page': 0,
                'advance_search': 'false'
            }
            scraping_google_api_url = os.getenv('SCRAPING_GOOGLE_API_URL')
            scraping_google_api_response = requests.get(scraping_google_api_url, params=scraping_google_api_param).json()
            results = scraping_google_api_response['organic_results']
            record.linkedin_results.unlink()
            for result in results:
                record.linkedin_results.create({
                    'lead_id': record.id,
                    'title': result['title'],
                    'link': result['link'],
                })
