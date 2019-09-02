$('#sensor_iot').on('change', function () {
    $.ajax({
        url: "/graph_iot",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'sensor_iot': document.getElementById('sensor_iot').value,
            'time_iot': document.getElementById('time_iot').value,
        },
        dataType: "json",
        success: function (data) {
            Plotly.plot('graph_iot', data);
            Plotly.deleteTraces('graph_iot', 0);
        }
    });
})

$('#time_iot').on('change', function () {
    $.ajax({
        url: "/graph_iot",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'sensor_iot': document.getElementById('sensor_iot').value,
            'time_iot': document.getElementById('time_iot').value,
        },
        dataType: "json",
        success: function (data) {
            Plotly.plot('graph_iot', data);
            Plotly.deleteTraces('graph_iot', 0);
        }
    });
})

setInterval(function () {
    $.ajax({
        url: "/graph_iot",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'sensor_iot': document.getElementById('sensor_iot').value,
            'time_iot': document.getElementById('time_iot').value,
        },
        dataType: "json",
    })
        .done(function (data) {
            Plotly.plot('graph_iot', data);
            Plotly.deleteTraces('graph_iot', 0);
        })
}, 1000 * 5);