google.charts.load('current', {
    'packages': ['geochart'],
});
let hashrate_data = []
hashrate_data.push(['Latitude', 'Longitude', 'Hashrate']);
google.charts.setOnLoadCallback(getHashrateDataMarkers);

function drawMarkersMap(hashrate_data_markers) {

    for (let i = 0; i < hashrate_data_markers.length; i++) {
        hashrate_data.push(hashrate_data_markers[i]);
    }

    var data = google.visualization.arrayToDataTable(hashrate_data);

    var options = {
        displayMode: 'markers',
        backgroundColor: '#e5f6fc',
        colorAxis: {
            colors: ['#e7711c', '#4374e0'] // orange to blue
        }
    };

    var chart = new google.visualization.GeoChart(document.getElementById('world_map_div'));
    chart.draw(data, options);
    addGeomagneticLatitudes();
}


async function getHashrateDataMarkers() {
    let data_api_url = 'http://127.0.0.1:5000/api/hashrate/solar/markers/bitcoin/30/3'
    // make a request to a url
    fetch(data_api_url)
        .then(response => response.json())
        .then(data => {
                drawMarkersMap(data);
            }
        )
        .catch(error => {
                console.log(error);
                return undefined;
            }
        )
}

function addGeomagneticLatitudes() {
    let geomagnetic_svg = document.createElementNS("/../../templates/geomagnetic-latitudes.svg", "svg");
    document.getElementById('world_map_div').appendChild(geomagnetic_svg)
}