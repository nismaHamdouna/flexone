from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.sessions import Session

import frappe.defaults

def set_home_page():
    user = frappe.session.user
    roles = frappe.get_roles(user)

def on_session_creation(login_manager):
	info = frappe.db.get_value("User", frappe.local.session_obj.user,
			["home_page_link"], as_dict=1)

	frappe.local.response["home_page"] = info.home_page_link or "/desk"


def add_records(records):
    # from erpnext/setup/setup_wizard/install_fixtures.py
    # this should be added as a function in frappe like frappe.add_records(records)
    from frappe.modules import scrub
    for r in records:
        doc = frappe.new_doc(r.get("doctype"))
        doc.update(r)
        doc.insert(ignore_permissions=True)

def add_paper_item_groups(raw_material_group):
    raw_material_group.is_group = True
    raw_material_group.save()

    records = [
       

        {"doctype": "Item Group", "item_group_name": _("Paper"), "is_group": 0, "parent_item_group": raw_material_group.name },
        {"doctype": "Item Group", "item_group_name": _("Gum"), "is_group": 0, "parent_item_group": raw_material_group.name },
        {"doctype": "Item Group", "item_group_name": _("Ink"), "is_group": 0, "parent_item_group": raw_material_group.name },
        {"doctype": "Item Group", "item_group_name": _("Coil"), "is_group": 0, "parent_item_group": raw_material_group.name },
        {"doctype": "Item Group", "item_group_name": _("Board"), "is_group": 0, "parent_item_group": raw_material_group.name },
        {"doctype": "Item Group", "item_group_name": _("Board Layer"), "is_group": 0, "parent_item_group": raw_material_group.name },
    ]
    print("Adding new categories to Raw Material")
    add_records(records)

def delete_custom_roles(role):
    frappe.db.sql('delete from `tabCustom Role` where name in( select parent from `tabHas Role` where role=%s)', role)
    frappe.db.sql('delete from `tabHas Role` where role=%s', role)

    print("Removing custom roles")

def delete_users(role):
	for user in frappe.get_all("User", ["name"], {"role": role}):
		frappe.delete_doc("User", user.name)
        print("Removing users")


def delete_Custom_DocPerm(role):
    frappe.db.sql('delete from `tabCustom DocPerm` where role=%s', role)
    print("Removing custom doc perm")


def delete_role(role):
    frappe.delete_doc("Role", role)
    print("Removing roles")

def add_my_role(my_role):
    role = frappe.db.get_value("Role", my_role)
    if (role is not None): return
    print(role)    
    records = [
        {"doctype": "Role","name":my_role,"role_name":my_role,"disabled":0,"desk_access":1,"two_factor_auth":0,"restrict_to_domain":""},

    ]
    print(records)
    print("Adding Roles")
    add_records(records)

def add_Custom_DocPerm(role):
    role = frappe.db.get_value("Role", role)
    if (role is not None): 
        records = [
        {"doctype":"Custom DocPerm","parent":"Item Group","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Holiday List","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Employment Type","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Item Variant Settings","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Supplier Type","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Employee","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Payment Request","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Leave Application","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Journal Entry","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Purchase Invoice","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Expense Claim Type","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Item","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Terms and Conditions","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Employee Loan","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"User","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"HR Settings","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Stock Entry","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Expense Claim","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Stock Reconciliation","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Purchase Order","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"User Permission","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Account","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Customer","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"GL Entry","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Price List","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Payment Entry","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Buying Settings","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Sales Taxes and Charges Template","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Quotation","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Item Price","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Supplier","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Upload Attendance","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Salary Structure","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Salary Slip","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Stock Ledger Entry","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Territory","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Item Attribute","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Fiscal Year","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Warehouse","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Stock Settings","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Pricing Rule","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Leave Allocation","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Company","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Employee Loan Application","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Leave Block List","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Sales Person","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Leave Type","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Sales Order","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Sales Invoice","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Brand","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Payment Term","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Leave Control Panel","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Purchase Taxes and Charges Template","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Employee Attendance Tool","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Tax Rule","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Accounts Settings","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Selling Settings","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Employee Advance","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},
        {"doctype":"Custom DocPerm","parent":"Loan Type","parentfield":"permissions","parenttype":"DocType","share":1,"export":1,"cancel":0,"create":1,"submit":0,"write":1,"role":role,"print":1,"import":0,"permlevel":0,"apply_user_permissions":0,"read":1,"set_user_permissions":0,"report":1,"amend":0,"email":1,"if_owner":0},         

        ]
        print("Adding Custom DocPerm")
        add_records(records)


def add_paper_template(name):
    frappe.db.sql("""delete from `tabItem Attribute` where name='Colour'""")
    frappe.db.sql("""delete from `tabItem Attribute Value` where parent='Colour'""")
    frappe.db.sql("""delete from `tabItem Attribute` where name='Size'""")
    frappe.db.sql("""delete from `tabItem Attribute Value` where parent='Size'""")
    records = [
        {"doctype": "Item Attribute", "attribute_name":_("BF"), "numeric_values": True, "from_range": 12, "increment": 2, "to_range": 30},
        {"doctype": "Item Attribute", "attribute_name":_("GSM"), "numeric_values": True, "from_range": 100, "increment": 5, "to_range": 250},
        {"doctype": "Item Attribute", "attribute_name":_("Deck"), "numeric_values": True, "from_range": 50, "increment": 0.5, "to_range": 250},
        {'doctype': "Item Attribute", "attribute_name": _("Colour"), "item_attribute_values": [
                                                                        {"attribute_value": _("White"), "abbr": "WHI"},
                                                                        {"attribute_value": _("Brown"), "abbr": "BRW"},]
        },
        {"doctype": "Item", "item_code": name, "item_group": "Paper", "stock_uom": "Kg", "default_material_request_type": "Purchase",
                            "is_stock_item": True, "is_sales_item": False, "has_variants": True, "variant_based_on": "Item Attribute",
                            "attributes": [
                                {"attribute": _("Colour")},
                                {"attribute": _("BF")},
                                {"attribute": _("GSM")},
                                {"attribute": _("Deck")},
                            ]
        },
    ]
    print("Adding paper template as Item")
    add_records(records)

def update_mf_settings():
    #Allow over production
    print "Updating manufacturing settings"
    mf_settings = frappe.get_doc({"doctype": "Manufacturing Settings", "allow_production_on_holidays": 0})
    mf_settings.allow_production_on_holidays = 1
    mf_settings.allow_overtime = 1
    mf_settings.over_production_allowance_percentage = 50
    #This doesn't handle multiple companies
    mf_settings.default_wip_warehouse = frappe.db.get_value("Warehouse", filters={"warehouse_name": _("Stores")})
    mf_settings.default_fg_warehouse  = frappe.db.get_value("Warehouse", filters={"warehouse_name": _("Finished Goods")})
    mf_settings.save()

    stock_settings = frappe.get_doc({"doctype": "Stock Settings", "tolerance": 0})
    stock_settings.tolerance = 50
    stock_settings.save()

    buy_settings = frappe.get_doc({"doctype": "Buying Settings", "maintain_same_rate": 1})
    if (buy_settings is not None):
        buy_settings.maintain_same_rate = 0
        buy_settings.save()

def before_install():
    #update_mf_settings()

    #rm_group = "Raw Material"
    #paper_template = "PPR"
    #raw_material_group = frappe.get_doc("Item Group", rm_group)
    #if (raw_material_group.is_group == False):
    #    add_paper_item_groups(raw_material_group)
    delete_custom_roles("FlexOneAdmin")
    delete_users("FlexOneAdmin")
    delete_Custom_DocPerm("FlexOneAdmin")
    delete_role("FlexOneAdmin")
    print("removed roles")
    role_name = "FlexOneAdmin"
    print(role_name)
    add_my_role(role_name)
    add_Custom_DocPerm("FlexOneAdmin")
    print("added roles")
    #paper_rm = frappe.db.sql_list("""select name from `tabItem` where item_name=%s""", paper_template)
    #if not paper_rm:
    #    add_paper_template(paper_template)

def after_install():
    doc = frappe.new_doc("CM Paper")
    #doc.save(ignore_permissions=True)
