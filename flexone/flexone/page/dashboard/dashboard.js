frappe.pages['dashboard'].on_page_load = function (wrapper) {

	frappe.require([

	], function () {
		frappe.dashboard = new frappe.Dashboard(wrapper);
	});
};


frappe.Dashboard = Class.extend({
	init: function (parent) {
		frappe.ui.make_app_page({
			parent: parent,
			title: __("Dashboard"),
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
		var $container = $(frappe.render_template('dashboard', data)).appendTo(this.body);

		me.render_widget("total_sales");
		me.render_widget("total_collection");
		me.render_widget("due_amount");
		me.render_date_widget("current_date");
		me.render_chart("profit_and_loss_chart");
		me.render_outstanding_chart("top_10_customer_outstanding");
		me.render_top5items_chart("top_5_items_chart");
		me.render_email_digest($container);
	},

	render_email_digest: function ($container) {

		frappe
			.call({
				method: "flexone.flexone.page.dashboard.dashboard.weekly_data"
			})
			.then(function (r) {
				if (!r.exc && r.message) {
					$container.find("#email-digest").html(r.message);

				}
			});
	},
render_top5items_chart: function (chart_id) {
	frappe
		.call({
			method: "flexone.flexone.page.dashboard.dashboard.top_moving_items"
		})
		.then(function (r) {
			if (!r.exc && r.message) {
				let data = r.message;
				if (data) {
					cust_colors = ['#ff9600', '#ffe100', '#ff0000', '#ff5b00', '#e084f9']
					var inputdata = {
						x: __('Items'),
						columns: [
							[],
							[]
						],
						type: 'bar',
						colors: {
							Sales: function (d) {
								return cust_colors[d.index]
							},
							مبيعات: function (d) {
								return cust_colors[d.index]
							}
						},
					};

					inputdata.columns[0].push(__('Items'))
					for (i = 0; i < data.length; i++) {
						inputdata.columns[0].push(__(data[i].name))
					}

					inputdata.columns[1].push(__('Sales'))
					for (i = 0; i < data.length; i++) {
						inputdata.columns[1].push(data[i].value)
					}

					var chart = c3.generate({
						bindto: '#Top5ItemsChart',
						data: inputdata,
						axis: {
							x: {
								type: 'category'
							}
						},
						legend: {
							show: false
						},
						bar: {
							width: {
								ratio: 0.5
							}
						},
						onrendered: function () {
							$("g").attr("direction", "ltr");
						}
					});

					$("#" + chart_id + "_title").html(__("Top 5 Items"));
				}
				$("#" + chart_id + "_title").html(__("Top 5 Items"));
			}
		});
},

render_chart: function (chart_id) {
		frappe
			.call({
				method: "flexone.flexone.page.dashboard.dashboard." + chart_id
			})
			.then(function (r) {
				if (!r.exc && r.message) {
					let data = r.message;
					if (data) {
						cust_colors = ['#7cd6fd', '#e084f9', '#743ee2']
						var inputdata = {
							x: 'x',
							columns: [
								['x']
							],
							colors: {},
							type: 'bar',
							label: true,
							bar: {
								width: {
									ratio: 0.5
								}
							},
							axis: {
								x: {
									type: 'category',
									
								}
							}
						};
						for (i = 0; i < data.data.labels.length; i++) {
							inputdata.columns[0].push(data.data.labels[i])
						}
						for (i = 0; i < data.data.datasets.length; i++) {
							inputdata.columns[i + 1] = [__(data.data.datasets[i].title)]
							inputdata.colors[__(data.data.datasets[i].title)] = cust_colors[i]
							
							for (d = 0; d < data.data.datasets[i].values.length; d++) {
								inputdata.columns[i + 1].push(data.data.datasets[i].values[d].toString());
							}
						}
						var chart = c3.generate({
							bindto: '#ProfitLossChart',
							data: inputdata,
							onrendered: function () {
								$("g").attr("direction","ltr");
							 }
						});
						$("#" + chart_id + "_title").html(__("Profit and Loss"));
					}
					$("#" + chart_id + "_title").html(__("Profit and Loss"));
				}
			});
	},

	render_outstanding_chart: function (chart_id) {
		frappe.call({
			method: "erpnext.utilities.page.leaderboard.leaderboard.get_leaderboard",
			args: {
				doctype: "Customer",
				timespan: "Year",
				company: frappe.defaults.get_default('company'),
				field: "outstanding_amount",
			},
			callback: function (r) {
				if (r.message != undefined) {
					let results = r.message || [];
					let graph_items = results.slice(0, 5);
					cust_colors = ['#78fca4', '#f7fc78', '#78a4fc', '#fc7986', '#788cfc']
					var inputdata = {
						columns: [
							[]
						],
						colors: {},
						type: 'pie',
						label: true
					};
					for (i = 0; i < graph_items.length; i++) {
						val = __(graph_items[i].name) + "-" + graph_items[i].value
						inputdata.columns[i] = [val]
						inputdata.colors[val] = cust_colors[i]
						inputdata.columns[i].push(graph_items[i].value)
					}
					var chart = c3.generate({
						bindto: '#OutstandingCustomerChart',
						data: inputdata,
						onrendered: function () {
							$("g").attr("direction","ltr");
						 },
							pie: {
								label: {
										format: function (value, ratio, id) {
												return value;
										}
								}
						}
					});
					$("#outstanding_customer_header").html(__("Top 5 Outstanding Customer"));
				}
				$("#outstanding_customer_header").html(__("Top 5 Outstanding Customer"));
			}
		});
	},
	render_widget(function_name) {
		var me = this;
		const company = frappe.defaults.get_default('company');
		const currency = frappe.get_doc(":Company", company).default_currency;
		frappe.call({
				method: "flexone.flexone.page.dashboard.dashboard." + function_name,
			})
			.then(function (r) {
				if (!r.exc && r.message) {
					let data = r.message;
					amount = format_currency(data[1], currency)
					if (data) {
						$("#" + function_name + "_name").html(__(data[0]));
						$("#" + function_name + "_value").html(amount);
					}
				}
			});
	},
	render_date_widget(function_name) {
		var me = this;
		current_date = frappe.datetime.get_today();
		$("#" + function_name + "_name").html(__('Today'));
		$("#" + function_name + "_value").html(current_date);
	}
});