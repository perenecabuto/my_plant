var statusURL = "/status",
    irrigationURL = "/irrigate";

function irrigate() {
    $('#irrigate').attr('disabled', true);

    $.ajax({
        url: irrigationURL,
        error: function () { irrigate(); }
    });
}

function getStatus() {
    $.getJSON(statusURL, function(data) {
        $("#humidity").text('--').attr('class', 'progress-bar');
        $("#status").text('--').attr('class', 'label');

        if (data.humidity && data.humidity.value) {
            var labelClass = 'progress-bar-danger',
                percent = data.humidity.percent + "%",
                text = percent + " (" + data.humidity.value + ")";

            if (data.humidity.percent >= 70) {
                labelClass = 'progress-bar-success';
            } else if (data.humidity.percent >= 50) {
                labelClass = 'progress-bar-warning';
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
            $("#status").text('SERVER ERROR').addClass('label-danger');
        }
    });
}

$(function() {
    setInterval(getStatus, 1000);
    $("#irrigate").on("click", irrigate);
});

