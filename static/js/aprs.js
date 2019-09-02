$('#type_aprs').on('change', function () {
    $.ajax({
        url: "/map_aprs",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'type_aprs': document.getElementById('type_aprs').value,
            'prop_aprs': document.getElementById('prop_aprs').value,
            'time_aprs': document.getElementById('time_aprs').value,
        },
        dataType: "json",
        success: function (data) {
            Plotly.plot('map_aprs', data);
            Plotly.deleteTraces('map_aprs', 0);

        }
    });
})

$('#prop_aprs').on('change', function () {
    $.ajax({
        url: "/map_aprs",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'type_aprs': document.getElementById('type_aprs').value,
            'prop_aprs': document.getElementById('prop_aprs').value,
            'time_aprs': document.getElementById('time_aprs').value,
        },
        dataType: "json",
        success: function (data) {
            Plotly.plot('map_aprs', data);
            Plotly.deleteTraces('map_aprs', 0);

        }
    });
})

$('#time_aprs').on('change', function () {
    $.ajax({
        url: "/map_aprs",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'type_aprs': document.getElementById('type_aprs').value,
            'prop_aprs': document.getElementById('prop_aprs').value,
            'time_aprs': document.getElementById('time_aprs').value,
            'update': true,
        },
        dataType: "json",
        success: function (data) {
            Plotly.plot('map_aprs', data);
            Plotly.deleteTraces('map_aprs', 0);

        }
    });
})

setInterval(function () {
    $.ajax({
        url: "/map_aprs",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'type_aprs': document.getElementById('type_aprs').value,
            'prop_aprs': document.getElementById('prop_aprs').value,
            'time_aprs': document.getElementById('time_aprs').value,
            'update': true,
        },
        dataType: "json",
    })
        .done(function (data) {
            Plotly.plot('map_aprs', data);
            Plotly.deleteTraces('map_aprs', 0);
        })
}, 1000 * 60);