var showArea = 'age';



function remove_layers(){
    if (geojson){
        map.removeLayer(geojson)
    }
    if (baselayer){
        map.removeLayer(baselayer)
    }
    if (edges){
        map.removeLayer(edges)
    }
}

$(document).ready(function() {

    $("#age-risk-btn")
        .click(function() {
            $('html, body').animate({
                scrollTop: $("#age-cont").offset().top
            }, 1000);
        })
        .qtip({
            content: {
                text: "Areas with older age distributions are considered higher risk."
            },
            style: {
                classes: 'qtip-blue qtip-rounded'
            },
            position: {
                my: 'bottom left',
                at: 'top right',
                target: this
            }
        });

    $('#close-alert').click(function(){
        $(this).parent().parent().remove();
    });

    $("#ind-risk-btn")
        .click(function() {
            $('html, body').animate({
                scrollTop: $("#ind-cont").offset().top
            }, 1000);
        })
        .qtip({
            content: {
                text: "Areas with a high concentration of jobs in one industry are considered higher risk."
            },
            style: {
                classes: 'qtip-blue qtip-rounded'
            },
            position: {
                my: 'bottom left',
                at: 'top right',
                target: this
            }
        });

    $("#fam-risk-btn")
        .click(function() {
            $('html, body').animate({
                scrollTop: $("#fam-cont").offset().top
            }, 1000);
        })
        .qtip({
            content: {
                text: "Areas with a higher numbers of retired or empty nest households are considered higher risk."
            },
            style: {
                classes: 'qtip-blue qtip-rounded'
            },
            position: {
                my: 'bottom right',
                at: 'top left',
                target: this
            }
        });

    $("#job-risk-btn")
        .click(function() {
            $('html, body').animate({
                scrollTop: $("#job-cont").offset().top
            }, 1000);
        })
        .qtip({
                content: {
                    text: "Areas with a lower numbers of working professionals are considered higher risk."
                },
                style: {
                    classes: 'qtip-blue qtip-rounded'
                },
                position: {
                    my: 'bottom right',
                    at: 'top left',
                    target: this
                }
            });

    $("#skills-risk-btn")
        .click(function() {
            $('html, body').animate({
                scrollTop: $("#skills-cont").offset().top
            }, 1000);
        })
        .qtip({
            content: {
                text: "Areas with a high concentration of skills in one category are considered higher risk."
            },
            style: {
                classes: 'qtip-blue qtip-rounded'
            },
            position: {
                my: 'bottom left',
                at: 'top right',
                target: this
            }
        });

    $("#occu-risk-btn")
        .click(function() {
            $('html, body').animate({
                scrollTop: $("#occu-cont").offset().top
            }, 1000);
        })
        .qtip({
            content: {
                text: "Areas with a low proportion of occupied properties are considered higher risk."
            },
            style: {
                classes: 'qtip-blue qtip-rounded'
            },
            position: {
                my: 'bottom left',
                at: 'top right',
                target: this
            }
        });

    $("#mort-risk-btn")
        .click(function() {
            $('html, body').animate({
                scrollTop: $("#mort-cont").offset().top
            }, 1000);
        })
        .qtip({
                content: {
                    text: "Areas that have a high concentration of mortgage owners are considered higher risk.<br/><br/>" +
                    "However, this does not take into account rented properties, where the mortgage status of the property is unknown."
                },
                style: {
                    classes: 'qtip-blue qtip-rounded'
                },
                position: {
                    my: 'bottom right',
                    at: 'top left',
                    target: this
                }
            });

    $("#pr-risk-btn")
        .click(function() {
            $('html, body').animate({
                scrollTop: $("#mort-cont").offset().top
            }, 1000);
        })
        .qtip({
                content: {
                    text: "If predicted property price is over or undervalued compared to historical baselines.</br></br>See disclaimer below chart and <a href='/our-data'>here</a> for more information."
                },
                style: {
                    classes: 'qtip-blue qtip-rounded'
                },
                position: {
                    my: 'bottom right',
                    at: 'top left',
                    target: this
                }
            });

    $('#sc-8-2-1')
        .click(function () {
            remove_layers();
            showArea = 'age';
            update_colors(map, h_popup, c_popup, showArea);
        });

    $('#sc-8-2-2')
        .click(function () {
            remove_layers();

            showArea = 'industry';
            update_colors(map, h_popup, c_popup, showArea);
        });


    $('#sc-8-2-3')
        .click(function () {
            remove_layers();

            showArea = 'family';
            update_colors(map, h_popup, c_popup, showArea);
        });

    $('#sc-8-2-4')
        .click(function () {
            showArea = 'occupation';
            remove_layers();
            update_colors(map, h_popup, c_popup, showArea);
        });

    $('#sc-8-2-5')
        .click(function () {
            showArea = 'skills';
            remove_layers();
            update_colors(map, h_popup, c_popup, showArea);

        });

    $('#sc-8-2-6')
        .click(function () {
            showArea = 'occupancy';
            remove_layers();
            update_colors(map, h_popup, c_popup, showArea);

        });

    $('#sc-8-2-7')
        .click(function () {
            showArea = 'ownership';
            remove_layers();
            update_colors(map, h_popup, c_popup, showArea);
        });

    $('#sc-8-2-8')
        .click(function () {
            showArea = 'price';
            remove_layers();
            update_colors(map, h_popup, c_popup, showArea);

        });
});