frappe.pages['modules'].refresh = function(wrapper){
    frappe.after_ajax(()=>{
		$("a[data-name='Learn']").hide();
        $("div.module-section-column:contains('Help')").addClass('hide');
    });
};