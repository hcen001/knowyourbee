updateMenu('#packages');

var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

var create_select2 = function (element, placeholder) {
    $(element).select2({
        allowClear: true,
        placeholder: placeholder,
        width: null
    });
};

var deactivate_select2 = function (element) {
    $(element).prop("disabled", true);
    $(element).html('').select2();
};

var update_datepicker = function (datepicker, value) {
    var date = value.split('/');
    var month = months.indexOf(date[1]);
    $(datepicker).datepicker('update', new Date(date[2], month, date[0]));
    $(datepicker).prop("disabled", false);
};

var update_datepicker_startDate = function (datepicker, value) {
    var start_date = new Date(value);
    start_date.setDate(start_date.getDate() + 1);
    $(datepicker).datepicker('setStartDate', start_date);
};

jQuery(document).ready(function(){
    create_select2($("#partner_id"), "Select the partner");
    create_select2($("#location_id"), "Select the storage location");
    create_select2($("#sender_id"), "Select the person who sent");
    create_select2($("#receiver_id"), "Select the person who received");
    create_select2($("#courier_id"), "Select a courier");

    if (jQuery().datepicker) {
        $('#date_sent, #date_received').datepicker({
            rtl: App.isRTL(),
            orientation: "left",
            autoclose: true,
            format: "dd/MM/yyyy"
        }).on('changeDate', function(ev){
            if (ev.target.id == "date_sent") {
                $("#date_received").prop("disabled", false);
                $("#date_received").datepicker("update", "");
                $("#date_received").datepicker("setStartDate", ev.target.value)
            }
            $(this).valid();
        });
    }

    $("#date_sent").datepicker('show');
    $("#date_sent").datepicker('hide');
    $("#date_received").datepicker('show');
    $("#date_received").datepicker('hide');
    $("#date_received").datepicker("setStartDate", $("#date_sent").datepicker("getDate"));

});