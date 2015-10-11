$(document).ready(function() {
	$('.contactForm').bootstrapValidator({
		submitButtons: '#sendnewcontact',
		live: 'enabled',
		fields: {
			name: {
				trigger: 'keyup focus blur',
			    validators: {
                    notEmpty: {
                        message: 'Name is required.'
                    }
                }
			},
			email: {
				trigger: 'keyup focus blur',
				validators: {
					notEmpty: {
						message: 'Email is required.'
					},
                    emailAddress: {
                        message: 'Not a valid Email Address.'
                    }
				}
			},
			message: {
				trigger: 'keyup focus blur',
				validators: {
					notEmpty: {
						message: 'Message is required.'
					},
                    stringLength: {
                        max: 500,
                        message: 'Message must be less than 500 characters'
                    }
				}
			}
		}
	}).on('success.form.bv', function(e) {
            // $(e.target) --> The form instance

         $('#sendnewcontact').text('Validating...');
         $('#sendnewcontact').css("background-color", "#90A7BD");
         $('#sendnewcontact').css("background-position", "75%");
         $('#sendnewcontact').css('background-repeat',  'no-repeat');
         $('#sendnewcontact').css('background-image', 'url(/images/btc-loader.gif)');
         $('#sendnewcontact').css("color", "#000000");

       var data_value = $('#contactname').val();
        var data_value2 = $('#contactemail').val();
        var data_value3 = $('#contactmessage').val();
        var data_value4 = $('#csrf').val();
        var data_value5 = $('#recaptcha_challenge_field').val();
        var data_value6 = $('#recaptcha_response_field').val();
        var data_value7 = $('#botemail').val();
        var data_value8 = $('#botemailtime').val();
        var url = '/contact/send';
        $.ajax({
            type: "POST",
            url: url,
            data:{'name':data_value,
                           'email': data_value2,
                           'message': data_value3,
                           'csrfbase': data_value4,
                           'recaptcha_challenge_field':data_value5,
                           'recaptcha_response_field':data_value6,
                            'botemail':data_value7,
                            'botemailtime':data_value8
                 },
            success:function(data){
                $('.contactForm').bootstrapValidator('resetForm', true);

                $('#sendnewcontact').text('Send');
                $('#sendnewcontact').css("background-color", "#204f7b");
                $('#sendnewcontact').css("color", "#ffffff");
                $('#sendnewcontact').css('background-image', '');

                $('#contact').modal('hide');
                $('#contactconfirm').modal('show');
                $('#contactresponse').html(data);
            }
        });

        isDirty = false;
        e.preventDefault()
        return
        //$(e.target).data('bootstrapValidator').defaultSubmit();
    });

		
	$('.submitlist').bootstrapValidator({
		submitButtons: '#submitlistbtn',
		live: 'enabled',
		fields: {
			email: {
				trigger: 'keyup focus blur',
			    validators: {
                    notEmpty: {
                        message: 'Email is required.'
                    },
                    emailAddress: {
                        message: 'Not a valid Email Address.'
                    }
                }
			}
		}
	}).on('success.form.bv', function(e) {
            // $(e.target) --> The form instance
            $('#submitlistbtn').text("");
            $('#submitlistbtn').css("height", '34px');
            $('#submitlistbtn').css("width", '37px');
            $('#submitlistbtn').css("background-color", "#90A7BD");
            $('#submitlistbtn').css("background-position", "50%");
            $('#submitlistbtn').css('background-repeat',  'no-repeat');
            $('#submitlistbtn').css('background-image', 'url(/images/snakegif.gif)');
            $('#submitlistbtn').css("color", "#000000");
            isDirty = false;
            $(e.target).data('bootstrapValidator').defaultSubmit();
        });

    $('#contact').on('shown.bs.modal', function() {
    $('.contactForm').bootstrapValidator('resetForm', true);
    });

});


 