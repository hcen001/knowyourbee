updateMenu('#packages');

var initStateDropdown = function(element, country_id) {

    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};

    $.ajax({
        url: $SCRIPT_ROOT+"/packages/country/"+country_id+"/states",
        dataType: "json",
        success: function(data) {
            $(element).select2({
                allowClear: true,
                placeholder: "Select a state/province",
                data: data
            }).trigger('change');
            $(element).removeAttr("disabled");
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(jqXHR.responseText);
            alert('An unexpected error occured. Please try again.');
        }
    });
}

var initCityDropdown = function(element, state_id) {

    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};

    $.ajax({
        url: $SCRIPT_ROOT+"/packages/state/"+state_id+"/cities",
        dataType: "json",
        success: function(data) {
            $(element).select2({
                allowClear: true,
                placeholder: "Select a city",
                data: data
            }).trigger('change');
            $(element).removeAttr("disabled");
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(jqXHR.responseText);
            alert('An unexpected error occured. Please try again.');
        }
    });
}

var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

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
                }
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

        // $("#pack_country").on('select2:select', function(){
        //     var id = $(this).select2("val");
        //     $("#pack_state").html('').select2();
        //     initStateDropdown($("#pack_state"), id);
        // });
        // $("#pack_country").on('select2:unselect', function(){
        //     $("#pack_state").prop("disabled", true);
        //     $("#pack_state").html('').select2();
        // });
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
                        required: true
                    },
                    date_received: {
                        required: true
                    },
                    courier_id: {
                        required: true
                    },
                    tracking_number: {
                        required: false,
                        maxlength: 20
                    },
                    partner_id: {
                        required: true
                    },
                    location_id: {
                        required: true
                    },
                    sender_id: {
                        required: true
                    },
                    receiver_id: {
                        required: true
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
                $('#tab3 .form-control-static', form).each(function(){
                    var input = $('[name="'+$(this).attr("data-display")+'"]', form);
                    // console.log(input);
                    if (input.is(":radio")) {
                        input = $('[name="'+$(this).attr("data-display")+'"]:checked', form);
                    }
                    if (input.is(":text") || input.is("textarea")) {
                        $(this).html(input.val());
                    } else if (input.is("select")) {
                        $(this).html(input.find('option:selected').text());
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
    // $(element).find("input[name*='collection_sample_id']").val(last_specimen["collection_sample_id"]);
    // $(element).find("input[name*='dna']").val(last_specimen["dna"]);
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
    var last_specimen = specimens[specimens.length-2];

    update_datepicker($(element).find("input[name*='date_collected']"), last_specimen["date_collected"]);
    var start_date = $(element).closest("div.mt-repeater-item").prev("div.mt-repeater-item").find("input[name*='date_collected']").datepicker('getStartDate');
    update_datepicker_startDate($(element).find("input[name*='date_collected']"), start_date);
    copy_specimen_data(element, last_specimen);
};

var copy_country = function(element, id) {
    $(element).find("select[name*='country_id']").val(id).trigger("change");
};

var copy_state = function(element, id) {
    if ($(element).prev().find("select[name*='country_id']").val()) {
        var state_options = $(element).prev().find("select[name*='state_id'] > option").clone();
        $(element).find("select[name*='state_id']").append(state_options);
        $(element).find("select[name*='state_id']").prop("disabled", false);
        $(element).find("select[name*='state_id']").val(id).trigger("change");
    }
};

var copy_city = function (element, id) {
    if ($(element).prev().find("select[name*='state_id']").val()) {
        var city_options = $(element).prev().find("select[name*='city_id'] > option").clone();
        $(element).find("select[name*='city_id']").append(city_options);
        $(element).find("select[name*='city_id']").prop("disabled", false);
        $(element).find("select[name*='city_id']").val(id).trigger("change");
    }
};

var copy_previous_vial = function(element) {
    var repeater = $(element.parent()).repeaterVal();
    var add_specimen_button = $(element).find(".mt-repeater-add");

    var vials = repeater['samples'];
    // console.log(vials);
    var last_vial = vials[vials.length-2];

    $(element).find("input[name*='sender_source_id']").val(last_vial['sender_source_id']);
    $(element).find("input[name*='latitude']").val(last_vial['latitude']);
    $(element).find("input[name*='longitude']").val(last_vial['longitude']);
    $(element).find("input[name*='additional_gps_info']").val(last_vial['additional_gps_info']);
    $(element).find("input[name*='locality']").val(last_vial['locality']);
    $(element).find("input[name*='hive']").val(last_vial['hive']);
    $(element).find("input[name*='additional_info']").val(last_vial['additional_info']);
    $(element).find("input[name*='state']").val(last_vial['state']);

    $(element).find("input[name*='freezer']").filter(function(){
        return !this.name.match(/specimens/);
    }).val(last_vial['freezer']);
    $(element).find("input[name*='shelf']").filter(function(){
        return !this.name.match(/specimens/);
    }).val(last_vial['shelf']);
    $(element).find("input[name*='box']").filter(function(){
        return !this.name.match(/specimens/);
    }).val(last_vial['box']);
    $(element).find("textarea[name*='comments']").val(last_vial['comments']);

    $(element).find("input[value='"+last_vial["caste"]+"']").prop('checked', true);
    $(element).find("input[value='"+last_vial["gender"]+"']").prop('checked', true);
    $(element).find("input[value='"+last_vial["stage"]+"']").prop('checked', true);
    $(element).find("input[value='"+last_vial["sample_quality"]+"']").prop('checked', true);

    $(element).find("select[name*='collector']").val(last_vial["collector"]).trigger("change.select2");
    $(element).find("select[name*='processor']").val(last_vial["processor"]).trigger("change.select2");
    $(element).find("select[name*='process_location']").val(last_vial["process_location"]).trigger("change");

    copy_country(element, last_vial["country_id"]);
    copy_state(element, last_vial["state_id"]);
    copy_city(element, last_vial["city_id"]);

    $(element).find("select[name*='genus_id']").val(last_vial["genus_id"]).trigger("change.select2");
    $(element).find("select[name*='species_id']").val(last_vial["species_id"]).trigger("change.select2");
    $(element).find("select[name*='subspecies_id']").val(last_vial["subspecies_id"]).trigger("change.select2");
    $(element).find("select[name*='lineage_id']").val(last_vial["lineage_id"]).trigger("change.select2");

    var start_date = $(element).prev().find("input[name*='date_received']").datepicker('getStartDate');
    update_datepicker_startDate($(element).find("input[name*='date_received']"), start_date);

    update_datepicker_startDate($(element).find("input[name*='date_collected']"), start_date);
    $(element).find("input[name*='date_collected']").prop("disabled", false);
    update_datepicker($(element).find("input[name*='date_received']"), last_vial["sample_date_received"]);
    update_datepicker($(element).find("input[name*='date_sampled']"), last_vial["sample_date_sampled"]);

    var last_specimen = last_vial['specimens'][0];
    update_datepicker($(element).find("input[name*='date_collected']"), last_specimen['date_collected']);

    // $(element).find("input[name*='collection_sample_id']").val(last_specimen["collection_sample_id"]);
    // $(element).find("input[name*='dna']").val(last_specimen["dna"]);
    $(element).find("input[name*='body_part']").val(last_specimen["body_part"]);
    $(element).find("div.inner-repeater").find("input[name*='freezer']").val(last_specimen["freezer"]);
    $(element).find("div.inner-repeater").find("input[name*='box']").val(last_specimen["box"]);
    $(element).find("div.inner-repeater").find("textarea[name*='comments']").val(last_specimen["comments"]);
    $(element).find("input[value='"+last_specimen["measurement"]+"']").prop('checked', true);

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
                    // create_select2($("select[name*='state_id']"), "Select a state");
                    // create_select2($("select[name*='city_id']"), "Select a city");


                    // $("select[name*='country_id']", current_item).on('select2:select', function(e){
                    //     var id = $(this).select2("val");
                    //     var element = $(current_item).find("select[name*='state_id']");
                    //     $(element).html('').select2()
                    //     initStateDropdown(element, id);
                    // });

                    // $("select[name*='country_id']", current_item).on('select2:unselect', function(e){
                    //     var state_element = $(current_item).find("select[name*='state_id']");
                    //     deactivate_select2(state_element);

                    //     var city_element = $(current_item).find("select[name*='city_id']");
                    //     deactivate_select2(city_element);
                    // });

                    // $("select[name*='state_id']", current_item).on('select2:select', function(e){
                    //     var id = $(this).select2("val");
                    //     var element = $(current_item).find("select[name*='city_id']");
                    //     $(element).html('').select2()
                    //     initCityDropdown(element, id);
                    // });

                    // $("select[name*='state_id']", current_item).on('select2:unselect', function(){
                    //     var element = $(current_item).find("select[name*='city_id']");
                    //     deactivate_select2(element);
                    // });

                    create_select2($("select[name*='genus_id']"), "Select genus");
                    create_select2($("select[name*='species_id']"), "Select species");
                    create_select2($("select[name*='subspecies_id']"), "Select subspecies");
                    create_select2($("select[name*='lineage_id']"), "Select lineage");

                    $("input[name*='sample_date_sampled']").datepicker({
                        rtl: App.isRTL(),
                        orientation: "left",
                        autoclose: true,
                        format: "dd/MM/yyyy"
                    }).on('changeDate', function(ev){
                        var sample_date = $(ev.target).closest("div.col-md-2").next("div.col-md-2").find("input[name*='sample_date_received']");
                        $(sample_date).val("");
                        $(sample_date).prop("disabled", false);
                        $(sample_date).datepicker("setStartDate", ev.target.value)
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

                    $(this).find("input[name*='sample_date_received']").prop("disabled", true);
                    $(this).find("input[name*='date_collected']").prop("disabled", true);

                    $("input[name*='collected']").datepicker({
                        rtl: App.isRTL(),
                        orientation: "left",
                        autoclose: true,
                        format: "dd/MM/yyyy"
                    });

                    copy_previous_vial($(this));

                    // $(".mt-repeater-item:nth-child(odd)").css('background-color', 'LightGray');
                    // $(".mt-repeater-item:nth-child(even)").css('background-color', 'white');
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
    FormWizard.init();
    FormRepeater.init();

    create_select2($("#collector"), "Select a collector");
    create_select2($("#processor"), "Select a processor");
    // create_select2($("#pack_country"), "Select the country of origin");
    create_select2($("#process_location"), "Process location");
    create_select2($("#country_id"), "Country of origin");

    // $("select[name*='country_id']").on('select2:select', function(){
    //     var id = $(this).select2("val");
    //     var element = $("select[name*='state_id']:first");
    //     $(element).html('').select2()
    //     initStateDropdown(element, id);
    // });

    // $("select[name*='country_id']:first").on('select2:unselect', function(){
    //     $("select[name*='state_id']:first").prop("disabled", true).html('').select2();
    //     $("select[name*='city_id']:first").prop("disabled", true).html('').select2();
    // });

    // $("select[name*='state_id']").on('select2:select', function(){
    //     var id = $(this).select2("val");
    //     var element = $("select[name*='city_id']:first");
    //     $(element).html('').select2()
    //     initCityDropdown(element, id);
    // });

    // $("select[name*='state_id']:first").on('select2:unselect', function(){
    //     $("select[name*='city_id']:first").prop("disabled", true).html('').select2();
    // });

    // create_select2($("#state"), "Select a state");
    // create_select2($("#city"), "Select a city");
    create_select2($("#genus_id"), "Select genus");
    create_select2($("#species_id"), "Select species");
    create_select2($("#subspecies_id"), "Select subspecies");
    create_select2($("#lineage_id"), "Select lineage");

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

    $("input[name*='sample_date_received']").prop("disabled", true);
    $("input[name*='date_collected']").prop("disabled", true);

});
