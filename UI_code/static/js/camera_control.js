$(document).ready(function(){
    $("#f_control").click(function(){
        $.post("/camera_manual",
        {
            direction: "UP"
       });
    });
    $("#picture").click(function(){
        $.post("/camera_manual",
        {
            direction: "PIC"
       });
        $.get("/camera_manual",function(data)
        {
            //alert(data);
            if (data !== "failure")
            {

                d = new Date();
                $("#image_taken").attr("src", data+'?'+d.getTime());

            }
        });
    });
    $("#b_control").click(function(){
        $.post("/camera_manual",
        {
             direction: "DOWN"
       });
    });
});
