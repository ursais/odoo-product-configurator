# -*- coding: utf-8 -*-
# Copyright (C) 2012 - TODAY, Ursa Information Systems
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductAttributeValueLine(models.Model):
    _inherit = 'product.attribute.value.line'

    is_user_qty = fields.Boolean("User Defined Qty")
    default_qty = fields.Integer("Default Quantity", default=1)
    maximum_qty = fields.Integer("Maximum Quantity", default=1)

    @api.onchange('default_qty', 'maximum_qty')
    def onchange_user_qty(self):
        if self.default_qty < 0:
            self.default_qty = 0
        if self.maximum_qty < 0:
            self.maximum_qty = 0
