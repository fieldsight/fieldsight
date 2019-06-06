// Basic DataTable
$(function(){
	$('#basicExample').DataTable({
		"scrollX": "1000px",
		"scrollCollapse": true,
		'iDisplayLength': 3,
		
	});
});

$(function(){
	$('#siteinfo_table').DataTable({
		"scrollY": "300px",
		"scrollCollapse": true,
		"paging": false,
		'iDisplayLength': 3,
		
	});
});
$(function(){
	$('#paging7_table').DataTable({
		"scrollX": true,
		"scrollCollapse": true,
		"paging": true,
		"info": false,
		'iDisplayLength': 7,
		"language": {
            "lengthMenu": "Show _MENU_ Regions",
        }
		
	});
});
$(function(){
	$('#no_paging_table').DataTable({
		"scrollX": true,
		"scrollCollapse": true,
		"paging": false,
		"lengthChange": false,
		// "searching": false,
		"info":false,
		'iDisplayLength': 7,
		
		
	});
});
$(function(){
	$('#substage_table').DataTable({
		"scrollX": true,
		"scrollCollapse": true,
		"paging": false,
		'iDisplayLength': 6,
		
	});
});

$(function(){
	$('#substage1_table').DataTable({
		"scrollX": true,
		"scrollCollapse": true,
		"paging": false,
		'iDisplayLength': 6,
		
	});
});
$(function(){
	$('#substage2_table').DataTable({
		"scrollX": true,
		"scrollCollapse": true,
		"paging": false,
		'iDisplayLength': 6,
		
	});
});
$(function(){
	$('#manage_table').DataTable({
		"scrollX": true,
		"scrollCollapse": true,
		"paging": true,
		'iDisplayLength': 6,
		
	});
});
$(function(){
	$('#survey_table').DataTable({
		"scrollX": true,
		"scrollCollapse": true,
		"paging": true,
		'iDisplayLength': 6,
		
	});
});
$(function(){
	$('#general_table').DataTable({
		"scrollX": true,
		"scrollCollapse": true,
		"paging": true,
		'iDisplayLength': 6,
		
	});
});
// Vertical Scroll
$(function(){
	$('#scrollVertical').DataTable({
		"scrollY": "200px",
		"scrollCollapse": true,
		"paging": false,
		'iDisplayLength': 3,
	});
});


// Row Selection
$(function(){
	$('#rowSelection').DataTable({
		'iDisplayLength': 3,
	});
	var table = $('#rowSelection').DataTable();

	$('#rowSelection tbody').on( 'click', 'tr', function () {
		$(this).toggleClass('selected');
	});

	$('#button').on('click', function () {
		alert( table.rows('.selected').data().length +' row(s) selected' );
	});
});


// Highlighting rows and columns
$(function(){
	$('#highlightRowColumn').DataTable({
		'iDisplayLength': 3,
	});
	var table = $('#highlightRowColumn').DataTable();  
	$('#highlightRowColumn tbody').on('mouseenter', 'td', function (){
		var colIdx = table.cell(this).index().column;
		$(table.cells().nodes()).removeClass('highlight');
		$(table.column(colIdx).nodes()).addClass('highlight');
	});
});


// Using API in callbacks
$(function(){
  $('#apiCallbacks').DataTable({
  	'iDisplayLength': 3,
    "initComplete": function(){
      var api = this.api();
      api.$('td').on('click', function(){
        api.search(this.innerHTML).draw();
      });
    }
  });
});


// Fixed Header
$(document).ready(function(){
	var table = $('#fixedHeader').DataTable({
	  fixedHeader: true,
	  'iDisplayLength': 3,
	});
});