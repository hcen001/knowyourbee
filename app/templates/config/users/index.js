updateMenu('#admin', '#users');

// Set the "bootstrap" theme as the default theme for all Select2
// widgets.
//
// @see https://github.com/select2/select2/issues/2927
$.fn.select2.defaults.set("theme", "bootstrap");

var initTable = function () {

    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};

    var table = $('#users_tbl');

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

        "ajax": $SCRIPT_ROOT+'/config/users/list',

        "columns": [
            {"data": "name", "width": "10%"},
            {"data": "email", "width": "10%",
                render: function(data, type, row, meta){
                    return '<a href="mailto:'+data+'">'+data+'</a>'
                }
            },
            {"data": "role", "width": "20%",
                render: function(data, type, row, meta) {
                    var roles = '';
                    roles += '<span class="label label-info" >'+data+'</span>   ';
                    return roles;
                }
            },
            {"data": "authenticated", "width": "10%",
                render: function(data, type, row, meta){
                    if (data) {
                        return '<a class="btn red btn-outline sbold" data-user-id="'+row['id']+'" data-toggle="modal" href="#logout"> Log out </a>';
                    };
                    return '<span class="label label-info" >Not authenticated</span>';
                }
            },
            {"data": "active", "width": "10%",
                render: function(data, type, row, meta){
                    if (data) {
                        return '<a class="btn red btn-outline sbold" data-user-id="'+row['id']+'" data-toggle="modal" href="#deactivate"> Deactivate </a>';
                    };
                    return '<a class="btn green btn-outline sbold" data-user-id="'+row['id']+'" data-toggle="modal" href="#reactivate"> Reactivate </a>';
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

    function updateUser(user_id, action){

        $.ajax({
            url: $SCRIPT_ROOT+'/config/users/update_status',
            type: 'POST',
            dataType: "json",
            contentType:"application/json",
            data: JSON.stringify({"user_id": user_id, "action": action}),
        })
        .done(function(result) {
            window.location.href=$SCRIPT_ROOT+'/config/users';
        });

    };

    $('#deactivate').on('shown.bs.modal', function (event) {
        btn = $(event.relatedTarget);
        $('#deactivateBtn').data('user_id', btn.data('user-id'));
        $('#deactivateBtn').data('action', 'deactivate');
    });

    $('#deactivateBtn').on('click', function(event) {
        event.preventDefault();
        updateUser($(this).data('user_id'), $(this).data('action'));
    });

    $('#reactivate').on('shown.bs.modal', function (event) {
        btn = $(event.relatedTarget);
        $('#reactivateBtn').data('user_id', btn.data('user-id'));
        $('#reactivateBtn').data('action', 'reactivate');
    });

    $('#reactivateBtn').on('click', function(event) {
        event.preventDefault();
        updateUser($(this).data('user_id'), $(this).data('action'));
    });

    $('#logout').on('shown.bs.modal', function (event) {
        btn = $(event.relatedTarget);
        $('#logoutBtn').data('user_id', btn.data('user-id'));
        $('#logoutBtn').data('action', 'logout');
    });

    $('#logoutBtn').on('click', function(event) {
        event.preventDefault();
        updateUser($(this).data('user_id'), $(this).data('action'));
    });

}

initTable();

$(".select2, .select2-multiple").select2({
    placeholder: "Select the user role(s)",
    allowCleart: true,
    width: null
});

$("#users_tbl_wrapper > .dt-buttons").appendTo("div.table-toolbar > .row > .col-md-6:last");
