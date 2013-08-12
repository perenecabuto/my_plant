var statusURL = "/status",
    irrigationURL = "/irrigate";

function irrigate() {
    $('#irrigate').attr('disabled', true);

    $.ajax({
        url: irrigationURL,
        error: function () { irrigate(); }
    });
}

function showServerError() {
    $("#status").text('SERVER ERROR').attr('class', 'label label-danger');
}

function getStatus() {
    $.getJSON(statusURL).done(function(data) {
        $("#humidity").text('--').attr('class', 'progress-bar');
        $("#status").text('--').attr('class', 'label');

        if (data.humidity && data.humidity.value) {
            var percent = data.humidity.percent + "%",
                text = percent + " (" + data.humidity.value + ")";

                wetClass = 'progress-bar-info',
                warnClass = 'progress-bar-warning',
                dryClass = 'progress-bar-danger';

                labelClass = 'progress-bar-danger'

            if (data.humidity.percent >= 75) {
                labelClass = wetClass;
            } else if (data.humidity.percent >= 61) {
                labelClass = warnClass;
            }

            $("#humidity").css('width', percent).addClass(labelClass).text(text);
        }

        if (data.status) {
            var labelClass = 'label-warning';
            $('#irrigate').attr('disabled', true);

            if (data.status == 'IDLE') {
                labelClass = 'label-success';
                $('#irrigate').attr('disabled', false)
            }

            $("#status").text(data.status).addClass(labelClass);
        } else {
            showServerError();
        }
    }).fail(showServerError);
}

$(function() {
    setInterval(getStatus, 1000);
    $("#irrigate").on("click", irrigate);
});

