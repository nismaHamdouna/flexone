from __future__ import unicode_literals

import frappe
import frappe.defaults
from frappe.utils import cstr, flt, fmt_money, formatdate, getdate
from frappe.utils import (cint, split_emails, get_request_site_address, cstr,get_files_path, get_backups_path, get_url, encode)
from frappe import _
from frappe.sessions import Session


@frappe.whitelist()
def import_arabic_translation():
	frappe.db.sql('delete from `tabTranslation`')
	from frappe.core.doctype.data_import.data_import import import_file_by_path
	import_file_by_path(path=frappe.utils.get_bench_path()+'/apps/flexone/flexone/public/translation/Translation.csv',ignore_links=False, overwrite=True,submit=False, pre_process=None, no_email=True)


def on_session_creation(login_manager):
	info = frappe.db.get_value("User", frappe.local.session_obj.user,
			["home_page_link"], as_dict=1)

	frappe.local.response["home_page"] = info.home_page_link or "/desk#home-page"

def add_remark_in_journal_entry_account(self,method):
	gl_entry=[]
	gl_entry=frappe.get_list('GL Entry', filters={'voucher_no': self.name}, fields=['name', 'remarks', 'account'])
	for d in gl_entry:
		for jv_acct in self.get("accounts"):
			if ((jv_acct.account==d.account) and (jv_acct.remark)):
				gl_matched_entry = frappe.get_doc('GL Entry', d.name)
				gl_matched_entry.flags.ignore_permissions = 1
				df = frappe.get_meta('GL Entry').get_field("remarks")
				df.allow_on_submit = 1
				gl_matched_entry.remarks=jv_acct.remark
				gl_matched_entry.save()

				df = frappe.get_meta('GL Entry').get_field("remarks")
				df.allow_on_submit = 0


def get_favicon():
	frappe.msgprint("d")
	return "/assets/flexone/images/icon.png"
