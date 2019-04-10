
function toggleRecognition(){
    var toggle_text = document.getElementById("toggle_recognition_button").value;
    var new_toggle_text = "";

    if (toggle_text=="Start Recognition"){
        new_toggle_text = "End Recognition";
        $.post("/toggle_recognition",{new_state:"ACTIVE"});

    } else if (toggle_text =="End Recognition"){
        new_toggle_text = "Start Recognition";
        $.post("/toggle_recognition",{new_state:"INACTIVE"});
    }
    document.getElementById("toggle_recognition_button").value=new_toggle_text;
}