from odoo import http
from odoo.http import request
from ... import utils
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
        
    @http.route('/crm-lead/linkedin/preview', auth='public', type='json')
    def preview_linkedin(self, **post):
        try:
            payload = json.loads(request.httprequest.data)
            link_id = payload.get('link_id', '')
            scraping_linkedin_api_param = {
                'api_key': os.getenv('SCRAPING_API_KEY'),
                'type': 'profile',
                'linkId': link_id,
                'private': 'true'
            }
            scraping_linkedin_api_url = os.getenv('SCRAPING_API_URL') + '/linkedin'
            scraping_linkedin_api_response = requests.get(scraping_linkedin_api_url, params=scraping_linkedin_api_param).json()
            _logger.info(scraping_linkedin_api_response)
            scraping_linkedin_result = None
            if isinstance(scraping_linkedin_api_response, list) and len(scraping_linkedin_api_response) > 0:
                scraping_linkedin_result = scraping_linkedin_api_response[0]
            
            return scraping_linkedin_result
        except Exception as e:
            raise e
        
    @http.route('/crm-lead/linkedin', auth='public', type='json')
    def insert_linkedin(self, **post):
        try:
            payload = json.loads(request.httprequest.data)
            crm_lead_record = request.env['crm.lead'].browse(payload.get('id', 0))
            if not crm_lead_record.exists():
                return {"error": "Record not found"}
            
            data = payload.get('data', {})
            crm_lead_record.write({
                'linkedin_title': payload.get('title', '') if payload.get('title', '') else 'N/A',
                'linkedin_link': payload.get('link', '') if payload.get('link', '') else 'N/A',
                'linkedin_full_name': data.get('fullName', '') if data.get('fullName', '') else 'N/A',
                'linkedin_profile_photo_preview': utils.file.convert_url_to_base64(data.get('profile_photo', '')),
                'linkedin_profile_photo': data.get('profile_photo', '') if data.get('profile_photo', '') else 'N/A',
                'linkedin_headline': data.get('headline', '') if data.get('headline', '') else 'N/A',
                'linkedin_about': data.get('about', '') if data.get('about', '') else 'N/A',
                'linkedin_location': data.get('location', '') if data.get('location', '') else 'N/A',
                'linkedin_description1': data.get('description', {}).get('description1', '') if data.get('description', {}).get('description1', '') else 'N/A',
                'linkedin_description1_link': data.get('description', {}).get('description1_link', '') if data.get('description', {}).get('description1_link', '') else 'N/A',
                'linkedin_description2': data.get('description', {}).get('description2', '') if data.get('description', {}).get('description2', '') else 'N/A',
                'linkedin_description2_link': data.get('description', {}).get('description2_link', '') if data.get('description', {}).get('description2_link', '') else 'N/A',
                'linkedin_url': payload.get('link', '') if payload.get('link', '') else 'N/A',
            })

            crm_lead_record.linkedin_experiences.unlink()
            crm_lead_record.linkedin_educations.unlink()

            for experience in data.get('experience', []):
                crm_lead_record.linkedin_experiences.create({
                    'lead_id': crm_lead_record.id,
                    'position': experience.get('position', '') if experience.get('position', '') else 'N/A',
                    'company_name': experience.get('company_name', '') if experience.get('company_name', '') else 'N/A',
                    'company_url': experience.get('company_url', '') if experience.get('company_url', '') else 'N/A',
                    'location': experience.get('location', '') if experience.get('location', '') else 'N/A',
                    'starts_at': experience.get('starts_at', '') if experience.get('starts_at', '') else 'N/A',
                    'duration': experience.get('duration', '') if experience.get('duration', '') else 'N/A',
                })

            for education in data.get('education', []):
                crm_lead_record.linkedin_educations.create({
                    'lead_id': crm_lead_record.id,
                    'college_name': education.get('college_name', '') if education.get('college_name', '') else 'N/A',
                    'college_url': education.get('college_url', '') if education.get('college_url', '') else 'N/A',
                    'college_degree': education.get('college_degree', '') if education.get('college_degree', '') else 'N/A',
                    'college_degree_field': education.get('college_degree_field', '') if education.get('college_degree_field', '') else 'N/A',
                    'college_duration': education.get('college_duration', '') if education.get('college_duration', '') else 'N/A',
                })

            return {"success": "Data updated successfully"}
        except Exception as e:
            raise e