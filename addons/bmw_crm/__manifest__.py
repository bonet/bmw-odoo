{
    'name': "BMW CRM",
    'version': '1.0',
    'depends': ['crm'],
    'data': [
        'views/crm_lead_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
