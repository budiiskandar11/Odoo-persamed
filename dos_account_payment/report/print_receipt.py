import time
from openerp.report import report_sxw
from openerp.tools.translate import _
from openerp.osv import osv
#from dos_amount2text_idr import amount_to_text_id

from openerp.addons.dos_amount2text_idr import amount_to_text_id
from openerp.addons.report_webkit import webkit_report
from openerp.addons.report_webkit.report_helper import WebKitHelper
from openerp.addons.report_webkit.webkit_report import webkit_report_extender
from openerp import SUPERUSER_ID


class DosWebkitParser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(DosWebkitParser, self).__init__(cr, uid, name, context=context)
        self.line_no = 0
        self.localcontext.update({
#             'time': time,
            'convert':self.convert,
        })
     
    def convert(self, amount, cur):
        amt_id = amount_to_text_id.amount_to_text(amount, 'id', cur)
        return amt_id

#         
webkit_report.WebKitParser('report.webkit.cheque',
                       'account.voucher', 
                       'addons/dos_account_payment/report/print_cheque.mako',
                       parser=DosWebkitParser)
