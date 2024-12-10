from odoo import http
from odoo.http import request
import os
import json
import requests
import logging

_logger = logging.getLogger(__name__)

class CrmLeadController(http.Controller):
    @http.route('/crm-lead/linkedin/load', auth='public', type='json')
    def load_linkedin(self, **post):
        try:
            payload = json.loads(request.httprequest.data)
            user_name = payload.get('partner_name', '')
            scraping_google_api_param = {
                'api_key': os.getenv('SCRAPING_API_KEY'),
                'query': f'site:linkedin.com/in intitle:"{user_name}"',
                'results': 10,
                'country': 'us',
                'page': 0,
                'advance_search': 'false'
            }
            scraping_google_api_url = os.getenv('SCRAPING_API_URL') + '/google'
            scraping_google_api_response = requests.get(scraping_google_api_url, params=scraping_google_api_param).json()
            scraping_google_results = scraping_google_api_response.get('organic_results', [])
            
            return scraping_google_results
        except Exception as e:
            raise e