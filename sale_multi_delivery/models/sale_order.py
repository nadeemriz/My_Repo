from odoo import models,fields,api,_


class SaleOrderConfirm(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        super(SaleOrderConfirm, self).action_confirm()
        self.create_order_deliveries()

    def create_order_deliveries(self):
        for order in self:
            products = {}
            for line in order.order_line:

                product = line.product_id
                if product in products:
                    products[product] += line.product_uom_qty
                else:
                    products[product] = line.product_uom_qty
            for product, qty in products.items():
                picking = self.env['stock.picking'].create({
                    'partner_id': order.partner_id.id,
                    'picking_type_id': order.warehouse_id.out_type_id.id,
                    'location_id': order.warehouse_id.lot_stock_id.id,
                    'location_dest_id': order.partner_id.property_stock_customer.id,
                    'origin': order.name,
                    'state': 'draft',
                    'sale_order_id': order.id,
                })

                self.env['stock.move'].create({
                    'name': product.name,
                    'product_id': product.id,
                    'product_uom_qty': qty,
                    'product_uom': product.uom_id.id,
                    'picking_id': picking.id,
                    'location_id': order.warehouse_id.lot_stock_id.id,
                    'location_dest_id': order.partner_id.property_stock_customer.id,
                })
                picking.action_confirm()

        stock_orders = self.env['stock.picking'].search([('origin','=',self.name)])
        for stock in stock_orders:
            if not stock.sale_order_id:
                stock.unlink()


class DeliveryOrder(models.Model):
    _inherit = 'stock.picking'

    sale_order_id = fields.Many2one('sale.order',"Sale Order")


