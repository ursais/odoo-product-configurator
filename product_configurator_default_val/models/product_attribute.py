# -*- coding: utf-8 -*-
# Copyright (C) 2012 - TODAY, Ursa Information Systems
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _


class ProductAttributeLine(models.Model):
    _inherit = 'product.attribute.line'

    @api.onchange('value_ids')
    def onchange_values(self):
        if self.default_val and self.default_val not in self.value_ids:
            self.default_val = None

    default_val = fields.Many2one(
        comodel_name='product.attribute.value',
        string='Default Value'
    )
