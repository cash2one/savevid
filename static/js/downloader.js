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

function loadmore(obj) {
    var pager_html = '<li class="text-primary">加载中<img style="width:32px;" src="/static/img/loading.gif"></img></li>';
    $('ul.pager').html(pager_html);
    $obj = $(obj);
    keyword = $obj.attr("keyword");
    page_num = $obj.attr("page_num");
    var data = {
        keyword: keyword,
        page_num: page_num
    };

    $.ajax({
        type: 'GET',
        url: '/search_vid/',
        data: data,
        success: function(resp) {
            if(resp.success) {
                var tmpl = '\
                {{#results}} \
                  <div class="media"> \
                    <div class="srch-item"> \
                      {{#img}} \
                      <div class="media-left"> \
                        <a href="{{ vid }}"> \
                          <img class="media-object" src="{{ img }}" alt="{{ title }}"> \
                        </a> \
                      </div> \
                      {{/img}} \
                      <div class="media-body"> \
                        <h4 class="media-heading"><a target="_blank" href="{{ vid }}">{{ title }}</a></h4> \
                        <p>{{ desc }}</p> \
                        <!--<a class="btn btn-info" href="{{ vid }}" download="{{ vid }}">下载地址</a>--> \
                      </div> \
                    </div> \
                  </div> \
                {{/results}}';
                var html = $('#result-items').html() + Mustache.render(tmpl, { results: resp.result});
                $("#result-items").html(html);
                var pager_tmpl = '<li><a class="more" keyword="{{ keyword }}" page_num="{{ page_num }}" onclick="javascript:loadmore(this);">更多搜索结果</a></li>';
                pager_html = Mustache.render(pager_tmpl, {keyword: resp.keyword, page_num: resp.next});
                $("ul.pager").html(pager_html);
            }
            else {
                var pager_tmpl = '<li class="text-danger">没有更多结果了<li>';
                pager_html = Mustache.render(pager_tmpl, {keyword: resp.keyword, page_num: resp.next});
                $("ul.pager").html(pager_html);
            }
        }
    });
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
            // init
            $('div.msg').empty();
            var url = $('input[name="url"]').val();
            if(url == "") {
                $('div.msg').html('请输入视频链接:');
                return;
            }

            var html_load = '<div class="alert alert-info rs-status"><span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span><span class="stat-text"> 正在获取下载链接中...</span></div>';
            $("#result").html(html_load).fadeIn();
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
                        <div class="alert alert-success rs-status"><span class="glyphicon glyphicon-ok"></span><span class="stat-text"> 成功获取下载地址</span></div> \
                        <div class="media rs-content"> \
                          <div class="media-left"> \
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
                        var tmpl_err = '<div class="alert alert-danger rs-status"><span class="glyphicon glyphicon-exclamation-sign"></span><span class="stat-text"> {{ msg }}</span></div>';
                        var html_err = Mustache.render(tmpl_err, { msg: resp.msg });
                        $("#result").html(html_err);
                    }
                }
            });
        });

        $('#search').click(function(e) {
            // init
            $('div.msg').empty();
            var keyword = $('input[name="keyword"]').val();
            if(keyword == "") {
                $('div.msg').html('请输入关键字:');
                return;
            }

            var html_load = '<div class="alert alert-info rs-status"><span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span><span class="stat-text"> 正在全力搜索视频...</span></div>';
            $("#result").html(html_load).fadeIn();
            var keyword = $('input[name="keyword"]').val();
            var data = {
                keyword: keyword,
                page_num: 1
            };
            $.ajax({
                type: 'GET',
                url: '/search_vid/',
                data: data,
                success: function(resp) {
                    if(resp.success) {
                        var tmpl = '\
                        <div id="result-items"> \
                        {{#results}} \
                          <div class="media"> \
                            <div class="srch-item"> \
                              {{#img}} \
                              <div class="media-left"> \
                                <a href="{{ vid }}"> \
                                  <img class="media-object" src="{{ img }}" alt="{{ title }}"> \
                                </a> \
                              </div> \
                              {{/img}} \
                              <div class="media-body"> \
                                <h4 class="media-heading"><a target="_blank" href="{{ vid }}">{{ title }}</a></h4> \
                                <p>{{ desc }}</p> \
                                <!--<a class="btn btn-info" href="{{ vid }}" download="{{ vid }}">下载地址</a>--> \
                              </div> \
                            </div> \
                          </div> \
                        {{/results}} \
                        </div>';
                        var html = Mustache.render(tmpl, { results: resp.result});
                        var pager_tmpl = '<nav> \
                          <ul class="pager"> \
                            <li><a class="more" keyword="{{ keyword }}" page_num="{{ page_num }}" onclick="javascript:loadmore(this);">更多搜索结果</a></li> \
                          </ul> \
                        </nav>';
                        var pager_html = Mustache.render(pager_tmpl, {keyword: resp.keyword, page_num: resp.next});
                        html += pager_html;
                        $("#result").html(html);
                    }
                    else {
                        var tmpl_err = '<div class="alert alert-danger rs-status"><span class="glyphicon glyphicon-exclamation-sign"></span><span class="stat-text"> {{ msg }}</span></div>';
                        var html_err = Mustache.render(tmpl_err, { msg: resp.msg });
                        $("#result").html(html_err);
                    }
                }
            });
        });

        $('input[name="url"]').keydown(function(e){
            if(e.keyCode == 13){
                e.preventDefault();
                $('#download').trigger('click');
            }
        });

        $('input[name="keyword"]').keydown(function(e){
            if(e.keyCode == 13){
                e.preventDefault();
                $('#search').trigger('click');
            }
        });
    }
};
