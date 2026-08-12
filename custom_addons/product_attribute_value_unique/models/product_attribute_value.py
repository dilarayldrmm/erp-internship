from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    _sql_constraints = [
        (
            'unique_name_attribute',
            'unique(name, attribute_id)',
            'This attribute value already exists!',
        ),
    ]

    @api.model
    def _normalize_value_name(self, name):
        return name.strip() if name else name

    def _find_duplicate_siblings(self, name, attribute_id, exclude_ids=None):
        """Return values on the same attribute that share the same name (case-insensitive)."""
        exclude_ids = set(exclude_ids or [])
        normalized = name.casefold()
        siblings = self.search([('attribute_id', '=', attribute_id)])
        return siblings.filtered(
            lambda value: value.id not in exclude_ids
            and value.name.casefold() == normalized
        )

    def _raise_duplicate_error(self, name, attribute):
        raise ValidationError(_(
            'The value "%(value)s" already exists for the attribute "%(attribute)s".',
            value=name,
            attribute=attribute.display_name,
        ))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name'):
                vals['name'] = self._normalize_value_name(vals['name'])

        attribute_model = self.env['product.attribute']
        seen_in_batch = set()
        for vals in vals_list:
            name = vals.get('name')
            attribute_id = vals.get('attribute_id')
            if not name or not attribute_id:
                continue

            batch_key = (attribute_id, name.casefold())
            if batch_key in seen_in_batch:
                attribute = attribute_model.browse(attribute_id)
                self._raise_duplicate_error(name, attribute)
            seen_in_batch.add(batch_key)

            attribute = attribute_model.browse(attribute_id)
            if self._find_duplicate_siblings(name, attribute_id):
                self._raise_duplicate_error(name, attribute)

        return super().create(vals_list)

    def write(self, vals):
        if vals.get('name'):
            vals['name'] = self._normalize_value_name(vals['name'])
        return super().write(vals)

    @api.constrains('name', 'attribute_id')
    def _check_unique_attribute_value(self):
        for record in self:
            if not record.name or not record.attribute_id:
                continue
            duplicates = record._find_duplicate_siblings(
                record.name,
                record.attribute_id.id,
                exclude_ids=record.ids,
            )
            if duplicates:
                record._raise_duplicate_error(record.name, record.attribute_id)
