from datetime import date
from odoo.tests import TransactionCase, tagged
from odoo.addons.faker.generators.sequential_dates import \
    get_sequential_dates_value, \
    get_sequential_dates
from odoo.addons.faker.wizard.generator_wizard import BatchInfo

@tagged('faker')
class TestSequentialDates(TransactionCase):
    def test_get_sequential_dates_value(self):
        # Prepare
        field = self.env['faker.generator.fields'].new()
        field.value_type = 'sequential_dates'
        field.sequential_dates_min = date(2000, 1, 1)
        field.sequential_dates_max = date(2000, 1, 2)

        # Act
        first_date = get_sequential_dates_value(field, BatchInfo(row_count=2, row_number=1))
        second_date = get_sequential_dates_value(field, BatchInfo(row_count=2, row_number=2))

        # Assert
        assert (first_date - field.sequential_dates_min).days == 0
        assert (second_date - field.sequential_dates_max).days == 0

    def test_get_sequential_dates(self):
        # Prepare
        today = date.today()
        first_day_of_the_year = date(today.year, 1, 1)
        period_in_days = (today - first_day_of_the_year).days

        # Act
        first_date = get_sequential_dates(row_count=period_in_days, row_number=1)
        last_date = get_sequential_dates(row_count=period_in_days, row_number=period_in_days)

        # Assert
        assert (first_date - first_day_of_the_year).days == 0
        assert (last_date - today).days == 0