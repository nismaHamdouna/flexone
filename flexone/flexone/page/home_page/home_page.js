frappe.pages['home-page'].on_page_load = function (wrapper) {

	frappe.require([

	], function () {
		frappe.homepage = new frappe.Homepage(wrapper);
	});
};


frappe.Homepage = Class.extend({
	init: function (parent) {
		frappe.ui.make_app_page({
			parent: parent,
			title: __("Flexsofts.com"),
			single_column: true
		});

		this.parent = parent;
		this.page = this.parent.page;
		this.make();
},


make: function () {
		var me = this;
    this.body = $('<div></div>').appendTo(this.page.main);
    var data = "";
    var $container =$(frappe.render_template('homepage', data)).appendTo(this.body);

  },


});

