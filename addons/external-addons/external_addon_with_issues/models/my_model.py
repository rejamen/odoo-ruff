from odoo import models, fields, _, Command
import logging
import json

class MyModel(models.Model):
    _name ='my.model'
    
    name=fields.Char(string='Name' ) 

