# -*- coding: utf-8 -*-
# Copyright (C) 2012 - TODAY, Ursa Information Systems
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductAttributeValueLine(models.Model):
    _inherit = "product.attribute.value.line"

    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.user.company_id)
