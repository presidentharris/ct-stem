// -------------------------------------------------------------------------------------------- //
// This JS files uses/calls the google JS Chart library. Documentation can be found here:
// https://developers.google.com/chart/interactive/docs/index
// -------------------------------------------------------------------------------------------- //


// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.setOnLoadCallback(doitQ9);

// -------------------------------------------------------------------------------------------- //
// -------------------------------- QUESTION 13 ----------------------------------------------- //
// -------------------------- Explore Cause of Warbler Decline -------------------------------- //
// -------------------------------------------------------------------------------------------- //

function doitQ9() {
  var query = new google.visualization.Query('https://docs.google.com/spreadsheet/pub?key=0Al8qqiDbFFxodEJvSkFPYXJHbS02TzY3b1I1ZTZrOEE');
  query.send(handleQueryResponseQ9);
}

function handleQueryResponseQ9(response) {
  if (response.isError()) {
    alert('Error in query: ' + response.getMessage() + ' ' + response.getDetailedMessage());
    return;
  }

  var data = response.getDataTable();

// -------------------------------------------------------------------------------------------- //
// ------------------------------------ All Data By Site -------------------------------------- //
// -------------------------------------------------------------------------------------------- //
  var view1 = new google.visualization.DataView(data);
  view1.setRows(view1.getFilteredRows([{column: 0, value: "Highland Park"}]));
  view1.setColumns([1,2,3,4,5]);
  all_factors1 = new google.visualization.LineChart(document.getElementById('all_factors_site_1'));
  var all_factors_site1 = {width: '600', height: '350', title: 'Highland Park Data Over Time',
                   chartArea: {width:"75%", height:"80%", left: 0},
                   legend: {position: 'right', alignment: 'center'} }
  all_factors1.draw(view1, all_factors_site1);

  var view2 = new google.visualization.DataView(data);
  view2.setRows(view2.getFilteredRows([{column: 0, value: "Morton Grove"}]));
  view2.setColumns([1,2,3,4,5]);
  all_factors2 = new google.visualization.LineChart(document.getElementById('all_factors_site_2'));
  var all_factors_site2 = {width: '600', height: '350', title: 'Morton Grove Data Over Time',
                   chartArea: {width:"75%", height:"80%", left: 0},
                   legend: {position: 'right', alignment: 'center'} }
  all_factors2.draw(view2, all_factors_site2);

  var view3 = new google.visualization.DataView(data);
  view3.setRows(view3.getFilteredRows([{column: 0, value: "Elmhurst"}]));
  view3.setColumns([1,2,3,4,5]);
  all_factors3 = new google.visualization.LineChart(document.getElementById('all_factors_site_3'));
  var all_factors_site3 = { width: '600', height: '350', title: 'Elmhurst Data Over Time',
                   chartArea: {width:"75%", height:"80%", left: 0},
                   legend: {position: 'right', alignment: 'center'} }
  all_factors3.draw(view3, all_factors_site3);

  var view4 = new google.visualization.DataView(data);
  view4.setRows(view4.getFilteredRows([{column: 0, value: "Oak Lawn"}]));
  view4.setColumns([1,2,3,4,5]);
  all_factors4 = new google.visualization.LineChart(document.getElementById('all_factors_site_4'));
  var all_factors_site4 = { width: '600', height: '350', title: 'Oak Lawn Data Over Time',
                   chartArea: {width:"75%", height:"80%", left: 0},
                   legend: {position: 'right', alignment: 'center'} }
  all_factors4.draw(view4, all_factors_site4);

  var view5 = new google.visualization.DataView(data);
  view5.setRows(view5.getFilteredRows([{column: 0, value: "Englewood"}]));
  view5.setColumns([1,2,3,4,5]);
  all_factors5 = new google.visualization.LineChart(document.getElementById('all_factors_site_5'));
  var all_factors_site5 = { width: '600', height: '350', title: 'Englewood Data Over Time',
                   chartArea: {width:"75%", height:"80%", left: 0},
                   legend: {position: 'right', alignment: 'center'} }
  all_factors5.draw(view5, all_factors_site5);

}

