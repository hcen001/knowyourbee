updateMenu('#partners');

// Set the "bootstrap" theme as the default theme for all Select2
// widgets.
//
// @see https://github.com/select2/select2/issues/2927
$.fn.select2.defaults.set("theme", "bootstrap");

var initTable = function () {

    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};

    var table = $('#partners_tbl');

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

        buttons: [
            { extend: 'print', className: 'btn dark btn-outline' },
            { extend: 'copy', className: 'btn red btn-outline' },
            { extend: 'pdf', className: 'btn green btn-outline' },
            { extend: 'excel', className: 'btn yellow btn-outline ' },
            { extend: 'csv', className: 'btn purple btn-outline ' },
            { extend: 'colvis', className: 'btn dark btn-outline', text: 'Columns'}
        ],

        // setup responsive extension: http://datatables.net/extensions/responsive/
        responsive: true,

        "order": [
            [5, 'desc']
        ],

        "lengthMenu": [
            [5, 10, 15, 20, -1],
            [5, 10, 15, 20, "All"] // change per page values here
        ],
        // set the initial value
        "pageLength": 15,

        "ajax": $SCRIPT_ROOT+'/config/partners/list',

        "columns": [
            {"data": "name", "width": "20%"},
            {"data": "email", "width": "10%"},
            {"data": "phone", "width": "10%"},
            {"data": "institution"},
            {"data": "active", "width": "15%",
                render: function(data, type, row, meta){
                    if (data) {
                        return '<a class="btn red btn-outline sbold" data-partner-id="'+row['id']+'" data-toggle="modal" href="#deactivate"> Deactivate </a>';
                    };
                    return '<a class="btn green btn-outline sbold" data-partner-id="'+row['id']+'" data-toggle="modal" href="#reactivate"> Reactivate </a>';
                }
            },
            {"data": "added_date", "visible": false, "searchable": false}
        ],
        "dom": 'flrtipB'
    });

    // handle datatable custom tools
    $('#sample_3_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });

    function updatePartner(partner_id, action){

        $.ajax({
            url: $SCRIPT_ROOT+'/config/partners/update_status',
            type: 'POST',
            dataType: "json",
            contentType:"application/json",
            data: JSON.stringify({"partner_id": partner_id, "action": action}),
        })
        .done(function(result) {
            window.location.href=$SCRIPT_ROOT+'/config/partners';
        });

    };

    $('#deactivate').on('shown.bs.modal', function (event) {
        btn = $(event.relatedTarget);
        $('#deactivateBtn').data('partner_id', btn.data('partner-id'));
        $('#deactivateBtn').data('action', 'deactivate');
    });

    $('#deactivateBtn').on('click', function(event) {
        event.preventDefault();
        updatePartner($(this).data('partner_id'), $(this).data('action'));
    });

    $('#reactivate').on('shown.bs.modal', function (event) {
        btn = $(event.relatedTarget);
        $('#reactivateBtn').data('partner_id', btn.data('partner-id'));
        $('#reactivateBtn').data('action', 'reactivate');
    });

    $('#reactivateBtn').on('click', function(event) {
        event.preventDefault();
        updatePartner($(this).data('partner_id'), $(this).data('action'));
    });

};

initTable();

$("#partners_tbl_wrapper > .dt-buttons").appendTo("div.table-toolbar > .row > .col-md-6:last");
