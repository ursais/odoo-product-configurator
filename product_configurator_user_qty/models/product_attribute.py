# -*- coding: utf-8 -*-
# Copyright (C) 2012 - TODAY, Ursa Information Systems
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _


class ProductAttributeLine(models.Model):
    _inherit = 'product.attribute.line'

    user_qty = fields.Boolean(compute='_is_user_qty',
                                  string="User Qty", store=True)

    @api.depends('value_idss.is_user_qty')
    def _is_user_qty(self):
        for line in self:
            user_qty_lines = [user_qty for user_qty in
                             line.value_idss.mapped('is_user_qty') if user_qty]
            if user_qty_lines:
                line.user_qty = True
            else:
                line.user_qty = False
