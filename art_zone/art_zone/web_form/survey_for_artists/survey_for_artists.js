frappe.ready(function() {
    frappe.web_form.set_value("language", "ar");

    const sections = [
        {
            checkboxes: ["photographer", "makeup_artist", "hairdresser", "model", "bridesmaid"],
            other_field: "other"
        },
        {
            checkboxes: ["less_than_a_year", "1_to_3_years", "4_to_6_years", "more_than_6_years"],
            other_field: "" 
        },
        {
            checkboxes: ["fixed_prices", "negotiable"],
            other_field: "" 
        },
        {
            checkboxes: ["less_than_500_sar", "500_to_1000_sar", "1000_to_2000_sar", "more_than_2000_sar"],
            other_field: "other_service_price"
        },
        {
            checkboxes: ["yes", "no"],
            other_field: "other_customer_type"
        },
        {
            checkboxes: ["appointment_management", "order_management", "customer_communication", "view_portfolio"],
            other_field: "other_app_experiencec"
        },
        {
            checkboxes: ["yes_east_to_use", "no_east_to_use"],
            other_field: "" 
        }
    ];

    const handleCheckboxToggle = (checkboxes, other_field, changedField) => {
        checkboxes.forEach((fieldname) => {
            if (fieldname !== changedField) {
                frappe.web_form.set_value(fieldname, "0");
            }
        });
        if (other_field) {
            frappe.web_form.set_value(other_field, ""); 
        }
    };

    sections.forEach((section) => {
        section.checkboxes.forEach((fieldname) => {
            $(`[data-fieldname="${fieldname}"] input`).on('change', function() {
                if ($(this).is(':checked')) {
                    handleCheckboxToggle(section.checkboxes, section.other_field, fieldname);
                }
            });
        });

        if (section.other_field) {
            $(`[data-fieldname="${section.other_field}"] input`).on('input', function() {
                section.checkboxes.forEach((fieldname) => {
                    frappe.web_form.set_value(fieldname, "0");
                });
            });
        }
    });
});