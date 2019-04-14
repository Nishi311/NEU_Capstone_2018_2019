setInterval("update_queue_table();", 1000);

var queue_directory = "static/generalIO/queue";
var recognition_in_progress = false;

function toggleRecognition(){
    var toggle_text = document.getElementById("toggle_recognition_button").value;
    var new_toggle_text = "";


    var sub_image_width = document.getElementById("sub_image_width").value;
    var sub_image_height = document.getElementById("sub_image_height").value;
    var pos_threshold = document.getElementById("pos_threshold").value;

    if (toggle_text=="Start Recognition"){
        new_toggle_text = "End Recognition";
        recognition_in_progress = true;
        $.post("/toggle_recognition",{new_state:"ACTIVE", "sub_image_width":sub_image_width,
                                      "sub_image_height": sub_image_height, "pos_threshold":pos_threshold});

    } else if (toggle_text =="End Recognition"){
        new_toggle_text = "Start Recognition";
        recognition_in_progress = false;
        $.post("/toggle_recognition",{new_state:"INACTIVE"});

    }
    document.getElementById("toggle_recognition_button").value=new_toggle_text;
}

function update_queue_table()
{
    $.get("/get_queued_images",function(returned_data){
        var table = '<table><tr><th><b>First 5 Images in Queue</b></th></tr>';
        if (returned_data == "No images in queue"){
            table += 'No Images in queue';

            table += '<div class="queue_window" style="width:100px; background-color: lightyellow; justify-content: start;">'
            table += '</div>'

            table += '</table>'
            $("div.table_of_queued_images").html(table);
        }
        else {
            var table = '<table><tr><th><b>Queued Image</b></th></tr>';
            table += '<div class="queue_window" style="width:100px; background-color: lightyellow; justify-content: start;">'

            var arrayed_results = returned_data.split("|");
            var table_length = 5
            if (arrayed_results.length < 5){
                table_length = arrayed_results.length
            }
            for (var i = 0, len = table_length; i < len; i++) {
                if (arrayed_results[i] != ""){
                    var image_path = arrayed_results[i].replace('\\', '/');

                    table +='<tc><th><center><img src="' + image_path + '" alt="test" style="float:middle;display:table-column;width:100px;height:100px;"></center></th></tc>';
                }
            }
            table += '</div>'
            table += '</table>'
            $("div.table_of_queued_images").html(table);
        }

    });
}
