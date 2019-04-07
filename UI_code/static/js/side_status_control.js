setInterval("update_side_status_bar();",1000);
setInterval("update_side_status_grid();",1000);

setInterval("update_status_side_selected();",1000);

var selected_status_side = "NO SIDE CHOSEN"
$(document).on("click", "div.grid-item", function() {

    var quadrant_name = $(this).attr("id");

    var lat_limit_left = $(this).attr("lat_limit_left");
    var long_limit_left = $(this).attr("long_limit_left");

    var lat_limit_right = $(this).attr("lat_limit_right");
    var long_limit_right = $(this).attr("long_limit_right");

    var top_limit = $(this).attr("top_limit");
    var bottom_limit = $(this).attr("bottom_limit");

    var str = quadrant_name + "\n\n"
    str += "Decimal Degree Format: (Latitude, Longitude, Altitude)\n\n"
    str += "Top Left Coordinate: (" + lat_limit_left + ", " + long_limit_left + ", " + top_limit + ")\n";
    str += "Top Right Coordinate: (" + lat_limit_right + ", " + lat_limit_right + ", " + top_limit + ")\n";
    str += "Bottom Left Coordinate: (" + lat_limit_left + ", " + long_limit_left + ", " + bottom_limit + ")\n";
    str += "Bottom Right Coordinate: (" + lat_limit_right + ", " + lat_limit_right + ", " + bottom_limit + ")\n";

    alert(str);
});

function update_status_side_selected(){
    $.get("/get_sides_list",function(data){
        var dropdown = '';
        if (data != "No sides found"){
            for (var i = 0, len = data.length; i < len; ++i) {
                dropdown += '<a href="#" onclick=\"select_new_status_side(\'' + data[i] + '\');\">' + data[i] + '</a>';
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
    });
}

function update_side_status_grid(){

}

function update_side_status_bar()
{
    var total = $("div.grid-wrapper").attr("data-total-number");
    var num = $("div.grid-wrapper").attr("data-complete");

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
}



