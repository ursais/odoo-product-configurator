# -*- coding: utf-8 -*-
# Copyright (C) 2012 - TODAY, Ursa Information Systems
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    
    attribute_line_id = fields.Many2one('product.attribute.line',
                                    'Product Attribute')

    @api.multi
    def name_get(self):
        res = []
        for value in self:
            name = value.name
            if self._context.get('show_price'):
                # Get Currency symbol
                currency_id = value.product_id.product_tmpl_id.company_id.currency_id
                name = '%s (%s%s)' % (
                value.name, currency_id.symbol, value.product_id.lst_price)
            res.append((value.id, name))
        return res


class ProductAttributeLine(models.Model):
    _inherit = 'product.attribute.line'

    @api.multi
    def _get_attribute_values(self):
        for line in self:
            attribute_value_ids = line.value_idss.mapped('attrib_value_id')
            if attribute_value_ids:
                line.value_ids = [(6, 0, attribute_value_ids.ids)]

    value_idss = fields.One2many('product.attribute.value.line',
                                 'attribute_line_id', 'Values', copy=True)
    value_ids = fields.Many2many(compute='_get_attribute_values',
                                 comodel_name='product.attribute.value',
                                 string='Attribute Values')
    default_val = fields.Many2one('product.attribute.value',
                                  compute='_get_default_value',
                                  string="Default Value")
    default_val_ids = fields.One2many('product.attribute.value',
                                      'attribute_line_id',
                                  compute='_is_default_value',
                                  string="Default Value")

    def _get_default_value(self):
        for line in self:
            default_attribute_ids = [value_line.attrib_value_id.id for value_line in
                         line.value_idss if value_line.company_id == self.env.user.company_id and value_line.is_default]
            if default_attribute_ids:
                line.default_val = default_attribute_ids[0]

    @api.depends('value_idss.is_default')
    def _is_default_value(self):
        for line in self:
            default_lines = [default for default in
                             line.value_idss.mapped('is_default') if default]
    
            # Company vise default attribute value
            def_company_attrib_dict = {}
            if default_lines:
                for value in line.value_idss:
                    if value.is_default:
                        if value.company_id.id not in def_company_attrib_dict:
                            def_company_attrib_dict.update({value.company_id.id:value.attrib_value_id.id})
                        else:
                            raise ValidationError(_("Default Attribute %s is already available for company %s!"%(value.attrib_value_id.name, value.company_id.name)))
                # Enter default value company wise to default_value_ids
                default_list = []
                for element in def_company_attrib_dict:
                    default_list.append((4, def_company_attrib_dict.get(element)))
                line.default_val_ids = default_list

    @api.multi
    @api.constrains('value_ids', 'default_val')
    def _check_default_values(self):
        return True
