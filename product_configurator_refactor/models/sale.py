# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    config_bom_id = fields.Many2one('mrp.bom', string="Config. BoM")
