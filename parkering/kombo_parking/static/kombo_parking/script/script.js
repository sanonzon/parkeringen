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

    /* multiple modals test */
    var modalUniqueClass = ".modal";
    $('.modal').on('show.bs.modal', function(e) {
      var $element = $(this);
      var $uniques = $(modalUniqueClass + ':visible').not($(this));
      if ($uniques.length) {
        $uniques.modal('hide');
        $uniques.one('hidden.bs.modal', function(e) {
          $element.modal('show');
        });
        return false;
      }
    });
});
