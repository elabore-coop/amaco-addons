# -*- coding: utf-8 -*-

from odoo import models, api

class Lead(models.Model):
    _inherit="crm.lead"
    
    @api.depends('active')
    def archive_analytic_account(self):
        import pdb; pdb.set_trace()
        if self.analytic_account:
            self.analytic_account.active = self.active
    
    def write(self, vals):
        res = super(Lead, self).write(vals)
        import pdb; pdb.set_trace()
        if self.analytic_account:
            self.analytic_account.active = self.active
        return res