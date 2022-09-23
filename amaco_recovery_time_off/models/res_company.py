from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    recovery_time_ratio = fields.Float(string="Recoverty Time Ratio")
