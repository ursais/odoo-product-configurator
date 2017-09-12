# -*- coding: utf-8 -*-

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def create_get_variant(self, value_ids, custom_values=None,
                           website_values={}):
        """Add bill of matrials to the configured variant."""
        if custom_values is None:
            custom_values = {}

        variant = super(ProductTemplate, self).create_get_variant(
            value_ids, custom_values=custom_values
        )
        # Prepare BoM lines and calculate product variant price
        wizard_values = {}
        line_vals = []
        price = 0

        if website_values:
            wizard_values = website_values
        else:
            wizard_values = self._context.get('wizard_values', {})

        for attribute_value in variant.attribute_value_ids:
            product_qty = wizard_values and int(
                wizard_values.get(attribute_value.id, 1)) or 1
            line_vals.append(
                (0, 0, {'product_id': attribute_value.product_id.id,
                        'product_qty': product_qty,
                        }))
            price += attribute_value.product_id.lst_price * (product_qty - 1)
        values = {
            'product_tmpl_id': self.id,
            'product_id': variant.id,
            'bom_line_ids': line_vals
        }
        # Set Variant price with new calculated Price and extra price as 0
        variant.list_price = price
        _logger.info("Variant price %s." % variant.lst_price)
        self.env['mrp.bom'].create(values)
        return variant
