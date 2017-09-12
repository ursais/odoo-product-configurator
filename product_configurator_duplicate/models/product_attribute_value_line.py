# -*- coding: utf-8 -*-
# Copyright (C) 2012 - TODAY, Ursa Information Systems
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductAttributeValueLine(models.Model):
    _inherit = 'product.attribute.value.line'

    attribute_line_id = fields.Many2one('product.attribute.line',
                                        'Product Attribute',
                                        copy=True)
    attrib_value_id = fields.Many2one('product.attribute.value',
                                      'Attribute Value',
                                      copy=True)
    is_default = fields.Boolean("Is Default", copy=True)
    is_user_qty = fields.Boolean("User Defined Qty", copy=True)
    default_qty = fields.Integer("Default Quantity", default=1, copy=True)
    maximum_qty = fields.Integer("Maximum Quantity", default=1, copy=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.user.company_id,
                                 copy=True)
