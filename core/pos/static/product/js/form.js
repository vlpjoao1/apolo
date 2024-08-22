var input_is_inventoried;
var form_group;
$(function () {
    input_is_inventoried = $('input[name="is_inventoried"]');
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    form_group = document.getElementsByClassName('form-group');

    $('input[name="pvp"]')
        .TouchSpin({
            min: 0.01,
            max: 1000000,
            step: 0.01,
            decimals: 2,
            boostat: 5,
            verticalbuttons: true,
            maxboostedstep: 10,
            prefix: '$'
        })
        .on('keypress', function (e) {
            return validate_decimals($(this), e);
        });

    $('input[name="stock"]')
        .TouchSpin({
            min: 0,
            max: 1000000,
            step: 1,
            verticalbuttons: true,
        })
        .on('keypress', function (e) {
            return validate_form_text('numbers', e, null);
        });

    input_is_inventoried.on('change', function () {
        // Localize the container of stock
        var container = $(this).parent().parent().find('input[name="stock"]').parent().parent();
        console.log(container);
        if (!this.checked) {
            container.hide();
        } else {
            container.show();
        }
    });

    if($('input[name="action"]').val() === 'edit'){
        //activa el evento change
        input_is_inventoried.trigger('change');
    }
});