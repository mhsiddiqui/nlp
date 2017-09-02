/**
 * Created by mhassan on 8/30/17.
 */
$(document).ready(function () {
    $(".dropdown-button").dropdown();
});

$('#play_sound').click(function () {
    var settings = {
        "crossDomain": true,
        "url": "/nlp/tts/demo/",
        "method": "POST",
        "data": {
            "text": $('#urdu_text_area').val()
        }
    };

    $.ajax(settings).done(function (response) {
        debugger;
        $('#output_div').empty().append(response);
        $('#generated_voice').get(0).play();
    });
});
