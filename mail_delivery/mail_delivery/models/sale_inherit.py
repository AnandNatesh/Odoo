

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError,ValidationError

from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT


class MailDelivery(models.Model):
    _name='mail.delivery'

    sale_order_id =fields.Many2one("sale.order","Sale Order",required=True)

    @api.onchange("sale_order_id")
    def onchange_sale_order_id(self):
        if self.sale_order_id:
            self.env.cr.execute("""select so.id as sale_id from sale_order so
                                join mail_delivery md on (so.id=md.sale_order_id)""")
            sale_orders = self.env.cr.dictfetchall()
            for saless in sale_orders:
                if self.sale_order_id.id==saless['sale_id']:
                    raise ValidationError("Selected Sale Order Already Exist")

    @api.multi
    def send_delivery_mail(self):
        send_mail = self.env['mail.mail']
        send_ids = []
        mail_ids = []
        mail_template = self.env['mail.template']
        # dt = datetime.now().date()
        sale=self.env['sale.order'].search([('id','=',self.sale_order_id.id)])
        if sale:
            subject = 'Sale Confirmation'
            body = _("Dear Customer,</br>")
            body += _("<br/> Please check the sale.")
            footer = "</br>With Regards,<br/>Admin<br/>"
            self.env.cr.execute(
                '''SELECT email FROM res_partner''')
            vas = self.env.cr.dictfetchall()
            for res in vas:
                send_ids.append(send_mail.create({
                    'email_to': res['email'],
                    'subject': subject,
                    'body_html':
                        '''<span  style="font-size:14px"><br/>
                        <br/>%s</span>
                        <br/>%s</span>
                        <br/><br/>''' % (body, footer),
                }))
                for i in range(len(send_ids)):
                    send_ids[i].send(self)

