setInterval("update_dynamic_table();",1000);
setInterval("update_dynamic_quadrants();",1000);

function update_dynamic_table()
{
    $.get("/get_images",function(data){
        var table = '<table><tr><th><b>Image</b></th><th><b>Status</b></th><th><b>Quadrant</b></th></tr>';
        for (var i = 0, len = data.length; i < len; ++i) {
            table +='<tr><th><center><img src="static/images' + data[i] + '" alt="test" style="float:middle;display:inline-block;width:50%;height:auto;"></center><th>TBD</th><th>NA</th></tr>';
        }
        table += '</table>'
        //alert( "Data Loaded: " + table);
        $("div.table_of_images").html(table);
    });

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
    $.post("/select_new_quadrant",
    {
        quadrant: value
    });
});
