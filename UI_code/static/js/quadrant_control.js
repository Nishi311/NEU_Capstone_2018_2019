setInterval("update_dynamic_table();",1000);
//setInterval("update_dynamic_quadrants();",1000);
setInterval("update_dynamic_sides_and_quadrants();", 1000);

var output_directory = "static/generalIO/output"
var output_photo_directory = output_directory + "/finished_photos"
var output_report_directory = output_directory + "/finished_reports"
var selected_side = "No Side Chosen"
var selected_quadrant = "No Quadrant Chosen"

function update_dynamic_table()
{
    $.get("/get_all_image_data",function(returned_data){
        var table = '<table><tr><th><b>Image</b></th><th><b>Status</b></th><th><b>GPS Coordinates</b></th></tr>';
        if (returned_data !== "No Images"){
            for (var i = 0, len = returned_data.length; i < len; ++i) {
                var image_result_string = returned_data[i]
                var arrayed_results = image_result_string.split("|")

                var image_path = "/" + arrayed_results[0].replace('\\', '/')
                var photo_path = output_photo_directory + image_path

                var coordinate_bundle = arrayed_results[1]
                var success_value = arrayed_results[3]

                table +='<tr><th><center><img src="' + photo_path + '" alt="test" style="float:middle;display:inline-block;width:50%;height:auto;"></center><th>' + success_value + '</th><th>' + coordinate_bundle + '</th></tr>';
            }
            table += selected_quadrant + '<br>';

            table += '</table>'
            $("div.table_of_images").html(table);
        } else{
            table += selected_quadrant + '<br>';
            table += "No Images yet processed for quadrant";
            table += '</table>'
            $("div.table_of_images").html(table);
        }
    });

}

function retrieve_image_info(partial_image_path){
    path_components = partial_image_path.split("/")

    quadrant_name = path_components[0]
    image_name_no_ext = path_components[1].split(".jpg")[0]

    return [quadrant_name, image_name_no_ext]

}

function update_dynamic_sides_and_quadrants()
{
    $.get("/count_sides",function(data){
        var dropdown = '';
        if (data != "No sides found"){
            for (var i = 0, len = data.length; i < len; ++i) {
                dropdown += '<a href="#" onclick=\"select_new_side(\'' + data[i] + '\');\">' + data[i] + '</a>';
            }
        } else{
             dropdown +='<a href="#">No Sides Found</a>';
        }
        //alert( "Data Loaded: " + table);
        $("div.side_dropdown_content").html(dropdown);
    });

    $.get("/count_quadrants",function(data){
        var dropdown = '';
        if (data != "No quadrants found"){
            for (var i = 0, len = data.length; i < len; ++i) {
                dropdown +='<a href="#" onclick=\'select_new_quad(' + data[i] + ');\'>' + data[i] + '</a>';
            }
        } else{
            var no_quad_string = 'No Quadrants Found';
            dropdown += '<a href="#" onclick=\"select_new_quad(\'' + no_quad_string + '\');\">' + no_quad_string + '</a>';
        }
        //alert( "Data Loaded: " + table);
        $("div.quad_dropdown_content").html(dropdown);
    });
}

// When document is ready...

$(document).on("mouseenter", "tr", function() {
    var captured_image = $(this).find("th:first")
    if (captured_image.text() !== "Image")
    {
        captured_image = captured_image.find("center:first");
        var name = captured_image.find("img").attr("src");

        d = new Date();
        $(".quick_image").attr("src", name+'?'+d.getTime());
    }
});

function select_new_quad(new_quad){
    $.post("/select_new_quadrant",{quadrant:new_quad});
}

function select_new_side(new_side){
    $.post("/select_new_side",{side:new_side});
}
