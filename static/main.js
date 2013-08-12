var statusURL = "/status",
    irrigationURL = "/irrigate";

function irrigate(attempt) {
    attempt = attempt || 0;

    $('#irrigate').attr('disabled', true);

    $.ajax({
        url: irrigationURL,
        error: function () {
            setStatusLabel('IRRIGATION ERROR: trying again (' + (++attempt) + ')', 'label-danger');
            setTimeout(function() { irrigate(attempt) }, 500);
        }
    });
}

function showServerError() {
    setStatusLabel('SERVER ERROR', 'label-danger');
}

function setStatusLabel(value, extraclass) {
    extraclass = extraclass || '';
    $("#status").text(value).attr('class', 'label ' + extraclass);
}

function getStatus() {
    $.getJSON(statusURL).done(function(data) {
        $("#humidity").text('--').attr('class', 'progress-bar');
        setStatusLabel('--');

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

            setStatusLabel(data.status, labelClass);
        } else {
            showServerError();
        }
    }).fail(showServerError);
}

$(function() {
    setInterval(getStatus, 1000);
    $("#irrigate").on("click", irrigate);
});

