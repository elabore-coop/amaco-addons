# -*- coding: utf-8 -*-

from odoo import _, models, fields
from odoo.exceptions import UserError

AMACO_SOLLICITATION_PROJECT_ID = 1135

class Project(models.Model):
    _inherit = "project.project"

    team_id = fields.Many2one("crm.team", string=_("Pôle"))

    def unlink(self):
        if self.id == AMACO_SOLLICITATION_PROJECT_ID:
            raise UserError(_("It is a system project that cannot be deleted."))
        return super(Project, self).unlink()
