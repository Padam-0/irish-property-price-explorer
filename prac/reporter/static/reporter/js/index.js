var hold = {'rad': true, 'cou': true, 'reg': true};
var overlays = [];

function test_deploy(area, selector, qt){
    if (hold[area]) {
        $(selector)
            .css('outline-color', '#00b300')
            .css('border-color', '#00b300')
            .css('box-shadow', '0 0 10px #00b300')
            .qtip({
            show: false
        });

        hold[area] = true
    } else {
        $(selector)
            .css('outline-color', '#e62e00')
            .css('border-color', '#e62e00')
            .css('box-shadow', '0 0 10px #e62e00')
            .qtip(qt);

        hold[area] = false
    }
}

function showZone(){
    gmap.data.forEach(function(feature) {
        gmap.data.remove(feature);
    });

    while(overlays.length > 0) {
        overlays.pop().setMap(null);
    }

    if (document.getElementById("sc-5-1-1").checked == true) {
        drawArea = 'map'
    } else if (document.getElementById("sc-5-1-2").checked == true) {
        drawArea = 'radius'
    } else if (document.getElementById("sc-5-1-3").checked == true) {
        drawArea = 'county'
    } else if (document.getElementById("sc-5-1-4").checked == true) {
        drawArea = 'region'
    } else if (document.getElementById("sc-5-1-5").checked == true) {
        drawArea = 'country'
    }


    var checkedValue = document.querySelector('#showzone:checked');
    if (checkedValue != null){

        if (drawArea == 'map'){
            drawMapEdges(gmap);
        } else if (drawArea == 'radius'){
            drawRadius(gmap)
        } else {
            data = getArea(drawArea);
            gmap.data.loadGeoJson(data);
            gmap.data.setStyle({
                "fillOpacity": 0.1,
                "strokeColor": 'black',
                "strokeOpacity": 0.7,
                "strokeWeight": 3
            });
        }
    } else {
        gmap.data.forEach(function(feature) {
            gmap.data.remove(feature);
        });

        while(overlays.length > 0) {
          overlays.pop().setMap(null);
        }
    }
}

$(document).ready(function() {
    document.getElementById("sc-5-1-1").checked = true;
    document.getElementById("sc-7-1-7").checked = true;
    document.getElementById("sc-7-2-7").checked = true;
    document.getElementById("sc-7-3-7").checked = true;
    document.getElementById("sc-7-4-7").checked = true;
    document.getElementById("sc-3-11-2").checked = true;
    document.getElementById("sc-3-21-2").checked = true;
    document.getElementById("sc-3-31-2").checked = true;
    document.getElementById("sc-3-1-1").checked = true;
    document.getElementById("sc-2-1-2").checked = true;
    document.getElementById("sc-2-2-1").checked = true;
    document.getElementById("sc-2-21-2").checked = true;

    document.getElementById("sc-2-3-1").checked = true;
    document.getElementById("sc-2-31-2").checked = true;

    document.getElementById("sc-2-4-1").checked = true;
    document.getElementById("sc-2-41-2").checked = true;

    document.getElementById("sc-2-5-1").checked = true;
    document.getElementById("sc-2-51-2").checked = true;

    document.getElementById("sc-2-6-1").checked = true;
    document.getElementById("sc-2-61-2").checked = true;

    document.getElementById("sc-2-7-1").checked = true;
    document.getElementById("sc-2-71-2").checked = true;

    document.getElementById("sc-2-8-1").checked = true;
    document.getElementById("sc-2-81-2").checked = true;

    document.getElementById("sc-2-9-1").checked = true;
    document.getElementById("sc-2-91-2").checked = true;

    document.getElementById("sc-2-10-1").checked = true;
    document.getElementById("sc-2-101-2").checked = true;

    document.getElementById("sc-2-11-1").checked = true;
    document.getElementById("sc-2-111-2").checked = true;

    document.getElementById("sc-2-12-1").checked = true;
    document.getElementById("sc-2-121-2").checked = true;

    document.getElementById("sc-2-13-1").checked = true;
    document.getElementById("sc-2-131-2").checked = true;

    document.getElementById("sc-2-14-1").checked = true;
    document.getElementById("sc-2-141-2").checked = true;

    document.getElementById("sc-2-15-1").checked = true;
    document.getElementById("sc-2-151-2").checked = true;

    document.getElementById("sc-2-16-1").checked = true;
    document.getElementById("sc-2-161-2").checked = true;

    document.getElementById("sc-2-17-1").checked = true;
    document.getElementById("sc-2-171-2").checked = true;

    document.getElementById("sc-2-18-1").checked = true;
    document.getElementById("sc-2-181-2").checked = true;

    $('#showzone').click(function () {
        showZone();
    });

    county_list = ['Galway', 'Leitrim', 'Mayo', 'Roscommon', 'Sligo',
        'Carlow', 'Dublin', 'Kildare', 'Kilkenny', 'Laois', 'Longford',
        'Louth', 'Meath', 'Offaly', 'Westmeath', 'Wexford', 'Wicklow',
        'Clare', 'Cork', 'Kerry', 'Limerick', 'Tipperary', 'Waterford',
        'Cavan', 'Donegal', 'Monaghan'];

    region_list = ['Connacht', 'Leinster', 'Munster', 'Ulster'];

    rad_qt = {
        content: {
            text: 'Error: Must be a number'
        },
        style: {
            classes: 'qtip-red qtip-rounded'
        },
        position: {
            my: 'bottom left',
            at: 'top right',
            target: this
        },
            show: true,
            hide: false
        };

    cou_qt = {
        content: {
            text: 'Error: Must be a valid county'
        },
        style: {
            classes: 'qtip-red qtip-rounded'
        },
        position: {
            my: 'bottom left',
            at: 'top right',
            target: this
        },
            show: true,
            hide: false
        };

    reg_qt = {
        content: {
            text: 'Error: Must be a valid region'
        },
        style: {
            classes: 'qtip-red qtip-rounded'
        },
        position: {
            my: 'bottom left',
            at: 'top right',
            target: this
        },
            show: true,
            hide: false
        };

    rec_qt = {
        content: {
            text: 'Please correct errors above before recalculating statistics'
        },
        style: {
            classes: 'qtip-red qtip-rounded'
        },
        position: {
            my: 'bottom left',
            at: 'top middle',
            target: this
        },
            show: true,
            hide: 'mouseleave'
        };

    $('#radius-selector')
        .prop('disabled', true)
        .focus(function(){
            $(this).keyup(function () {
                hold['rad'] = $.isNumeric(this.value);

                test_deploy('rad', '#radius-selector', rad_qt);
                showZone();
            });
        });

    $('#county-selector')
        .prop('disabled', true)
        .focus(function(){
            $(this).keyup(function () {
                if (county_list.indexOf(this.value) > -1) {
                    hold['cou'] = true
                } else {
                    hold['cou'] = false
                }

                test_deploy('cou', '#county-selector', cou_qt);
                showZone();
            });

            $(this).change(function(){
                if (county_list.indexOf(this.value) > -1) {
                    hold['cou'] = true
                } else {
                    hold['cou'] = false
                }

                test_deploy('cou', '#county-selector', cou_qt);
            });
        });

    $('#region-selector')
        .prop('disabled', true)
        .focus(function(){
            $(this).keyup(function () {
                if (region_list.indexOf(this.value) > -1) {
                    hold['reg'] = true
                } else {
                    hold['reg'] = false
                }

                test_deploy('reg', '#region-selector', reg_qt)
                showZone();
            });

            $(this).change(function(){
                if (region_list.indexOf(this.value) > -1) {
                    hold['reg'] = true
                } else {
                    hold['reg'] = false
                }

                test_deploy('reg', '#region-selector', reg_qt)
            });
        });

    $('#radius')
        .css('opacity', 0.4);

    $('#bad_data')
        .prop('disabled', true)
        .click(function () {
            if (document.querySelector('#bad_data:checked') != null){
                bad_data = 'false'
            } else {
                bad_data = 'true'
            }
        });

    $('#dist-opt-right')
        .css('opacity', 0.4);

    $('#sc-5-1-1')
        .click(function(){
            calcArea = 'map';
            showZone();

            $('#radius')
                .css("display", "flex")
                .css('opacity', 0.4);
            $('#radius-selector')
                .prop('disabled', true)
                .qtip({show: false});
            $('#county')
                .css("display", "none");
            $('#county-selector')
                .prop('disabled', true)
                .qtip({show: false});
            $('#region')
                .css("display", "none");
            $('#region-selector')
                .prop('disabled', true)
                .qtip({show: false});
            $('#bad_data')
                .prop('disabled', true);
            $('#dist-opt-right')
                .css('opacity', 0.4);
    });

    $('#sc-5-1-2')
        .click(function(){
            calcArea = 'radius';
            showZone();

            $('#radius')
                .css("display", "flex")
                .css('opacity', '');
            if (hold['rad'] === true) {
                $('#radius-selector')
                    .prop('disabled', false)
                    .qtip({show: false});
            } else {
                $('#radius-selector')
                    .prop('disabled', false)
                    .qtip(rad_qt);
            }

            $('#county')
                .css("display", "none");
            $('#county-selector')
                .prop('disabled', true)
                .qtip({show: false});

            $('#region').css("display", "none");
            $('#region-selector')
                .prop('disabled', true)
                .qtip({show: false});

            $('#bad_data')
                .prop('disabled', true);
            $('#dist-opt-right')
                .css('opacity', 0.4);
    });

    $('#sc-5-1-3')
        .click(function(){
            showZone();
            calcArea = 'county';

            $('#radius')
                .css("display", "none");
            $('#radius-selector')
                .qtip({show: false})
                .prop('disabled', true);

            $('#county')
                .css("display", "flex");
            if (hold['cou'] === true) {
                $('#county-selector')
                    .prop('disabled', false)
                    .qtip({show: false});
            } else {
                $('#county-selector')
                    .prop('disabled', false)
                    .qtip(cou_qt);
            }

            $('#region')
                .css("display", "none");
            $('#region-selector')
                .prop('disabled', true)
                .qtip({show: false});

            $('#bad_data')
                .prop('disabled', false);
            $('#dist-opt-right')
                .css('opacity', '');
    });

    $('#sc-5-1-4')
        .click(function(){
            showZone();
            calcArea = 'region';

            $('#radius')
                .css("display", "none");
            $('#radius-selector')
                .qtip({show: false})
                .prop('disabled', true);

            $('#county')
                .css("display", "none");
            $('#county-selector')
                .prop('disabled', true)
                .qtip({show: false});

            $('#region').css("display", "flex");
            if (hold['reg'] === true) {
                $('#region-selector')
                    .prop('disabled', false)
                    .qtip({show: false});
            } else {
                $('#region-selector')
                    .prop('disabled', false)
                    .qtip(reg_qt);
            }

            $('#bad_data')
                .prop('disabled', false);
            $('#dist-opt-right')
                .css('opacity', '');
    });

    $('#sc-5-1-5')
        .click(function(){
            showZone();
            calcArea = 'country';

            $('#radius').css("display", "flex")
                .css('opacity', 0.4);
            $('#radius-selector')
                .qtip({show: false})
                .prop('disabled', true);
            $('#county').css("display", "none");
            $('#county-selector').prop('disabled', true);
            $('#region').css("display", "none");
            $('#region-selector').prop('disabled', true);

            $('#bad_data')
                .prop('disabled', false);
            $('#dist-opt-right')
                .css('opacity', '');
    });

    $('#rec-button').click(function(){
        $(this).qtip({show: false});

        if ($("#sc99 input[type='radio']:checked")[0].labels == null){
            var selector = document.getElementsByName('sc-99');
            for(var i = 0; i < selector.length; i++) {
                //Check if button is checked
                var button = selector[i];
                if(button.checked) {
                    //Return value
                    id = button.id;
                }
            }

            if (id.slice(id.length - 1) == 1){
                calcArea = 'map';
            } else if (id.slice(id.length - 1) == 2){
                calcArea = 'radius'
            } else if (id.slice(id.length - 1) == 3){
                calcArea = 'county'
            } else if (id.slice(id.length - 1) == 4){
                calcArea = 'region'
            } else if (id.slice(id.length - 1) == 5){
                calcArea = 'country'
            }

        } else {
            // Chrome
            calcArea = $("#sc99 input[type='radio']:checked")[0].labels[0].innerHTML.toLowerCase();
        }

        con = true;

        if (calcArea == 'radius') {
            r = $('#radius-selector')[0].value;
            if (hold['rad'] === false || r == ''){
                hold['rad'] = false;
                test_deploy('rad', '#radius-selector', rad_qt);
                con = false
            }
        } else if (calcArea == 'county') {
            areaSecond = $('#county-selector')[0].value;
            if (hold['cou'] === false || areaSecond == ''){
                hold['cou'] = false;
                test_deploy('cou', '#county-selector', cou_qt);
                con = false
            }
        } else if (calcArea == 'region') {
            areaSecond = $('#region-selector')[0].value;

            if (hold['reg'] === false || areaSecond == ''){
                hold['reg'] = false;
                test_deploy('reg', '#region-selector', reg_qt);
                con = false
            }
        }

        if (con) {
            setcookie('areaMain', calcArea.toLowerCase());

            setcookie('min_date', Math.round(tSlider.noUiSlider.get()[0]));
            setcookie('max_date', Math.round(tSlider.noUiSlider.get()[1]));
            setcookie('min_price', Math.round(pSlider.noUiSlider.get()[0]));
            setcookie('max_price', Math.round(pSlider.noUiSlider.get()[1]));

            var r = gmap.getBounds().getNorthEast().lng();
            var l = gmap.getBounds().getSouthWest().lng();
            var t = gmap.getBounds().getNorthEast().lat();
            var b = gmap.getBounds().getSouthWest().lat();
            setcookie('right', r);
            setcookie('left', l);
            setcookie('top', t);
            setcookie('bottom', b);

            if (document.querySelector('#bad_data:checked') != null) {
                bad_data = 'false'
            } else {
                bad_data = 'true'
            }

            if (calcArea == 'radius'){
                radius = document.getElementById("radius-selector").value;
                setcookie('radius', radius);
            } else if (calcArea == 'county'){
                areaSecond = $('#county-selector')[0].value;
                setcookie('areaSecond', areaSecond);
                setcookie('bad_data_inc', bad_data);
            } else if (calcArea == 'region'){
                areaSecond = $('#region-selector')[0].value;
                setcookie('areaSecond', areaSecond);
                setcookie('bad_data_inc', bad_data);
            } else if (calcArea == 'country') {
                setcookie('bad_data_inc', bad_data);
            }
            //reload page
            window.location.reload();
        } else {
            $(this).qtip(rec_qt)
        }
    });

    $('#address').keyup(function(event){
        if (event.keyCode == '13') {
            $.ajax({
                type: "POST",
                url: "/table/ajax-response-map/",
                data: {'address': $('#address').val()},
                async: true,
                dataType: 'json',
                success: function (data) {
                    if (data['status'] == 2){
                        r = parseFloat(Cookies.get('right'));
                        l = parseFloat(Cookies.get('left'));
                        t = parseFloat(Cookies.get('top'));
                        b = parseFloat(Cookies.get('bottom'));

                        lat = (t - b)/2 + b;
                        lng = (l - r)/2 + r;

                        gmap.setCenter({lat: lat, lng: lng});

                        $('#address').after("<div id='alert-holder'>" +
                            "<div id='return-status' class='alert alert-danger'>" +
                                "<a class='close' id='close-alert'>&times; </a>" +
                                "<strong>Sorry!</strong> We couldn't find a matching address. " +
                                    "Please try searching for a street name or suburb." +
                            "</div><div id='alert-pad'></div></div>")

                        $('#close-alert').click(function(){
                            $(this).parent().parent().remove();
                        });

                    } else {
                        gmap.setCenter({lat: data['location']['lat'], lng: data['location']['lng']});
                    }

                }
            })
        }
    });

    $('#search-submit').click(function(){
        $.ajax({
                type: "POST",
                url: "/table/ajax-response-map/",
                data: {'address': $('#address').val()},
                async: true,
                dataType: 'json',
                success: function (data) {
                    if (data['status'] == 2){
                        r = parseFloat(Cookies.get('right'));
                        l = parseFloat(Cookies.get('left'));
                        t = parseFloat(Cookies.get('top'));
                        b = parseFloat(Cookies.get('bottom'));

                        lat = (t - b)/2 + b;
                        lng = (l - r)/2 + r;

                        gmap.setCenter({lat: lat, lng: lng});

                        $('#address').after("<div id='alert-holder'>" +
                            "<div id='return-status' class='alert alert-danger'>" +
                                "<a class='close' id='close-alert'>&times; </a>" +
                                "<strong>Sorry!</strong> We couldn't find a matching address. " +
                                    "Please try searching for a street name or suburb." +
                            "</div><div id='alert-pad'></div></div>")

                        $('#close-alert').click(function(){
                            $(this).parent().parent().remove();
                        });

                    } else {
                        gmap.setCenter({lat: data['location']['lat'], lng: data['location']['lng']});
                    }

                }
            })
    })

});