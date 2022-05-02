# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrDepartureWizard(models.TransientModel):
    _inherit = "hr.departure.wizard"

    departure_reason = fields.Selection(
        selection_add=[
            ("contract_ended", "End of contract"),
            ("agreed_termination", "Mutually agreed termination of contract"),
        ],
        default="fired",
    )
