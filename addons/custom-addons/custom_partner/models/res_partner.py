from odoo import models, fields, _, Command, api
import logging
import json

class ResPartner(models.Model):
    _inherit ='res.partner'
    
    custom_field=fields.Char(string='Custom Field')
    custom_compute = fields.Char(compute='_compute_custom_field')
    
    @api.depends('custom_field')
    def _compute_custom_field(self):
        for record in self:
            # this is a very long line to test the line length. Just adding random text here to see if I go far beyond the line length :)
            record.custom_compute=record.custom_field  
            
    
    
    def actionConfirmContactName(self):
        a = 3+6
        return True