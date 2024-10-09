def get_value_types():
    return [
        ('faker', 'Faker'),
        ('constant', 'Constant'),
        ('random_record', 'Random record'),
        ('generated_rows', 'Generated rows'),
    ]

def get_typed_value(record, value):
    if value == None:
        return None

    if record.field_id.ttype in ('integer', 'many2one'):
        return int(value)

    if record.field_id.ttype == 'boolean':
        if str(value).lower() in ['true', '1']:
            return True
        if str(value).lower() in ['false', '0']:
            return False

    if record.field_id.ttype in ['char', 'text']:
        return str(value)

    return value