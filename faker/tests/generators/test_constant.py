from odoo.tests import TransactionCase, tagged
from odoo.addons.faker.generators.constant import clear_constant_fields

@tagged('faker')
class TestConstant(TransactionCase):
    def test_clear_constant_fields(self):
        # Prepare
        field = self.env['faker.generator.fields'].new()
        field.constant_value = 'filled'

        # Act
        clear_constant_fields(field)

        # Assert
        assert not field.constant_value