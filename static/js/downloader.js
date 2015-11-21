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
            var html_load = '<div class="alert alert-info"><span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span><span class="stat-text"> 正在获取下载链接中...</span></div>';
            $("#result").html(html_load).fadeIn();
            var url = $('input[name="url"]').val();
            var data = {
                url: url
            };
            $.ajax({
                type: 'POST',
                url: '/get_link/',
                data: data,
                success: function(resp) {
                    if(resp.success) {
                        var tmpl = '\
                        <div class="alert alert-success"><span class="glyphicon glyphicon-ok"></span><span class="stat-text"> 成功获取下载地址</span></div> \
                        <div class="media"> \
                          <div class="media-left media-middle"> \
                            <a href="{{ vid }}"> \
                              <img class="media-object vid-img" src="{{ img }}" alt="{{ desc }}"> \
                            </a> \
                          </div> \
                          <div class="media-body"> \
                            <h4 class="media-heading">{{ desc }}</h4> \
                            <a class="btn btn-info" href="{{ vid }}" download="{{ vid }}">下载地址</a> \
                          </div> \
                        </div>';
                        var html = Mustache.render(tmpl, resp.result);
                        $("#result").html(html);
                    }
                    else {
                        var html_err = '<div class="alert alert-danger"><span class="glyphicon glyphicon-exclamation-sign"></span><span class="stat-text"> 获取下载地址失败</span></div>';
                        $("#result").html(html_err);
                    }
                }
            });
        });
    }
};
