from odoo import fields, models
from odoo.exceptions import ValidationError

class GeneratorWizard(models.TransientModel):
    _name = 'faker.generator.wizard'
    _description = 'Wizard to run a generation batch'

    def default_generator_id(self):
        context = self._context.copy()

        if 'generator_id' in context:
            return context['generator_id']

    generator_id = fields.Many2one('faker.generator', string='Generator', required=True, default=default_generator_id)
    records = fields.Integer(string='Number of records', required=True, default=25)
    max_errors = fields.Integer(string='Error tolerance', required=True, default=3)

    def action_generate_records(self):
        generated_records = 0
        raised_errors = 0
        errors = []

        while generated_records < self.records and raised_errors < self.max_errors:
            try:
                self.generator_id.generate_and_save()
                generated_records += 1
            except Exception as e:
                raised_errors += 1
                error = str(e)
                if not error in errors:
                    errors.append(error)
                continue

        if raised_errors >= self.max_errors:
            raise ValidationError(
                "\n".join(errors) + "\n\n" +
                "The maximum accepted number of errors was reached.\n\n"
                "Please, check your generators and try again."
            )