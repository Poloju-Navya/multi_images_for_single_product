from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_default_image(self):
        self.ref_image = self.image_1920

    multi_image_ids = fields.Many2many('product.image', string="Images")
    ref_image = fields.Binary('Image', compute="_get_default_image")
    product_count = fields.Integer('Product Count')

    def open_multi_iamges(self):
        return {
            'name': _('Product Images'),
            'type': 'ir.actions.act_window',
            'res_model': 'product.image',
            'view_mode': 'kanban,tree,form',
            'domain': [('id', 'in', self.multi_image_ids.ids)],
            'context': {'default_product_tmpl_id': self.id}
        }


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    no_of_product = fields.Integer(string='Count', default=1,
                                   config_parameter='multi_images_for_single_product.no_of_product')


class ProductImage(models.Model):
    _inherit = 'product.image'

    @api.model
    def create(self, vals_list):
        res = super(ProductImage, self).create(vals_list)
        count = self.env['ir.config_parameter'].sudo().get_param('multi_images_for_single_product.no_of_product')
        count = int(count)
        if res.product_tmpl_id:
            res.product_tmpl_id.multi_image_ids = [(4, res.id)]
        elif res.product_variant_id:
            res.product_variant_id.multi_image_ids = [(4, res.id)]
        if len(res.product_tmpl_id.multi_image_ids) and count:
            if len(res.product_tmpl_id.multi_image_ids) > count:
                raise UserError(_("Please Modify the Product Count in Setting/Inventory/Products/Count"))
            elif len(res.product_tmpl_id.multi_image_ids) == count:
                res.product_tmpl_id.product_count = count
        elif len(res.product_variant_id.multi_image_ids) and count:
            if len(res.product_variant_id.multi_image_ids) > count:
                raise UserError(_("Please Modify the Product Count in Setting/Inventory/Products/Count"))
            elif len(res.product_variant_id.multi_image_ids) == count:
                res.product_variant_id.product_count = count
        return res

class ProductProduct(models.Model):
    _inherit = "product.product"

    def open_multi_iamges(self):
        return {
            'name': _('Product Images'),
            'type': 'ir.actions.act_window',
            'res_model': 'product.image',
            'view_mode': 'kanban,tree,form',
            'domain': [('id', 'in', self.multi_image_ids.ids)],
            'context': {'default_product_variant_id': self.id}
        }

