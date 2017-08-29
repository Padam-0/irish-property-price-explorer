
function thousandsDisplay(float){
    r = Math.round(float);
    s = [];
    for (var i = String(r).length - 1; i >= 0; i--) {
        s.unshift(String(r)[i]);
        if ((String(r).length - i) % 3 == 0 && i != 0){
            s.unshift(",")
        }
    }
    return s.join("")
}

function to_dms(coord){
    d = parseInt(Math.abs(coord));
    t = (Math.abs(coord) - d) * 60;
    m = parseInt(t);
    s = parseInt((t - m) * 60 * 10000) / 10000;

    return d + "&deg; " + m + "\" " + s + "\'"
}

function setcookie(cookieName,cookieValue) {
    var today = new Date();
    var expire = new Date();
    expire.setTime(today.getTime() + 3600000*24*14);
    document.cookie = cookieName + "=" + cookieValue + ";expires="+expire.toGMTString() + "; path=/";
}

$(document).ready(function() {

    if (Cookies.get('cook_pop') == null){
        setcookie('cook_pop', 0)
    }
    if (Cookies.get('zoom_warning') == null){
        setcookie('zoom_warning', 0)
    }
    if (Cookies.get('top') == null){
        setcookie('top', 53.36527008496904)
    }
    if (Cookies.get('bottom') == null){
        setcookie('bottom', 53.33432429896267)
    }
    if (Cookies.get('left') == null){
        setcookie('left', -6.318579037475615)
    }
    if (Cookies.get('right') == null){
        setcookie('right', -6.17713006286624)
    }
    if (Cookies.get('areaMain') == null){
        setcookie('areaMain', 'map')
    }
    if (Cookies.get('areaSecond') == null){
        setcookie('areaSecond', '')
    }
    if (Cookies.get('radius') == null){
        setcookie('radius', 1)
    }
    if (Cookies.get('min_price') == null){
        setcookie('min_price', 0)
    }
    if (Cookies.get('max_price') == null){
        setcookie('max_price', 26500000)
    }
    if (Cookies.get('min_date') == null){
        setcookie('min_date', 1262304000000)
    }
    if (Cookies.get('max_date') == null){
        setcookie('max_date', 1491001200000)
    }
    if (Cookies.get('bad_data_inc') == null){
        setcookie('bad_data_inc', 'true')
    }

    c = Cookies.get('cook_pop');
    if (c === 0) {

        var message = $('<p />', {text: 'We use cookies to give you the best possible experience with our website. By continuing to use our site, you accept our '}),
            link = $('<a />', {
                text: 'cookies policy',
                href: '/privacy-cookies'
            }),
            ok = $('<button />', {text: 'Ok', 'class': 'full'});

        $('<div />').qtip({
            content: {
                text: message.append(link).append('.').add(ok),
                title: 'Cookies Policy'
            },
            position: {
                target: [0, 0],
                container: $('#qtip-growl-container')
            },
            show: {
                event: false,
                ready: true,
                effect: function () {
                    $(this).stop(0, 1).animate({height: 'toggle'}, 400, 'swing');
                },
                delay: 0
            },
            hide: {
                event: false,
                effect: function (api) {
                    $(this).stop(0, 1).animate({height: 'toggle'}, 400, 'swing');
                }
            },
            style: {
                classes: 'jgrowl qtip-light qtip-rounded qtip-shadow',
                tip: false
            },
            events: {
                render: function (event, api) {
                    $('button', api.elements.content).click(function (e) {
                        api.hide(e);
                    });
                },
                hide: function (event, api) {
                    setcookie('cook_pop', '1');
                    api.destroy();
                }
            }
        });
    }

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
            }
        }
    });
});