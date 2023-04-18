# -*- coding: utf-8 -*-

from odoo import _, models, fields, api

class SaleOrderTemplateLine(models.Model):
    _inherit = "sale.order.template.line"

    price_unit = fields.Float(string="Unit Price")
        