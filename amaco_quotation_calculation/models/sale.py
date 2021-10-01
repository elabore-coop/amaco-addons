# -*- coding: utf-8 -*-

from odoo import api, models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_hr = fields.Float('HR', required=True, digits='Product Price', default=0.0)
    price_fourniture = fields.Float('Fourniture', required=True, digits='Product Price', default=0.0)
    price_misc = fields.Float('Misc.', required=True, digits='Product Price', default=0.0)
    price_service = fields.Float('Service', required=True, digits='Product Price', default=0.0)
    apply_coeff = fields.Boolean('Apply Coeff', default=False)
 
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'price_hr', 'price_fourniture', 'price_misc', 'price_service', 'apply_coeff')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            input_price = line.price_unit + line.price_hr + line.price_fourniture + line.price_misc + line.price_service
            if line.apply_coeff:
                global_coeff = 1
                coeff_lines = self.env['quotation.coefficient'].search([])
                for coeff_line in coeff_lines:
                    global_coeff = global_coeff + coeff_line.coeff
                price = input_price * global_coeff * (1 - (line.discount or 0.0) / 100.0)
            else:
                price = input_price * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])


class QuotationCoefficient(models.Model):
    _name = 'quotation.coefficient'
    _description = 'Coefficients for the order line price calculation'

    name = fields.Text(string='Nom', required=True)
    description = fields.Text(string='Description', required=False)
    coeff = fields.Float(string='Coefficient', required=True, default=0.00)