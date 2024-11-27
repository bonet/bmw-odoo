from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class LinkedInResult(models.Model):
    _name = 'bmw.crm.linkedin.result'
    _description = 'LinkedIn Search Result'

    lead_id = fields.Many2one('crm.lead', string="Lead", required=True)
    title = fields.Char(string="Title", required=True)
    link = fields.Char(string="Link", required=True)

    def set_as_linkedin_url(self):
        _logger.info("Setting LinkedIn URL")
        for result in self:
            if result.lead_id:
                result.lead_id.linkedin_url = result.link