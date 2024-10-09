from random import randint
from faker import Faker

def clear_generated_rows_fields(record):
    record.row_generator_id = None
    record.row_count_min = None
    record.row_count_max = None

def get_generated_rows_value(record):
    if record.value_type != 'generated_rows':
        raise Exception('A generated row cannot be created for this {} field'.format(record.value_type))

    if not record.row_generator_id or not record.row_count_min or not record.row_count_max:
        return None

    row_count = randint(
        int(record.row_count_min),
        int(record.row_count_max)
    )

    rows = []
    for _ in range(0, row_count):
        generated = record.row_generator_id.generate()
        rows.append((0, 0, generated))

    return rows