$(document).ready(function() {
    $.get("site_messages.txt", function(data) {
        var text_size = data.length;        
        if (text_size > 3) {
            var element = '<div class="well site-message"></div>';
            $("#main").prepend($(element).html(data));
        }
    });
});