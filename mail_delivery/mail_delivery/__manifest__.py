# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Inherit',
    'version': '1.1',
    'category': 'Sales',
    'summary': 'Sales internal machinery',
    'description': """
This module contains all the common features of Sales Management and eCommerce.
    """,
    'depends': ['sale', 'mail'],
    'data': [
        'views/sale_inherit.xml',
        
    ],
   
       'installable': True,
    'auto_install': False,
}
