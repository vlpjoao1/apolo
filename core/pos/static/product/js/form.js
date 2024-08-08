$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

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
});