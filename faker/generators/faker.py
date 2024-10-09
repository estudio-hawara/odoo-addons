from faker import Faker

def clear_faker_fields(record):
    record.faker_generator = None
    record.faker_locale = None

def get_faker_generators():
    return [
        (method, method)
        for method in dir(Faker())
        if not method.startswith('_') and
            not method.startswith('get_') and
            not method.startswith('py') and
            not method.startswith('set_') and
            method not in [
                'add_provider', 'cache_pattern', 'del_arguments', 'enum', 'factories',
                'format', 'generator_attrs', 'get_formatter', 'items', 'locales', 'optional',
                'parse', 'provider', 'providers', 'random', 'seed', 'seed_instance', 'seed_locale',
                'tar', 'time_series', 'unique', 'xml', 'weights', 'zip'
            ]
        ]

def get_faked_value(record):
    if record.value_type != 'faker':
        raise Exception('A faked value cannot be created for this {} field'.format(record.value_type))

    if not record.faker_generator:
        return None

    locale = 'en_US' if not record.faker_locale else record.faker_locale.code
    faker = Faker(locale)
    generator = getattr(faker, record.faker_generator)
    return generator()