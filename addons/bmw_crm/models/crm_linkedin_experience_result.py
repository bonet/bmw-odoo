from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class CrmLinkedInExperienceResult(models.Model):
    _name = 'crm.linkedin.experience.result'
    _description = 'LinkedIn Experience Result'

    linkedin_result_id = fields.Many2one(
        'crm.linkedin.result',
        string="LinkedIn Result",
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
