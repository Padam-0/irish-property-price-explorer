$(document).ready(function() {

    county_list = ['Galway City', 'Galway County','Leitrim', 'Mayo', 'Roscommon', 'Sligo',
        'Carlow', 'Dublin', 'Kildare', 'Kilkenny', 'Laois', 'Longford', 'Louth', 'Meath',
        'Offaly', 'Westmeath', 'Wexford', 'Wicklow', 'Clare', 'Cork City', 'Cork County',
        'Kerry', 'Limerick City', 'Limerick County','Tipperary', 'Waterford City', 'Waterford County',
        'Cavan', 'Donegal', 'Monaghan'];

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

    pred_qt = {
        content: {
            text: 'Please correct errors above before predicting house price.'
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
            hide: 'mouseleave'
        };


    $('#submit-btn').click(function(){
        $(this).qtip({show: false});

        con = true;

        county = $('#county-selector')[0].value;
        if (county_list.indexOf(county) == -1){
            $('#county-selector')
                .css('outline-color', '#e62e00')
                .qtip(cou_qt);

            con = false
        } else {
            $('#county-selector')
                .css('outline-color', '#00b300')
                .qtip({
                    show: false
                });
        }

        if (con) {

            $('#submit-btn')
                .prop('disabled', true)
                .attr('opacity', 0.4);

            $('#output-data').html('')
                .append("<h4 id='predicting'>Predicting property price...</h4>")
                .append("<span class='ld ld-ring ld-spin'></span>");

            address = document.getElementById("address").value;
            county = document.getElementById("county-selector").value;

            if ($("#sc-dop input[type='radio']:checked")[0].labels == null){
                var selector = document.getElementsByName('sc-6');
                for(var i = 0; i < selector.length; i++) {
                    //Check if button is checked
                    var button = selector[i];
                    if(button.checked) {
                        //Return value
                        id = button.id;
                    }
                }

                if (id.slice(id.length - 1) == 1){
                    dop = 'Semi-Detached';
                } else if (id.slice(id.length - 1) == 2){
                    dop = 'Detached'
                } else if (id.slice(id.length - 1) == 3){
                    dop = 'Terraced'
                } else {
                    dop = 'Other'
                }

            } else {
                // Chrome
                dop = $("#sc-dop input[type='radio']:checked")[0].labels[0].innerHTML;
            }

            if ($("#sc-condition input[type='radio']:checked")[0].labels == null){
                var selector = document.getElementsByName('sc-2');
                for(var i = 0; i < selector.length; i++) {
                    //Check if button is checked
                    var button = selector[i];
                    if(button.checked) {
                        //Return value
                        id = button.id;
                    }
                }

                if (id.slice(id.length - 1) == 1){
                    condition = 'Second-Hand House / Apartment';
                } else {
                    condition = 'New House / Apartment'
                }

            } else {
                // Chrome
                condition = $("#sc-condition input[type='radio']:checked")[0].labels[0].innerHTML;
            }

            if ($("#sc-beds input[type='radio']:checked")[0].labels == null){
                var selector = document.getElementsByName('sc-9');
                for(var i = 0; i < selector.length; i++) {
                    //Check if button is checked
                    var button = selector[i];
                    if(button.checked) {
                        //Return value
                        id = button.id;
                    }
                }

                if (id.slice(id.length - 1) == 1){
                    beds = '1';
                } else if (id.slice(id.length - 1) == 2) {
                    beds = '2';
                } else if (id.slice(id.length - 1) == 3) {
                    beds = '3';
                } else if (id.slice(id.length - 1) == 4) {
                    beds = '4';
                } else {
                    beds = '5+';
                }

            } else {
                // Chrome
                beds = $("#sc-beds input[type='radio']:checked")[0].labels[0].innerHTML;
            }

            if ($("#sc-baths input[type='radio']:checked")[0].labels == null){
                var selector = document.getElementsByName('sc-8');
                for(var i = 0; i < selector.length; i++) {
                    //Check if button is checked
                    var button = selector[i];
                    if(button.checked) {
                        //Return value
                        id = button.id;
                    }
                }

                if (id.slice(id.length - 1) == 1){
                    baths = '1';
                } else if (id.slice(id.length - 1) == 2) {
                    baths = '2';
                } else if (id.slice(id.length - 1) == 3) {
                    baths = '3';
                } else if (id.slice(id.length - 1) == 4) {
                    baths = '4';
                } else {
                    baths = '5+';
                }

            } else {
                // Chrome
                baths = $("#sc-baths input[type='radio']:checked")[0].labels[0].innerHTML;
            }

            var data_to_send = {
                'address': address, 'county': county, 'dop': dop,
                'condition': condition, 'beds': beds, 'baths': baths
            };

            $.ajax({
                type: "POST",
                url: "/hp-predictor/ajax-post-prediction/",
                data: data_to_send,
                async: true,
                dataType: 'json',
                success: function(data) {

                    $('#submit-btn')
                        .prop('disabled', false)
                        .attr('opacity', 1);

                    if (data['status'] === 0) {
                        $('#output-data').html('')
                            .append("<h3>Predicted Price (Today): <strong>&euro;" + thousandsDisplay(data['price']) + "</strong> +/- &euro; " + thousandsDisplay(data['moe']) + "</h3>")
                            .append(function(){
                                pd = data['plotdata'];
                                if (pd[pd.length - 1] > data['ti_data'] + data['moe']){
                                    return "<h4>The prediction suggests that properties similar to that searched are overvalued compared to a historical baseline.</h4>"
                                } else if (pd[pd.length - 1] < data['ti_data'] - data['moe']){
                                    return "<h4>The prediction suggests that properties similar to that searched are undervalued compared to a historical baseline.</h4>"
                                } else {
                                    return "<h4>The prediction suggests that properties similar to that searched are in line with historical baselines.</h4>"
                                }
                            });
                    } else if (data['status'] === 1) {
                        $('#output-data').html('')
                            .append("<h4>We weren't able to match that exact address, but a partial result was returned:</h4>")
                            .append("<br/><h4>Predicted Price (Today): &euro;" + thousandsDisplay(data['price']) + "</strong> +/- &euro; " + thousandsDisplay(data['moe']) + "</h4>")
                            .append(function(){
                                pd = data['plotdata'];
                                if (pd[pd.length - 1] > data['ti_data'] + data['moe']){
                                    return "<h4>The prediction suggests that properties similar to that searched are overvalued compared to a historical baseline.</h4>"
                                } else if (pd[pd.length - 1] < data['ti_data'] - data['moe']){
                                    return "<h4>The prediction suggests that properties similar to that searched are undervalued compared to a historical baseline.</h4>"
                                } else {
                                    return "<h4>The prediction suggests that properties similar to that searched are in line with historical baselines.</h4>"
                                }
                            });
                    } else {
                        $('#output-data').html('')
                            .append("<h4>I'm sorry, no result was able to be returned based on the following parameters:</h4>");
                    }

                    $('#output-data')
                        .append("<div id='pricechart'><svg id='chart' xmlns='http://www.w3.org/2000/svg'></svg></div>")
                        .append("<p id='disclaimer'>Disclaimer: This prediction is made by a predictive model and assumptions made about properties in the area of question." +
                        " The accuracy of the model is highly dependent on data quality, which you can read more about <a href='/our-data'>here</a>.</p>")

                    if (data['status'] === 0 || data['status'] === 1) {
                        $('#output-data')
                            .append("</br><h4>Prediction is based on the following parameters:</h4>")
                            .append(function(){
                                if (data_to_send['address'] == ''){
                                    return "<p><strong>Address:</strong> None.</p>"
                                } else {
                                    return "<p><strong>Address:</strong> " + data_to_send['address'] + "</p>"
                                }
                            })
                            .append("<p><strong>County:</strong> " + data_to_send['county'] + "</p>")
                            .append("<p><strong>Type of House:</strong> " + data_to_send['dop'] + "</p>")
                            .append("<p><strong>Condition:</strong> " + data_to_send['condition'] + "</p>")
                            .append("<p><strong>Bedrooms:</strong> " + data_to_send['beds'] + "</p>")
                            .append("<p><strong>Bathrooms:</strong> " + data_to_send['baths'] + "</p>")
                            .append("<p id='lastp'><strong>Date:</strong> " + data['date'] + "</p>");

                        drawChart(data['plotdata'], data['ti_data'], data['moe']);
                    } else {
                        $('#output-data').html('')
                            .append("<h4>I'm sorry, no result was able to be returned based on the following parameters:</h4>")
                            .append(function(){
                                if (data_to_send['address'] == ''){
                                    return "<p><strong>Address:</strong> None</p>"
                                } else {
                                    return "<p><strong>Address:</strong> " + data_to_send['address'] + "</p>"
                                }
                            })
                            .append("<p><strong>County:</strong> " + data_to_send['county'] + "</p>")
                            .append("<p><strong>Type of House:</strong> " + data_to_send['dop'] + "</p>")
                            .append("<p><strong>Condition:</strong> " + data_to_send['condition'] + "</p>")
                            .append("<p><strong>Bedrooms:</strong> " + data_to_send['beds'] + "</p>")
                            .append("<p><strong>Bathrooms:</strong> " + data_to_send['baths'] + "</p>")
                            .append("<p id='lastp><strong>Date:</strong> " + data['date'] + "</p>");
                    }
                }
            });
        } else{
            $(this).qtip(pred_qt)
        }
    });

});