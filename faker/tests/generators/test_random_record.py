from unittest.mock import MagicMock, PropertyMock
from odoo.tests import TransactionCase, tagged
from odoo.tools import Query
from odoo.addons.faker.generators.random_record import get_random_record

@tagged('faker')
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

        mocked_model = MagicMock()
        mocked_query = MagicMock()
        mocked_record = MagicMock()
        mocked_ev = MagicMock()

        mocked_model._where_calc.return_value = mocked_query
        type(mocked_record).id = PropertyMock(return_value=10)
        mocked_model._fetch_query.return_value = mocked_record
        mocked_ev.__getitem__.side_effect = {'ir.model.fields': mocked_model}.__getitem__

        # Act
        random_record_id = get_random_record(field, mocked_ev)

        # Assert
        mocked_model._where_calc.assert_called()
        mocked_model._fetch_query.assert_called()

        assert mocked_query.order == 'RANDOM()'
        assert mocked_query.limit == 1
        assert random_record_id == 10