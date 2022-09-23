from odoo import _, api, fields, models


class RecoveryAllocationRequests(models.TransientModel):
    _name = "recovery.allocation.requests"
    _description = "Generate Recovery Allocations Requests"
    campaign_name = fields.Char('Campaign', required=True)
    date_from = fields.Datetime(
        string=_("Start Date"),
        required=True
    )
    date_to = fields.Datetime(
        string=_("End Date"),
        required=True
    )

    def generate_recovery_allocations(self):
        values = {}
        values["campaign_name"] = self.campaign_name
        values["date_from"] = self.date_from
        values["date_to"] = self.date_to
        employees = self.env["hr.employee"].search(
            [
                ("id", "in", self.env.context.get("active_ids")),
            ]
        )
        employees.generate_mass_recovery_allocations(values)
        # Open time-off allocation tree view
        return self.env["ir.actions.act_window"]._for_xml_id("hr_holidays.hr_leave_allocation_action_approve_department")
