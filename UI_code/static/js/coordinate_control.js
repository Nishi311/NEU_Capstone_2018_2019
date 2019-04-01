setInterval("update_dynamic_quadrants_progress();",1000);

$(document).on("click", "#update_grid", function() {


    //TODO: Need a better way to establish 3 coordinate system. Having one degree locked means can only scan
    //on a strictly N/S or E/W basis.

    
    //get coordinate corner points
    var locked_coordinate_name = $("#locked_coordinate").val();
    var locked_coord_value = $("#locked_coordinate_value").val();

    var top_right_var = $("#top_right_variable").val();
    var top_right_alt = $("#top_right_alt").val();

    var top_left_var = $("#top_left_variable").val();
    var top_left_alt = $("#top_left_alt").val();

    var bottom_right_var = $("#bottom_right_variable").val();
    var bottom_right_alt = $("#bottom_right_alt").val();

    var bottom_left_var = $("#bottom_left_variable").val();
    var bottom_left_alt = $("#bottom_left_alt").val();

    var detect_height = 6;
    var detect_width = 6;
    var detect

    // calculate number of columns and rows
    var columns = Math.abs(Math.ceil((top_right_var-top_left_var)/detect_width));
    var rows = Math.abs(Math.ceil((top_right_alt-bottom_right_alt)/detect_height));

    var num = rows*columns;

    var quadrant_grid = '';
    var top = rows*detect_height;

    for(var i= 0, end = rows; i<end; ++i){

        var left = columns*detect_width;

        for(var j=0, len = columns; j < len; ++j){
            var str = "Quadrant ".concat(num);

            if ($("div.grid-wrapper").attr("data-current") === str) {
                quadrant_grid +='<div class="grid-item examined-next" id="' + str + '" locked-coord="' + locked_coordinate_name+ '" locked-coord-value="' + locked_coord_value + '" data-left="' + left + '" data-right="' + (left-detect_width)+ '" data-top="' + top + '" data-bottom="' + (top-detect_height) + '"></div>';
            }
            else if ($('#'.concat(str)) === str) {
                quadrant_grid +='<div class="grid-item examined-next" id="' + str + '" locked-coord="' + locked_coordinate_name+ '" locked-coord-value="' + locked_coord_value + '" data-left="' + left + '" data-right="' + (left-detect_width)+ '" data-top="' + top + '" data-bottom="' + (top-detect_height) + '"></div>';
            }
            else {
                quadrant_grid +='<div class="grid-item examined-next" id="' + str + '" locked-coord="' + locked_coordinate_name+ '" locked-coord-value="' + locked_coord_value + '" data-left="' + left + '" data-right="' + (left-detect_width)+ '" data-top="' + top + '" data-bottom="' + (top-detect_height) + '"></div>';
            }

            num -= 1;
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

function update_dynamic_quadrants_progress()
{
    var total = $("div.grid-wrapper").attr("data-total-number");
    var num = $("div.grid-wrapper").attr("data-complete");

    $("#myBar").css( "width", ((num/total)*100));
    $("#myBar").text("".concat((num/total)*100).concat("% Completed"));
}

//var val = $("div.grid-wrapper").attr("data-current");
