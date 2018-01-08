# -*- coding: utf-8 -*-
from openerp import tools
from openerp import models, fields, api,exceptions
from email.utils import formataddr
import email
from email.header import Header

class server_desk(models.Model):
    _name = 'server_desk.server_desk'

    name = fields.Char()

class Cco(models.Model):
    _name ='server_desk.cco_account'
    _rec_name = 'account'

    account = fields.Char(required=True)
    passward = fields.Char(required=True)

class equipment(models.Model):
    _name ='server_desk.equipment'
    _rec_name = 'SN'

    SN = fields.Char(required=True,string="SERIAL NUMBER / PAK NUMBER") #序列号
    contract = fields.Many2one('server_desk.contract', string="CONTRACT NUMBER") #合同号
    server_level = fields.Char(string="SERVICE LEVEL") #服务级别
    company = fields.Char(string="BILL TO NAME") #公司名称
    customer = fields.Many2one('res.partner',string="SITE NAME" ,domain=[('category','=',u'case客户')]) #客户名称
    product = fields.Char(string="PRODUCT NUMBER") #产品型号
    product_relationship = fields.Char(string="PRODUCT RELATIONSHIP") #产品相互关系
    description  = fields.Char(string="DESCRIPTION") #产品描述
    begin_date = fields.Date(string="BEGIN DATE") #维保开始日期
    end_date = fields.Date(string="END DATE") #维保结束日期
    last_date_of_support = fields.Date(string="LAST DATE OF SUPPORT") #EOS日期
    product_ship_date = fields.Date(string="PRODUCT SHIP DATE") #产品发货日期
    contract_label  = fields.Char(string="CONTRACT LABEL") #
    service_level_status  = fields.Char(string="SERVICE LEVEL STATUS") #
    bill_to_name  = fields.Char(string="BILL TO NAME") #
    bill_to_address  = fields.Char(string="BILL TO ADDRESS") #
    bill_to_city  = fields.Char(string="BILL TO CITY / PROVINCE") #
    bill_to_postal_code  = fields.Char(string="BILL TO POSTAL CODE") #
    bill_to_country  = fields.Char(string="BILL TO COUNTRY") #
    bill_to_phone  = fields.Char(string="BILL-TO PHONE") #
    bill_to_email  = fields.Char(string="BILL-TO EMAIL") #
    site_id  = fields.Char(string="SITE ID") #
    site_address  = fields.Char(string="SITE ADDRESS") #
    site_address_line2  = fields.Char(string="SITE ADDRESS LINE2") #
    site_address_line3  = fields.Char(string="SITE ADDRESS LINE3") #
    site_city  = fields.Char(string="SITE CITY") #
    site_state = fields.Char(string="SITE STATE / PROVINCE") #
    site_postal_code  = fields.Char(string="SITE POSTAL CODE") #
    site_country  = fields.Char(string="SITE COUNTRY") #
    site_parent_company_name  = fields.Char(string="SITE PARENT COMPANY NAME") #
    site_email  = fields.Char(string="SITE EMAIL") #
    site_parent_company_id  = fields.Char(string="SITE PARENT COMPANY ID") #
    site_notes  = fields.Char(string="SITE NOTES") #
    site_label  = fields.Char(string="SITE LABEL") #
    site_contact  = fields.Char(string="SITE CONTACT") #
    site_phone  = fields.Char(string="SITE PHONE") #
    distributor_bill_to_id  = fields.Char(string="DISTRIBUTOR BILL TO ID") #
    distributor_bill_to_name  = fields.Char(string="DISTRIBUTOR BILL TO NAME") #
    product_quantity  = fields.Char(string="PRODUCT QUANTITY") #
    priority_item = fields.Char(string="PRIORITY ITEM (GROUP S)") #
    host_id  = fields.Char(string="HOST ID") #
    instance_number  = fields.Char(string="INSTANCE NUMBER") #
    parent_instance_number  = fields.Char(string="PARENT INSTANCE NUMBER") #
    product_label  = fields.Char(string="PRODUCT LABEL") #
    product_type  = fields.Char(string="PRODUCT TYPE") #
    covered_product_status  = fields.Char(string="COVERED PRODUCT STATUS") #
    product_so_number  = fields.Char(string="PRODUCT SO NUMBER") #
    product_po_number  = fields.Char(string="PRODUCT PO NUMBER") #
    maintenance_so_number  = fields.Char(string="MAINTENANCE SO NUMBER") #
    maintenance_po_number  = fields.Char(string="MAINTENANCE PO NUMBER") #
    do_not_renew_reason_code  = fields.Char(string="DO NOT RENEW REASON CODE") #
    warranty_type  = fields.Char(string="WARRANTY TYPE") #
    warranty_end_date  = fields.Date(string="WARRANTY END DATE") #
    shipment_delivery_notice  = fields.Char(string="SHIPMENT DELIVERY NOTICE") #

class Contract(models.Model):
    _name ='server_desk.contract'
    _rec_name = 'contract_id'

    contract_id = fields.Char(string="Contract Number", required=True)
    start_time = fields.Date(compute='_count_time',store='True')
    stop_time = fields.Date(compute='_count_time',store='True')
    serivce_category1 = fields.Char()
    serivce_category2 = fields.Char()
    sow = fields.Text()
    serivce_level = fields.Char()
    cco = fields.Many2many('server_desk.cco_account', string="CCO")
    bill2id = fields.Char(string="Bill To ID ")
    contract_type = fields.Char(string="Contract Type")
    access_level = fields.Char(string="Access Level")
    software_download = fields.Char(string="Software Download")
    srv_req = fields.Char(string="Service Request Management")
    locked = fields.Char(string="Locked")
    site_name = fields.Char(string="Installed-At Site Name ")
    partner_id = fields.Many2many('res.partner', string="客户", domain=[('category','=',u'case客户')])
    equipment_ids = fields.One2many('server_desk.equipment','contract',string="设备")

    @api.multi
    @api.depends('equipment_ids')
    def _count_time(self):
        for record in self:
            if len(record.equipment_ids):
                record.start_time = record.equipment_ids[0].begin_date
                record.stop_time = record.equipment_ids[0].end_date
                for equipment in record.equipment_ids:
                    if record.start_time > equipment.begin_date:
                        record.start_time = equipment.begin_date
                    if record.stop_time < equipment.end_date:
                        record.stop_time=equipment.end_date


class Case(models.Model):
    _name ='server_desk.case'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _mail_post_access = 'read'
    _rec_name = 'case_id'
    _track = {
        'state':{
            'server_desk.case_cds':lambda self, cr, uid, obj, ctx=None: obj.state and obj.state == 'cds',
            'server_desk.case_state':lambda self, cr, uid, obj, ctx=None: obj.state and obj.state != 'cds',
            },
    }
    case_id = fields.Char()
    applicant_id = fields.Many2one('res.users', string="申请人",required=True,default=lambda self: self.env.user)
    applicant_way = fields.Char(string="申请方式",default=lambda self: self._get_app_way_def())
    case_type = fields.Selection([('Technology diagnosis','技术诊断'),
                                  ('Technical consulting','技术咨询'),
                                  ('RMA','RMA'),
                                  ('DOA','DOA'),
                                  ('standby','standby')],default='Technology diagnosis',string="case类型",required=True)
    server_type = fields.Many2one('server_desk.server_type',string="服务类型")
    case_level = fields.Selection([('level1','1'),('level2','2'),('level3','3'),('level4','4')],default='level1')
    case_type_note = fields.Text(string="case类型说明")
    user_id = fields.Many2one('res.users', string="当前处理人",default=lambda self: self.env.user)
    cds_id = fields.Many2one('res.users', string="服务台处理人")
    tac1_id = fields.Many2one('res.users', string="TAC1处理人")
    tac2_id = fields.Many2one('res.users', string="TAC2处理人")
    master_id = fields.Many2one('res.users', string="专家处理人")
    product_id = fields.Many2one('res.users', string="产品经理")
    group_id = fields.Many2one('res.groups',string="当前处理组",domain =[('group_id','in','self.groups_id')] )
    note = fields.Text(string="备注")
    state = fields.Selection([
        ('new',"新建case"),
        ('cds',"坐席处理"),
        ('tac1',"TAC一线处理"),
        ('tac2',"TAC二线线处理"),
        ('master',"专家处理"),
        ('oem',"厂商处理"),
        ('customer_feedback',"客户反馈"),
        ('audit',"审核"),
        ('done',"关闭"),
    ],default='new',string="状态",ack_visibility='onchange')
    error_description = fields.Text(string="故障描述",required=True)
    error_log = fields.Text()
    customer_feedback = fields.Text(string="客户反馈")
    feedback_ids = fields.One2many('server_desk.feedback', 'case_id', string="处理过程")
    contact_user = fields.Char(string="故障联系人",required=True)
    contact_user_phone = fields.Char(string="联系电话",required=True)
    contact_email = fields.Char(string="联系邮箱")
    preemption = fields.Integer(default=0)
    priority = fields.Char(default="高优先级")
    close_date = fields.Datetime(string="关闭时间")
    case_title=fields.Char(string='case标题')
    case_oem_no=fields.Char(string='厂商case编号')
    start_time =fields.Datetime(string="开始时间")
    end_time = fields.Datetime(string="结束时间")
    change_SN = fields.Char(string="新的SN")
    is_oem = fields.Boolean(string="是否厂商处理")
    name = fields.Char()
    keyword = fields.Text()
    error_name = fields.Many2one('server_desk.fault', string="error_name")
    device_id = fields.Many2one('server_desk.equipment', string="device")
    solution = fields.Text()
    next_group = fields.Selection([('ACS\CDN',"ACS\CDN"),
        (u'交换机\路由器',u"交换机\路由器"),])

    #  以下这些字段，跟维保服务平台并行
    SN_char = fields.Char(string="SN_char")
    contract_id = fields.Many2one("server_desk.contract",string="合同",readonly=1)
    SN = fields.Many2one('server_desk.equipment',string="SN")
    customer_id = fields.Many2one(related='SN.customer', string="客户", readonly=1, domain=[('category', '=', u'case客户')],store=True)
    product = fields.Char(string="产品型号")  # 产品型号

    eq_wbfw_id = fields.Many2one('nantian_wbfw.equipment',string="维保合同的设备", store="True")# compute="_verify_contract_id",
    contract_wbfw_id = fields.Many2one('nantian_wbfw.maintenance_contract', string="维保合同",store="True")
    customer_wbfw = fields.Char(string="客户")
    product_wbfw = fields.Char(string="产品型号(弃用)")

    # 添加个字段用于在tree上显示客户
    view_customer = fields.Char(string="客户")

    @api.multi
    def _view_customer_product(self):
        case_records = self.env['server_desk.case'].search([])
        for s in case_records:
            if s.customer_id:
                s.view_customer = s.customer_id.name
            elif s.customer_wbfw:
                s.view_customer = s.customer_wbfw
                s.product = s.product_wbfw
            else:
                pass

    # 还没写完的RMA功能
    def pop_window(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        form_res = mod_obj.get_object_reference(cr, uid, 'server_desk', 'case_change_SN_view')
        form_id = form_res and form_res[1] or False
        value = {
            'name': ('更换SN号'),
            'res_model': 'server_desk.log',
            'views': [[False, 'form']],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        return value



    @api.multi
    def onchange_SN(self,SN_char):
        result = {'value': {}}
        if SN_char:
            get_sn = self.env['server_desk.equipment'].search([('SN','=',SN_char)],limit=1)
            get_wbfw_sn = self.env['nantian_wbfw.equipment'].search([('SN','=',SN_char)])
            if get_sn or get_wbfw_sn:
                if get_wbfw_sn:
                    if fields.Date.from_string(get_wbfw_sn.end_date) >= fields.date.today():
                        result['value']['eq_wbfw_id'] = get_wbfw_sn.id
                        result['value']['contract_wbfw_id'] = get_wbfw_sn.contract_id.id
                        result['value']['customer_wbfw'] = get_wbfw_sn.customer
                        result['value']['product'] = get_wbfw_sn.type
                        result['value']['view_customer'] = get_wbfw_sn.customer
                    else:
                        raise exceptions.ValidationError('SN号已过保')
                elif get_sn:
                    if fields.Date.from_string(get_sn.end_date) >= fields.date.today():
                        result['value']['SN'] = get_sn.id
                        result['value']['customer_id'] = get_sn.customer.id
                        result['value']['contract_id'] = get_sn.contract.id
                        result['value']['product'] = get_sn.product
                        result['value']['view_customer'] = get_sn.customer.name
                    else:
                        raise exceptions.ValidationError('SN号已过保')
                return result
            else:
                raise exceptions.ValidationError('SN号不存在')



    def change_SN(self, cr, uid, ids, *args):
        return self.pop_window(cr, uid, ids, None)


    @api.model
    def _get_app_way_def(self):
        if self.env['res.groups'].search([('name', '=', '服务台')],limit=1) in self.env.user.groups_id:
            return "电话"
        return "Web"


    def send_email(self,cr,uid,users,data=[],context=None):
            template_model = self.pool.get('email.template')
            ids = template_model.search(cr,uid,[('name','=','case邮件提醒')],context=None)
            template = template_model.browse(cr,uid,ids,context=None)
            to_list = []
            for user in users:
                to_list.append(formataddr((Header(user.name,'utf-8').encode(),user.email)))
            mail_mail = self.pool.get('mail.mail')
            for i in range(len(data)):
                if not data[i]:
                    data[i] = ''
            mail_id = mail_mail.create(cr, uid, {
                            'body_html': '<div><p>您好:</p>'
                                '<p>这个case需要您处理,您可登录：<a href="http://123.56.147.94:8000">http://123.56.147.94:8000</a></p></div>',
                            # 'subject': 'Re: %s+%s+%s' %(str(data[0]).decode('utf-8').encode('gbk'),str(data[1]).decode('utf-8').encode('gbk'),str(data[2]).decode('utf-8').encode('gbk')),
                            'subject':data[0]+u','+data[1]+u','+data[2],
                             'email_to': to_list,
                            'auto_delete': True,
                        }, context=context)
            mail_mail.send(cr, uid, [mail_id], context=context)

    ### load balance the request 
    @api.multi
    def _load_balance(self,group,method=None):
        system_obj = self.env['server_desk.system'].search([('name','=','system')],limit=1)
        i = getattr(system_obj,group)
        group_users = self.env['res.groups'].search([('name','=',group)]).users
        if i == 0:
            self.env['server_desk.system'].search([('name','=','system')]).write({group:len(group_users)})
            i = getattr(system_obj,group)
        try:
            user = group_users[i-1]
        except:
            self.env['server_desk.system'].search([('name','=','system')]).write({group:len(group_users)})
            i = getattr(system_obj,group)
            user = group_users[i-1]
        self.env['server_desk.system'].search([('name','=','system')]).write({group:i-1})
        return user
    @api.multi
    def judge_deal(self):
        for feedback in self.feedback_ids:
            if feedback.processor_id == self.env.user and feedback.record:

                return True
        return False
    @api.multi
    def judge_feedback(self):
        for feedback in self.feedback_ids:
            if feedback.processor_id == self.env.user and feedback.feedback_user_id == self.env.user and not feedback.result:
                return False
            if feedback.processor_id == self.env.user and feedback.feedback_user_id == self.env.user and not feedback.note:
                return False
        return True
    @api.multi
    def action_cds(self):
        self.state = 'cds'
        recs = self.env['res.groups'].search([('name','=','cds_group')])
        self.group_id = recs[0] 
        ### load balance the request to tac1 and achieve session hold
        if not self.cds_id:
            self.cds_id = self._load_balance('cds_group')
            # 添加任务处理人为关注者
            self.message_subscribe([self.cds_id.partner_id.id])
        data=[self.case_id,self.product,self.case_title]
        self.send_email([self.cds_id],data)
        self.user_id = self.cds_id

    @api.multi
    def action_new(self):
        self.state = 'new'
        self.user_id = self.env.uid

    @api.multi
    def action_tac1(self,subtype_ids=None):
        recs = self.env['res.groups'].search([('name','=','tac1_group')])
        self.group_id = recs[0] 
        ### load balance the request to tac1 and achieve session hold
        if not self.tac1_id:

            self.tac1_id = self._load_balance('tac1_group')
            # 添加任务处理人为关注者
            self.message_subscribe([self.tac1_id.partner_id.id])
        # if not self.case_oem_no:
        #     raise exceptions.ValidationError('请填写case厂家编号')
        data = [self.case_id, self.product, self.case_title]
        self.send_email([self.tac1_id],data)
        self.state = 'tac1'
        self.env['server_desk.feedback'].create({'processor_id': self.tac1_id.id,'case_id': self.id,'state':self.state})
        self.user_id = self.tac1_id

    @api.multi
    def action_tac2(self):
        if not self.judge_feedback():
            raise exceptions.ValidationError('转下一步前，请填写处理结果及反馈描述')
        if not self.next_group:
            raise exceptions.ValidationError('转下一步前，请选择处理组')
        elif self.next_group == 'ACS\CDN':
            recs = self.env['res.groups'].search([('name','=','tac2_ACS_CDN_group')])
        elif self.next_group == u'交换机\路由器':
            recs = self.env['res.groups'].search([('name', '=', 'tac2_switch_router_group')])
        self.group_id = recs[0] 
        ### load balance the request to tac2 and achieve session hold
        if not self.tac2_id:
            self.tac2_id = self._load_balance(recs[0].name)
            # 添加任务处理人为关注者
            self.message_subscribe([self.tac2_id.partner_id.id])
        if not self.next_group:
            raise exceptions.ValidationError('转下一步前，请填写处理结果及反馈描述')

        data = [self.case_id, self.product, self.case_title]
        self.send_email([self.tac2_id],data)
        self.state = 'tac2'
        self.env['server_desk.feedback'].create({'processor_id': self.tac2_id.id,'case_id': self.id,'state':self.state})
        self.user_id = self.tac2_id

    @api.multi
    def action_master(self):
        if not self.judge_feedback():
            raise exceptions.ValidationError('转下一步前，请填写处理结果及反馈描述')
        recs = self.env['res.groups'].search([('name','=','master_group')])
        self.group_id = recs[0]
        ### load balance the request to master and achieve session hold
        if not self.master_id:
            self.master_id = self._load_balance('master_group')
            # 添加任务处理人为关注者
            self.message_subscribe([self.master_id.partner_id.id])
        data = [self.case_id, self.product, self.case_title]
        self.send_email([self.master_id],data)
        self.state = 'master'
        self.env['server_desk.feedback'].create({'processor_id': self.master_id.id,'case_id': self.id,'state':self.state})
        self.user_id = self.master_id
    @api.multi
    def action_done(self):
        self.state = 'done'
        self.close_date = fields.datetime.now()
        if self.case_type != 'standby':
            self.env['server_desk.solution'].create({'case_id':self.id,'keyword':self.keyword,'fault_type':self.error_name.id,'equipment_type':self.product,'solution':self.solution ,'fault_symptom':self.error_description})
    @api.multi
    def action_oem(self):
        if not self.judge_feedback():
            raise exceptions.ValidationError('转下一步前，请填写处理结果及反馈描述')
        self.state = 'oem'
        recs = self.env['res.groups'].search([('name','=','tac1_group')])
        self.is_oem = True
        self.group_id = recs[0]
        self.priority = "低优先级"
        data = [self.case_id, self.product, self.case_title]
        self.send_email([self.tac1_id],data)
        self.env['server_desk.feedback'].create({'processor_id': self.tac1_id.id, 'case_id': self.id,'state':self.state})
        self.user_id = self.tac1_id

    @api.multi
    def action_customer_feedback(self):
        if self.state != 'audit':
            if not self.judge_deal():
                raise exceptions.ValidationError('转下一步前，请填写处理过程及记录')
            self.state = 'customer_feedback'
            for feedback in self.feedback_ids:
                if feedback.processor_id == self.env.user:
                    feedback.feedback_user_id=self.env.user
        else:
            self.state = 'customer_feedback'
            data = [self.case_id, self.product, self.case_title]
            self.send_email([self.tac1_id],data)
            self.user_id = self.feedback_ids[-1].processor_id
        
    @api.multi
    def action_customer_feedback_to_tac1(self):
        if not self.judge_feedback():
            raise exceptions.ValidationError('转下一步前，请填写处理结果及反馈描述')
        self.state = 'tac1'
        self.env['server_desk.feedback'].create({'processor_id': self.user_id.id,'case_id': self.id,'state':self.state})


    @api.multi
    def action_customer_feedback_to_tac2(self):
        if not self.judge_feedback():
            raise exceptions.ValidationError('转下一步前，请填写处理结果及反馈描述')
        self.state = 'tac2'
        self.env['server_desk.feedback'].create({'processor_id': self.user_id.id,'case_id': self.id,'state':self.state})


    @api.multi
    def action_customer_feedback_to_master(self):
        if not self.judge_feedback():
            raise exceptions.ValidationError('转下一步前，请填写处理结果及反馈描述')
        self.state = 'master'
        self.env['server_desk.feedback'].create({'processor_id': self.user_id.id,'case_id': self.id,'state':self.state})


    @api.multi
    def action_customer_feedback_to_oem(self):
        if not self.judge_feedback():
            raise exceptions.ValidationError('转下一步前，请填写处理结果及反馈描述')
        self.state = 'oem'
        self.is_oem = True
        self.env['server_desk.feedback'].create({'processor_id': self.user_id.id,'case_id': self.id,'state':self.state})


    @api.multi
    def judge_tac1(self):
        if self.user_id == self.env.user and self.tac1_id == self.env.user and not self.tac2_id:
           return True
        return False

    @api.multi
    def judge_tac2(self):
        if self.user_id == self.env.user and self.tac2_id == self.env.user and not self.master_id:
           return True
        return False

    @api.multi
    def judge_master(self):
        if self.user_id == self.env.user and self.master_id == self.env.user:
           return True
        return False

    @api.multi
    def judge_oem(self):
        if self.user_id == self.env.user and self.tac1_id == self.env.user and self.master_id:
           return True
        return False

    @api.multi
    def action_audit(self):
        if self.case_type != 'standby':
            if not self.solution or not self.error_name:
                raise exceptions.ValidationError('转产品经理前，请填写解决方案与与故障原因')
        if not self.judge_feedback():
            raise exceptions.ValidationError('转下一步前，请填写处理结果及反馈描述')
        self.state = 'audit'
        self.product_id = self.env['res.groups'].search([('name','=','product_manager_group')]).users[0]
        data = [self.case_id, self.product, self.case_title]
        self.send_email([self.product_id],data)
        self.user_id = self.env['res.groups'].search([('name', '=', 'product_manager_group')]).users[0]


    def create(self, cr, uid, vals, context=None):
        dates= fields.Date.today().split('-')
        date = ''.join(dates)
        template_model = self.pool.get('server_desk.case')
        ids = template_model.search(cr,uid,[('case_id','like',date)],context=None)
        cases = template_model.browse(cr,uid,ids,context=None).sorted(key=lambda r: r.case_id)
        if vals['case_type'] == 'standby' and not vals['start_time'] and not vals['end_time']:
            raise exceptions.ValidationError('请填写case开始时间，结束时间，关闭时间')
        if len(cases):
            vals['case_id']='C'+str(int(cases[-1].case_id[1:])+1)
        else:
            vals['case_id']='C'+date+'001'
        return super(Case,self).create(cr,uid,vals,context=context)


    @api.model
    def _needaction_domain_get(self):
        return [('user_id.id', '=', self.env.uid), ('state', '!=', 'done')]

class ServerType(models.Model):
    _name = 'server_desk.server_type'
    _rec_name = 'name'

    name = fields.Char(string="类型")


class Feedback(models.Model):
    _name = 'server_desk.feedback'

    processor_id = fields.Many2one('res.users', string="processor")
    result = fields.Char()
    record = fields.Text()
    feedback_user_id = fields.Many2one('res.users',string="feedback_user")
    note = fields.Text()
    case_id =  fields.Many2one('server_desk.case', string="case")
    feedback_time=fields.Datetime(string="反馈时间")
    state = fields.Char(string='处理阶段')
    
    #@api.depends()
    @api.onchange('note','result')
    def _onchange_feedback_time(self):
        for record in self:
            #self.update({'feedback_time':fields.datetime.now()})
            record.feedback_time = fields.datetime.now()
class Fault(models.Model):
    _name = 'server_desk.fault'
    _rec_name = 'error_name'

    error_log = fields.Char()
    error_name = fields.Char()
    device_id = fields.Many2one('server_desk.equipment', string="device")
    deal_user = fields.Many2one('hr.employee', string="deal_user")
    description = fields.Text()

class Solution(models.Model):
    _name = 'server_desk.solution'

    name = fields.Char(string="解决方案编号",readonly='True')
    case_id = fields.Many2one('server_desk.case')
    keyword = fields.Char(string="关键字")
    fault_type = fields.Many2one('server_desk.fault',string="故障类型")
    #fault_type = fields.Selection([("硬件", "硬件"), ("软件", "软件"), ("配置", "配置"), ("其他", "其他")], string="问题类型")
    equipment_type = fields.Char(string="设备型号")
    platfrom = fields.Char(string="平台")
    version = fields.Char(string="软件版本")
    # keyword = fields.Text(string="告警信息")
    fault_symptom = fields.Text(string="告警信息")
    fault_condition = fields.Text(string="故障发生条件")
    fault_conclusion = fields.Text(string="故障结论")
    cmd_list = fields.Text(string="命令列表")
    workaround = fields.Text(string="变通方案")
    solution = fields.Text(string="解决方案")
    counter = fields.Text(string="counter()")

    def create(self, cr, uid, vals, context=None):
        vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'server_desk.solution')
        return super(Solution, self).create(cr, uid, vals, context=context)




class System(models.Model):
    _name = 'server_desk.system'

    name = fields.Char()
    tac1_group = fields.Integer(default=lambda self:len(self.env['res.groups'].search([('name','=','tac1_group')]).users))
    tac2_ACS_CDN_group = fields.Integer(default=lambda self:len(self.env['res.groups'].search([('name','=','tac2_ACS\CDN_group')]).users))
    tac2_switch_router_group =fields.Integer(default=lambda self:len(self.env['res.groups'].search([('name','=','tac2_switch_router_group')]).users))
    master_group = fields.Integer(default=lambda self:len(self.env['res.groups'].search([('name','=','master_group')]).users))
    cds_group = fields.Integer(default=lambda self:len(self.env['res.groups'].search([('name','=','cds_group')]).users))

class log(models.Model):
    _name = 'server_desk.log'

    old_SN = fields.Char()
    new_SN = fields.Char()

    def create(self, cr, uid, vals, context=None):
        print context.get('active_id')
        template_model = self.pool.get('server_desk.equipment')

        ids = template_model.search(cr, uid, [('SN', 'like', vals['old_SN'])], context=None)
        equipment= template_model.browse(cr, uid, ids, context=None)
        equipment.SN = vals['new_SN']
        return super(log, self).create(cr, uid, vals, context=context)

class res_partner(models.Model):
    _inherit = 'res.partner'
    contact_users = fields.Many2many('res.users',string="联系人")
    SN = fields.One2many('server_desk.equipment','customer', string="设备",)  # 客户名称