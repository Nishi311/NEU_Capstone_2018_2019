setInterval("update_queue_table();", 1000);

var queue_directory = "static/generalIO/queue"

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

function update_queue_table()
{
    $.get("/get_queued_images",function(returned_data){
        var table = '<table><tr><th><b>Queued Image</b></th></tr>';
        if (returned_data == "No images in queue"){

            table += '<div class="queue_window" style="width:240px; background-color: lightyellow; justify-content: start;">'
            table += "No Images in Queue";
            table += '</div>'
            table += '</table>'
            $("div.table_of_queued_images").html(table);

            var arrayed_results = returned_data.split("|");
            for (var i = 0, len = arrayed_results.length; i < len; i++) {
                if (arrayed_results[i] != ""){
                    var image_path = arrayed_results[i].replace('\\', '/');

                    table +='<tr><th><center><img src="' + image_path + '" style="float:middle;display:inline-block;width:"500";height:"500";"></center></th></tr>';

                }
            }
            table += '</table>'
            $("div.table_of_queued_images").html(table);
        } else if (returned_data != "No changes to queue"){
            var table = '<table><tr><th><b>Queued Image</b></th></tr>';
            table += '<div class="queue_window" style="width:240px; background-color: lightyellow; justify-content: start;">'

            var arrayed_results = returned_data.split("|");
            for (var i = 0, len = arrayed_results.length; i < len; i++) {
                if (arrayed_results[i] != ""){
                    var image_path = arrayed_results[i].replace('\\', '/');

                    table +='<tr><th><center><img src="' + image_path + '" alt="test" style="float:middle;display:inline-block;width:50%;height:auto;"></center></th></tr>';
                }
            }
            table += '</div>'
            table += '</table>'
            $("div.table_of_queued_images").html(table);
        }
    });
}
