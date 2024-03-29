# -*- coding: utf-8 -*-

from odoo import fields, models

class HrExpense(models.Model):
    _inherit = "hr.expense"

    # add check_company = False to allow multi company selection
    #analytic_account_id = fields.Many2one(required=True, check_company=False)
    employee_id = fields.Many2one(check_company=False)    
    project_id = fields.Many2one(check_company=False)


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    # add check_company = False to allow multi company selection 
    #analytic_account_id = fields.Many2one(check_company=False)
    employee_id = fields.Many2one(check_company=False)
    address_id = fields.Many2one(check_company=False)