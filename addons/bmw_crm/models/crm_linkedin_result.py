from odoo import models, fields
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

    def set_as_linkedin_url(self):
        _logger.info("Setting LinkedIn URL")
        for result in self:
            if result.lead_id:
                result.lead_id.linkedin_url = result.link