$(document).ready(function() {
    function getData(currentDate, direction) {
        var currentMonth = currentDate[0];
        var currentYear = currentDate[1];

        $.ajax({
            url: "/events/ajax",
            method: 'get',
            dataType: 'json',
            data: {
                "month": currentMonth,
                "year": currentYear,
                "direction": direction
            },
            success: function(data) {
                $(".calendar-wrapper").append(data.calendar);
                $("th:not(:first)").text(function (i, text) {
                    return text.slice(0, -2);
                });

                if (data.calendar_events.length) {
                    $.each(data.calendar_events, function(index, event) {
                        $("td").filter(function() { 
                            return $(this).text() === event.day;
                        }).addClass("marked");

                        $(".info-event-list").append(
                            "<div class='info-event-item' data-day='" + event.day + "'><div class='item-title'><a class='info-event-item-link' href='" +
                            $(location).attr("href") + "/" + event.slug + "'>" + event.title + "</a></div><div class='item-time'>" +
                            event.time + "</div></div>"
                        );
                    });

                    $("td").filter(function() { 
                        return $(this).text() === data.calendar_events[0].day;
                    }).addClass("selected");

                    $(".info-date-day").text(data.calendar_events[0].day);
                    $(".info-date-weekday").text(data.calendar_events[0].weekday);
                    $(".info-event-item[data-day=" + data.calendar_events[0].day + "]").show();
                } else {
                    $("td").filter(function() { 
                        return $(this).text() === "1";
                    }).addClass("selected");
                    $(".info-date-day").text("1");
                    $(".info-date-weekday").text(data.firstweekday);
                    $(".empty-list").css("display", "grid").show();
                }
            }
        });
    };

    // PREPARE AND FIRST DISPLAY CURRENT MONTH CALENDAR
    $("th:not(:first)").text(function (i, text) {
        return text.slice(0, -2);
    });

    if ($("[data-day]").length) {
        $.each($("[data-day]"), function(index, item) {
            var day = $(this).attr("data-day");
            if (index === 0) {
                $("td").filter(function() { 
                    return $(this).text() === day;
                }).addClass("selected");

                $(".info-event-item[data-day=" + day + "]").show();
            };

            $("td").filter(function() {
                return $(this).text() === day;
            }).addClass("marked");
        });
    } else {
        $("td").filter(function() { 
            return $(this).text() === "1";
        }).addClass("selected");

        var weekday = $("td.selected").attr("class").split(" ")[0];

        $(".info-date-day").text("1");
        $(".info-date-weekday").text(weekday);
        $(".empty-list").css("display", "grid").show();
    };

    // CALENDAR ACTIONS
    $("#btn-calendar").on("click", function() {
        $(".event-calendar").toggle();
    });

    $("#btn-prev-month").on("click", function() {
        var currentDate = $("th.month").text().split(" ");
        $("table.month").remove();
        $(".info-event-item").remove();
        $(".info-date-day").empty();
        $(".info-date-weekday").empty();
        $(".empty-list").hide();
        getData(currentDate, -1);
    });

    $("#btn-next-month").on("click", function() {
        var currentDate = $("th.month").text().split(" ");
        $("table.month").remove();
        $(".info-event-item").remove();
        $(".info-date-day").empty();
        $(".info-date-weekday").empty();
        $(".empty-list").hide();
        getData(currentDate, 1);
    });

    $("body").on("click", "td", function() {
        var day = $(this).text();
        var weekday = $(this).attr("class").split(" ")[0];

        $("td").removeClass("selected");
        $(this).addClass("selected");

        $(".info-date-day").text(day);
        $(".info-date-weekday").text(weekday);

        $(".info-event-item").hide();
        $(".empty-list").hide();
        if ($(".info-event-item[data-day=" + day + "]").length) {
            $(".info-event-item[data-day=" + day + "]").show();
        } else {
            $(".empty-list").css("display", "grid").show();
        };
    });
});
