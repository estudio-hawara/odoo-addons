from faker import Faker
from odoo.tests import TransactionCase, tagged
from odoo.addons.faker.generators.generated_rows import \
    clear_generated_rows_fields, \
    get_generated_rows_value

@tagged('faker')
class TestGeneratedRows(TransactionCase):
    def test_clear_generated_rows_fields(self):
        # Prepare
        field = self.env['faker.generator.fields'].new()
        field.row_generator_id = 1
        field.row_count_min = 1
        field.row_count_max = 2

        # Act
        clear_generated_rows_fields(field)

        # Assert
        assert not field.row_generator_id
        assert not field.row_count_min
        assert not field.row_count_max

    def test_get_generated_rows_value(self):
        # Prepare
        partner_model = self.env['ir.model'].search([('model', '=', 'res.partner')])

        partner_field_name = self.env['ir.model.fields'].search([
            ('model', '=', 'res.partner'),
            ('name', '=', 'name'),
        ])

        partner_generator = self.env['faker.generator'].create({
            'model_id': partner_model.id,
            'field_ids': [(0, 0, {
                'field_id': partner_field_name.id,
                'value_type': 'constant',
                'constant_value': 'Emmy Nöether',
            })],
        })

        field = self.env['faker.generator.fields'].new()
        field.value_type = 'generated_rows'
        field.row_generator_id = partner_generator
        field.row_count_min = 1
        field.row_count_max = 1

        # Act
        generated = get_generated_rows_value(field)

        # Assert
        assert len(generated) == 1
        assert generated[0][2]['name'] == 'Emmy Nöether'