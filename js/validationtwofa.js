// This function creates a new anchor element and uses location
// properties (inherent) to get the desired URL data. Some String
// operations are used (to normalize results across browsers).

function parseURL(url) {
    var a =  document.createElement('a');
    a.href = url;
    return {
        source: url,
        protocol: a.protocol.replace(':',''),
        host: a.hostname,
        port: a.port,
        query: a.search,
        params: (function(){
            var ret = {},
                seg = a.search.replace(/^\?/,'').split('&'),
                len = seg.length, i = 0, s;
            for (;i<len;i++) {
                if (!seg[i]) { continue; }
                s = seg[i].split('=');
                ret[s[0]] = s[1];
            }
            return ret;
        })(),
        file: (a.pathname.match(/\/([^\/?#]+)$/i) || [,''])[1],
        hash: a.hash.replace('#',''),
        path: a.pathname.replace(/^([^\/])/,'/$1'),
        relative: (a.href.match(/tps?:\/\/[^\/]+(.+)/) || [,''])[1],
        segments: a.pathname.replace(/^\//,'').split('/')
    };
}

var isDirty = false;
$(document).ready(function() {

    var showmodal = "{{show2famodal}}";
    //console.log(showmodal);
    if (showmodal != null) {
        $('#TwoFAModal').modal('show');
    }

	
	$('.submit2fa').bootstrapValidator({
		submitButtons: '#submittwofabtn',
		live: 'enabled',
		fields: {
			accesscode: {
				trigger: 'keyup focus blur',
			    validators: {
			        regexp: {
                        regexp: /^[0-9]{6,7}$/,
                        message: 'Not a valid Access Code format.'
                    },
                    notEmpty: {
                        message: 'Access Code is required.'
                    }
                }
			}
		}
	}).on('success.form.bv', function(e) {
             $('.submit2fa').find(':submit').attr('disabled','disabled');
             console.log('disabled to prevent double submit');
            // $(e.target) --> The form instance
            $('#submittwofabtn').text('Validating...');
            $('#submittwofabtn').css("background-color", "#90A7BD");
            $('#submittwofabtn').css("background-position", "75%");
            $('#submittwofabtn').css('background-repeat', 'no-repeat');
            $('#submittwofabtn').css('background-image', 'url(/images/btc-loader.gif)');
            $('#submittwofabtn').css("color", "#000000");
            isDirty = false;
            $(e.target).data('bootstrapValidator').defaultSubmit();

    });
	
    $("#submittwofabtn").on("click",function() {
		isDirty = false;
	});

    $("#smstwofabtn").on("click",function() {
		isDirty = false;
	});

    $("#authytwofabtn").on("click",function() {
		isDirty = false;
	});

    $("#TwoFAModal").on('hidden.bs.modal', function () {
        console.log(location.href);
        var myURL = parseURL(location.href)
        path = myURL.path
        console.log(path);
        if (path == '/profile/edit') {
           location.href = location.href + '#security';
        }
        location.reload();
    });

});


 