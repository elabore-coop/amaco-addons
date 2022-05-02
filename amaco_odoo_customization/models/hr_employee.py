# -*- coding: utf-8 -*-

from odoo import fields, models


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    departure_reason = fields.Selection(
        selection_add=[
            ("contract_ended", "End of contract"),
            ("agreed_termination", "Mutually agreed termination of contract"),
        ],
    )
