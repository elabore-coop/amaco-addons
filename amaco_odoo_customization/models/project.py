# -*- coding: utf-8 -*-

from odoo import _, models, fields
from odoo.addons.sale_timesheet.models.project_overview import _to_action_data
import json

class Project(models.Model):
    _inherit = "project.project"

    team_id = fields.Many2one("crm.team", string=_("Pôle"))

    def _plan_get_stat_button(self):
        stat_buttons = super()._plan_get_stat_button()
        if self.env.user.has_group('hr_expense.group_hr_expense_user'):
            stat_buttons.append({
                'name': _("Expenses"),
                'count': self.env['hr.expense'].search_count([('project_id', 'in', self.ids)]),
                'icon': 'fa fa-dollar',
                'action': _to_action_data(
                    'hr.expense',
                    domain=[('project_id', 'in', self.ids)],
                    context={'create': True, 'edit': True, 'delete': True}
                ),
            })
        return stat_buttons