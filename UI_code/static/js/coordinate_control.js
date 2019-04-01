setInterval("update_dynamic_quadrants_progress();",1000);

$(document).on("click", "#update_grid", function() {


    //TODO: Need a better way to establish 3 coordinate system. Having one degree locked means can only scan
    //on a strictly N/S or E/W basis.

    //get coordinate corner points
    var top_right_lat = $("#top_right_lat").val();
    var top_right_long = $("#top_right_long").val();
    var top_right_alt = $("#top_right_alt").val();

    var top_left_lat = $("#top_left_lat").val();
    var top_left_long = $("#top_left_long").val();
    var top_left_alt = $("#top_left_alt").val();

    var bottom_right_lat = $("#bottom_right_lat").val();
    var bottom_right_long = $("#bottom_right_long").val();
    var bottom_right_alt = $("#bottom_right_alt").val();

    var bottom_left_lat = $("#bottom_left_lat").val();
    var bottom_left_long = $("#bottom_left_long").val();
    var bottom_left_alt = $("#bottom_left_alt").val();

    // Length of a grid in METERS
    var quad_length_meters = 6;
    var quad_width_meters = 6;

    var quad_length_offset_DD = offset_calculation

    var lat_diff = top_right_lat-top_left_lat
    var long_diff = top_right_long-top_left_long

    // Assuming starting from left-most

    // calculate number of columns and rows
    //TODO: 3 Coordinate system issues largely revolve around how columns are formulated. Don't want to think
    // About that right now but you will need to change column calculations to account for diagonals.
    var columns = Math.ceil(Math.sqrt(Math.pow(lat_diff, 2) + Math.pow(long_diff, 2))/detect_width);
    var rows = Math.ceil(Math.abs(Math.ceil((top_right_alt-bottom_right_alt)/detect_height)));

    var num = rows*columns;

    var quadrant_grid = '';
    var top = rows*detect_height;

    /*
        THOUGHT BLURB: The fundamental problem is that Lat / Long do NOT match to meter offsets.
        Need to figure out the line from top left to top right of a grid.
        Need to figure out how to progress x number of meters along that line from one end to the other.
        Need to figure out how to get the lat / long coordinates from any point on that line.

        Need to figure out what to do when dividing the length of that line by x does not result in a clean division.

        What system of numbers do I use to keep track of that?

        LOOK AT THIS.
        https://www.movable-type.co.uk/scripts/latlong.html
    */




    for(var i= 0, end = rows; i<end; ++i){

        var left = columns*detect_width;
        if (left-detect_width < 0){
            var right = 0
        }
        else{
            var right = left-detect_width;
        }

        var left_lat_long_coord = Math.sqrt(Math.pow(left,2)/2)
        var right_lat_long_coord = Math.sqrt(Math.pow(right,2)/2)

        quad_lat = Math.sqrt(Math.pow())

        for(var j=0, len = columns; j < len; ++j){
            var str = "Quadrant ".concat(num);

            if ($("div.grid-wrapper").attr("data-current") === str) {
                quadrant_grid +='<div class="grid-item examined-next" id="' + str + '" lat-coord="' + locked_coordinate_name+ '" locked-coord-value="' + locked_coord_value + '" data-left="' + left + '" data-right="' + (left-detect_width)+ '" data-top="' + top + '" data-bottom="' + (top-detect_height) + '"></div>';
            }
            else if ($('#'.concat(str)) === str) {
                quadrant_grid +='<div class="grid-item examined-next" id="' + str + '" locked-coord="' + locked_coordinate_name+ '" locked-coord-value="' + locked_coord_value + '" data-left="' + left + '" data-right="' + (left-detect_width)+ '" data-top="' + top + '" data-bottom="' + (top-detect_height) + '"></div>';
            }
            else {
                quadrant_grid +='<div class="grid-item examined-next" id="' + str + '" locked-coord="' + locked_coordinate_name+ '" locked-coord-value="' + locked_coord_value + '" data-left="' + left + '" data-right="' + (left-detect_width)+ '" data-top="' + top + '" data-bottom="' + (top-detect_height) + '"></div>';
            }

            num -= 1;

            if (left-detect_width < 0){
                left = Math.abs(left-detect_width)
            }

            left -= detect_width;


        }
        top -=detect_height;
    }

//    for (var k = num, len = 0; i > len; --i) {
//        top += 6;


//    }
    $("div.grid-wrapper").html(quadrant_grid);
    $("div.grid-wrapper").css({"grid-template-columns": "repeat("+columns+",1fr)", "grid-template-rows": "repeat("+rows+",25px)"});
    $("div.grid-wrapper").attr("data-total-number",rows*detect_height);
    $("div.building_image").scrollTop = $("div.building_image").scrollHeight;

    $.post("/update_quadrant_config", {grid_data: quadrant_grid});

});


$(document).on("click", "div.grid-item", function() {
    var top = $(this).attr("data-top");
    var bot = $(this).attr("data-bottom");
    var left = $(this).attr("data-left");
    var right = $(this).attr("data-right");
    var str = "top coordinate: " + top + "\n";
    str += "bot coordinate: " + bot + "\n";
    str += "left coordinate: " + left + "\n";
    str += "right coordinate: " + right + "\n";

    alert(str);
});

//Thanks to Numan Karaasian on stack overflow:
//https://stackoverflow.com/questions/7477003/calculating-new-longitude-latitude-from-old-n-meters

function offset_calculation(var meters, var orig_lat, var orig_long){
    // number of km per degree = ~111km (111.32 in google maps, but range varies
    // between 110.567km at the equator and 111.699km at the poles)
    // 1km in degree = 1 / 111.32km = 0.0089
    // 1m in degree = 0.0089 / 1000 = 0.0000089
    var coef = meters * 0.0000089;

    var new_lat = orig_lat + coef;

    // pi / 180 = 0.018
    var new_long = orig_long + coef / Math.cos(orig_lat * 0.018);

    return [new_lat, new_long]
}

function update_dynamic_quadrants_progress()
{
    var total = $("div.grid-wrapper").attr("data-total-number");
    var num = $("div.grid-wrapper").attr("data-complete");

    $("#myBar").css( "width", ((num/total)*100));
    $("#myBar").text("".concat((num/total)*100).concat("% Completed"));
}

//var val = $("div.grid-wrapper").attr("data-current");
