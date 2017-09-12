# -*- coding: utf-8 -*-
# Copyright (C) 2012 - TODAY, Ursa Information Systems
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Ursa Product Attribute Value Multi-Company",
    "summary": "To support multi-company rule on attribute value",
    "version": "10.0.1.0.0",
    "license": "AGPL-3",
    "author": "Ursa Information Systems",
    "category": "Sales",
    "maintainer": "Ursa Information Systems",
    "website": "http://www.ursainfosystems.com",
    "depends": [
        "product_configurator",
        "product_configurator_refactor",
    ],
    "qweb": [
    ],
    "data": [
        "views/product_attribute_views.xml",
        "security/attribute_value_security.xml",
        "views/product_view.xml",
    ],
    "application": False,
}
