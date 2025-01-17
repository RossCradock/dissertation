// https://developers.google.com/chart/interactive/docs/gallery/geochart

google.charts.load('current', {
        'packages':['geochart'],
      });
      google.charts.setOnLoadCallback(drawRegionsMap);

      function drawRegionsMap() {
        var data = google.visualization.arrayToDataTable([
          ['Country', 'Popularity'],
          ['Germany', 200],
          ['United States', 300],
          ['Brazil', 400],
          ['Canada', 500],
          ['France', 600],
          ['RU', 700]
        ]);

        var options = {backgroundColor: '#e5f6fc'};
        var chart = new google.visualization.GeoChart(document.getElementById('world_map_div'));
        chart.draw(data, options);
      }
