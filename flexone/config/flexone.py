from frappe import _

def get_data():
	return [
		{
			"label": _("Flexone"),
			"items": [
				{
					"type": "page",
					"name": "dashboard",
				}
			]
		}
    ]
