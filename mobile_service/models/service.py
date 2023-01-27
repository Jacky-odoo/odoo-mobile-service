from datetime import datetime, date, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
import pytz


class MobileServiceShop(models.Model):
    _name = 'moblie_service.service'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True

    name = fields.Char(
        string='Service Number',
        copy=False,
        default="New")
    person_name = fields.Many2one(
        comodel_name='res.partner',
        string="Customer Name",
        required=True)
    contact_no = fields.Char(
        related='person_name.mobile',
        string="Contact Number")
    email_id = fields.Char(
        related='person_name.email',
        string="Email")
    street = fields.Char(
        related='person_name.street',
        string="Address")
    street2 = fields.Char(
        related='person_name.street2',
        string="Address")
    city = fields.Char(
        related='person_name.city',
        string="Address")
    state_id = fields.Many2one(
        related='person_name.state_id',
        string="Address")
    zip = fields.Char(
        related='person_name.zip',
        string="Address")
    country_id = fields.Many2one(
        string="Address",
        related='person_name.country_id',
        help="Country")

    imei_no = fields.Char(
        string="IMEI Number")
    warranty_id = fields.Many2one(
        comodel_name="mobile.warranty",
        string='Warranty Number',
        help="warranty details")
    is_in_warranty = fields.Boolean(
        string='In Warranty',
        default=False,
        help="Specify if the product is in warranty.",
        copy=False)

    re_repair = fields.Boolean(
        string='Re-repair',
        default=False,
        help="Re-repairing.")
    # TODO: maso, 2023: rename to brand_id
    brand_id = fields.Many2one(
        comodle_name='mobile_service.brand',
        string="Mobile Brand")
    model_id = fields.Many2one(
        comodel_name='moblie_service.brand.model',
        string="Model",
        domain="[('mobile_brand_name','=',brand_name)]")
    image_medium = fields.Image(
        related='model_name.image',
        store=True,
        attachment=True)

    date_request = fields.Date(
        string="Requested date",
        default=fields.Date.context_today)
    accept_date = fields.Date(
        string="Accepted date")

    return_date = fields.Date(
        string="Return date",
        default=fields.Date.context_today,
        required=True)
    technician_name = fields.Many2one(
        comodel_name='res.users',
        string="Technician Name",
        default=lambda self: self.env.user,
        required=True)
    service_state = fields.Selection(
        selection=[('draft', 'Draft'),
                   ('accepted', 'Accepted'),
                   ('assigned', 'Assigned'),
                   ('completed', 'Completed'),
                   ('returned', 'Returned'),
                   ('not_solved', 'Not solved')],
        string='Service Status',
        default='draft',
        track_visibility='always')

    complaints_tree = fields.One2many(
        comodel_name='mobile.complaint.tree',
        inverse_name='complaint_id',
        string='Complaints Tree')

    product_order_line = fields.One2many(
        comodel_name='product.order.line',
        inverse_name='product_order_id',
        string='Parts Order Lines')

    internal_notes = fields.Text(
        string="Internal notes")
    invoice_count = fields.Integer(
        compute='_invoice_count',
        string='# Invoice',
        copy=False)
    invoice_ids = fields.Many2many(
        comodel_name="account.move",
        string='Invoices',
        compute="_get_invoiced",
        readonly=True,
        copy=False)

    first_payment_inv = fields.Many2one(
        comodel_name='account.move',
        copy=False)

    first_invoice_created = fields.Boolean(
        string="First Invoice Created",
        invisible=True,
        copy=False)

    service_count = fields.Integer(
        compute='_service_count',
        string='# Services',
        copy=False)

    journal_type = fields.Many2one(
        comodel_name='account.journal',
        string='Journal',
        invisible=True,
        default=lambda self: self.env['account.journal'].search([('code', '=', 'SERV')]))

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company)

    @api.model
    def _default_picking_transfer(self):
        type_obj = self.env['stock.picking.type']
        company_id = self.env.context.get(
            'company_id') or self.env.user.company_id.id
        types = type_obj.search(
            [('code', '=', 'outgoing'), ('warehouse_id.company_id', '=', company_id)], limit=1)
        if not types:
            types = type_obj.search(
                [('code', '=', 'outgoing'), ('warehouse_id', '=', False)])
        return types[:4]

    stock_picking_id = fields.Many2one('stock.picking', string="Picking Id")

    picking_transfer_id = fields.Many2one('stock.picking.type',
                                          'Deliver To',
                                          required=True,
                                          default=_default_picking_transfer,
                                          help="This will determine picking type of outgoing shipment")

    picking_count = fields.Integer()

    ################################################################################
    #              Models
    ################################################################################

    @api.onchange('return_date')
    def check_date(self):
        if self.return_date != False:
            return_date_string = datetime.strptime(
                str(self.return_date), "%Y-%m-%d")
            request_date_string = datetime.strptime(
                str(self.date_request), "%Y-%m-%d")
            if return_date_string < request_date_string:
                raise UserError(
                    "Return date should be greater than requested date")

    ################################################################################
    #              State Machin: Actions
    ################################################################################
    def approve(self):
        self.service_state = 'assigned'

    def complete(self):
        self.service_state = 'completed'

    def return_to(self):
        self.service_state = 'returned'

    def return_to(self):
        self.service_state = 'returned'

    def not_solved(self):
        self.service_state = 'not_solved'

    def action_accept_service(self):
        """
        Accepts incoming request (in draft) and move them to the accepted state.
        """
        self.accept_date = datetime.now()
        self.service_state = 'accepted'

    def action_reject_service(self):
        """
        Rejects incoming service request (in draft state) and move them to the not solved state.
        """
        self.service_state = 'not_solved'

    def action_send_mail(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data._xmlid_lookup(
                'mobile_service.email_template_mobile_service')[2]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data._xmlid_lookup(
                'mail.email_compose_message_wizard_form')[2]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'mobile.service',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        }
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def return_advance(self):
        inv_obj = self.env['account.move'].search(
            [('invoice_origin', '=', self.name)])
        inv_ids = []
        for each in inv_obj:
            inv_ids.append(each.id)
        view_id = self.env.ref('account.view_move_form').id

        if inv_ids:
            if len(inv_ids) <= 1:
                value = {
                    'view_mode': 'form',
                    'res_model': 'account.move',
                    'view_id': view_id,
                    'type': 'ir.actions.act_window',
                    'name': 'Invoice',
                    'res_id': inv_ids[0]
                }
            else:
                value = {
                    'domain': str([('id', 'in', inv_ids)]),
                    'view_mode': 'tree,form',
                    'res_model': 'account.move',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name': 'Invoice',
                    'res_id': inv_ids[0]
                }

            return value
        else:
            raise UserError("No invoice created")

    def _invoice_count(self):
        invoice_ids = self.env['account.move'].search(
            [('invoice_origin', '=', self.name)])
        self.invoice_count = len(invoice_ids)

    @api.onchange('imei_no')
    def _service_count(self):
        self.service_count = self.search(
            [('imei_no', '=', self.imei_no)], count=True)

    @api.model
    def create(self, vals):
        print(self.env.user.company_id)
        if 'company_id' in vals:
            vals['name'] = self.env['ir.sequence'].with_context(force_company=self.env.user.company_id.id).next_by_code(
                'mobile.service') or _('New')
        else:
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'mobile.service') or _('New')
        vals['service_state'] = 'draft'
        return super(MobileServiceShop, self).create(vals)

    def unlink(self):
        for i in self:
            if i.service_state != 'draft':
                raise UserError(
                    _('You cannot delete an assigned service request'))
        return super(MobileServiceShop, self).unlink()

    def action_invoice_create_wizard(self):

        return {
            'name': _('Create Invoice'),
            'view_mode': 'form',
            'res_model': 'mobile.invoice',
            'type': 'ir.actions.act_window',
            'target': 'new'
        }

    def action_post_stock(self):
        flag = 0
        for order in self.product_order_line:
            if order.product_uom_qty > order.qty_stock_move:
                flag = 1
                pick = {
                    'picking_type_id': self.picking_transfer_id.id,
                    'partner_id': self.person_name.id,
                    'origin': self.name,
                    'location_dest_id': self.person_name.property_stock_customer.id,
                    'location_id': self.picking_transfer_id.default_location_src_id.id,

                }

                picking = self.env['stock.picking'].create(pick)
                self.stock_picking_id = picking.id
                self.picking_count = len(picking)
                moves = order.filtered(
                    lambda r: r.product_id.type in ['product', 'consu'])._create_stock_moves_transfer(picking)
                move_ids = moves._action_confirm()
                move_ids._action_assign()
            if order.product_uom_qty < order.qty_stock_move:
                raise UserError(
                    _('Used quantity is less than quantity stock move posted. '))
        if flag != 1:
            raise UserError(_('Nothing to post stock move'))
        if flag != 1:
            raise UserError(_('Nothing to post stock move'))

    def action_view_services(self):
        self.ensure_one()
        ctx = dict(
            create=False,
        )
        action = {
            'name': _("Services"),
            'type': 'ir.actions.act_window',
            'res_model': 'mobile.service',
            'target': 'current',
            'context': ctx
        }
        service_ids = self.search([('imei_no', '=', self.imei_no)])
        serv_ids = []
        for each in service_ids:
            serv_ids.append(each.id)
        if len(serv_ids) == 1:
            service_id = serv_ids and serv_ids[0]
            action['res_id'] = service_id
            action['view_mode'] = 'form'
            action['views'] = [
                (self.env.ref('mobile_service.mobile_service_request_form_view').id, 'form')]
        else:
            action['view_mode'] = 'tree,form'
            action['domain'] = [('id', 'in', serv_ids)]
        return action

    def action_view_invoice(self):
        self.ensure_one()
        ctx = dict(
            create=False,
        )
        action = {
            'name': _("Invoices"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'target': 'current',
            'context': ctx
        }
        invoice_ids = self.env['account.move'].search(
            [('invoice_origin', '=', self.name)])
        inv_ids = []
        for each in invoice_ids:
            inv_ids.append(each.id)
        if len(invoice_ids) == 1:
            invoice = inv_ids and inv_ids[0]
            action['res_id'] = invoice
            action['view_mode'] = 'form'
            action['views'] = [
                (self.env.ref('account.view_move_form').id, 'form')]
        else:

            action['view_mode'] = 'tree,form'
            action['domain'] = [('id', 'in', inv_ids)]
        return action

    def get_ticket(self):
        self.ensure_one()
        user = self.env['res.users'].browse(self.env.uid)
        if user.tz:
            tz = pytz.timezone(user.tz)
            time = pytz.utc.localize(datetime.now()).astimezone(tz)
            date_today = time.strftime("%Y-%m-%d %H:%M %p")
        else:
            date_today = datetime.strftime(
                datetime.now(), "%Y-%m-%d %I:%M:%S %p")
        complaint_text = ""
        description_text = ""
        complaint_id = self.env['mobile.complaint.tree'].search(
            [('complaint_id', '=', self.id)])
        if complaint_id:
            for obj in complaint_id:
                complaint = obj.complaint_type_tree
                description = obj.description_tree
                complaint_text = complaint.complaint_type + ", " + complaint_text
                if description.description:
                    description_text = description.description + ", " + description_text
        else:
            for obj in complaint_id:
                complaint = obj.complaint_type_tree
                complaint_text = complaint.complaint_type + ", " + complaint_text
        data = {
            'ids': self.ids,
            'model': self._name,
            'date_today': date_today,
            'date_request': self.date_request,
            'date_return': self.return_date,
            'sev_id': self.name,
            'warranty': self.is_in_warranty,
            'customer_name': self.person_name.name,
            'imei_no': self.imei_no,
            'technician': self.technician_name.name,
            'complaint_types': complaint_text,
            'complaint_description': description_text,
            'mobile_brand': self.brand_name.brand_name,
            'model_name': self.model_name.mobile_brand_models,

        }
        return self.env.ref('mobile_service.mobile_service_ticket').report_action(self, data=data)

    @api.onchange('imei_no')
    def _onchange_imei_find_warranty(self):
        # Check if warranty find
        warranty_ids = False
        if self.imei_no:
            warranty_ids = self.env['mobile.warranty'].search(
                ['|', ('imei1', '=', self.imei_no), ('imei2', '=', self.imei_no)])
        if warranty_ids:
            self.is_in_warranty = True
            self.warranty_id = warranty_ids[0]
        else:
            self.is_in_warranty = False
            self.warranty_id = False