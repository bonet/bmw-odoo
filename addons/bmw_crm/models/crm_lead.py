from odoo import models, fields, api
import os
import requests
import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    linkedin_url = fields.Char(string="LinkedIn URL")
    linkedin_results = fields.One2many(
        'crm.linkedin.result', 'lead_id', string="LinkedIn Results"
    )

    def reload_linkedin_results(self):
        _logger.info("Reloading LinkedIn results")
        for record in self:
            if not record.partner_id:
                _logger.warning("No customer associated with this lead.")
                continue

            user_name = record.partner_id.name
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
            record.linkedin_results.unlink()
            for scraping_google_result in scraping_google_results:
                scraping_linkedin_api_param = {
                    'api_key': os.getenv('SCRAPING_API_KEY'),
                    'type': 'profile',
                    'linkId': scraping_google_result.get('link', '').split('/')[-1],
                    'private': 'false'
                }
                scraping_linkedin_api_url = os.getenv('SCRAPING_API_URL') + '/linkedin'
                scraping_linkedin_api_response = requests.get(scraping_linkedin_api_url, params=scraping_linkedin_api_param).json()
                scraping_linkedin_result = {}
                if isinstance(scraping_linkedin_api_response, list) and len(scraping_linkedin_api_response) > 0:
                    scraping_linkedin_result = scraping_linkedin_api_response[0]

                linkedin_result = record.linkedin_results.create({
                    'lead_id': record.id,
                    'title': scraping_google_result.get('title', ''),
                    'link': scraping_google_result.get('link', ''),
                    'full_name': scraping_linkedin_result.get('fullName', ''),
                    'profile_photo': scraping_linkedin_result.get('profile_photo', ''),
                    'headline': scraping_linkedin_result.get('headline', ''),
                    'about': scraping_linkedin_result.get('about', ''),
                    'location': scraping_linkedin_result.get('location', ''),
                    'description1': scraping_linkedin_result.get('description', {}).get('description1', ''),
                    'description1_link': scraping_linkedin_result.get('description', {}).get('description1_link', ''),
                    'description2': scraping_linkedin_result.get('description', {}).get('description2', ''),
                    'description2_link': scraping_linkedin_result.get('description', {}).get('description2_link', ''),
                })
                for experience in scraping_linkedin_result.get('experience', []):
                    linkedin_result.experiences.create({
                        'linkedin_result_id': linkedin_result.id,
                        'position': experience.get('position', ''),
                        'company_name': experience.get('company_name', ''),
                        'company_url': experience.get('company_url', ''),
                        'location': experience.get('location', ''),
                        'starts_at': experience.get('starts_at', ''),
                        'duration': experience.get('duration', ''),
                    })
                for education in scraping_linkedin_result.get('education', []):
                    linkedin_result.educations.create({
                        'linkedin_result_id': linkedin_result.id,
                        'college_name': education.get('college_name', ''),
                        'college_url': education.get('college_url', ''),
                        'college_degree': education.get('college_degree', ''),
                        'college_degree_field': education.get('college_degree_field', ''),
                        'college_duration': education.get('college_duration', ''),
                    })
