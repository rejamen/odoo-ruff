from odoo import models, fields, _, Command
import logging
import json

class SaleOrder(models.Model):
    _inherit ='sale.order'
    
    custom_date=fields.Date()
    
    def action_set_date(self):
        self.custom_date=fields.Date.today()
        return True
     

