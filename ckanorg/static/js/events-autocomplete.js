$(document).ready(function() {
    $("#btn-search").on( "click", function() {
        $(".search-events").toggle();
    });

    $( "#search" ).on( "keyup", function() {
        var value = $(this).val();

        $(".btn-search-close").show();

        $(".search-events-result").empty();

        if ($("#search").val() == "") {
            $(".btn-search-close").hide();
        };

        if (value.length > 2) {
            var url = window.location.origin + "/search/ajax?term=" + value

            $(".search-events-result").css("display", "block");

            $.ajax({
                url: url,
                method: 'get',
                dataType: 'json',
                success: function(data) {
                    var div = $(".search-events-result")
                    var currentCategory = "";

                    if (data.length) {
                        $.each(data, function(index, item) {
                            if (item.category != currentCategory) {
                                div.append("<ul class='events-list' data-category='" + item.category + "'><div class='event-category'>" + item.category + "</div></ul>");
                                currentCategory = item.category;
                            }

                            var ul = $("ul.events-list[data-category=" + item.category + "]");
                            var bold_text = item.label.replace(new RegExp(value, "gi"), "<strong>$&</strong>");
                            ul.append(
                                "<li class='event-item'><a class='event-link' href='" + $(location).attr("href") + "/"  + item.value + "'>" + bold_text + "</a>"
                            );
                        });
                    } else {
                        div.append("<div class='empty-list'>No recent searches</div>");
                    }
                }
            });
        } else {
            $(".search-events-result").css("display", "none");
        };
    });

    $(".btn-search-close").on( "click", function() {
        $("#search").val("");
        $(".search-events").hide();
        $(".btn-search-close").hide();
        $(".search-events-result").empty();
    });
});
