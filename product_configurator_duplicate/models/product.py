# -*- coding: utf-8 -*-
# Copyright (C) 2012 - TODAY, Ursa Information Systems
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


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

    @api.multi
    def copy(self, defaults={}):
        for oldTemplate in self:
            newTemplate = super(ProductTemplate, oldTemplate).copy(defaults)
            # Set new config steps attribute lines
            for config_step in newTemplate.config_step_line_ids:
                new_attribute_line_ids = []
                for attrib_line in config_step.attribute_line_ids:
                    # Re-check attribute lines for this step
                    attrib_id = attrib_line.attribute_id.id
                    # Get original attribute line id for this attribute
                    new_attrib_line_id = newTemplate.attribute_line_ids.filtered(
                        lambda x: x.attribute_id.id == attrib_id)
                    if new_attrib_line_id:
                        new_attribute_line_ids.append(new_attrib_line_id.id)
                # Set this list of new attribute lines to config step
                config_step.attribute_line_ids = [
                    (6, 0, new_attribute_line_ids)]
            return newTemplate
