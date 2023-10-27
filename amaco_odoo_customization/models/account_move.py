# -*- coding: utf-8 -*-

from odoo import fields, models, api
import logging


class AccountMove(models.Model):
    _inherit = "account.move"

    invoice_origin = fields.Char(readonly=False)
    analytic_account_id = fields.Many2one('account.analytic.account', "Analytic account", 
                                          compute="compute_analytic_account_id", 
                                          search="_search_analytic_account_id")
    
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
    
    def _search_analytic_account_id(self, operator, value):
        """
            search all move with analytic account match id : 
                - all move lines of the move having the same analytic account id
            to do this, check if averrage equals max of analytic_account_id
        """
        analytic_accounts = self.env['account.analytic.account'].name_search(value,operator=operator)
        if analytic_accounts:
            self.env.cr.execute("""select am.id, max(aml.analytic_account_id) m
                from account_move am left join account_move_line aml on aml.move_id = am.id 
                group by am.id
                having 
                max(aml.analytic_account_id) = avg(aml.analytic_account_id)
                and
                max(aml.analytic_account_id) in %s
                order by am.id
                """, [tuple([a[0] for a in analytic_accounts])])
            res = self.env.cr.fetchall()
            return [('id','in',[t[0] for t in res])]
        return [('id', 'in', [])]

    def set_default_sender(self, sender_id):
        '''
        in a invoice email template (such as "Facture: envoyer par email"), set a choosen user based on his ID
        '''
        return self.env['res.users'].browse(sender_id) or False