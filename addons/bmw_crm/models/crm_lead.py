from odoo import fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    linkedin_url = fields.Char(string="LinkedIn URL")
