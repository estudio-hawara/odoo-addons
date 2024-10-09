from odoo import fields, models, api
from odoo.tools import get_lang

class Generator(models.Model):
    _name = 'faker.generator'
    _description = 'Generators of fake data for each model'

    def default_faker_locale(self):
        return get_lang(self.env)

    name = fields.Char(string='Name')
    model_id = fields.Many2one('ir.model', string='Model')
    field_ids = fields.One2many('faker.generator.fields', 'generator_id', string='Fields')
    faker_locale = fields.Many2one('res.lang', string='Faker locale', default=default_faker_locale)

    def show_generator_wizard(self):
        self.ensure_one()
        action = self.env.ref('faker.show_generator_wizard_action').read()[0]
        action['context'] = {'generator_id': self.id}
        return action

    def generate(self):
        generated = {}
        for field in self.field_ids:
            generated[field.field_id.name] = field.generate(include_rows=True)
        return generated

    def generate_and_save(self):
        generated = self.generate()
        self.env[self.model_id.model].create(generated)