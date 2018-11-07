updateMenu('#packages');

$.validator.addMethod("unique", function(value, element) {
    var parentForm = $(element).closest('form');
    var timeRepeated = 0;
    if (value != '') {
        $(parentForm.find("[name*='collection_sample_id']")).each(function () {
            if ($(this).val() === value) {
                timeRepeated++;
            }
        });
    }
    return timeRepeated === 1 || timeRepeated === 0;

}, "* Duplicate");

$.validator.addMethod("regex", function(value, element) {

    var regexp = '';
    if ($(element).attr('id') === 'latitude') {
        regexp = '(\\d{1,2})\\s(\\d{1,2})\\s(\\d{1,2}(\\.\\d{1,3})?)\\s[NSns]$';
    } else {
        regexp = '(\\d{1,2})\\s(\\d{1,2})\\s(\\d{1,2}(\\.\\d{1,3})?)\\s[EWew]$';
    };
    var re = new RegExp(regexp);
    return this.optional(element) || re.test(value);

}, "Please check your input.");

var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

$SCRIPT_ROOT = {{ request.script_root|tojson|safe }};

$(".button-cancel").click(function(e){
    e.preventDefault();
    var choice = confirm("Are you sure you want to cancel? You will lose all data that has not been saved");
    if (choice) {
        window.location.href = $SCRIPT_ROOT+"/packages";
    }
    return false;
});

var FormWizard = function () {

    var handleDatePickers = function () {

        if (jQuery().datepicker) {
            $('#date_sent, #date_received').datepicker({
                rtl: App.isRTL(),
                orientation: "left",
                autoclose: true,
                format: "dd/MM/yyyy"
            }).on('changeDate', function(ev){
                if (ev.target.id == "date_sent") {
                    $("#date_received").prop("disabled", false);
                    $("#date_received").datepicker("setStartDate", ev.target.value)
                    $("#date_received").val("");
                    $("#sample_date_received").datepicker("setStartDate", ev.target.value)
                    $("#sample_date_received").val("");
                };
                if (ev.target.id == "date_received") {
                    $("#sample_date_received").datepicker("setDate", ev.target.value)
                };
                $(this).valid();
            });
        }

        $("#date_received").prop("disabled", true);

    };

    var handleSelect2 = function () {
        // Set the "bootstrap" theme as the default theme for all Select2
        // widgets.
        //
        // @see https://github.com/select2/select2/issues/2927
        $.fn.select2.defaults.set("theme", "bootstrap");

        $("#courier_id").select2({
            allowClear: true,
            placeholder: "Select courier",
            width: null
        });

        $("#partner_id").select2({
            allowClear: true,
            placeholder: "Select the partner",
            width: null
        });

        $("#location_id").select2({
            allowClear: true,
            placeholder: "Select the storage location",
            width: null
        });

        $("#sender_id").select2({
            allowClear: true,
            placeholder: "Select the person who sent",
            width: null
        });

        $("#receiver_id").select2({
            allowClear: true,
            placeholder: "Select the person who received",
            width: null
        });

        // copy Bootstrap validation states to Select2 dropdown
        //
        // add .has-waring, .has-error, .has-succes to the Select2 dropdown
        // (was #select2-drop in Select2 v3.x, in Select2 v4 can be selected via
        // body > .select2-container) if _any_ of the opened Select2's parents
        // has one of these forementioned classes (YUCK! ;-))
        $(".select2").on("select2:open", function() {
            if ($(this).parents("[class*='has-']").length) {
                var classNames = $(this).parents("[class*='has-']")[0].className.split(/\s+/);

                for (var i = 0; i < classNames.length; ++i) {
                    if (classNames[i].match("has-")) {
                        $("body > .select2-container").addClass(classNames[i]);
                    }
                }
            }
        });
    }

    return {
        //main function to initiate the module
        init: function () {
            if (!jQuery().bootstrapWizard) {
                return;
            }

            var form = $('#submit_form');
            var error = $('.alert-danger', form);
            var success = $('.alert-success', form);

            form.validate({
                doNotHideMessage: true, //this option enables to show the error/success messages on tab switch.
                errorElement: 'span', //default input error message container
                errorClass: 'help-block help-block-error', // default input error message class
                focusInvalid: false, // do not focus the last invalid input
                rules: {
                    //package metadata
                    package_id: {
                        required: true
                    },
                    date_sent: {
                        required: false
                    },
                    date_received: {
                        required: false
                    },
                    courier_id: {
                        required: false
                    },
                    tracking_number: {
                        required: false,
                        maxlength: 20
                    },
                    partner_id: {
                        required: false
                    },
                    location_id: {
                        required: false
                    },
                    sender_id: {
                        required: false
                    },
                    receiver_id: {
                        required: false
                    },
                    comments: {
                        required: false,
                        maxlength: 512
                    }
                },

                errorPlacement: function (error, element) { // render error placement for each input type
                    if (element.hasClass("select2")) {
                        error.insertAfter(element.next());
                    } else if (element.parent().hasClass("date-picker")) {
                        error.insertAfter(element.parent())
                    } else {
                        error.insertAfter(element); // for other inputs, just perform default behavior
                    }
                },

                invalidHandler: function (event, validator) { //display error alert on form submit
                    success.hide();
                    error.show();
                    App.scrollTo(error, -200);
                },

                highlight: function (element) { // hightlight error inputs
                    $(element)
                        .closest('.form-group').removeClass('has-success').addClass('has-error'); // set error class to the control group
                },

                unhighlight: function (element) { // revert the change done by hightlight
                    $(element)
                        .closest('.form-group').removeClass('has-error'); // set error class to the control group
                },

                success: function (label) {
                    if (label.attr("for") == "gender" || label.attr("for") == "payment[]") { // for checkboxes and radio buttons, no need to show OK icon
                        label
                            .closest('.form-group').removeClass('has-error').addClass('has-success');
                        label.remove(); // remove error label here
                    } else { // display success icon for other inputs
                        label
                            .addClass('valid') // mark the current input as valid and display OK icon
                        .closest('.form-group').removeClass('has-error').addClass('has-success'); // set success class to the control group
                    }
                },

                submitHandler: function (form) {
                    success.show();
                    error.hide();
                    form.submit();
                    //add here some ajax code to submit your form or just call form.submit() if you want to submit the form without ajax
                }

            });

            var displayConfirm = function() {
                var tables = ["vials", "specimens"];
                var items = $('#submit_form').repeaterVal();
                $('#tab3 .form-control-static', form).each(function(){
                    var table = $(this).attr("data-display");
                    if ( tables.includes(table) ) {
                        var tbl = $(this).find("table > tbody");
                        tbl.empty();
                        if (table == "vials") {
                            items['samples'].forEach(function(element){
                                var tr = $('<tr></tr>');
                                tr.append('<td>'+element.sender_source_id+'</td>');
                                tr.append('<td>'+element.sample_date_sampled+'</td>');
                                tr.append('<td>'+element.sample_date_received+'</td>');
                                tr.append('<td>'+element.specimens.length+'</td>');
                                tbl.append(tr);
                            });
                        };
                        if (table == "specimens") {
                            items['samples'].forEach(function(element){
                                element['specimens'].forEach(function(specimen){
                                    var tr = $('<tr></tr>');
                                    tr.append('<td>'+element.sender_source_id+'</td>');
                                    tr.append('<td>'+specimen.collection_sample_id+'</td>');
                                    tr.append('<td>'+specimen.dna+'</td>');
                                    tr.append('<td>'+specimen.date_collected+'</td>');
                                    tbl.append(tr);
                                });
                            });
                        };
                    };
                    if ($(this).attr("data-display") == "number_vials") {
                        $(this).html(items["samples"].length);
                        return;
                    };
                    if ($(this).attr("data-display") == "number_specimens") {
                        var total_specimens = 0;
                        items['samples'].forEach(function(element){
                            total_specimens = total_specimens + element['specimens'].length;
                        });
                        $(this).html(total_specimens);
                        return;
                    };
                    var input = $('[name="'+$(this).attr("data-display")+'"]', form);
                    // console.log(input);
                    if (input.is(":radio")) {
                        input = $('[name="'+$(this).attr("data-display")+'"]:checked', form);
                    }
                    if (input.is(":text") || input.is("textarea")) {
                        $(this).html(input.val());
                    } else if (input.is("select")) {
                        var selected_status = $('#'+$(this).attr("data-display")).select2('data');
                        $(this).html(selected_status[0].text);
                    } else if (input.is(":radio") && input.is(":checked")) {
                        $(this).html(input.attr("data-title"));
                    }
                });
            }

            var handleTitle = function(tab, navigation, index) {
                var total = navigation.find('li').length;
                var current = index + 1;
                // set wizard title
                $('.step-title', $('#form_wizard_1')).text('Step ' + (index + 1) + ' of ' + total);
                // set done steps
                jQuery('li', $('#form_wizard_1')).removeClass("done");
                var li_list = navigation.find('li');
                for (var i = 0; i < index; i++) {
                    jQuery(li_list[i]).addClass("done");
                }

                if (current == 1) {
                    $('#form_wizard_1').find('.button-previous').hide();
                } else {
                    $('#form_wizard_1').find('.button-previous').show();
                }

                if (current >= total) {
                    $('#form_wizard_1').find('.button-next').hide();
                    $('#form_wizard_1').find('.button-submit').show();
                    displayConfirm();
                } else {
                    $('#form_wizard_1').find('.button-next').show();
                    $('#form_wizard_1').find('.button-submit').hide();
                }
                App.scrollTo($('.page-title'));
            }

            // default form wizard
            $('#form_wizard_1').bootstrapWizard({
                'nextSelector': '.button-next',
                'previousSelector': '.button-previous',
                onTabClick: function (tab, navigation, index, clickedIndex) {
                    return false;

                    success.hide();
                    error.hide();
                    if (form.valid() == false) {
                        return false;
                    }

                    handleTitle(tab, navigation, clickedIndex);
                },
                onNext: function (tab, navigation, index) {
                    success.hide();
                    error.hide();

                    if (form.valid() == false) {
                        return false;
                    }

                    handleTitle(tab, navigation, index);
                },
                onPrevious: function (tab, navigation, index) {
                    success.hide();
                    error.hide();

                    handleTitle(tab, navigation, index);
                },
                onTabShow: function (tab, navigation, index) {
                    var total = navigation.find('li').length;
                    var current = index + 1;
                    var $percent = (current / total) * 100;
                    $('#form_wizard_1').find('.progress-bar').css({
                        width: $percent + '%'
                    });
                }
            });

            $('#form_wizard_1').find('.button-previous').hide();
            $('#form_wizard_1 .button-submit').click(function () {
                $(form).submit();
            }).hide();

            //apply validation on select2 dropdown value change, this only needed for chosen dropdown integration.
            $('.select2', form).change(function () {
                form.validate().element($(this)); //revalidate the chosen dropdown value and show error or success message for the input
            });

            handleDatePickers();
            handleSelect2();
        }

    };

}();

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
    $(element).find("input[name*='specimen_freezer']").val(last_specimen["specimen_freezer"]);
    $(element).find("input[name*='specimen_box']").val(last_specimen["specimen_box"]);
    $(element).find("input[name*='dna_freezer']").val(last_specimen["dna_freezer"]);
    $(element).find("input[name*='dna_box']").val(last_specimen["dna_box"]);
    $(element).find("input[name*='wing_box']").val(last_specimen["wing_box"]);
    $(element).find("select[name*='measurement_id']").val(last_specimen["measurement_id"]).trigger("change.select2");
    $(element).find("textarea[name*='comments']").val(last_specimen["comments"]);
};

var copy_previous_specimen = function(element) {
    var repeater = $(element.offsetParent()).repeaterVal();
    var samples = repeater["samples"];
    var specimens = samples[samples.length-1]["specimens"];
    if (specimens.length > 1) {
        var last_specimen = specimens[specimens.length-2];

        var start_date = $(element).closest("div.mt-repeater-item").prev("div.mt-repeater-item").find("input[name*='date_collected']").datepicker('getStartDate');
        update_datepicker_startDate($(element).find("input[name*='date_collected']"), start_date);
        update_datepicker($(element).find("input[name*='date_collected']"), last_specimen["date_collected"]);
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
        $(element).find("input[name*='specimens_in_received_vial']").val(last_vial['specimens_in_received_vial']);

        $(element).find("input[value='"+last_vial["gender"]+"']").prop('checked', true);
        $(element).find("input[value='"+last_vial["sample_quality"]+"']").prop('checked', true);

        $(element).find("select[name*='collector']").val(last_vial["collector"]).trigger("change.select2");
        $(element).find("select[name*='processor']").val(last_vial["processor"]).trigger("change.select2");
        $(element).find("select[name*='process_location']").val(last_vial["process_location"]).trigger("change");

        copy_country(element, last_vial["country_id"]);

        $(element).find("select[name*='genus_id']").val(last_vial["genus_id"]).trigger("change.select2");
        $(element).find("select[name*='species_id']").val(last_vial["species_id"]).trigger("change.select2");
        $(element).find("select[name*='subspecies_id']").val(last_vial["subspecies_id"]).trigger("change.select2");
        $(element).find("select[name*='lineage_id']").val(last_vial["lineage_id"]).trigger("change.select2");
        $(element).find("select[name*='caste_id']").val(last_vial["caste_id"]).trigger("change.select2");
        $(element).find("select[name*='development_stage_id']").val(last_vial["development_stage_id"]).trigger("change.select2");

        var start_date = $(element).prev().find("input[name*='sample_date_received']").datepicker('getStartDate');

        update_datepicker_startDate($(element).find("input[name*='sample_date_received']"), start_date);

        update_datepicker($(element).find("input[name*='sample_date_received']"), last_vial["sample_date_received"]);
        update_datepicker($(element).find("input[name*='sample_date_sampled']"), last_vial["sample_date_sampled"]);


        if (last_vial['specimens'] === undefined) {
            return;
        }

        var last_specimen = last_vial['specimens'][0];
        update_datepicker_startDate($(element).find("input[name*='date_collected']"), start_date);
        update_datepicker($(element).find("input[name*='date_collected']"), last_specimen['date_collected']);

        $(element).find("input[name*='body_part']").val(last_specimen["body_part"]);
        $(element).find("div.inner-repeater").find("input[name*='specimen_freezer']").val(last_specimen["specimen_freezer"]);
        $(element).find("div.inner-repeater").find("input[name*='specimen_box']").val(last_specimen["specimen_box"]);
        $(element).find("div.inner-repeater").find("input[name*='dna_freezer']").val(last_specimen["dna_freezer"]);
        $(element).find("div.inner-repeater").find("input[name*='dna_box']").val(last_specimen["dna_box"]);
        $(element).find("div.inner-repeater").find("input[name*='wing_box']").val(last_specimen["wing_box"]);
        $(element).find("div.inner-repeater").find("select[name*='measurement_id']").val(last_specimen["measurement_id"]).trigger("change.select2");
        $(element).find("div.inner-repeater").find("textarea[name*='comments']").val(last_specimen["comments"]);

    };

};

var deactivate_select2 = function (element) {
    $(element).prop("disabled", true);
    $(element).html('').select2();
};

var FormRepeater = function () {

    return {
        //main function to initiate the module
        init: function () {
            $('#tab2').repeater({
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
                    create_select2($("select[name*='measurement_id']"), "DNA measurement");

                    $("input[name*='collected']").datepicker({
                        rtl: App.isRTL(),
                        orientation: "left",
                        autoclose: true,
                        format: "dd/MM/yyyy"
                    });

                    $("input[name*='sample_date_sampled']").datepicker({
                        rtl: App.isRTL(),
                        orientation: "left",
                        autoclose: true,
                        format: "dd/MM/yyyy",
                        endDate: $("#date_received").datepicker("getDate")
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

                    // $("input[name*='latitude']").inputmask({
                    //     "mask": "(bc|c)|(\\90)\˚ (ic|c)|(60)\' [i]c.[i]c\" N|S",
                    //     "autoUnmask": true,
                    //     "greedy": false,
                    //     "placeholder": "",
                    //     "skipOptionalCharacter": " ",
                    //     "definitions": {
                    //         "i": {
                    //             validator: "[0-5]" //t
                    //         },
                    //         "b": {
                    //             validator: "[0-8]" //8
                    //         },
                    //         "c": {
                    //             validator: "[0-9]" //7
                    //         },
                    //         "N": {
                    //             validator: "n|N",
                    //             casing: "upper"
                    //         },
                    //         "S": {
                    //             validator: "s|S",
                    //             casing: "upper"
                    //         }
                    //     }
                    // });
                    // $("input[name*='longitude']").inputmask({
                    //     "mask": "(1r7|77)|(180)\˚ [t]7|(60)\' [t]7.[7]7\" E|W",
                    //     "autoUnmask": true,
                    //     "greedy": false,
                    //     "placeholder": "",
                    //     "skipOptionalCharacter": " ",
                    //     "definitions": {
                    //         "r": {
                    //             validator: "[0-7]"
                    //         },
                    //         "t": {
                    //             validator: "[0-5]"
                    //         },
                    //         "7": {
                    //             validator: "[0-9]"
                    //         },
                    //         "E": {
                    //             validator: "e|E",
                    //             casing: "upper"
                    //         },
                    //         "W": {
                    //             validator: "w|W",
                    //             casing: "upper"
                    //         }
                    //     },
                    // });

                    // $(this).find("input[name*='sample_date_received']").prop("disabled", true);
                    // $(this).find("input[name*='date_collected']").prop("disabled", true);

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
                            create_select2($("select[name*='measurement_id']"), "DNA measurement");
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
    FormWizard.init();
    FormRepeater.init();

    $("#id-availability").hide();

    $("#package_id").blur(function(){
        var package_id = $(this).val().toUpperCase();
        if (package_id !== '') {
            $.ajax({
                url: $SCRIPT_ROOT+'/packages/check_id',
                type: 'POST',
                dataType: "json",
                contentType:"application/json",
                data: JSON.stringify({"package_id": package_id}),
            })
            .done(function(result) {
                if (result['available']) {
                    $("#id-availability div div p").html("<strong>"+$("#package_id").val().toUpperCase()+"</strong> is <span class=\"label label-success\">Available</span>");
                }
                else {
                    $("#id-availability div div p").html("<strong>"+$("#package_id").val().toUpperCase()+"</strong> is <span class=\"label label-danger\">Not available</span>");
                }
                $("#id-availability").show();
            });
        }
        else {
            $("#id-availability").hide();
        };
    });

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
        // if (ev.target.name.includes("sample_date_sampled")) {
            // var sample_date = $(ev.target).closest("div.col-md-2").next("div.col-md-2").find("input[name*='sample_date_received']");
            // $(sample_date).val("");
        //     $(sample_date).prop("disabled", false);
        //     $(sample_date).datepicker("setStartDate", ev.target.value);
        // }
        if (ev.target.name.includes("sample_date_received")) {
            var dna_collection_date = $(ev.target).closest("div.mt-repeater-item").find("input[name*='date_collected']");
            $(dna_collection_date).val("");
            $(dna_collection_date).prop("disabled", false);
            $(dna_collection_date).datepicker("setStartDate", ev.target.value);
        };
    });

    // $("input[name*='sample_date_received']").prop("disabled", true);
    // $("input[name*='date_collected']").prop("disabled", true);

    // $("input[name*='latitude']").inputmask({
    //     "mask": "(bc|c)|(\\90)\˚ (ic|c)|(60)\' [i]c.[c][c]c\" N|S",
    //     "autoUnmask": true,
    //     "greedy": false,
    //     "placeholder": "",
    //     "skipOptionalCharacter": " ",
    //     "definitions": {
    //         "i": {
    //             validator: "[0-5]" //t
    //         },
    //         "b": {
    //             validator: "[0-8]" //8
    //         },
    //         "c": {
    //             validator: "[0-9]" //7
    //         },
    //         "N": {
    //             validator: "n|N",
    //             casing: "upper"
    //         },
    //         "S": {
    //             validator: "s|S",
    //             casing: "upper"
    //         }
    //     }
    // });
    // $("input[name*='longitude']").inputmask({
    //     "mask": "(1r7|77)|(180)\˚ [t]7|(60)\' [t]7.[7][7]7\" E|W",
    //     "autoUnmask": true,
    //     "greedy": false,
    //     "placeholder": "",
    //     "skipOptionalCharacter": " ",
    //     "definitions": {
    //         "r": {
    //             validator: "[0-7]"
    //         },
    //         "t": {
    //             validator: "[0-5]"
    //         },
    //         "7": {
    //             validator: "[0-9]"
    //         },
    //         "E": {
    //             validator: "e|E",
    //             casing: "upper"
    //         },
    //         "W": {
    //             validator: "w|W",
    //             casing: "upper"
    //         }
    //     },
    // });

});
