/**
 * Created by mhassan on 8/30/17.
 */
$(document).ready(function () {
});

$('#play_sound').click(function () {
    debugger;
    var urdu_text_area = $('#urdu_text_area');
    if (urdu_text_area.val() == '') {
        $('#error').show()
    }
    else {
        var settings = {
            "crossDomain": true,
            "url": "/nlp/tts/generate/voice/",
            "method": "POST",
            "data": {
                "text": urdu_text_area.val()
            }
        };

        $.ajax(settings).done(function (response) {
            $('#output_div').empty().append(response);
            $('#generated_voice').get(0).play();
        });
    }
});
