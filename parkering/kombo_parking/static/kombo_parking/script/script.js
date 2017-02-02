$(document).ready(function () {
    function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
    }

    $( "#id_rentout_stop_date" ).datepicker({
        beforeShow: function(input, inst) {
            var widget = $(inst).datepicker('widget');
            widget.css('margin-right', $(input).outerWidth() - widget.outerWidth());
        }
    })

    $( "#id_rentout_start_date" ).datepicker({
        beforeShow: function(input, inst) {
            var widget = $(inst).datepicker('widget');
            widget.css('margin-right', $(input).outerWidth() - widget.outerWidth());
        }
    })

    $( "#id_request_stop_date" ).datepicker({
        beforeShow: function(input, inst) {
            var widget = $(inst).datepicker('widget');
            widget.css('margin-right', $(input).outerWidth() - widget.outerWidth());
        }
    })

    $( "#id_request_start_date" ).datepicker({
        beforeShow: function(input, inst) {
            var widget = $(inst).datepicker('widget');
            widget.css('margin-right', $(input).outerWidth() - widget.outerWidth());
        }
    })

});