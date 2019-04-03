setInterval("update_dynamic_table();",1000);
setInterval("update_dynamic_quadrants();",1000);
var output_directory = "static/generalIO/output"
var output_photo_directory = output_directory + "/finished_photos"
var output_report_directory = output_directory + "/finished_reports"
var selected_quadrant = "No Quadrant Chosen"
function update_dynamic_table()
{
    $.get("/get_images",function(returned_data){
        var table = '<table><tr><th><b>Image</b></th><th><b>Status</b></th><th><b>Quadrant</b></th></tr>';
        if (returned_data !== "No Images"){
            for (var i = 0, len = returned_data.length; i < len; ++i) {
                var image_string = returned_data[i]
                var image_path = "/" + image_string.split(": ")[0].replace('\\', '/')
                var info_bundle = image_string.split(": ")[1]
                var image_quadrant = info_bundle.split(",")[0]
                var success_value = info_bundle.split(",")[1]
                var photo_path = output_photo_directory + image_path

                table +='<tr><th><center><img src="' + photo_path + '" alt="test" style="float:middle;display:inline-block;width:50%;height:auto;"></center><th>' + success_value + '</th><th>' + image_quadrant + '</th></tr>';
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

function update_dynamic_quadrants()
{
    $.get("/count_quadrants",function(data){
        var dropdown = '';
        for (var i = 0, len = data.length; i < len; ++i) {
            dropdown +='<a href="#">' + data[i] + '</a>';
        }
        //alert( "Data Loaded: " + table);
        $("div.dropdown-content").html(dropdown);
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

$(document).on("click", "a", function() {
    var value = $(this).html();
    selected_quadrant = value;

    $.post("/select_new_quadrant",
    {
        quadrant: value
    });

});
//
