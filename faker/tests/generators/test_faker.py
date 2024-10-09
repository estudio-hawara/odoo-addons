from faker import Faker
from odoo.tests import TransactionCase, tagged
from odoo.addons.faker.generators.faker import \
    clear_faker_fields, \
    get_faker_generators, \
    get_faked_value

@tagged('faker')
class TestFaker(TransactionCase):
    def test_clear_faker_fields(self):
        # Prepare
        field = self.env['faker.generator.fields'].new()
        field.faker_generator = 'city'
        field.faker_locale = 'en_US'

        # Act
        clear_faker_fields(field)

        # Assert
        assert not field.faker_generator
        assert not field.faker_locale

    def test_get_faker_generators(self):
        # Prepare
        faker = Faker()
        generators = get_faker_generators()

        # Act
        for generator in generators:
            generator_function = getattr(faker, generator[0])

            # Assert
            assert callable(generator_function)

            try:
                # Act
                str(generator_function())
            except:
                # Assert
                self.fail('{} did not generate a stringifiable value'.format(generator[0]))

    def test_get_faked_value(self):
        # Prepare
        field = self.env['faker.generator.fields'].new()
        field.value_type = 'faker'
        field.faker_generator = 'boolean'

        # Act
        value = get_faked_value(field)

        # Assert
        assert isinstance(value, bool)

    def test_get_faked_value_ensures_generator_type(self):
        # Prepare
        field = self.env['faker.generator.fields'].new()
        field.value_type = 'constant'

        # Assert
        with self.assertRaises(Exception):
            # Act
            value = get_faked_value(field)

    def test_get_faked_value_returns_none_without_generator(self):
        # Prepare
        field = self.env['faker.generator.fields'].new()
        field.value_type = 'faker'

        # Act
        value = get_faked_value(field)

        # Assert
        assert value == None