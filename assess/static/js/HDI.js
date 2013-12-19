// -------------------------------------------------------------------------------------------- //
// This JS files uses/calls the google JS Chart library. Documentation can be found here:
// https://developers.google.com/chart/interactive/docs/index
// -------------------------------------------------------------------------------------------- //


// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart', 'motionchart']});

// Set a callback to run when the Google Visualization API is loaded.
google.setOnLoadCallback(drawHDIChart);


// -------------------------------------------------------------------------------------------- //
// ------------------------------ BASIC GOOGLE EXAMPLES --------------------------------------- //
// -------------------------------------------------------------------------------------------- //

function drawHDIChart() {
  var query = new google.visualization.Query('https://docs.google.com/spreadsheet/ccc?key=0Al8qqiDbFFxodDNfNjc1a1BsZFQ2YkJfeEhYTWt3Unc');
  query.send(handleHDIChartResponse);
}

var chart1, chart2, chart3, chart4, chart5;

function handleHDIChartResponse(response) {

  if (response.isError()) {
    alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
    return;
  }

  var data = response.getDataTable();

  var view = new google.visualization.DataView(data);
  view.setRows(view.getFilteredRows([{column: 1, minValue: '1950', maxValue: '2010'}]));

  var opts = {
          width: 600,
          height:320, 
          showXScalePicker : false,
          showYScalePicker : false,
          showAdvancedPanel : false,
          showChartButtons : true,
          showSidePanel : false,
          backgroundColor: '#fcfdfd'
          //, state : '{"showTrails":false,"time":"2011-09-01","xZoomedDataMax":1314835200000,"iconKeySettings":[],"sizeOption":"_UNISIZE","xZoomedDataMin":1009843200000,"dimensions":{"iconDimensions":["dim0"]},"playDuration":15088.88888888889,"orderedByX":false,"xZoomedIn":false,"yZoomedDataMax":500,"iconType":"LINE","duration":{"timeUnit":"D","multiplier":1},"yZoomedIn":false,"colorOption":"_UNIQUE_COLOR","orderedByY":false,"nonSelectedAlpha":0.4,"xLambda":1,"xAxisOption":"_TIME","uniColorForNonSelected":false,"yAxisOption":"2","yZoomedDataMin":0,"yLambda":1}' 
        };

  chart1 = new google.visualization.MotionChart(document.getElementById('hdi1'));
  opts['showSidePanel'] = false;
  opts['state'] = '{"xZoomedIn":false,"iconKeySettings":[],"yZoomedDataMin":0,"yZoomedIn":false,"orderedByY":false,"colorOption":"_UNIQUE_COLOR","yLambda":1,"time":"1954","xZoomedDataMin":-631152000000,"sizeOption":"_UNISIZE","iconType":"BUBBLE","showTrails":false,"playDuration":15000,"yZoomedDataMax":100,"xAxisOption":"2","yAxisOption":"3","uniColorForNonSelected":false,"duration":{"timeUnit":"Y","multiplier":1},"orderedByX":false,"nonSelectedAlpha":0.4,"xLambda":1,"dimensions":{"iconDimensions":["dim0"]},"xZoomedDataMax":1262304000000}';
  chart1.draw(view, opts);
  
  chart2 = new google.visualization.MotionChart(document.getElementById('hdi2'));
  opts['state'] = '{"iconType":"VBAR","duration":{"multiplier":1,"timeUnit":"Y"},"iconKeySettings":[],"xZoomedDataMin":0,"time":"1950","uniColorForNonSelected":false,"nonSelectedAlpha":0.4,"xZoomedIn":false,"sizeOption":"_UNISIZE","xAxisOption":"_ALPHABETICAL","xLambda":1,"yZoomedIn":false,"xZoomedDataMax":6,"showTrails":false,"yZoomedDataMin":0,"yAxisOption":"3","dimensions":{"iconDimensions":["dim0"]},"orderedByX":true,"colorOption":"_UNIQUE_COLOR","yLambda":1,"yZoomedDataMax":100,"playDuration":15000,"orderedByY":false}';
  opts['showChartButtons'] = false;
  opts['showXMetricPicker'] = false;
  chart2.draw(view, opts);

  chart3 = new google.visualization.MotionChart(document.getElementById('hdi3'));
  opts['state'] = '{"dimensions":{"iconDimensions":["dim0"]},"iconType":"BUBBLE","colorOption":"_UNIQUE_COLOR","orderedByY":false,"yAxisOption":"3","xZoomedDataMin":41831805,"orderedByX":false,"time":"1967","duration":{"multiplier":1,"timeUnit":"Y"},"yLambda":1,"playDuration":15000,"yZoomedDataMax":83.212,"uniColorForNonSelected":false,"xZoomedIn":false,"sizeOption":"_UNISIZE","nonSelectedAlpha":0.4,"xLambda":1,"yZoomedIn":false,"xZoomedDataMax":1341335152,"showTrails":true,"iconKeySettings":[],"yZoomedDataMin":31.63176,"xAxisOption":"4"}';
  opts['showXMetricPicker'] = true;
  chart3.draw(view, opts);
  
  chart4 = new google.visualization.MotionChart(document.getElementById('hdi4'));
  opts["state"] = '{"showTrails":false,"yZoomedDataMin":0,"yZoomedIn":false,"orderedByX":false,"yAxisOption":"2","iconType":"LINE","colorOption":"_UNIQUE_COLOR","yLambda":1,"xZoomedIn":false,"xZoomedDataMin":-631152000000,"iconKeySettings":[],"dimensions":{"iconDimensions":["dim0"]},"xAxisOption":"_TIME","time":"2010","playDuration":15000,"yZoomedDataMax":100,"uniColorForNonSelected":false,"duration":{"timeUnit":"Y","multiplier":1},"sizeOption":"_UNISIZE","nonSelectedAlpha":0.4,"xLambda":1,"orderedByY":false,"xZoomedDataMax":1262304000000}';
  chart4.draw(view, opts);
  
  chart5 = new google.visualization.MotionChart(document.getElementById('hdi5'));
  opts["state"] = '{"xZoomedIn":false,"iconKeySettings":[],"yZoomedDataMin":0,"yZoomedIn":false,"orderedByY":false,"colorOption":"_UNIQUE_COLOR","yLambda":1,"time":"2010","xZoomedDataMin":-631152000000,"sizeOption":"_UNISIZE","iconType":"BUBBLE","showTrails":false,"playDuration":15000,"yZoomedDataMax":100,"xAxisOption":"2","yAxisOption":"3","uniColorForNonSelected":false,"duration":{"timeUnit":"Y","multiplier":1},"orderedByX":false,"nonSelectedAlpha":0.4,"xLambda":1,"dimensions":{"iconDimensions":["dim0"]},"xZoomedDataMax":1262304000000}';
  opts['showChartButtons'] = true;
  chart5.draw(view, opts);
}
