setInterval("update_dynamic_quadrants_progress();",1000);

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

function update_dynamic_quadrants_progress()
{
    var total = $("div.grid-wrapper").attr("data-total-number");
    var num = $("div.grid-wrapper").attr("data-complete");

    $("#myBar").css( "width", ((num/total)*100));
    $("#myBar").text("".concat((num/total)*100).concat("% Completed"));
}



