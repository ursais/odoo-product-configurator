# -*- coding: utf-8 -*-

from odoo import models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def create_get_variant(self, value_ids, custom_values=None):
        """Add bill of matrials to the configured variant."""
        if custom_values is None:
            custom_values = {}

        variant = super(ProductTemplate, self).create_get_variant(
            value_ids, custom_values=custom_values
        )
        line_vals = [
            (0, 0, {'product_id': attribute_value.product_id.id,
                    'product_qty': self._context.get('wizard_values') and self._context.get('wizard_values').get(attribute_value.id,1) or 1
                    }) for attribute_value in variant.attribute_value_ids
        ]
        values = {
            'product_tmpl_id': self.id,
            'product_id': variant.id,
            'bom_line_ids': line_vals
        }
        self.env['mrp.bom'].create(values)

        return variant
