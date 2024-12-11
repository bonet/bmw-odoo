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
                'private': 'false'
            }
            scraping_linkedin_api_url = os.getenv('SCRAPING_API_URL') + '/linkedin'
            scraping_linkedin_api_response = requests.get(scraping_linkedin_api_url, params=scraping_linkedin_api_param).json()
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
                'linkedin_preview_title': payload.get('title', ''),
                'linkedin_preview_link': payload.get('link', ''),
                'linkedin_preview_full_name': data.get('fullName', ''),
                'linkedin_preview_profile_photo_preview': utils.file.convert_url_to_base64(data.get('profile_photo', '')),
                'linkedin_preview_profile_photo': data.get('profile_photo', ''),
                'linkedin_preview_headline': data.get('headline', ''),
                'linkedin_preview_about': data.get('about', ''),
                'linkedin_preview_location': data.get('location', ''),
                'linkedin_preview_description1': data.get('description', {}).get('description1', ''),
                'linkedin_preview_description1_link': data.get('description', {}).get('description1_link', ''),
                'linkedin_preview_description2': data.get('description', {}).get('description2', ''),
                'linkedin_preview_description2_link': data.get('description', {}).get('description2_link', ''),
            })

            crm_lead_record.linkedin_preview_experiences.unlink()
            crm_lead_record.linkedin_preview_educations.unlink()

            for experience in data.get('experience', []):
                crm_lead_record.linkedin_preview_experiences.create({
                    'lead_id': crm_lead_record.id,
                    'position': experience.get('position', ''),
                    'company_name': experience.get('company_name', ''),
                    'company_url': experience.get('company_url', ''),
                    'location': experience.get('location', ''),
                    'starts_at': experience.get('starts_at', ''),
                    'duration': experience.get('duration', ''),
                })

            for education in data.get('education', []):
                crm_lead_record.linkedin_preview_educations.create({
                    'lead_id': crm_lead_record.id,
                    'college_name': education.get('college_name', ''),
                    'college_url': education.get('college_url', ''),
                    'college_degree': education.get('college_degree', ''),
                    'college_degree_field': education.get('college_degree_field', ''),
                    'college_duration': education.get('college_duration', ''),
                })

            return {"success": "Data updated successfully"}
        except Exception as e:
            raise e