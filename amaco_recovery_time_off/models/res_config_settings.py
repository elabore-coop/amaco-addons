# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    recovery_time_ratio = fields.Float(string="Recoverty Time Ratio", related="company_id.recovery_time_ratio", readonly=False)

