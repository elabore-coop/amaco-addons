# -*- coding: utf-8 -*-

from odoo import fields, models

class HrExpense(models.Model):
    _inherit = "hr.expense"

    analytic_account_id = fields.Many2one(required=True)
    