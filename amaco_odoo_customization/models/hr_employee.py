# -*- coding: utf-8 -*-

from odoo import fields, models


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    departure_reason = fields.Selection(
        [
            ("resigned", "Resigned"),
            (
                "agreed_termination",
                "Mutually agreed termination of contract",
            ),
            ("redudancy_firing", "Redudancy Firing"),
            (
                "personnal_firing",
                "Fired for personal reasons",
            ),
            ("retired", "Retired"),
            ("fixed_term_contract_ended", "End of fixed-term contract"),
            (
                "fixed_term_contract_agreed_termination",
                "Mutually agreed termination of fixed-term contract",
            ),
            (
                "transition_fixed_term_to_permanent_contract",
                "Transition from fixed-term to permanent contract",
            ),
            (
                "fixed_term_contract_other_termination",
                "End of fixed-term contract for other reasons",
            ),
            (
                "try_period_termination",
                "Try period termination",
            ),
        ],
    )
