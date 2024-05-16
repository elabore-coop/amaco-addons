# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.http import request

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    def unlink(self):
        for event in self:
            if event.res_model == 'hr.leave':
                raise UserError(_('Cannot delete a leave in calendar event. Manage yours holidays in Leaves app'))
        return super().unlink()
              
    def write(self, values):
        for event in self :
            #if the only key in  param 'values' is 'active' that means that we come from the 'refuse' buton in Leave app. And in that case, we want to allow the modification
            if event.res_model == 'hr.leave' and list(values.keys()) != ['active']:
                raise UserError(_('Cannot modify a leave in calendar event. Manage yours holidays in Leaves app'))
        return super().write(values)

