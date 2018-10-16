# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "flexone"
app_title = "flexone"
app_publisher = "GreyCube Technologies"
app_description = "ERPnext Theme"
app_icon = "fa fa-paint-brush"
app_color = "gold"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
    "assets/css/flexone.min.css"  
]
app_include_js = [
    "/assets/js/flexone.min.js",
    "/assets/js/flexone-template.min.js",
    "/assets/flexone/js/d3.min.js",
    "/assets/flexone/js/c3.min.js"
]

# include js, css files in header of web template
web_include_css = "/assets/flexone/css/flexone-web.css"
# web_include_js = "/assets/flexone/js/flexone.js"

# login
on_session_creation = "flexone.api.on_session_creation"

# include js in page
# page_js = {"page" : "public/js/file.js"}
page_js = {"modules" : "public/js/flexone_hide_help.js"}
# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Home Pages
# ----------
website_context = {
	"favicon": 	"/assets/flexone/images/icon.png",
	"splash_image": "/assets/flexone/images/logo.jpg"
}
# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "flexone.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

#before_install = "flexone.install.before_install"
after_install = "flexone.api.import_arabic_translation"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "flexone.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# copy journal_entry_account remark field to general ledger remark field
doc_events = {
    "Journal Entry": {
        "on_submit": "flexone.api.add_remark_in_journal_entry_account",        
    }
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"flexone.tasks.all"
# 	],
# 	"daily": [
# 		"flexone.tasks.daily"
# 	],
# 	"hourly": [
# 		"flexone.tasks.hourly"
# 	],
# 	"weekly": [
# 		"flexone.tasks.weekly"
# 	]
# 	"monthly": [
# 		"flexone.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "flexone.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "flexone.event.get_events"
# }

