# -*- coding: utf-8 -*-

from odoo import _, models, fields, api
from datetime import timedelta


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    def _timesheet_create_project_prepare_values(self):
        values = super(SaleOrderLine, self)._timesheet_create_project_prepare_values()
        values["team_id"] = self.order_id.team_id.id
        return values
    
    def _timesheet_create_project(self):
        project = super()._timesheet_create_project()
        # when creating project at sale_order confirmation, link project to sale order
        project.sale_order_id.project_id = project.id
        return project
    


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sum_outstanding = fields.Monetary(string="Remains to be invoiced")
    sum_pending_work = fields.Monetary(string="Remains to be done")

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        """ WARNING !!!!
            Copy/paste of onchange_sale_order_template_id function in sale_management/sale_order.py
            No other solution to set good price unit on sale order lines

            Price unit is a new field on sale_order_template_line, to force price, not depending on product

            Only modification of this function is :
                price unit is set from template when template change

            For migration, rewrite all, from functionnal problem (above), depending on new Odoo Code.
        """

        if not self.sale_order_template_id:
            self.require_signature = self._get_default_require_signature()
            self.require_payment = self._get_default_require_payment()
            return

        template = self.sale_order_template_id.with_context(lang=self.partner_id.lang)

        # --- first, process the list of products from the template
        order_lines = [(5, 0, 0)]
        for line in template.sale_order_template_line_ids:
            data = self._compute_line_data_for_template_change(line)

            price = 0
            discount = 0

            if line.product_id:
                price = line.product_id.lst_price
                discount = 0

                if self.pricelist_id:
                    pricelist_price = self.pricelist_id.with_context(uom=line.product_uom_id.id).get_product_price(line.product_id, 1, False)

                    if self.pricelist_id.discount_policy == 'without_discount' and price:
                        discount = max(0, (price - pricelist_price) * 100 / price)
                    else:
                        price = pricelist_price

                data.update({
                    'product_id': line.product_id.id,
                    'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                })

            if line.price_unit:
                price = line.price_unit

            data.update({
                'price_unit': price,
                'discount': discount,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom_id.id,
            })

            order_lines.append((0, 0, data))

        self.order_line = order_lines
        self.order_line._compute_tax_id()

        # then, process the list of optional products from the template
        option_lines = [(5, 0, 0)]
        for option in template.sale_order_template_option_ids:
            data = self._compute_option_data_for_template_change(option)
            option_lines.append((0, 0, data))

        self.sale_order_option_ids = option_lines

        if template.number_of_days > 0:
            self.validity_date = fields.Date.context_today(self) + timedelta(template.number_of_days)

        self.require_signature = template.require_signature
        self.require_payment = template.require_payment

        if template.note:
            self.note = template.note