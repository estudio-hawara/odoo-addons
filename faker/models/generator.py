from odoo import fields, models, api
from odoo.tools import get_lang

class Generator(models.Model):
    _name = 'faker.generator'
    _description = 'Generators of fake data for each model'

    def default_faker_locale(self):
        return get_lang(self.env)

    name = fields.Char(string='Name')
    model_id = fields.Many2one('ir.model', string='Model')
    field_ids = fields.One2many('faker.generator.fields', 'generator_id', string='Fields', copy=True)
    faker_locale = fields.Many2one('res.lang', string='Faker locale', default=default_faker_locale)

    def show_generator_wizard(self):
        self.ensure_one()
        action = self.env.ref('faker.show_generator_wizard_action').read()[0]
        action['context'] = {'generator_id': self.id}
        return action

    def get_empty_record(self):
        empty = {}
        for field in self.field_ids.search([('generator_id', '=', self.id)], order='sequence asc, id asc'):
            empty[field.field_id.name] = None
        return empty

    def generate(self, batch_info=None, break_at=None):
        generated = {}
        for field in self.field_ids.search([('generator_id', '=', self.id)], order='sequence asc, id asc'):
            if break_at and field.sequence >= break_at.sequence and field.id >= break_at.id:
                break
            generated[field.field_id.name] = field.generate(batch_info=batch_info, include_rows=True)
        return generated

    def generate_and_save(self, batch_info):
        generated = self.generate(batch_info)
        self.env[self.model_id.model].create(generated)