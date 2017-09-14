# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductConfigDomain(models.Model):
    _inherit = 'product.config.domain'

    @api.multi
    @api.depends('implied_ids')
    def _get_trans_implied(self):
        "Computes the transitive closure of relation implied_ids"

        def linearize(domains):
            trans_domains = domains
            for domain in domains:
                implied_domains = domain.implied_ids - domain
                if implied_domains:
                    trans_domains |= linearize(implied_domains)
            return trans_domains

        for domain in self:
            domain.trans_implied_ids = linearize(domain)

    name = fields.Char(
        string='Name',
        required=True,
        size=256,
        copy=True,
    )
    domain_line_ids = fields.One2many(
        comodel_name='product.config.domain.line',
        inverse_name='domain_id',
        string='Restrictions',
        required=True,
        copy=True,
    )
    implied_ids = fields.Many2many(
        comodel_name='product.config.domain',
        relation='product_config_domain_implied_rel',
        string='Inherited',
        column1='domain_id',
        column2='parent_id',
        copy=True,
    )
    trans_implied_ids = fields.Many2many(
        comodel_name='product.config.domain',
        compute=_get_trans_implied,
        column1='domain_id',
        column2='parent_id',
        string='Transitively inherits',
        copy=True,
    )


class ProductConfigDomainLine(models.Model):
    _inherit = 'product.config.domain.line'

    def _get_domain_conditions(self):
        operators = [
            ('in', 'In'),
            ('not in', 'Not In')
        ]

        return operators

    def _get_domain_operators(self):
        andor = [
            ('and', 'And'),
            ('or', 'Or'),
        ]

        return andor

    attribute_id = fields.Many2one(
        comodel_name='product.attribute',
        string='Attribute',
        required=True,
        copy=True, )

    domain_id = fields.Many2one(
        comodel_name='product.config.domain',
        required=True,
        string='Rule',
        copy=True, )

    condition = fields.Selection(
        selection=_get_domain_conditions,
        string="Condition",
        required=True,
        copy=True, )

    value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        relation='product_config_domain_line_attr_rel',
        column1='line_id',
        column2='attribute_id',
        string='Values',
        required=True,
        copy=True,
    )

    operator = fields.Selection(
        selection=_get_domain_operators,
        string='Operators',
        default='and',
        required=True,
        copy=True,
    )

    sequence = fields.Integer(
        string="Sequence",
        default=1,
        copy=True,
        help="Set the order of operations for evaluation domain lines"
    )


class ProductConfigLine(models.Model):
    _inherit = 'product.config.line'

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template',
        ondelete='cascade',
        required=True,
        copy=True,
    )

    attribute_line_id = fields.Many2one(
        comodel_name='product.attribute.line',
        string='Attribute Line',
        ondelete='cascade',
        required=True,
        copy=True,
    )

    attr_line_val_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        related='attribute_line_id.value_ids'
    )

    value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        id1="cfg_line_id",
        id2="attr_val_id",
        string="Values",
        copy=True,
    )

    domain_id = fields.Many2one(
        comodel_name='product.config.domain',
        required=True,
        string='Restrictions',
        copy=True,
    )

    sequence = fields.Integer(string='Sequence', default=10, copy=True)


class ProductConfigImage(models.Model):
    _inherit = 'product.config.image'

    name = fields.Char('Name', size=128, required=True, translate=True,
                       copy=True)

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product',
        ondelete='cascade',
        required=True,
        copy=True,
    )

    image = fields.Binary('Image', required=True, copy=True)

    sequence = fields.Integer(string='Sequence', default=10, copy=True)

    value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        string='Configuration',
        copy=True,
    )


class ProductConfigStep(models.Model):
    _inherit = 'product.config.step'

    name = fields.Char(
        string='Name',
        size=128,
        required=True,
        translate=True,
        copy=True,
    )


class ProductConfigStepLine(models.Model):
    _inherit = 'product.config.step.line'

    config_step_id = fields.Many2one(
        comodel_name='product.config.step',
        string='Configuration Step',
        required=True,
        copy=True,
    )
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template',
        ondelete='cascade',
        required=True,
        copy=True,
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        copy=True,
    )
