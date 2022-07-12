const user_input = $("#user-input")
const search_icon = $('#search-icon')
const replaceable_div = $('#replaceable-content')
const endpoint = Urls['movies:movies_min_by_title_api']()
const delay_by_in_ms = 500
let scheduled_function = false

// Can be used anywhere we need to issue an AJAX request to search for data.
// All that's needed is to define elements with ids matching the above constants.
// https://openfolder.sh/django-tutorial-as-you-type-search-with-ajax
// https://github.com/SHxKM/django-ajax-search
let render_result = function(html) {
    replaceable_div.fadeTo('slow', 0).promise().then(() => {
        // replace the HTML contents
        replaceable_div.html(html)
        // fade-in the div with new contents
        replaceable_div.fadeTo('slow', 1)
        // stop animating search icon
        search_icon.removeClass('blink')
    })
}

let ajax_call = function (endpoint, request_parameters) {
    // If the title param is empty (ie blank searchbar), don't search for anything.
    if (request_parameters.title.length == 0) {
        render_result("")
        return
    }

	$.getJSON(endpoint, request_parameters).done(response => {
        render_result(response['html_from_view'])
	})
}

// When there's typing in the searchbar, re-issue the search
user_input.on('keyup', function () {
    // start animating the search icon with the CSS class
    search_icon.addClass('blink')

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
	const request_parameters = {
		title: $(this).val() // value of the HTML element with id user-input (ie the searchbar)
    }
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})

// When the searchbar loses focus, hide the search results
// The delay is to ensure that if the user clicks a search result
// that gets triggered first. Otherwise the element is hidden before the click event.
user_input.focusout(function() {
    setTimeout(
        function() {
            replaceable_div.hide()
        },
        200); // 100 ms is the minimum
})

// When the searchbar gains focus, show the search results
user_input.focusin(function() {
    replaceable_div.show()
})