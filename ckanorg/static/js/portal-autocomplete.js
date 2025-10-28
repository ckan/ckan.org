// Wait for jQuery to become available, then initialize autocomplete.
(function waitForjQuery() {
    if (typeof window.jQuery === 'undefined') {
        // Retry after a short delay until jQuery is available.
        setTimeout(waitForjQuery, 50);
        return;
    }

    (function($) {
        $(function() {
            var $input = $("#portal-search");
            if (!$input.length) return;

            $input.autocomplete({
                source: "/portals/autocomplete/",
                minLength: 2,
                position: { my: "left top+2", at: "left bottom" },
                appendTo: ".search-box",
                select: function(event, ui) {
                    if (ui.item && ui.item.url) {
                        window.location.href = ui.item.url;
                        return false;
                    }
                }
            }).data("ui-autocomplete")._renderItem = function(ul, item) {
                return $("<li>")
                    .append(
                        '<div class="portal-suggestion">' +
                            '<a href="' + (item.url || '#') + '" class="portal-link">' +
                                '<div class="portal-title">' + (item.label || '') + 
                                '<span class="portal-country">' + (item.country || '') + 
                                '</span>' +
                                '</div>' +
                            '</a>' +
                        '</div>'
                    )
                    .appendTo(ul);
            };
        });
    })(window.jQuery);
})();
