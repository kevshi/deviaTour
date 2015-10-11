$(document).ready(function() {
    $('.submitlocation').bootstrapValidator({
            submitButtons: '#submitlocation',
            live: 'enabled',
            fields: {
                'required_field': {
                    trigger: 'keyup focus blur',
                    selector: '.required_field',
                    validators: {
                        notEmpty: {
                            message: 'Additional Information Field is required.'
                        }
                    }
                }
            }
        }).on('success.form.bv', function(e) {
                // $(e.target) --> The form instance
    //            $('#submitph').text('Validating...');
    //            $('#submitph').css("background-color", "#f2dede");
    //            $('#submitph').css("background-position", "75%");
    //            $('#submitph').css('background-repeat',  'no-repeat');
    //            $('#submitph').css('background-image', 'url(/images/btc-loader.gif)');
    //            $('#submitph').css("color", "#000000");
                $(e.target).data('bootstrapValidator').defaultSubmit();
            });
});


