from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

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

    @api.onchange('linkedin_preview_link')
    def onchange(self):
        _logger.info("Onchange")

    def load_linkedin(self):
        pass

    def set_as_linkedin_url(self):
        _logger.info("Setting as LinkedIn URL")
        for record in self:
            if record.linkedin_preview_link:
                record.linkedin_url = record.linkedin_preview_link