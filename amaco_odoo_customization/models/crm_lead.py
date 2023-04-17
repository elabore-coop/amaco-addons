# -*- coding: utf-8 -*-

from odoo import models, api
from odoo.exceptions import UserError

class Lead(models.Model):
    _inherit = "crm.lead"

    def write(self, vals):
        res = super(Lead, self).write(vals)
        #if self.analytic_account:
        #    self.analytic_account.active = self.active
        return res
    
    @api.model
    def create(self, vals_list):
        """On Lead creation, create a task on Sollicitation project
        """
        lead = super(Lead, self).create(vals_list)
        sollicitation_project_id = self.env['ir.config_parameter'].sudo().get_param('sollicitation_project_id')
        # set new context without default_stage_id to avoid error on create
        ctx = self.env.context.copy()
        if 'default_stage_id' in ctx:
            ctx.pop('default_stage_id')
        ctx['default_project_id'] = sollicitation_project_id
        project = self.env['project.task'].with_context(ctx).create({
            'project_id': int(sollicitation_project_id), 
            'name': lead.name
        })
        return lead        
        