# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals, print_function
import frappe
import erpnext
from frappe.utils import add_to_date
from frappe.utils import flt, today, cint
from erpnext.utilities.page.leaderboard.leaderboard import get_leaderboard
from erpnext.accounts.utils import get_fiscal_year, now
import datetime
from frappe import _

from erpnext.setup.doctype.email_digest.email_digest import get_digest_msg
from erpnext.accounts.report.accounts_receivable_summary.accounts_receivable_summary import execute



@frappe.whitelist()
def total_collection():
	company = erpnext.get_default_company()
	start_date = frappe.db.sql("""select min(posting_date) from `tabSales Invoice` where company = %s""", (company))[0][0] or today()
	end_date = today()
	custom_filter = {'from_date': start_date,'to_date': end_date,'company': company}
	report = frappe.get_doc('Report', "Sales Payment Summary") 
	columns, data = report.get_data(filters = custom_filter, as_dict=True)
	label=_('TOTAL COLLECTION')
	if not data:
		return label,0
	else:
		sales_abbr="Sales - {}".format(frappe.db.get_value('Company', company, 'abbr'))	
		list_of_total_payments = [i[_("Payments")] for i in data if _("Payments") in i]
		return label,list_of_total_payments[-1]

@frappe.whitelist()
def profit_and_loss_chart():
	company = erpnext.get_default_company()
	filters = frappe._dict()
	filters.from_fiscal_year = frappe.db.sql("""select YEAR(min(posting_date)) from `tabSales Invoice` where company = %s""", (company))[0][0] or today()
	filters.to_fiscal_year=datetime.datetime.today().year
	filters.periodicity="Yearly"
	filters.company=company
	filters.accumulated_values=0
	from erpnext.accounts.report.profit_and_loss_statement.profit_and_loss_statement import execute
	a,b,c,chart=execute(filters)
	for x in (chart['data']['datasets']):
		x['title']=_(x['title'])
	return chart
	


@frappe.whitelist()
def total_sales():
	company = erpnext.get_default_company()
	start_date = frappe.db.sql("""select min(posting_date) from `tabSales Invoice` where company = %s""", (company))[0][0] or today()
	to_date=today()
	data=frappe.db.sql("""SELECT sum(`tabSales Invoice`.base_net_total) AS sum FROM `tabSales Invoice` WHERE `tabSales Invoice`.docstatus = 1 and company = %s and posting_date >= %s and posting_date <= %s  """, (company,start_date,to_date))[0][0] 
	label=_('TOTAL SALES')
	if not data:
		return label,0
	else:
		return label,data

@frappe.whitelist()
def due_amount():
	due_amount=0
	label=_('DUE AMOUNT')
	data = execute()
	if len(data[1]) > 0:
		for i in data[1]:
			due_amount=i[4]+due_amount
	return label, due_amount


@frappe.whitelist()
def top_moving_items():
	company = erpnext.get_default_company()
	records = get_leaderboard("Item","Year",company, "total_sales_amount")
	return records[:5]

@frappe.whitelist()
def weekly_data():
	company = erpnext.get_default_company()
	doc_name=frappe.get_all('Email Digest', filters={'company': company,'frequency':'Weekly','name':('like', '%%Default Weekly Digest%%')}, fields=['name'])
	#doc_name="Default Weekly Digest - "+company
	if len(doc_name) > 0:
		doc=frappe.get_doc('Email Digest', doc_name[0].name)
		doc.income_year_to_date=0
		doc.expense_year_to_date=0
		doc.issue=0
		doc.project=0
		doc.calendar_events=0
		doc.todo_list=0
		doc.notifications=0
		doc.add_quote=0
		doc.save()
		html=get_digest_msg(doc.name)	
		return html
	else:
		return 'Missing email digest with name -- '+'Default Weekly Digest - '+company