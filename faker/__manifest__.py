{
    'name': 'Faker',
    'version': '18.0.0.0.1',
    'license': 'LGPL-3',

    'description': 'Provides support to dynamically generate demo data',
    'author': 'Estudio Hawara <estudio@hawara.es>',
    'category': 'Administration',

    'depends': ['base'],
    'extenal_dependencies': {
        'python': [
            'Faker'
        ]
    },

    'data': [
        'security/ir.model.access.csv',
        'views/generator_views.xml',
        'views/generator_wizard_views.xml',
        'views/menu_items.xml'
    ],
    'demo': [
        'demo/corporations_from_uk.xml',
    ],
    'images': [
        'static/description/screenshots/screencast.gif',
        'static/description/screenshots/generator_screenshot.png',
        'static/description/screenshots/generator_wizard.png',
    ]
}