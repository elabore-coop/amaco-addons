# -*- coding: utf-8 -*-
from datetime import datetime, time
from dateutil.rrule import rrule, DAILY
from pytz import UTC
from odoo import fields, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    def _calculate_number_eligible_days(self, values):
        nb_eligible_days = 0
        dfrom = datetime.combine(fields.Date.from_string(values["date_from"]), time.min).replace(tzinfo=UTC)
        dto = datetime.combine(fields.Date.from_string(values["date_to"]), time.max).replace(tzinfo=UTC)
        period_days = rrule(DAILY, dfrom, until=dto)
        calendar_resource = self.resource_calendar_id
        for day in period_days:
            # Check if this days is a working day
            if not calendar_resource.is_working_day(day):
                continue
            # The employee should work this day but...
            if not calendar_resource.is_full_working_day(day):
                # The recoverty time off is acquired only if the employee has worked the entire day 
                continue
            # Check leaves
            if not calendar_resource.is_worked_day(self, day):
                continue
            # The employee has worked this day but...
            if not calendar_resource.all_attendances_worked(self.resource_id, day):
                # The recoverty time off is acquired only if the employee has worked the entire day
                continue
            # All checks passed, the days is eligible for a voucher
            nb_eligible_days += 1
        return nb_eligible_days

    def generate_mass_recovery_allocations(self, values):
        for record in self:
            record.generate_recovery_allocation(values)

    def generate_recovery_allocation(self, values):
        self.ensure_one()
        nb_recovery_hours = self._calculate_number_eligible_days(values) * self.env.company.recovery_time_ratio
        # nb_recovery_days = nb_recovery_hours / self.resource_id.calendar_id.hours_per_day
        nb_recovery_days = nb_recovery_hours / 7 # Amaco calculation is based on a 35h week, then 7h/day.
        self.env['hr.leave.allocation'].create({
            'name': values["campaign_name"] + " - " + self.name,
            'holiday_status_id': self.env.ref("hr_holidays.holiday_status_comp").read()[0]["id"],
            'number_of_days': nb_recovery_days,
            'employee_id': self.id,
        })

    def action_recovery_requests_wizard(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "amaco_recovery_time_off.recovery_allocations_requests_wizard_action"
        )
        ctx = dict(self.env.context)
        ctx["active_ids"] = self.ids
        action["context"] = ctx
        return action