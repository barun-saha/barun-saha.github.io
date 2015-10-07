$(document).ready(function(){
    var selector = "#se-lite, #dtn-blog, #one-kb";
    $(selector).css("opacity", "0");
    $(selector).waypoint({
        handler: function(direction) {
            $(this.element).addClass("fadeInLeft");
        },
        offset: 'bottom-in-view'
    });
    
    $(".action").css("opacity", "0");
    $(".action").waypoint({
        handler: function(direction) {
            $(this.element).addClass("fadeInDown");
        },
        offset: 'bottom-in-view'
    });
});