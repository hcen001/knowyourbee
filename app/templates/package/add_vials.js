updateMenu('#packages');

$(".button-cancel").click(function(e){
    e.preventDefault();
    var choice = confirm("Are you sure you want to cancel? You will lose all data that has not been saved");
    if (choice) {
        window.history.go(-1);
    }
    return false;
});

var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

var create_select2 = function (element, placeholder) {
    $(element).select2({
        allowClear: true,
        placeholder: placeholder,
        width: null
    });
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

var copy_specimen_data = function (element, last_specimen) {
    $(element).find("input[name*='body_part']").val(last_specimen["body_part"]);
    $(element).find("input[name*='freezer']").val(last_specimen["freezer"]);
    $(element).find("input[name*='box']").val(last_specimen["box"]);
    $(element).find("input[value='"+last_specimen["measurement"]+"']").prop('checked', true);
    $(element).find("textarea[name*='comments']").val(last_specimen["comments"]);
};

var copy_previous_specimen = function(element) {
    var repeater = $(element.offsetParent()).repeaterVal();
    var samples = repeater["samples"];
    var specimens = samples[samples.length-1]["specimens"];
    if (specimens.length > 1) {
        var last_specimen = specimens[specimens.length-2];

        update_datepicker($(element).find("input[name*='date_collected']"), last_specimen["date_collected"]);
        var start_date = $(element).closest("div.mt-repeater-item").prev("div.mt-repeater-item").find("input[name*='date_collected']").datepicker('getStartDate');
        update_datepicker_startDate($(element).find("input[name*='date_collected']"), start_date);
        copy_specimen_data(element, last_specimen);
    };
};

var copy_country = function(element, id) {
    $(element).find("select[name*='country_id']").val(id).trigger("change");
};

var copy_previous_vial = function(element) {
    var repeater = $(element.parent()).repeaterVal();
    var add_specimen_button = $(element).find(".mt-repeater-add");

    var vials = repeater['samples'];
    if (vials.length > 1) {
        var last_vial = vials[vials.length-2];

        $(element).find("input[name*='sender_source_id']").val(last_vial['sender_source_id']);
        $(element).find("input[name*='latitude']").val(last_vial['latitude']);
        $(element).find("input[name*='longitude']").val(last_vial['longitude']);
        $(element).find("input[name*='additional_gps_info']").val(last_vial['additional_gps_info']);
        $(element).find("input[name*='locality']").val(last_vial['locality']);
        $(element).find("input[name*='hive']").val(last_vial['hive']);
        $(element).find("input[name*='additional_info']").val(last_vial['additional_info']);

        // $(element).find("input[name*='freezer']").filter(function(){
        //     return !this.name.match(/specimens/);
        // }).val(last_vial['freezer']);
        // $(element).find("input[name*='shelf']").filter(function(){
        //     return !this.name.match(/specimens/);
        // }).val(last_vial['shelf']);
        // $(element).find("input[name*='box']").filter(function(){
        //     return !this.name.match(/specimens/);
        // }).val(last_vial['box']);
        // $(element).find("textarea[name*='comments']").val(last_vial['comments']);

        $(element).find("input[value='"+last_vial["caste"]+"']").prop('checked', true);
        $(element).find("input[value='"+last_vial["gender"]+"']").prop('checked', true);
        $(element).find("input[value='"+last_vial["stage"]+"']").prop('checked', true);
        $(element).find("input[value='"+last_vial["sample_quality"]+"']").prop('checked', true);

        $(element).find("select[name*='collector']").val(last_vial["collector"]).trigger("change.select2");
        $(element).find("select[name*='processor']").val(last_vial["processor"]).trigger("change.select2");
        $(element).find("select[name*='process_location']").val(last_vial["process_location"]).trigger("change");

        copy_country(element, last_vial["country_id"]);

        $(element).find("select[name*='genus_id']").val(last_vial["genus_id"]).trigger("change.select2");
        $(element).find("select[name*='species_id']").val(last_vial["species_id"]).trigger("change.select2");
        $(element).find("select[name*='subspecies_id']").val(last_vial["subspecies_id"]).trigger("change.select2");
        $(element).find("select[name*='lineage_id']").val(last_vial["lineage_id"]).trigger("change.select2");

        var start_date = $(element).prev().find("input[name*='date_received']").datepicker('getStartDate');
        // update_datepicker_startDate($(element).find("input[name*='date_received']"), start_date);

        update_datepicker_startDate($(element).find("input[name*='date_collected']"), start_date);
        // $(element).find("input[name*='date_collected']").prop("disabled", false);
        update_datepicker($(element).find("input[name*='sample_date_received']"), last_vial["sample_date_received"]);
        update_datepicker($(element).find("input[name*='sample_date_sampled']"), last_vial["sample_date_sampled"]);

        if (last_vial['specimens'] === undefined) {
            return;
        }

        var last_specimen = last_vial['specimens'][0];
        update_datepicker($(element).find("input[name*='date_collected']"), last_specimen['date_collected']);

        $(element).find("input[name*='body_part']").val(last_specimen["body_part"]);
        $(element).find("div.inner-repeater").find("input[name*='specimen_freezer']").val(last_specimen["specimen_freezer"]);
        $(element).find("div.inner-repeater").find("input[name*='specimen_box']").val(last_specimen["specimen_box"]);
        $(element).find("div.inner-repeater").find("input[name*='dna_freezer']").val(last_specimen["dna_freezer"]);
        $(element).find("div.inner-repeater").find("input[name*='dna_box']").val(last_specimen["dna_box"]);
        $(element).find("input[value='"+last_specimen["measurement"]+"']").prop('checked', true);
    };

};

var FormRepeater = function () {

    return {
        //main function to initiate the module
        init: function () {
            $('.form-body').repeater({
                show: function () {
                    $(this).slideDown();
                    var current_item = $(this);

                    create_select2($("select[name*='collector']"), "Select a collector");
                    create_select2($("select[name*='processor']"), "Select a processor");
                    create_select2($("select[name*='process_location']"), "Process location");
                    create_select2($("select[name*='country_id']"), "Country of origin");

                    create_select2($("select[name*='genus_id']"), "Select genus");
                    create_select2($("select[name*='species_id']"), "Select species");
                    create_select2($("select[name*='subspecies_id']"), "Select subspecies");
                    create_select2($("select[name*='lineage_id']"), "Select lineage");
                    create_select2($("select[name*='caste_id']"), "Select caste");
                    create_select2($("select[name*='development_stage_id']"), "Select dev stage");

                    $("input[name*='sample_date_sampled']").datepicker({
                        rtl: App.isRTL(),
                        orientation: "left",
                        autoclose: true,
                        format: "dd/MM/yyyy"
                    }).on('changeDate', function(ev){
                        // var sample_date = $(ev.target).closest("div.col-md-2").next("div.col-md-2").find("input[name*='sample_date_received']");
                        // $(sample_date).val("");
                        // $(sample_date).prop("disabled", false);
                        // $(sample_date).datepicker("setStartDate", ev.target.value)
                    });
                    $("input[name*='sample_date_received']").datepicker({
                        rtl: App.isRTL(),
                        orientation: "left",
                        autoclose: true,
                        format: "dd/MM/yyyy"
                    }).on('changeDate', function(ev){
                        var dna_collection_date = $(ev.target).closest("div.mt-repeater-item").find("input[name*='date_collected']");
                        $(dna_collection_date).val("");
                        $(dna_collection_date).prop("disabled", false);
                        $(dna_collection_date).datepicker("setStartDate", ev.target.value)
                    });

                    $("input[name*='latitude']").inputmask({
                        "mask": "(bc|c)|(\\90)\˚ (ic|c)|(60)\' [i]c.[i]c\" N|S",
                        "autoUnmask": true,
                        "greedy": false,
                        "placeholder": "",
                        "skipOptionalCharacter": " ",
                        "definitions": {
                            "i": {
                                validator: "[0-5]" //t
                            },
                            "b": {
                                validator: "[0-8]" //8
                            },
                            "c": {
                                validator: "[0-9]" //7
                            },
                            "N": {
                                validator: "n|N",
                                casing: "upper"
                            },
                            "S": {
                                validator: "s|S",
                                casing: "upper"
                            }
                        }
                    });
                    $("input[name*='longitude']").inputmask({
                        "mask": "(1r7|77)|(180)\˚ [t]7|(60)\' [t]7.[7]7\" E|W",
                        "autoUnmask": true,
                        "greedy": false,
                        "placeholder": "",
                        "skipOptionalCharacter": " ",
                        "definitions": {
                            "r": {
                                validator: "[0-7]"
                            },
                            "t": {
                                validator: "[0-5]"
                            },
                            "7": {
                                validator: "[0-9]"
                            },
                            "E": {
                                validator: "e|E",
                                casing: "upper"
                            },
                            "W": {
                                validator: "w|W",
                                casing: "upper"
                            }
                        },
                    });

                    // $(this).find("input[name*='sample_date_received']").prop("disabled", true);
                    // $(this).find("input[name*='date_collected']").prop("disabled", true);

                    $("input[name*='collected']").datepicker({
                        rtl: App.isRTL(),
                        orientation: "left",
                        autoclose: true,
                        format: "dd/MM/yyyy"
                    });
                    create_select2($("select[name*='measurement_id']"), "DNA measurement");
                    copy_previous_vial($(this));
                },

                hide: function (deleteElement) {
                    $(this).slideUp(deleteElement);
                },

                repeaters: [
                    {
                        selector: '.inner-repeater',
                        show: function () {
                            $(this).slideDown();
                            $(this).find("input[name*='date_collected']").datepicker({
                                rtl: App.isRTL(),
                                orientation: "left",
                                autoclose: true,
                                format: "dd/MM/yyyy"
                            });

                            copy_previous_specimen($(this));
                        },

                        hide: function (deleteElement) {
                            $(this).slideUp(deleteElement);
                        }
                    }
                ]

            });
        }

    };

}();

jQuery(document).ready(function() {
    FormRepeater.init();

    create_select2($("#collector"), "Select a collector");
    create_select2($("#processor"), "Select a processor");
    create_select2($("#process_location"), "Process location");
    create_select2($("#country_id"), "Country of origin");
    create_select2($("#genus_id"), "Select genus");
    create_select2($("#species_id"), "Select species");
    create_select2($("#subspecies_id"), "Select subspecies");
    create_select2($("#lineage_id"), "Select lineage");
    create_select2($("#caste_id"), "Select caste");
    create_select2($("#development_stage_id"), "Select dev stage");
    create_select2($("#measurement_id"), "DNA measurement");

    $('#sample_date_sampled, #sample_date_received, #date_collected').datepicker({
        rtl: App.isRTL(),
        orientation: "left",
        autoclose: true,
        format: "dd/MM/yyyy"
    }).on('changeDate', function(ev){
        if (ev.target.name.includes("sample_date_sampled")) {
            var sample_date = $(ev.target).closest("div.col-md-2").next("div.col-md-2").find("input[name*='sample_date_received']");
            $(sample_date).val("");
            $(sample_date).prop("disabled", false);
            $(sample_date).datepicker("setStartDate", ev.target.value);
        }
        if (ev.target.name.includes("sample_date_received")) {
            var dna_collection_date = $(ev.target).closest("div.mt-repeater-item").find("input[name*='date_collected']");
            $(dna_collection_date).val("");
            $(dna_collection_date).prop("disabled", false);
            $(dna_collection_date).datepicker("setStartDate", ev.target.value);
        }
    });

    // $("input[name*='sample_date_received']").prop("disabled", true);
    // $("input[name*='date_collected']").prop("disabled", true);

    $("input[name*='latitude']").inputmask({
        "mask": "(bc|c)|(\\90)\˚ (ic|c)|(60)\' [i]c.[i]c\" N|S",
        "autoUnmask": true,
        "greedy": false,
        "placeholder": "",
        "skipOptionalCharacter": " ",
        "definitions": {
            "i": {
                validator: "[0-5]" //t
            },
            "b": {
                validator: "[0-8]" //8
            },
            "c": {
                validator: "[0-9]" //7
            },
            "N": {
                validator: "n|N",
                casing: "upper"
            },
            "S": {
                validator: "s|S",
                casing: "upper"
            }
        }
    });
    $("input[name*='longitude']").inputmask({
        "mask": "(1r7|77)|(180)\˚ [t]7|(60)\' [t]7.[7]7\" E|W",
        "autoUnmask": true,
        "greedy": false,
        "placeholder": "",
        "skipOptionalCharacter": " ",
        "definitions": {
            "r": {
                validator: "[0-7]"
            },
            "t": {
                validator: "[0-5]"
            },
            "7": {
                validator: "[0-9]"
            },
            "E": {
                validator: "e|E",
                casing: "upper"
            },
            "W": {
                validator: "w|W",
                casing: "upper"
            }
        },
    });

});