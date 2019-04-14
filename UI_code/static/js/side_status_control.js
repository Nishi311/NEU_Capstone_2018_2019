setInterval("update_side_status_bar();",1000);
setInterval("update_side_status_grid();",1000);

setInterval("update_status_side_selected();",1000);

var selected_status_side = "NO SIDE CHOSEN"

var total_quads_for_selected_side = 0
var completed_quads_for_side = 0

$(document).on("click", "div.grid-item", function() {

    var side_name = $(this).attr("side");
    var quadrant_name = $(this).attr("id");
    var lat_limit_left = $(this).attr("lat_limit_left");
    var long_limit_left = $(this).attr("long_limit_left");

    var lat_limit_right = $(this).attr("lat_limit_right");
    var long_limit_right = $(this).attr("long_limit_right");

    var top_limit = $(this).attr("top_limit");
    var bottom_limit = $(this).attr("bottom_limit");

    var str = side_name + ": " + quadrant_name + "\n\n"
    str += "Decimal Degree Format: (Latitude, Longitude, Altitude)\n\n"
    str += "Top Left Coordinate: (" + lat_limit_left + ", " + long_limit_left + ", " + top_limit + ")\n";
    str += "Top Right Coordinate: (" + lat_limit_right + ", " + long_limit_right + ", " + top_limit + ")\n";
    str += "Bottom Left Coordinate: (" + lat_limit_left + ", " + long_limit_left + ", " + bottom_limit + ")\n";
    str += "Bottom Right Coordinate: (" + lat_limit_right + ", " + long_limit_right + ", " + bottom_limit + ")\n";

    alert(str);
});

function update_status_side_selected(){
    $.get("/get_sides_list",function(data){
        var dropdown = '';
        if (data != "No sides found"){
            for (var i = 0, len = data.length; i < len; ++i) {
                if (data[i] != "Unknown Side"){
                    dropdown += '<a href="#" onclick=\"select_new_status_side(\'' + data[i] + '\');\">' + data[i] + '</a>';
                }
            }
        } else{
             dropdown +='<a href="#">No Sides Found</a>';
        }
        //alert( "Data Loaded: " + table);
        $("div.status_dropdown_content").html(dropdown);
    });
}

function select_new_status_side(new_side){
    $.post("/select_new_status_side",{side:new_side}, function(){
        selected_status_side = new_side
        update_side_status_grid()

        completed_quads_for_side = 0
        total_quads_for_selected_side = 0

        $(".building_display h2").html("Side Under Examination: " + new_side);
    });
}

function update_side_status_grid(){
    $.get("/get_side_status",{side_name:selected_status_side}, function(full_status_string){
        if (full_status_string != "NO SIDE CHOSEN"){
            var status_array = full_status_string.split("|");

            var row_count = status_array[1].split(":")[1];
            var column_count = status_array[2].split(":")[1];

            total_quads_for_selected_side = row_count * column_count;

            var quadrant_status_string = status_array[3];
            var quadrant_status_array = quadrant_status_string.split("?");

            //First item is blank, eliminate it.
            quadrant_status_array.shift()

            var test = "Hello world";
            var current_cell_num = 0;

            var quadrant_grid = '';
            for (var row_index = 0; row_index < row_count; row_index++){

                for (var col_index = 0; col_index < column_count; col_index++){
                    var current_quad_string = quadrant_status_array[current_cell_num];
                    var current_quad_value_array = current_quad_string.split(",");

                    var current_quad_name = current_quad_value_array[0];
                    var current_quad_status = current_quad_value_array[1];
                    var current_quad_left_lat = current_quad_value_array[2];
                    var current_quad_left_long = current_quad_value_array[3];
                    var current_quad_right_lat = current_quad_value_array[4];
                    var current_quad_right_long = current_quad_value_array[5];
                    var current_quad_top = current_quad_value_array[6];
                    var current_quad_bottom = current_quad_value_array[7];

                    if (current_quad_status == "COMPLETE"){
                        quadrant_grid +='<div class="grid-item examined" side="' + selected_status_side + '" id="' + current_quad_name + '" lat_limit_left="' + current_quad_left_lat+ '" long_limit_left="' + current_quad_left_long + '" lat_limit_right="' + current_quad_right_lat + '" long_limit_right="' + current_quad_right_long+ '" top_limit="' + current_quad_top + '" bottom_limit="' + current_quad_bottom + '"></div>';
                        completed_quads_for_side++;
                    } else if (current_quad_status == "IN PROGRESS"){
                        quadrant_grid +='<div class="grid-item examined-next" side="' + selected_status_side + '" id="' + current_quad_name + '" lat_limit_left="' + current_quad_left_lat+ '" long_limit_left="' + current_quad_left_long + '" lat_limit_right="' + current_quad_right_lat + '" long_limit_right="' + current_quad_right_long+ '" top_limit="' + current_quad_top + '" bottom_limit="' + current_quad_bottom + '"></div>';
                    } else{
                        quadrant_grid +='<div class="grid-item" side="' + selected_status_side + '" id="' + current_quad_name + '" lat_limit_left="' + current_quad_left_lat+ '" long_limit_left="' + current_quad_left_long + '" lat_limit_right="' + current_quad_right_lat + '" long_limit_right="' + current_quad_right_long+ '" top_limit="' + current_quad_top + '" bottom_limit="' + current_quad_bottom + '"></div>';
                    }
                    current_cell_num++;
                }
            }
            $("div.grid-wrapper").html(quadrant_grid);
            $("div.grid-wrapper").css({"grid-template-columns": "repeat("+column_count+",1fr)", "grid-template-rows": "repeat("+row_count+",25px)"});
            $("div.grid-wrapper").attr("data-total-number",column_count*row_count);
            $("div.building_image").scrollTop = $("div.building_image").scrollHeight;
        }
    });
}

function update_side_status_bar()
{
    if (selected_status_side != "NO SIDE CHOSEN"){
        var total = total_quads_for_selected_side
        var num = completed_quads_for_side

        var progress_width = ((num/total)*100);
        var progress_percent = '';

        if ((num/total)*100 > 100) {
            progress_width = '100%';
            progress_percent = '100%';
        } else {
           progress_width = (progress_width.toString()).concat('%');
           progress_percent = " ".concat((num/total)*100).concat("%");
        }

        $("#myBar").css( "width", progress_width);
        $("#myBar").text(progress_percent);
    } else {
        $("#myBar").css( "width", "0%");
        $("#myBar").text("0%");
    }
}



