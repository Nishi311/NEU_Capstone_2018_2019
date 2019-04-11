$(document).ready(function(){
    $("#close_window").click(function(){
       window.close();
        $.post("/exit",
               {
                   close: "yes"
               });
    });
    $.get("/get_images",function(data){
        var table = '<table><tr><th><b>Image</b></th><th><b>Status</b></th><th><b>Quadrant</b></th></tr>';
        for (var i = 0, len = data.length; i < len; ++i) {
            table +='<tr><td><img src="static/images/' + data[i] + '" alt="test" style="display: inline-block; width: 50%;height: auto;"><th>TBD</th><th>NA</th></tr>';
        }
        table += '</table>'
        //alert( "Data Loaded: " + table);
        $("div.results_display_table").html(table);
    });

});


