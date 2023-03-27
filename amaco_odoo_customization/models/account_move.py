# -*- coding: utf-8 -*-

from odoo import fields, models, api
import logging


class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_origin = fields.Char(readonly=False)
    analytic_account_id = fields.Many2one('account.analytic.account', "Analytic account", compute="compute_analytic_account_id")
    
    @api.depends('invoice_line_ids')
    def compute_analytic_account_id(self):        
        """ Set Analytic account of invoice to value of analytic account of invoice line, if all the sames
        """
        for move in self:            
            # all not null analytic account ids of invoice lines
            lines_analytic_account_ids = [move_line.analytic_account_id.id for move_line in move.invoice_line_ids if move_line.analytic_account_id]
            # if all the same, set move.analytic_account_id
            if lines_analytic_account_ids and all(x == lines_analytic_account_ids[0] for x in lines_analytic_account_ids):
                move.analytic_account_id = lines_analytic_account_ids[0]
            else:
                move.analytic_account_id = None
            