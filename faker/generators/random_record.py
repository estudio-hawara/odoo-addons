from odoo.tools.safe_eval import safe_eval
from odoo.addons.faker.wizard.generator_wizard import BatchInfo

def get_random_record(record, env):
    if not record.value_type == 'random_record':
        raise Exception('A random record cannot be created for this {} field'.format(record.value_type))

    if not record.field_id.relation:
        return None

    string_domain = '[]'
    if record.random_record_domain:
        string_domain = record.random_record_domain

    context = record.generator_id.generate(break_at=record)
    empty_record = record.generator_id.get_empty_record()
    locals_dict = {**empty_record, **context}
    domain = safe_eval(string_domain, locals_dict=locals_dict)

    model = env[record.field_id.relation]

    query = model._where_calc(domain)
    query.order = 'RANDOM()'
    query.limit = 1

    random_record = model._fetch_query(query, [])
    return random_record.id