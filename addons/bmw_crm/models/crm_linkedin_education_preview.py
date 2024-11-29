from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class CrmLinkedInEducationPreview(models.Model):
    _name = 'crm.linkedin.education.preview'
    _description = 'LinkedIn Education Preview'

    lead_id = fields.Many2one(
        'crm.lead',
        string="Lead",
        required=True,
        onupdate='cascade',
        ondelete='cascade',
    )
    college_name = fields.Char(string="College Name")
    college_url = fields.Char(string="College URL")
    college_degree = fields.Char(string="College Degree")
    college_degree_field = fields.Char(string="College Degree Field")
    college_duration = fields.Char(string="College Duration")
