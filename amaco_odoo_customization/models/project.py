# -*- coding: utf-8 -*-

from odoo import _, models, fields


class Project(models.Model):
    _inherit = "project.project"

    team_id = fields.Many2one("crm.team", string=_("Pôle"))
