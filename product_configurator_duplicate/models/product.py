# -*- coding: utf-8 -*-
# Copyright (C) 2012 - TODAY, Ursa Information Systems
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    config_ok = fields.Boolean(string='Can be Configured', copy=True)

    config_line_ids = fields.One2many(
        comodel_name='product.config.line',
        inverse_name='product_tmpl_id',
        string="Attribute Dependencies",
        copy=True
    )

    config_image_ids = fields.One2many(
        comodel_name='product.config.image',
        inverse_name='product_tmpl_id',
        string='Configuration Images',
        copy=True
    )

    config_step_line_ids = fields.One2many(
        comodel_name='product.config.step.line',
        inverse_name='product_tmpl_id',
        string='Configuration Lines',
        copy=True
    )
    attribute_line_ids = fields.One2many(
        'product.attribute.line',
        'product_tmpl_id',
        'Product Attributes',
        copy=True)
