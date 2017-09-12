# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductAttributeLine(models.Model):
    _inherit = 'product.attribute.line'

    product_tmpl_id = fields.Many2one('product.template', 'Product Template',
                                      ondelete='cascade', required=True,
                                      copy=True)
    attribute_id = fields.Many2one('product.attribute', 'Attribute',
                                   ondelete='restrict', required=True,
                                   copy=True)

    custom = fields.Boolean(
        string='Custom',
        copy=True,
        help="Allow custom values for this attribute?"
    )
    required = fields.Boolean(
        string='Required',
        copy=True,
        help="Is this attribute required?"
    )
    multi = fields.Boolean(
        string='Multi',
        copy=True,
        help='Allow selection of multiple values for this attribute?'
    )
    sequence = fields.Integer(string='Sequence', default=10, copy=True)
    default_val = fields.Many2one(
        comodel_name='product.attribute.value',
        string='Default Value',
        copy=True
    )
    value_idss = fields.One2many('product.attribute.value.line',
                                 'attribute_line_id', 'Values', copy=True)
    default_val = fields.Many2one('product.attribute.value',
                                  compute='_get_default_value',
                                  string="Default Value",
                                  copy=True)
    default_val_ids = fields.One2many('product.attribute.value',
                                      'attribute_line_id',
                                      compute='_is_default_value',
                                      string="Default Value",
                                      copy=True)

    def _get_default_value(self):
        for line in self:
            default_attribute_ids = [value_line.attrib_value_id.id for
                                     value_line in
                                     line.value_idss if
                                     value_line.company_id == self.env.user.company_id and value_line.is_default]
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
                            def_company_attrib_dict.update({
                                value.company_id.id: value.attrib_value_id.id})
                        else:
                            raise ValidationError(_(
                                "Default Attribute %s is already available for company %s!" % (
                                    value.attrib_value_id.name,
                                    value.company_id.name)))
                # Enter default value company wise to default_value_ids
                default_list = []
                for element in def_company_attrib_dict:
                    default_list.append(
                        (4, def_company_attrib_dict.get(element)))
                line.default_val_ids = default_list


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    active = fields.Boolean(
        string='Active',
        default=True,
        copy=True,
        help='By unchecking the active field you can '
             'disable a attribute value without deleting it'
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Related Product',
        copy=True
    )
    attribute_line_id = fields.Many2one('product.attribute.line',
                                        'Product Attribute',
                                        copy=True)


class ProductAttributeValueCustom(models.Model):
    _inherit = 'product.attribute.value.custom'

    name = fields.Char(
        string='Name',
        readonly=True,
        compute="_compute_val_name",
        store=True,
        copy=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product ID',
        required=True,
        copy=True,
        ondelete='cascade'
    )
    attribute_id = fields.Many2one(
        comodel_name='product.attribute',
        string='Attribute',
        required=True,
        copy=True,
    )
    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        relation='product_attr_val_custom_value_attachment_rel',
        column1='attr_val_custom_id',
        column2='attachment_id',
        string='Attachments',
        copy=True,
    )
    value = fields.Char(
        string='Custom Value',
        copy=True,
    )
