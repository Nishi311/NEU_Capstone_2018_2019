$(document).ready(function(){
    $("#lf_control").click(function(){
        $.post("/drone_manual",
        {
            direction: "LF"
       });
    });
    $("#f_control").click(function(){
        $.post("/drone_manual",
        {
            direction: "F"
       });
    });
    $("#rf_control").click(function(){
        $.post("/drone_manual",
        {
            direction: "RF"
       });
    });
    $("#l_control").click(function(){
        $.post("/drone_manual",
        {
            direction: "L"
       });
    });
    $("#l_control").click(function(){
        $.post("/drone_manual",
        {
            direction: "L"
       });
    });
    $("#up_control").click(function(){
        $.post("/drone_manual",
        {
            direction: "UP"
       });
    });
    $("#down_control").click(function(){
        $.post("/drone_manual",
        {
            direction: "DOWN"
       });
    });
    $("#r_control").click(function(){
        $.post("/drone_manual",
        {
            direction: "R"
       });
    });
    $("#lb_control").click(function(){
        $.post("/drone_manual",
        {
            direction: "LB"
       });
    });
    $("#b_control").click(function(){
        $.post("/drone_manual",
        {
            direction: "B"
       });
    });
    $("#rb_control").click(function(){
        $.post("/drone_manual",
        {
            direction: "RB"
       });
    });
});
