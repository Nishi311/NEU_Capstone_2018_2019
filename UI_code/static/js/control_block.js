$(document).ready(function(){
    $("#building_sweep").click(function(){
        $.post("/building_sweep",
        {
            close: "yes"
       });
    });
    $("#compress_data").click(function(){
        $.post("/building_sweep",
        {
            close: "yes"
       });
    });
});
