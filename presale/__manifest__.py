{
    'name': "Presale Orders",
    'version': '16.0.1.0.0',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'security/presale_security.xml',
        'views/presale_order_views.xml',
        'views/sale_order_views.xml',
        'views/presale_menus.xml',
        'data/presale_order_sequence.xml',
        'data/email_template.xml',
        'data/archive_presale_orders_cron.xml'
    ],
    'author': "Odoo PS",
    'license': 'LGPL-3',
    'category': 'Sales',
    'description': """
        This module is to add the presale orders feature to the current sales module
    """,
    'installable': True,
    'application': False,
    'auto_install': True
}
