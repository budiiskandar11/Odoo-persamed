from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import workflow

class sale_order(osv.Model):
    _inherit    = "sale.order"
    
    def _amount_all_wrapper(self, cr, uid, ids, field_name, arg, context=None):
        """ Wrapper because of direct method passing as parameter for function fields """
        return self._amount_all(cr, uid, ids, field_name, arg, context=context)
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'gross_total': 0.0,
                'discount_total': 0.0,
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = val2 = val3 = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                val3 += line.price_unit * line.product_uom_qty
                val2 += (line.price_unit * ((line.discount or 0.0) / 100.0)) * line.product_uom_qty
                val1 += line.price_subtotal
                val += self._amount_line_tax(cr, uid, line, context=context)
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[order.id]['gross_total'] = cur_obj.round(cr, uid, cur, val3)
            res[order.id]['discount_total'] = cur_obj.round(cr, uid, cur, val2)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return res

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    _columns    = {
            'date_valid': fields.date('Valid Date', required=False, readonly=True, select=True),
            'state': fields.selection([
                    ('draft', 'Draft'),
                    ('quot', 'Quotation'),
                    ('sent', 'Quotation Sent'),
                    ('cancel', 'Cancelled'),
                    ('waiting_date', 'Waiting Schedule'),
                    ('progress', 'Sales Order'),
                    ('manual', 'Sale to Invoice'),
                    ('invoice_except', 'Invoice Exception'),
                    ('done', 'Done'),
                    ], 'Status', readonly=True, track_visibility='onchange',
                    help="Gives the status of the quotation or sales order. \nThe exception status is automatically set when a cancel operation occurs in the processing of a document linked to the sales order. \nThe 'Waiting Schedule' status is set when the invoice is confirmed but waiting for the scheduler to run on the order date.", select=True),
                
            'gross_total': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Total',
                store={
                    'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                    'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
                },
                multi='sums', help="The amount gross total.", track_visibility='always'),
            'discount_total': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Total Disc',
                store={
                    'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                    'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
                },
                multi='sums', help="The amount discount total.", track_visibility='always'),
            'amount_untaxed': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Untaxed Amount',
                store={
                    'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                    'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
                },
                multi='sums', help="The amount without tax.", track_visibility='always'),
            'amount_tax': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Taxes',
                store={
                    'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                    'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
                },
                multi='sums', help="The tax amount."),
            'amount_total': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Net Total',
                store={
                    'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                    'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
                },
                multi='sums', help="The total amount."),
       }
    
    def action_confirm_quot(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.signal_order_confirm(cr, uid, ids)
        self.write(cr, uid, ids, {'state': 'quot'}, context=context)
        return True
   
    def print_quotation_test(self, cr, uid, ids, context=None):
        #super(sale_order, self).print_quotation(cr, uid, ids, context=context
        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        #super(sale_order, self).signal_quotation_sent(cr, uid, ids, context=context)
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        self.pool.get('sale.order').signal_quotation_sent(cr, uid, ids)
        return self.pool['report'].get_action(cr, uid, ids, 'sale.dos_new_quotation_report', context=context)
       
    def print_quotation(self, cr, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'sale.order', ids[0], 'quotation_sent', cr)
        datas = {
                 'model': 'sale.order',
                 'ids': ids,
                 'form': self.read(cr, uid, ids[0], context=context),
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'dos.new.quotation', 'datas': datas, 'nodestroy': True}
sale_order()