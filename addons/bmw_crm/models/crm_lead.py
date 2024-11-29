from odoo import models, fields, api
from ... import utils
import os
import requests
import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    linkedin_results = fields.One2many('crm.linkedin.result', 'lead_id', string="LinkedIn Results")
    linkedin_preview_title = fields.Char(string="Title", readonly=True)
    linkedin_preview_link = fields.Char(string="Link", readonly=True)
    linkedin_preview_full_name = fields.Char(string="Full Name", readonly=True)
    linkedin_preview_profile_photo_preview = fields.Image(string="Profile Photo Preview", readonly=True)
    linkedin_preview_profile_photo = fields.Char(string="Profile Photo", readonly=True)
    linkedin_preview_headline = fields.Char(string="Headline", readonly=True)
    linkedin_preview_about = fields.Text(string="About", readonly=True)
    linkedin_preview_location = fields.Char(string="Location", readonly=True)
    linkedin_preview_description1 = fields.Text(string="Description 1", readonly=True)
    linkedin_preview_description1_link = fields.Char(string="Description 1 Link", readonly=True)
    linkedin_preview_description2 = fields.Text(string="Description 2", readonly=True)
    linkedin_preview_description2_link = fields.Char(string="Description 2 Link", readonly=True)
    linkedin_preview_experiences = fields.One2many('crm.linkedin.experience.preview', 'lead_id', string="Experiences")
    linkedin_preview_educations = fields.One2many('crm.linkedin.education.preview', 'lead_id', string="Educations")
    linkedin_url = fields.Char(string="LinkedIn URL")

    def reload_linkedin_results(self):
        _logger.info("Reloading LinkedIn results")
        for record in self:
            if not record.partner_id:
                _logger.warning("No customer associated with this lead.")
                continue

            record.linkedin_preview_title = None
            record.linkedin_preview_link = None
            record.linkedin_preview_full_name = None
            record.linkedin_preview_profile_photo_preview = None
            record.linkedin_preview_profile_photo = None
            record.linkedin_preview_headline = None
            record.linkedin_preview_about = None
            record.linkedin_preview_location = None
            record.linkedin_preview_description1 = None
            record.linkedin_preview_description1_link = None
            record.linkedin_preview_description2 = None
            record.linkedin_preview_description2_link = None
            record.linkedin_preview_experiences.unlink()
            record.linkedin_preview_educations.unlink()

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
                    'profile_photo_preview': utils.file.convert_url_to_base64(scraping_linkedin_result.get('profile_photo', '')),
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

    def set_as_linkedin_url(self):
        _logger.info("Setting as LinkedIn URL")
        for record in self:
            if record.linkedin_preview_link:
                record.linkedin_url = record.linkedin_preview_link