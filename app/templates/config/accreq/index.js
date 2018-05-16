updateMenu('#accreq');

var initTable = function () {

    var table = $('#accreq_tbl');

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

        "ajax": '{{ url_for('config.accreqs') }}',

        "columns": [
            {"data": "fname"},
            {"data": "lname"},
            {"data": "email"},
            {"data": "phone"},
            {"data": "granted",
                render: function(data, type, row, meta){
                    if(data === false){
                        //data = '<a href="#" style="margin-right:20px" data-accreqid="'+row['id']+'" onclick="approveAccountRequest(this,true)">Approve</a>';
                        //data += '<a href="#" data-accreqid="'+row['id']+'" onclick="approveAccountRequest(this,false)">Reject</a>';
                        data = '<a class="btn green btn-outline sbold" data-accreqid="'+row['id']+'" data-toggle="modal" href="#approveModel"> Approve </a>';
                        data += '<a class="btn red btn-outline sbold" data-accreqid="'+row['id']+'" data-toggle="modal" href="#rejectModel"> Reject </a>';
                    }
                    return data;
                }
            }
        ]
    });

    // handle datatable custom tools
    $('#sample_3_tools > li > a.tool-action').on('click', function() {
        var action = $(this).attr('data-action');
        oTable.DataTable().button(action).trigger();
    });

    function approveAccountRequest(accreqid,approve){

        $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
        $.ajax({
            url: $SCRIPT_ROOT+'/config/accreq/approveAccount/'+accreqid,
            type: 'POST',
            dataType: "json",
            contentType:"application/json",
            data: JSON.stringify({"approve": approve}),
        })
        .done(function(result) {
            if(result.data===1){
                window.location.href=$SCRIPT_ROOT+'/config/accreq';
            }
        });
        
    };

    $('#approveModel').on('shown.bs.modal', function (event) {
      $btn = $(event.relatedTarget);
      $('#acceptBtn').data('accreqid', $btn.data('accreqid'));
    });

    $('#rejectModel').on('shown.bs.modal', function (event) {
      $btn = $(event.relatedTarget);
      $('#rejectBtn').data('accreqid', $btn.data('accreqid'));
    });

    $('#acceptBtn').on('click', function(event) {
        event.preventDefault();
        approveAccountRequest($(this).data('accreqid'),true);
    });

    $('#rejectBtn').on('click', function(event) {
        event.preventDefault();
        approveAccountRequest($(this).data('accreqid'),false);
    });

}

initTable();