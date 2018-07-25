# -*- coding: utf-8 -*-
{
    'name': "jwt_provider",

    'summary': """
        Provide a simple rest using jwt for odoo 11""",

    'description': """
        Key features:
         - jwt supported
         - Login via endpoint
    """,

    'author': "qnts",
    'website': "http://github.com/qnts",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web'],

    'external_dependencies': {
        'python': ['jwt'],
    },

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}