/**
 * Created by mhassan on 8/30/17.
 */
$(document).ready(function () {

});

$('#play_sound').click(function () {

    var urdu_text_area = $('#urdu_text_area').val();
    $('.alert').hide()
    if (urdu_text_area == '') {
        $('#required-error').show()
    }
    else if(/[a-zA-Z]+/.test(urdu_text_area) == true){
        $('#alphabet-error').show()
    }
    else {
        $('#loading-div').show();
        var settings = {
            "crossDomain": true,
            "url": "/nlp/tts/generate/voice/",
            "method": "POST",
            "data": {
                "text": urdu_text_area,
                "voice": $("input[name='voice_option']:checked").val()
            }
        };

        $.ajax(settings).done(function (response) {
            $('#output_div').empty().append(response);
            $('#loading-div').hide();
            $('#generated_voice').get(0).play();
        });
    }
});
