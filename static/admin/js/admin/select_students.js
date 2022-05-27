/*global SelectBox, interpolate*/
// Handles related-objects functionality: lookup link for raw_id_fields
// and Add Another links.
'use strict';
{
    const $ = django.jQuery;

    function update_products(triggeringLink) {
        // extend ajax request for products filtered by user_id
        // получаем id элемента в котором сработало событие
        const $this = $(triggeringLink);
        const value = $this.val();
        const elm_id = $this.attr("id");
        if (elm_id === "id_lesson") {
        // мы ожидаем что id селекта будет именно id_lesson, это зависит от названия поля в модели Grade
            const product = $(id_student);
            // получаем ссылку на селект с учениками, его id также зависит от имени поля
            product.val("");
            // сразу можно очистить ранее выбранное
            $('#id_student option:gt(0)').remove();
            // удаляем все опции из селекта учеников, кроме первого, так как первая опция отвечает за None значение

            // а теперь отправляем ajax запрос на бекенд со значением value(id урока)
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

    // данная функция добавлена в изначальном виде из примера, позволяет в url добавлять значение id поля
    // изменяемого селекта. Может когда нибудь пригодится.
    function example_update_products(triggeringLink) {
        // extend ajax request for products filtered by user_id
        const $this = $(triggeringLink);
        const value = $this.val();
        const elm_id = $this.attr("id");
        if (elm_id === "id_coupon_user") {
            const product = $(id_coupon_product);
            product.val("");
            $('#id_coupon_product option:gt(0)').remove();
            if (value) {
                $.ajax({
                    url: "/newapp/filter_products_by_user/" + value + "/",
                    success: function(newOptions){
                        $.each(newOptions, function(key, value) {
                            product.append($("<option></option>").attr("value", key).text(value));
                        });
                    }

                });
            } else {
                // do nothing
            }
        }
        // end
    }
}