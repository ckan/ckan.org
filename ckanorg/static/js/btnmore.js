$(document).ready(function() {
    $("#btn-more-events").click(function(){
        $(".event-item").each(function(i, obj) {
            if ($(this).attr("hidden")) {
                $(this).removeAttr("hidden");
                $(".more-events").hide();
            }
        });
    });
});
