# -*- coding: utf-8 -*-

from odoo import _, models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _timesheet_create_project_prepare_values(self):
        values = super(SaleOrderLine, self)._timesheet_create_project_prepare_values()
        values["team_id"] = self.order_id.team_id.id
        return values
