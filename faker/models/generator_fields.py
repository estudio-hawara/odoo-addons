from faker import Faker
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.addons.faker.generators.types import get_value_types, get_typed_value
from odoo.addons.faker.generators.constant import clear_constant_fields
from odoo.addons.faker.generators.faker import get_faker_generators, clear_faker_fields, get_faked_value
from odoo.addons.faker.generators.generated_rows import get_generated_rows_value, clear_generated_rows_fields
from odoo.addons.faker.generators.random_record import get_random_record

class GeneratorFields(models.Model):
    _name = 'faker.generator.fields'
    _description = 'Fields of each faker generator'
    _order = 'sequence'
    _sql_constraints = [
        ('unique_field_per_generator', 'unique(generator_id, field_id)', 'A field cannot be added twice to the same generator.'),
    ]

    def default_faker_locale(self):
        return self.generator_id.faker_locale

    sequence = fields.Integer(string='Sequence', default=1)
    generator_id = fields.Many2one('faker.generator', string='Generator', readonly=True)
    model = fields.Char(string='Model', readonly=True)
    field_id = fields.Many2one('ir.model.fields', string='Field', domain="[('model', '=', model), ('store', '=', True)]", ondelete='set null')
    value_type = fields.Selection(get_value_types(), string='Type', required=True)
    example = fields.Char(compute='get_example', string='Example')

    # Constant values
    constant_value = fields.Char(string='Constant value')

    # Fakers
    faker_generator = fields.Selection(get_faker_generators(), string='Faker generator')
    faker_locale = fields.Many2one('res.lang', string='Faker locale', default=default_faker_locale)

    # Random record
    random_record_domain = fields.Char(string='Random record domain', required=False)

    # Row generators
    row_generator_id = fields.Many2one('faker.generator', string='Row generator')
    row_count_min = fields.Char(string='Row count minimum', required=False)
    row_count_max = fields.Char(string='Row count maximum', required=False)

    def generate(self, include_rows = False):
        value = None

        if self.value_type == 'constant':
            value = self.constant_value

        if self.value_type == 'faker':
            value = get_faked_value(self)

        if self.value_type == 'random_record':
            value = get_random_record(self, self.env)

        if self.value_type == 'generated_rows' and include_rows:
            value = get_generated_rows_value(self)

        return get_typed_value(self, value)

    @api.constrains('field_id', 'value_type')
    def check_value_type(self):
        validation_result = self.validate_value_type()

        if validation_result and 'warning' in validation_result:
            raise ValidationError(validation_result['warning']['message'])

    @api.constrains('value_type', 'row_count_min', 'row_count_max')
    def check_row_count(self):
        validation_result = self.validate_row_count()

        if validation_result and 'warning' in validation_result:
            raise ValidationError(validation_result['warning']['message'])

    @api.onchange('field_id', 'value_type')
    def validate_value_type(self):
        for record in self:
            if not record.field_id:
                return

            message = None

            if record.value_type == 'random_record' and record.field_id.ttype != 'many2one':
                message = 'The random record type can only be used for fields that represent a many to one relationship.'

            if record.value_type == 'generated_rows' and record.field_id.ttype != 'one2many':
                message = 'The generated rows type can only be used for fields that represent a one to many relationship.'

            if not message:
                return

            message += "\nPlease, check the configuration of the field: {}.".format(record.field_id.display_name)

            return {
                'warning': {
                    'title': 'Validation warning',
                    'message': message,
                    'type': 'notification',
                }
            }

    @api.onchange('value_type', 'row_count_min', 'row_count_max')
    def validate_row_count(self):
        for record in self:
            if record.value_type != 'generated_rows':
                continue

            message = None

            if not record.row_count_min.isdigit():
                message = 'The minimum row count should be a positive integer'

            if not record.row_count_max.isdigit():
                message = 'The maximum row count should be a positive integer'

            if message:
                return {
                    'warning': {
                        'title': 'Validation warning',
                        'message': message,
                        'type': 'notification',
                    }
                }

    @api.onchange('value_type')
    def set_locale(self):
        for record in self:
            if record.value_type == 'faker' and not record.faker_locale:
                record.faker_locale = self.default_faker_locale()

    @api.onchange('value_type', 'constant_value', 'faker_generator', 'faker_locale')
    def get_example(self):
        for record in self:
            if record.value_type != 'constant':
                clear_constant_fields(record)

            if record.value_type != 'faker':
                clear_faker_fields(record)

            if record.value_type != 'generated_rows':
                clear_generated_rows_fields(record)

            record.example = record.generate()

    @api.onchange('generator_id')
    def update_model_on_generator_change(self):
        for record in self:
            self.model = self.generator_id.model_id.model