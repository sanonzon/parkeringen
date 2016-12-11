$(document).ready(function () {
    //~ $('.fast-workout-sections').hide();

    //~ console.log($('#oldWorkoutSelector').text());

    //~ switch ($('#oldWorkoutSelector').text()) {
        //~ case "Simning":
            //~ $("option[value='fastWorkoutSwimming']").attr('selected','selected');
            //~ $('#fastWorkoutSwimming').show();
            //~ break;
        //~ case "Loepning":
            //~ $("option[value='fastWorkoutRunning']").attr('selected','selected');
            //~ $('#fastWorkoutRunning').show();
            //~ break;
        //~ case "Styrketraening":
            //~ $("option[value='fastWorkoutStyrke']").attr('selected','selected');
            //~ $('#fastWorkoutStyrke').show();
            //~ break;
        
    //~ }
    //~ $('#').text($('#oldWorkoutSelector').text())

    //~ $('#selectFastWorkout').change(function () {
        //~ $('.fast-workout-sections').hide();
        //~ $('#'+$(this).val()).show();
    //~ });

    
   //~ var today = $('#datumet').text();
   //~ console.log(today);
   //~ var today = new Date(now()).format("YYYY-MM-DD");
    //~ $('#datePickerRun').val(today);
    //~ $('#datePickerSwim').val(today);
    //~ $('#datePickerGym').val(today);

    //~ $('[data-toggle="tooltip"]').tooltip();
    
    
    

//var minutesOffset = dateValue1.getTimezoneOffset();

//~ document.body.innerHTML += $.datepicker.formatDate(currentFormat, dateValue1) + "<br />";

});

//~ document.getElementById('toggleButton').onclick = function() {
    //~ document.getElementsByClassName('menu')[0].classList.toggle('responsive');
//~ }

// using jQuery
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
//~ var csrftoken = getCookie('csrftoken');

//~ $("#contactbutton").click(function() {
    //~ var formData = $("#contactform").serialize();
    //~ $.ajax({
        //~ type: "POST",
        //~ url: "contact.php",
        //~ data: formData,
        //~ success: function(serverResponse) {
            //~ $("#message-sent").text(serverResponse);
            //~ $("#message-sent").show(500).delay(5000).hide(500);
        //~ },
        //~ error: function(XMLHttpRequest, textStatus, errorThrown) {
            //~ console.log("some error: " + textStatus + ", " + errorThrown);
        //~ }
    //~ });
//~ });

//~ $('#notification-button').click(function() {
    //~ console.log("OKLART SOM FAN, success ka det vara.");
    //~ var csrftoken = getCookie('csrftoken');
    //~ $.ajax({
        //~ type: 'POST',
        //~ // url: $(this).attr('action'),
        //~ url: '/header/',
        //~ data: {
            //~ 'csrfmiddlewaretoken': csrftoken,
        //~ },
        //~ success: function(serverResponse) {
            //~ console.log("OKLART SOM FAN, success ka det vara.");
        //~ },
        //~ error: function(newData) {
            //~ console.log("FAIL");
        //~ },
    //~ });
//~ });

//~ http://stackoverflow.com/questions/19468088/handling-django-model-form-error-in-ajax-submit
