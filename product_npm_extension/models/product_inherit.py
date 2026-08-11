from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    npm = fields.Char(string="NPM")

    @api.constrains('npm')
    def _check_npm_unique(self):
        for record in self:
            if record.npm:
                # Aynı NPM'e sahip başka bir ürün var mı diye kontrol ediyoruz
                existing = self.search([('npm', '=', record.npm), ('id', '!=', record.id)])
                if existing:
                    raise ValidationError("Bu NPM kodu başka bir üründe zaten kullanılıyor! NPM benzersiz olmalıdır.")

class ProductProduct(models.Model):
    _inherit = 'product.product'

    npm = fields.Char(string="NPM", related='product_tmpl_id.npm', store=True)