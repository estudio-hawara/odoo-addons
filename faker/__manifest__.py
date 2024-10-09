{
    'name': 'Faker',
    'version': '18.0.0.0.1',
    'depends': ['base'],
    'author': 'Estudio Hawara <estudio@hawara.es>',
    'category': 'Administration',
    'description': 'Provides support to dynamically generate demo data',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/generator_views.xml',
        'views/generator_wizard_views.xml',
        'views/menu_items.xml'
    ],
    'extenal_dependencies': {
        'python': [
            'Faker'
        ]
    },
    'license': 'LGPL-3',
}