setInterval("update_dynamic_quadrants_progress();",1000);

$(document).on("click", "#update_grid", function() {

    //get coordinate corner points
    var top_right_x = $("#top_right-x").val();
    var top_right_y = $("#top_right-y").val();

    var top_left_x = $("#top_left-x").val();
    var top_left_y = $("#top_left-y").val();

    var bottom_right_x = $("#bottom_right-x").val();
    var bottom_right_y = $("#bottom_right-y").val();

    var bottom_left_x = $("#bottom_left-x").val();
    var bottom_left_y = $("#bottom_left-y").val();

    var detect_height = 6;
    var detect_width = 6;

    // calculate number of columns and rows
    var columns = Math.ceil((top_left_x-top_right_x)/detect_width);
    var rows = Math.ceil((top_right_y-bottom_right_y)/detect_height);



    var num = rows*columns;

    var quadrant_grid = '';
    var top = rows*detect_height;

    for(var i= 0, end = rows; i<end; ++i){

        var left = columns*detect_width;

        for(var j=0, len = columns; j < len; ++j)
        {
            var str = "Quadrant ".concat(num);

            if ($("div.grid-wrapper").attr("data-current") === str) {
                quadrant_grid +='<div class="grid-item examined-next" id="' + str + '" data-left="' + left + '" data-right="' + (left-detect_width) + '" data-top="' + top + '" data-bottom="' + (top-detect_height) + '">' + str + '</div>';
            } else if ($('#'.concat(str)) === str) {
                quadrant_grid +='<div class="grid-item examined" id="' + str + '" data-left="' + left + '" data-right="' + (left-detect_width) + '" data-top="' + top + '" data-bottom="' + (top-detect_height) + '">' + str + '</div>';
            } else {
                quadrant_grid +='<div class="grid-item" id="' + str + '" data-left="' + left + '" data-right="' + (left-detect_width) + '" data-top="' + top + '" data-bottom="' + (top-detect_height) + '">' + str + '</div>';
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
