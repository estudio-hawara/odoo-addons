from unittest.mock import MagicMock
from odoo.tests import TransactionCase, tagged
from odoo.tools import SQL
from odoo.addons.faker.generators.random_record import get_random_record

class TestRandomRecord(TransactionCase):
    def test_get_random_record(self):
        # Prepare
        field_model = self.env['ir.model'].search([('model', '=', 'ir.model.fields')])

        related_field = self.env['ir.model.fields'].search([
            ('model', '=', 'ir.model.fields'),
            ('name', '=', 'related_field_id'),
        ])

        model_generator = self.env['faker.generator'].create({
            'model_id': field_model.id,
            'field_ids': [(0, 0, {
                'field_id': related_field.id,
                'value_type': 'random_record',
            })],
        })

        field = self.env['faker.generator.fields'].search([
            ('generator_id', '=', model_generator.id)
        ])

        cr = MagicMock()
        cr.execute.return_value = None
        cr.fetchone.return_value = (1,)

        # Act
        random_record = get_random_record(field, cr)

        # Assert
        query = SQL('select id from "ir_model_fields" order by RANDOM() limit 1')
        cr.execute.assert_called_with(query)
        cr.fetchone.assert_called_with()
        assert random_record == 1