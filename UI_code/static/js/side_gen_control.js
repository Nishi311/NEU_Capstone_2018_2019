
$(document).on("click", "#add_side", function() {

    // Length of a grid in METERS
    var quad_side_meters = parseFloat($("#quadrant_side_size").val());
    var num_photos_per_quad = parseInt($("#num_photos_per_quad").val());

    //get coordinate corner points
    var top_right_lat = parseFloat($("#right_lat").val());
    var top_right_long = parseFloat($("#right_long").val());
    var top_right_alt = parseFloat($("#top_alt").val());

    var top_left_lat = parseFloat($("#left_lat").val());
    var top_left_long = parseFloat($("#left_long").val());
    var top_left_alt = parseFloat($("#top_alt").val());

    var bottom_right_lat = parseFloat($("#right_lat").val());
    var bottom_right_long = parseFloat($("#right_long").val());
    var bottom_right_alt = parseFloat($("#bottom_alt").val());

    var bottom_left_lat = parseFloat($("#left_lat").val());
    var bottom_left_long = parseFloat($("#left_long").val());
    var bottom_left_alt = parseFloat($("#bottom_alt").val());

    if (top_left_alt <= bottom_left_alt){
        return;
    }

    // Thanks to https://en.wikipedia.org/wiki/Decimal_degrees for the info
    // This number represents the number of meters represented by one degree of latitude
    var one_degree_const_meters_lat = 111320;

    // This number represents the number of meters represented by one degree of longitude.
    // NOTE: This varies as you get closer / further to equator and so will be a bit more dynamic.
    var one_degree_const_meters_long = 111320;

    if (Math.abs(top_right_long) > 23){
        one_degree_const_meters_long = 102470;
    }
    if (Math.abs(top_right_long) > 45){
        one_degree_const_meters_long = 78710;
    }
    if (Math.abs(top_right_long) > 67){
        one_degree_const_meters_long = 43496;
    }

    // Control variables that govern behavior of DD displacement calculation
    var lat_locked = false;
    var long_locked = false;

    // Variables that handle the lat / long displacement required to create quadrants of "quad_side_meters" dimensions
    var quad_lat_displacement_meters = 0;
    var quad_lat_displacement_DD = 0;

    var quad_long_displacement_meters = 0;
    var quad_long_displacement_DD = 0;

    var quad_alt_displacement_meters = 0;

    // Variables that contain the number of rows / columns necessary to make even sub-grids between the specified edges
    // of the grid structure.
    var columns = 0;
    var rows = 0;
    /* If either the latitudes or the longitudes match, then only the opposite parameter needs to be offset
       otherwise, both parameters will need to be offset.

       In the former scenario, the offset (which will need to be converted from meters to Decimal Degree format) will be
       the full "quad_side_meters".

       In the latter scenario, the two points form the hypotenuse (of length "quad_side_meters") of a right triangle and
       the lat / long offset will be represented by the two equal length legs of the triangle.
    */
    if (top_left_lat == top_right_lat){
        lat_locked = true;

        quad_long_displacement_meters = quad_side_meters;

        var total_long_diff_meters = dd_lat_long_diff(top_left_lat, top_left_long, top_right_lat, top_right_long);
        if (total_long_diff_meters < quad_side_meters){
            columns = 1
            quad_long_displacement_meters = quad_side_meters;
        } else{
            columns = Math.ceil(total_long_diff_meters/quad_side_meters);
            quad_long_displacement_meters = total_long_diff_meters / columns;
        }

        // Depending on what is considered the left and right coordinates, you may need to either add or subtract
        // the displacement.
        if (top_left_long < top_right_long){
            quad_long_displacement_DD = quad_long_displacement_meters / one_degree_const_meters_long;
        } else {
            quad_long_displacement_DD = -quad_long_displacement_meters / one_degree_const_meters_long;
        }
    }

    if (top_left_long == top_right_long){
        long_locked = true;

        quad_lat_displacement_meters = quad_side_meters;
        var total_lat_diff_meters = dd_lat_long_diff(top_left_lat, top_left_long, top_right_lat, top_right_long);
        if (total_lat_diff_meters < quad_side_meters){
            columns = 1
            quad_lat_displacement_meters = quad_side_meters;
        } else{
            columns = Math.ceil(total_lat_diff_meters/quad_side_meters);
            quad_lat_displacement_meters = total_lat_diff_meters / columns;
        }

        columns = Math.ceil(total_lat_diff_meters/quad_side_meters);

        quad_lat_displacement_meters = total_lat_diff_meters / columns;

        // Depending on what is considered the left and right coordinates, you may need to either add or subtract
        // the displacement.
        if (top_left_lat < top_right_lat){
            quad_lat_displacement_DD = quad_lat_displacement_meters / one_degree_const_meters_lat;
        } else{
            quad_lat_displacement_DD = -quad_lat_displacement_meters / one_degree_const_meters_lat;
        }
    }

    if (!lat_locked && !long_locked){
        // If neither Lat NOR Long are locked, then we the displacement necessary to affect a grid must be split evenly
        // between the two. This displacement will be the two arms of a right triangle where the  hypotenuse is of
        // "quade_side_meters" length.
        var hypotenuse_diff_meters = dd_lat_long_diff(top_left_lat, top_left_long, top_right_lat, top_right_long);

        if (hypotenuse_diff_meters < quad_side_meters){
            columns = 1
            arm_diff_meters = Math.sqrt(Math.pow(quad_side_meters, 2) / 2);
        } else{
            columns = Math.ceil(hypotenuse_diff_meters/quad_side_meters);
            arm_diff_meters = Math.sqrt(Math.pow(hypotenuse_diff_meters, 2) / 2);
        }

        // Depending on what is considered the left and right coordinates, you may need to either add or subtract
        // the displacement.
        if (top_left_long < top_right_long){
            quad_long_displacement_meters = arm_diff_meters / columns;
        } else{
            quad_long_displacement_meters = -arm_diff_meters / columns;
        }

        quad_long_displacement_DD = quad_long_displacement_meters / one_degree_const_meters_long;

        if (top_left_lat < top_right_lat){
            quad_lat_displacement_meters = arm_diff_meters / columns;
        } else{
            quad_lat_displacement_meters = -arm_diff_meters / columns;
        }

        quad_lat_displacement_DD = quad_lat_displacement_meters / one_degree_const_meters_lat;
    }

    var total_altitude_displacement_meters = top_left_alt-bottom_left_alt;
    rows = Math.ceil(total_altitude_displacement_meters/quad_side_meters);

    quad_alt_displacement_meters = quad_side_meters;

    // Assuming starting from left-most

    var quad_num = rows*columns;
    var quadrant_grid = '';

    var quad_left_lat_limit = top_left_lat;
    var quad_left_long_limit = top_left_long;

    var quad_right_lat_limit = quad_left_lat_limit + quad_lat_displacement_DD;
    var quad_right_long_limit = quad_left_long_limit + quad_long_displacement_DD;

    var quad_top_limit = top_left_alt;
    var quad_bottom_limit = quad_top_limit - quad_alt_displacement_meters;

    for(var i= 0, end = rows; i<end; ++i){

        if (quad_bottom_limit < bottom_left_alt){
            quad_bottom_limit = bottom_left_alt;
        }

        for(var j=0, len = columns; j < len; ++j){

            var str = "Quadrant ".concat(quad_num);
            quadrant_grid +='<div class="grid-item" id="' + str + '" lat_limit_left="' + quad_left_lat_limit+ '" long_limit_left="' + quad_left_long_limit + '" lat_limit_right="' + quad_right_lat_limit + '" long_limit_right="' + quad_right_long_limit+ '" top_limit="' + quad_top_limit + '" bottom_limit="' + quad_bottom_limit + '"></div>';

            quad_num -= 1;

            quad_left_lat_limit = quad_right_lat_limit;
            quad_left_long_limit = quad_right_long_limit;

            quad_right_lat_limit = quad_left_lat_limit + quad_lat_displacement_DD;
            quad_right_long_limit = quad_left_long_limit + quad_long_displacement_DD;

        }
        quad_top_limit = quad_bottom_limit;
        quad_bottom_limit = quad_top_limit - quad_alt_displacement_meters;
    }

    $("div.grid-wrapper").html(quadrant_grid);
    $("div.grid-wrapper").css({"grid-template-columns": "repeat("+columns+",1fr)", "grid-template-rows": "repeat("+rows+",25px)"});
    $("div.grid-wrapper").attr("data-total-number",rows*quad_side_meters);
    $("div.building_image").scrollTop = $("div.building_image").scrollHeight;

    $.post("/add_new_side", {grid_data: quadrant_grid, num_photos_per_quad:num_photos_per_quad, num_columns:columns, num_rows:rows});

    document.getElementById("right_lat").value = "0";
    document.getElementById("right_long").value = "0";
    document.getElementById("left_lat").value = "0";
    document.getElementById("left_long").value = "0";
    document.getElementById("top_alt").value = "0";
    document.getElementById("bottom_alt").value = "0";

    //TODO: Update the currently selected side in side_status_control (somehow).

});

// Courtesy of https://www.geodatasource.com/developers/javascript
// I don't actually know how this thing works.
function dd_lat_long_diff(lat1, lon1, lat2, lon2){
	if ((lat1 == lat2) && (lon1 == lon2)){
		return 0;
	} else {
		var radlat1 = Math.PI * lat1/180;
		var radlat2 = Math.PI * lat2/180;
		var theta = lon1-lon2;
		var radtheta = Math.PI * theta/180;
		var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
		if (dist > 1) {
			dist = 1;
		}
		dist = Math.acos(dist);
		dist = dist * 180/Math.PI;
		dist = dist * 60 * 1.1515;
		dist = dist * 1.609344;

        //Final answer given in Kilometers, quick conversion to meters
        dist = dist * 1000;

		return dist;
	}
}
