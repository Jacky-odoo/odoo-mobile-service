# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import  UserError
from odoo.http import request
from datetime import datetime, date, timedelta
import pytz
import re 


class MobileServiceShop(models.Model):
    _name = 'mobile_service.service'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True
    _description="Mobile service"

    name = fields.Char(
        string='Service Number',
        copy=False,
        default="New")

    # ----------------- person address ---------------------
    person_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer Name",
        required=True)
    contact_no = fields.Char(related='person_id.mobile')
    email_id = fields.Char(related='person_id.email')
    street = fields.Char(related='person_id.street')
    national_code = fields.Char(string="National id")
    city = fields.Char(related='person_id.city')
    zip = fields.Char(related='person_id.zip')
    state_id = fields.Many2one(related='person_id.state_id')
    country_id = fields.Many2one(related='person_id.country_id')
    # ------------------------------------------------

    imei_no = fields.Char(
        string="IMEI Number",
        required=True,
        tracking=True)
    warranty_id = fields.Many2one(
        comodel_name="mobile_service.warranty",
        string='Warranty Number',
        help="warranty details")
    is_in_warranty = fields.Boolean(
        compute='_compute_is_in_warranty',
        string='In Warranty',
        help="Specify if the product is in warranty.",
        copy=False)
    re_repair = fields.Boolean(
        string='Re-repair',
        default=False,
        help="Re-repairing.")

    # ------------------ Device Model --------------------
    model_id = fields.Many2one(
        comodel_name='mobile_service.brand.model',
        string="Model")
    brand_id = fields.Many2one(related='model_id.brand_id')
    image = fields.Image(related='model_id.image')
    # ----------------------------------------------------

    # ------------------ Request info --------------------
    date_request = fields.Date(
        string="Requested date",
        readonly=True,
        default=fields.Date.context_today)
    accept_date = fields.Date(
        readonly=True,
        string="Accepted date")
    return_date = fields.Date(
        string="Return date",
        readonly=True)
    acceptor_id = fields.Many2one(
        comodel_name='res.users',
        string="Acceptor Name",
        default=lambda self: self.env.user,
        tracking=True,
    )
    technician_id = fields.Many2one(
        comodel_name='res.users',
        string="Technician Name",
        default=lambda self: self.env.user,
        required=True,
        tracking=True)
    # --------------------- states  -----------------------
    service_state = fields.Selection(
        selection=[('draft', 'Draft'),
                   ('accepted', 'Accepted'),
                   ('customer', 'Customer'),
                   ('evaluation', 'Evaluation'),
                   ('quality', 'Quality'),
                   ('delivered', 'Delivered')],
        string='Service Status',
        default='draft',
        tracking=True)
    # ------------------------------------------------------
    complaint_tree_ids = fields.One2many(
        comodel_name='mobile_service.complaint.tree',
        inverse_name='service_id',
        string='Complaints Tree')
    internal_notes = fields.Text(string="Notes")
    product_order_line_ids = fields.One2many(
        comodel_name='product.order.line',
        inverse_name='product_order_id',
        string='Parts Order Lines')
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
    stock_picking_id = fields.Many2one(
        'stock.picking',
        string="Picking Id")
    picking_transfer_id = fields.Many2one(
        'stock.picking.type',
        'Deliver To',
        required=True,
        default=lambda self: self._default_picking_transfer(),
        help="This will determine picking type of outgoing shipment")

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

    picking_count = fields.Integer()

   

    ################################################################################
    #              Models
    ################################################################################
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
#! Here we check warranty for imei that user insert    
#! in Here check in two model function one of them 
#! with button and one of them with on change that 
#! we will remove button in feature .....         
    @api.onchange('imei_no')
    def action_chk_on_service(self):
        warranty_ids = False
        if self.imei_no:
            warranty_ids = self.env['mobile_service.warranty'].search(
                [
                    '&',
                    ('company_id', '=', self.company_id.id),
                    '|',
                    ('imei1', '=', self.imei_no),
                    ('imei2', '=', self.imei_no)],
                limit=1,
                order="expire_date DESC")
        if warranty_ids:
            self.warranty_id = warranty_ids[0]
            self.model_id = self.warranty_id.model_id
        else:
            self.warranty_id = False
            self.model_id = False
    

# Action for States that we create in mobile service ---------->
    def action_draftmobile_service(self):
        """ this is called when a record set in first level"""
        self.service_state = 'draft'
        return self.action_view_serv()
    
    def action_accept_service(self):
        """this is called when a service accepted"""
        if not self.accept_date:
            self.accept_date = datetime.now()
        self.service_state = 'accepted'
        return self.action_view_serv()
    
    def action_acceptmobile_service(self):
        """ this is called after draft this is Customer action and notification """
        self.service_state = 'customer'
        return self.action_view_serv()
    
    def action_easmobile_service(self):
        """ this called after accept """
        if self.warranty_id and (self.warranty_id.state in 'valid' or self.warranty_id.state in 'canceled'):
            self.service_state = 'evaluation'
            return self.action_view_serv()
        
        if not self.warranty_id:
            self.service_state = 'evaluation'
            return self.action_view_serv()
        
        #!Create an Error in warranty 
        return {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': _('Warranty: %s.',self.name),
            'message': _('Warranty is not valid please Check it...'),
            'type': 'danger',
            'sticky': True,  #True/False will display for few seconds if false
            'next': {'type': 'ir.actions.act_window_close'},
            },
        }
    
    def action_qcsmobile_service(self):
        """ this called after Evalution and service and this is quality Control and shipping"""
        self.service_state = 'quality'
        return self.action_view_serv()
    
    def action_finmobile_service(self):
        """this called after quality Control and shipping this is Delivery state
        to this level can send information to crm , Print , send email
        """
        self.return_date = datetime.now()
        self.service_state = 'delivered'
        return self.action_view_serv()


    def action_send_mail(self):
        """This function opens a window to compose an email, with the edi sale template message loaded by default"""
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
            'default_model': 'mobile_service.service',
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
    
#this function count the invoices for this service that active
    def _invoice_count(self):
        invoice_ids = self.env['account.move'].search(
            [('invoice_origin', '=', self.name)])
        self.invoice_count = len(invoice_ids)


#this function count that service with this imei number
    @api.onchange('imei_no')
    def _service_count(self):
        self.service_count = self.search(
            [('imei_no', '=', self.imei_no)], count=True)


#create function to this level create the request and request number and goto draft state
    @api.model
    def create(self, vals):
        print(self.env.user.company_id)
        if 'company_id' in vals:
            vals['name'] = self.env['ir.sequence'].with_context(force_company=self.env.user.company_id.id).next_by_code(
                'mobile_service.service.sequence') or _('New')
        else:
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'mobile_service.service.sequence') or _('New')
        vals['service_state'] = 'draft'
        
        return super(MobileServiceShop, self).create(vals)


#this function create error you cannot delete services that is not in draft state(or assigned)
    def unlink(self):
        for i in self:
            if i.service_state != 'draft':
                raise UserError(
                    _('You cannot delete an assigned service request'))
        return super(MobileServiceShop, self).unlink()


#action window for invoice create
    def action_invoice_create_wizard(self):
        """
        Create new invoice based on current items
        """
        return {
            'name': _('Create Invoice'),
            'view_mode': 'form',
            'res_model': 'mobile_service.invoice',
            'type': 'ir.actions.act_window',
            'target': 'new'
        }

#action for post stock level
    def action_post_stock(self):
        flag = 0
        for order in self.product_order_line:
            if order.product_uom_qty > order.qty_stock_move:
                flag = 1
                pick = {
                    'picking_type_id': self.picking_transfer_id.id,
                    'partner_id': self.person_id.id,
                    'origin': self.name,
                    'location_dest_id': self.person_id.property_stock_customer.id,
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


#! Actions for view forms -------------------------->
    def action_view_services(self):
        self.ensure_one()
        ctx = dict(
            create=False,
        )
        action = {
            'name': _("Services"),
            'type': 'ir.actions.act_window',
            'res_model': 'mobile_service.service',
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
    #create a view form for invoices
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
    #!Action Warranty View ----------------------------------->
    def action_view_warranty(self):
        self.ensure_one()
        ctx = dict(
            create=True,
        )
        action = {
            'name': _("Warranty"),
            'type': 'ir.actions.act_window',
            'res_model': 'mobile_service.warranty',
            'target': 'current',
            'context': ctx
        }
        warranty_idMs = self.env['mobile_service.warranty'].search(
            [('name', '=', self.warranty_id.name)])
        war_ids = []
        for each in warranty_idMs:
            war_ids.append(each.id)
        if len(warranty_idMs) == 1:
            warranti = war_ids and war_ids[0]
            action['res_id'] = warranti
            action['view_mode'] = 'form'
            action['views'] = [
                (self.env.ref('mobile_service.mobile_service_warranty_form_view').id, 'form')]
        else:
            action['view_mode'] = 'tree,form'
            action['domain'] = [('id', 'in', war_ids)]
        return action
    #! Get report action and return ticket
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
        complaint_ids = self.env['mobile_service.complaint.tree'].search(
            [('complaint_id', '=', self.id)])
        if complaint_ids:
            for obj in complaint_ids:
                complaint = obj.complaint_type_tree
                description = obj.description_tree
                complaint_text = complaint.complaint_type + ", " + complaint_text
                if description.description:
                    description_text = description.description + ", " + description_text
        else:
            for obj in complaint_ids:
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
            'customer_id': self.person_id.name,
            'imei_no': self.imei_no,
            'technician': self.technician_id.name,
            'complaint_types': complaint_text,
            'complaint_description': description_text,
            'mobile_brand': self.brand_id.name,
            'model_name': self.model_id.name,

        }
        return self.env.ref('mobile_service.mobile_service_ticket').report_action(self, data=data)
    
    #! checked that is in warranty and return true or false
    @api.depends('warranty_id')
    def _compute_is_in_warranty(self):
        self.is_in_warranty = self.warranty_id and (
            self.warranty_id.expire_date and self.warranty_id.expire_date > self.date_request) and self.warranty_id.state in 'valid'
        
#! Connect To Mobile Service and Create this item for this fields
    def register_to_crm_service(self):
        # Create CRM and record this fields
        Model = request.env['crm.lead']
        Model.sudo().create({
            'name': self.name,
            'street': self.street,
            'phone': self.contact_no,
            'email_from': self.email_id,
            'description': self.internal_notes,
            'date_closed' : self.warranty_id.expire_date,
            'partner_id' : self.person_id.id,
            'national_code' : self.national_code,
        })