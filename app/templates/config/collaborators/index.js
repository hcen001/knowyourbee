updateMenu('#admin', '#collaborators');

// Set the "bootstrap" theme as the default theme for all Select2
// widgets.
//
// @see https://github.com/select2/select2/issues/2927
$.fn.select2.defaults.set("theme", "bootstrap");

var initTable = function () {

    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};

    var table = $('#collaborators_tbl');

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
            [2, 'desc']
        ],

        "lengthMenu": [
            [5, 10, 15, 20, -1],
            [5, 10, 15, 20, "All"] // change per page values here
        ],
        // set the initial value
        "pageLength": 15,

        "ajax": $SCRIPT_ROOT+'/config/collaborators/list',

        "columns": [
            {"data": "name", "width": "20%"},
            {"data": "email", "width": "10%",
                render: function(data, type, row, meta){
                    return '<a href="mailto:'+data+'">'+data+'</a>'
                }
            },
            {"data": "phone", "width": "10%"},
            {"data": "role", "width": "20%",
                render: function(data, type, row, meta) {
                    var roles = '';
                    if (data.indexOf('S') >= 0) {
                        // roles += 'Sender, '
                        roles += '<span class="label label-info" >Sender</span>         ';
                    }
                    if (data.indexOf('C') >= 0) {
                        // roles += 'Collector, '
                        roles += '<span class="label label-default" >Collector</span>         ';
                    }
                    if (data.indexOf('P') >= 0) {
                        // roles += 'Processor, '
                        roles += '<span class="label label-primary" >Processor</span>         ';
                    }
                    if (data.indexOf('R') >= 0) {
                        // roles += 'Receiver, '
                        roles += '<span class="label label-success" >Receiver</span>         ';
                    }
                    return roles;
                    // return roles.replace(/,\s*$/, "");
                }
            },
            {"data": "active", "width": "20%",
                render: function(data, type, row, meta){
                    var a = '<a class="btn blue btn-outline sbold btn-delete"> Edit </a>';
                    if (data) {
                        var id = row['id'];
                        return a+'<a class="btn red btn-outline sbold" data-collaborator-id="'+row['id']+'" data-toggle="modal" href="#deactivate"> Deactivate </a>';
                    };
                    return a+'<a class="btn green btn-outline sbold" data-collaborator-id="'+row['id']+'" data-toggle="modal" href="#reactivate"> Reactivate </a>';
                }
            },
            {"data": "added_date", "visible": false, "searchable": false}
        ],
        "dom": 'flrtipB'
    });

    $('#collaborators_tbl tbody').on('click', '.btn-delete', function (){
       var $row = $(this).closest('tr');
       var data =  $('#collaborators_tbl').DataTable().row($row).data();
       var name = data['name'].split(" ");
       $("#collaborator_id").val(data["id"]);
       $("#first_name").val(name[0]);
       $("#last_name").val(name[1]);
       $("#email").val(data["email"]);
       $("#phone").val(data["phone"]);
       $("#roles").val(data["role"]).trigger("change");
       $("#add_collaborator").attr("action", $SCRIPT_ROOT+'/config/collaborators/update');
       $("#new_collaborator").modal('show');
    });

    // handle datatable custom tools
    $('#sample_3_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });

    function updateCollaborator(collaborator_id, action){

        $.ajax({
            url: $SCRIPT_ROOT+'/config/collaborators/update_status',
            type: 'POST',
            dataType: "json",
            contentType:"application/json",
            data: JSON.stringify({"collaborator_id": collaborator_id, "action": action}),
        })
        .done(function(result) {
            window.location.href=$SCRIPT_ROOT+'/config/collaborators';
        });

    };

    $('#deactivate').on('shown.bs.modal', function (event) {
        btn = $(event.relatedTarget);
        $('#deactivateBtn').data('collaborator_id', btn.data('collaborator-id'));
        $('#deactivateBtn').data('action', 'deactivate');
    });

    $('#deactivateBtn').on('click', function(event) {
        event.preventDefault();
        updateCollaborator($(this).data('collaborator_id'), $(this).data('action'));
    });

    $('#reactivate').on('shown.bs.modal', function (event) {
        btn = $(event.relatedTarget);
        $('#reactivateBtn').data('collaborator_id', btn.data('collaborator-id'));
        $('#reactivateBtn').data('action', 'reactivate');
    });

    $('#reactivateBtn').on('click', function(event) {
        event.preventDefault();
        updateCollaborator($(this).data('collaborator_id'), $(this).data('action'));
    });

}

initTable();

$('#new_collaborator').on('hidden.bs.modal', function () {
    $("#first_name").val("");
    $("#last_name").val("");
    $("#email").val("");
    $("#phone").val("");
    $("#collaborator_id").val("");
    $("#roles").val("").trigger("change");
    $("#add_collaborator").attr("action", $SCRIPT_ROOT+'/config/collaborators');
});

$(".select2, .select2-multiple").select2({
    placeholder: "Select the collaborator role(s)",
    allowClear: true,
    width: null
});

$("#collaborators_tbl_wrapper > .dt-buttons").appendTo("div.table-toolbar > .row > .col-md-6:last");
