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
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var downloader = {
    init: function() {
        $('#download').click(function(e) {
            var url = $('input[name="url"]').val();
            var data = {
                url: url
            };
            $.ajax({
                type: 'POST',
                url: '/downloader/get_link/',
                data: data,
                success: function(resp) {
                    var tmpl = '<div class="media"> \
                      <div class="media-left media-middle"> \
                        <a href="{{ vid_link }}"> \
                          <img class="media-object vid-img" src="{{ img_link }}" alt="{{ img_desc }}"> \
                        </a> \
                      </div> \
                      <div class="media-body"> \
                        <h4 class="media-heading">{{ img_desc }}</h4> \
                        <a href="{{ vid_link }}">下载地址</a> \
                      </div> \
                    </div>';
                    var html = Mustache.render(tmpl, { vid_link: resp.result.vid,
                        img_link: resp.result.img
                    });
                    $("#result").html(html);
                }
            });
        });
    }
};
