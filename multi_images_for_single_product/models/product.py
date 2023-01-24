from odoo import models,fields,api,_
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_default_image(self):
        if self.multi_image_ids:
            self.ref_image = self.multi_image_ids[0].image_1920
        else:
            self.ref_image = False

    multi_image_ids = fields.Many2many('product.image',string="Images")
    ref_image = fields.Binary('Image',compute="_get_default_image")
    product_count = fields.Integer('Product Count')
    # single_image = fields.Many2one('ir.attachment')

    def open_multi_iamges(self):
        return {
            'name': _('Product Images'),
            'type': 'ir.actions.act_window',
            'res_model': 'product.image',
            'view_mode': 'kanban,tree,form',
            'domain': [('id', 'in', self.multi_image_ids.ids)],
        }

    @api.onchange('multi_image_ids')
    def _onchange_multi_image_ids(self):
        count  = self.env['ir.config_parameter'].sudo().get_param('mutli_images_for_single_product.product_count')
        if len(self.multi_image_ids) and count:
            if len(self.multi_image_ids) > count:
                raise UserError(_("Please Modify the Product Count in Setting/Inventory/Products/Count"))
            elif len(self.multi_image_ids) == count:
                self.product_count = count

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_count = fields.Integer(string='Count',default="1")