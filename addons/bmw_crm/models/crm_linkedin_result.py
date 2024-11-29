from odoo import models, fields
from ... import utils
import logging

_logger = logging.getLogger(__name__)

class CrmLinkedInResult(models.Model):
    _name = 'crm.linkedin.result'
    _description = 'LinkedIn Search Result'

    lead_id = fields.Many2one(
        'crm.lead',
        string="Lead",
        required=True,
        onupdate='cascade',
        ondelete='cascade',
    )
    title = fields.Char(string="Title")
    link = fields.Char(string="Link")
    full_name = fields.Char(string="Full Name")
    profile_photo_preview = fields.Image(string="Profile Photo Preview")
    profile_photo = fields.Char(string="Profile Photo")
    headline = fields.Char(string="Headline")
    about = fields.Text(string="About")
    location = fields.Char(string="Location")
    description1 = fields.Text(string="Description 1")
    description1_link = fields.Char(string="Description 1 Link")
    description2 = fields.Text(string="Description 2")
    description2_link = fields.Char(string="Description 2 Link")
    experiences = fields.One2many('crm.linkedin.experience.result', 'linkedin_result_id', string="Experiences")
    educations = fields.One2many('crm.linkedin.education.result', 'linkedin_result_id', string="Educations")

    def set_as_linkedin_preview(self):
        _logger.info("Setting as LinkedIn preview")
        for result in self:
            if result.lead_id:
                result.lead_id.linkedin_preview_title = result.title
                result.lead_id.linkedin_preview_link = result.link
                result.lead_id.linkedin_preview_full_name = result.full_name
                result.lead_id.linkedin_preview_profile_photo_preview = utils.file.convert_url_to_base64(result.profile_photo)
                result.lead_id.linkedin_preview_profile_photo = result.profile_photo
                result.lead_id.linkedin_preview_headline = result.headline
                result.lead_id.linkedin_preview_about = result.about
                result.lead_id.linkedin_preview_location = result.location
                result.lead_id.linkedin_preview_description1 = result.description1
                result.lead_id.linkedin_preview_description1_link = result.description1_link
                result.lead_id.linkedin_preview_description2 = result.description2
                result.lead_id.linkedin_preview_description2_link = result.description2_link
                result.lead_id.linkedin_preview_experiences.unlink()
                for experience in result.experiences:
                    result.lead_id.linkedin_preview_experiences.create({
                        'lead_id': result.lead_id.id,
                        'position': experience.position,
                        'company_name': experience.company_name,
                        'company_url': experience.company_url,
                        'location': experience.location,
                        'starts_at': experience.starts_at,
                        'duration': experience.duration,
                    })
                result.lead_id.linkedin_preview_educations.unlink()
                for education in result.educations:
                    result.lead_id.linkedin_preview_educations.create({
                        'lead_id': result.lead_id.id,
                        'college_name': education.college_name,
                        'college_url': education.college_url,
                        'college_degree': education.college_degree,
                        'college_degree_field': education.college_degree_field,
                        'college_duration': education.college_duration,
                    })
                