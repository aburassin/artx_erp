app_name = "art_zone"
app_title = "Art Zone"
app_publisher = "abdelwahab"
app_description = "Art Zone Mobile apps integration"
app_email = "abdelwahab.00964@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "art_zone",
# 		"logo": "/assets/art_zone/logo.png",
# 		"title": "Art Zone",
# 		"route": "/art_zone",
# 		"has_permission": "art_zone.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/art_zone/css/art_zone.css"
# app_include_js = "/assets/art_zone/js/art_zone.js"

# include js, css files in header of web template
# web_include_css = "/assets/art_zone/css/art_zone.css"
# web_include_js = "/assets/art_zone/js/art_zone.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "art_zone/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "art_zone/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "art_zone.utils.jinja_methods",
# 	"filters": "art_zone.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "art_zone.install.before_install"
after_install = ["art_zone.after_install.after_install"]

# Uninstallation
# ------------
# Migration
# after_migrate = ["art_zone.after_install.after_install"]

# before_uninstall = "art_zone.uninstall.before_uninstall"
# after_uninstall = "art_zone.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "art_zone.utils.before_app_install"
# after_app_install = "art_zone.after_install.create_custom_fields_for_art_zone"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "art_zone.utils.before_app_uninstall"
# after_app_uninstall = "art_zone.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "art_zone.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"art_zone.tasks.all"
# 	],
# 	"daily": [
# 		"art_zone.tasks.daily"
# 	],
# 	"hourly": [
# 		"art_zone.tasks.hourly"
# 	],
# 	"weekly": [
# 		"art_zone.tasks.weekly"
# 	],
# 	"monthly": [
# 		"art_zone.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "art_zone.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "art_zone.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "art_zone.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["art_zone.utils.before_request"]
# after_request = ["art_zone.utils.after_request"]

# Job Events
# ----------
# before_job = ["art_zone.utils.before_job"]
# after_job = ["art_zone.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"art_zone.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


# Custom Field
# fixtures = [
#     {
#         "dt": "Custom Field", 
#         "filters": []
#     },
#     {
#         "dt": "Accounting Dimension",
#         "filters": []
#     },
# ]
