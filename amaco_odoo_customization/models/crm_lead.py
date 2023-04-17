# -*- coding: utf-8 -*-

from odoo import models, api


class Lead(models.Model):
    _inherit = "crm.lead"

    def write(self, vals):
        res = super(Lead, self).write(vals)
        #if self.analytic_account:
        #    self.analytic_account.active = self.active
        return res
