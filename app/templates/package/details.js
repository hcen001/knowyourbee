updateMenu('#packages');

var initSpecimensTable = function () {

    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};

    var table = $('#specimens_tbl');

    var oTable = table.dataTable({

        // Internationalisation. For more info refer to http://datatables.net/manual/i18n
        "language": {
            "aria": {
                "sortAscending": ": activate to sort column ascending",
                "sortDescending": ": activate to sort column descending"
            },
            "emptyTable": "No data available in table",
            "info": "Showing _START_ to _END_ of _TOTAL_ entries",
            "infoEmpty": "No entries found",
            "infoFiltered": "(filtered1 from _MAX_ total entries)",
            "lengthMenu": "_MENU_ entries",
            "search": "Search:",
            "zeroRecords": "No matching records found"
        },

        // Or you can use remote translation file
        //"language": {
        //   url: '//cdn.datatables.net/plug-ins/3cfcc339e89/i18n/Portuguese.json'
        //},

        // setup buttons extension: http://datatables.net/extensions/buttons/
        buttons: [
            { extend: 'print', className: 'btn dark btn-outline' },
            { extend: 'copyHtml5', className: 'btn red btn-outline' },
            { extend: 'pdfHtml5', className: 'btn green btn-outline' },
            { extend: 'excelHtml5', className: 'btn yellow btn-outline ' },
            { extend: 'csvHtml5', className: 'btn purple btn-outline ' },
            { extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
        ],

        // scroller extension: http://datatables.net/extensions/scroller/
        scrollY:        300,
        deferRender:    true,
        scroller:       true,
        scrollX:        true,
        scrollCollapse: true,

        stateSave:      true,

        "paging":         true,
        "info":           true,

        "order": [
            [0, 'asc']
        ],

        "lengthMenu": [
            [50, 100, 200, -1],
            [50, 100, 200, "All"] // change per page values here
        ],
        // set the initial value
        "pageLength": 50,

        "ajax": $SCRIPT_ROOT+"/packages/details/"+{{package_id}}+"/all_specimens",

        "columns": [
            {"data": "collection_sample_id"},
            {"data": "cooperator"},
            {"data": "number_specimens"},
            {"data": "date_received"},
            {"data": "country"},
            // {"data": "state"},
            {"data": "latitude"},
            {"data": "longitude"},
            {"data": "genus"},
            {"data": "species"},
            {"data": "subspecies"},
            {"data": "lineage"},
            {"data": "gender"},
            {"data": "freezer"},
            {"data": "box"},
            {"data": "dna"},
            {"data": "body_part"},
            {"data": "dna_freezer"},
            {"data": "dna_box"},
            {"data": "comments"}
        ],

        "dom": "Brfti",

        // "dom": "<'row'<'col-md-6'l><'col-md-6'f>r><'table-scrollable't><'row'<'col-md-6'i><'col-md-6'p>>", // horizobtal scrollable datatable

        // Uncomment below line("dom" parameter) to fix the dropdown overflow issue in the datatable cells. The default datatable layout
        // setup uses scrollable div(table-scrollable) with overflow:auto to enable vertical scroll(see: assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.js).
        // So when dropdowns used the scrollable div should be removed.
        // "dom": "<'row'<'col-md-6'B><'col-md-6'f>r>t<'row'<'col-md-6'i><'col-md-6'p>>"
    });
};

jQuery(document).ready(function() {
    initSpecimensTable();
    $("#specimens_tbl_wrapper > .dt-buttons").appendTo("div.table-toolbar > .row > .col-md-6:last");
});