$(document).ready(function() {
    if ($("#pills-archive-tab").hasClass("active")) {
        $(".featured-section-wrapper").hide();
    } else {
        $(".featured-section-wrapper").show();
    };
    $(".nav-link").click(function(){
        if ($("#pills-archive-tab").hasClass("active")) {
            $(".featured-section-wrapper").hide();
        } else {
            $(".featured-section-wrapper").show();
        };
    });
});
