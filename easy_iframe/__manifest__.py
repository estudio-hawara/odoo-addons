{
    'name': 'Easy iFrame',
    'version': '18.0.0.0.1',
    'license': 'LGPL-3',

    'description': 'Provides support to use Odoo\'s webforms in external websites via iframes',
    'author': 'Estudio Hawara <estudio@hawara.es>',
    'category': 'Administration',

    'depends': ['website'],

    'data': [
        'views/website_iframe.xml',
    ],
    'images': [
        'static/description/screenshots/screencast.gif',
    ],

    'installable': True,
    'application': False,
}