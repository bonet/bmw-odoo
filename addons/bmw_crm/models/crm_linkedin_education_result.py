from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class CrmLinkedInEducationResult(models.Model):
    _name = 'crm.linkedin.education.result'
    _description = 'LinkedIn Education Result'

    linkedin_result_id = fields.Many2one(
        'crm.linkedin.result',
        string="LinkedIn Result",
        required=True,
        onupdate='cascade',
        ondelete='cascade',
    )
    college_name = fields.Char(string="College Name")
    college_url = fields.Char(string="College URL")
    college_degree = fields.Char(string="College Degree")
    college_degree_field = fields.Char(string="College Degree Field")
    college_duration = fields.Char(string="College Duration")
