from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class CrmLinkedInExperiencePreview(models.Model):
    _name = 'crm.linkedin.experience.preview'
    _description = 'LinkedIn Experience Preview'

    lead_id = fields.Many2one(
        'crm.lead',
        string="Lead",
        required=True,
        onupdate='cascade',
        ondelete='cascade',
    )
    position = fields.Char(string="Position")
    company_name = fields.Char(string="Company Name")
    company_url = fields.Char(string="Company URL")
    location = fields.Char(string="Location")
    starts_at = fields.Char(string="Starts At")
    duration = fields.Char(string="Duration")
