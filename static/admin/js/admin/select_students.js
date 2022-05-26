/*global SelectBox, interpolate*/
// Handles related-objects functionality: lookup link for raw_id_fields
// and Add Another links.
'use strict';
{
    const $ = django.jQuery;

    function update_products(triggeringLink) {
        // extend ajax request for products filtered by user_id
        const $this = $(triggeringLink);
        const value = $this.val();
        const elm_id = $this.attr("id");
        if (elm_id === "id_lesson") {
            const product = $(id_student);
            product.val("");
            $('#id_student option:gt(0)').remove();

            $.ajax({
                url: "/filter_students_by_lesson/", // + value + "/",
                data: {
                'lesson': value
                },
                success: function (data) {
                $("#id_student").html(data);
                }

            });

        }
        // end
    }

    $(document).ready(function() {
        $(id_lesson).change(function(e) {
            const event = $.Event('django:update-related');
            $(this).trigger(event);
            if (!event.isDefaultPrevented()) {
                update_products(this);
            }
        });
    });
}