from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    linkedin_title = fields.Char(string="Title", readonly=True)
    linkedin_link = fields.Char(string="Link", readonly=True)
    linkedin_full_name = fields.Char(string="Full Name", readonly=True)
    linkedin_profile_photo_preview = fields.Image(string="Profile Photo Preview", readonly=True)
    linkedin_profile_photo = fields.Char(string="Profile Photo", readonly=True)
    linkedin_headline = fields.Char(string="Headline", readonly=True)
    linkedin_about = fields.Text(string="About", readonly=True)
    linkedin_location = fields.Char(string="Location", readonly=True)
    linkedin_description1 = fields.Text(string="Description 1", readonly=True)
    linkedin_description1_link = fields.Char(string="Description 1 Link", readonly=True)
    linkedin_description2 = fields.Text(string="Description 2", readonly=True)
    linkedin_description2_link = fields.Char(string="Description 2 Link", readonly=True)
    linkedin_experiences_count = fields.Integer(string="Experiences Count", compute='_compute_linkedin_experiences_count')
    linkedin_experiences = fields.One2many('crm.linkedin.experience.preview', 'lead_id', string="Experiences")
    linkedin_educations_count = fields.Integer(string="Educations Count", compute='_compute_linkedin_educations_count')
    linkedin_educations = fields.One2many('crm.linkedin.education.preview', 'lead_id', string="Educations")
    linkedin_url = fields.Char(string="LinkedIn URL")

    def research_user_linkedin(self):
        pass

    @api.depends('linkedin_experiences')
    def _compute_linkedin_experiences_count(self):
        for record in self:
            record.linkedin_experiences_count = len(record.linkedin_experiences)

    @api.depends('linkedin_educations')
    def _compute_linkedin_educations_count(self):
        for record in self:
            record.linkedin_educations_count = len(record.linkedin_educations)