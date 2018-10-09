$(function () {
    "use strict";
    let ajaxOpt;

    $("#id_birthday").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd/mm/yy",
        maxDate: '-16Y',
        yearRange : '1940:c'
    });

    $("#id_photo").on("change", function () {
        let input = this;

        if (input.files && input.files[0]) {
            let reader = new FileReader(),
                picture = $(".picture");

            reader.onload = function (e) {
                picture.css("max-width", 200);
                picture.css("max-height", 200);
                picture.attr("src", e.target.result);
            };
            reader.readAsDataURL(input.files[0]);
        }
    });

    function disableEnableFields(flag) {
        $("input, submit, textarea, button").attr("disabled", flag);
        $("#back_link").toggleClass("disable-links");
        $("#loading").toggle();
        if(flag) {
            $("#home-link").attr("aria-disabled", true).addClass("disabled")
        } else {
            $("#home-link").attr("aria-disabled", false).removeClass("disabled")
        }
    }

    function hideMessageResult() {
        let output = "#output1";
        setTimeout(function() {
            $(output).removeClass("alert-success alert-danger");
            $(output).text("");
        }, 2000);
    }

    function managerResponses(fTrigger, className, text) {
        disableEnableFields(fTrigger);
        let output = "#output1";
        $(output).addClass(className)
            .text(text);
        hideMessageResult();
    }

    ajaxOpt = {
        target: "#output1",
        dataType: "json",
        url: location.pathname,
        beforeSubmit: function () {
            disableEnableFields(true);
        },
        success: function () {
            managerResponses(false, "alert-success", "Changes have been save!");
            let selector = "#photo-clear_id";
            $("#id_photo").val("");
            if ($(selector).length && $(selector).is(":checked")) {
                $(selector).remove();
                $("label[for=photo-clear_id]").remove();
            }
        },
        error: function () {
            managerResponses(false, "alert-danger", "Changes have been not save!");
        }
    };

    $("#profile").on("submit", function (e) {
        e.preventDefault();
        if (this.checkValidity() === false) {
            e.stopPropagation();
        }
        $(this).ajaxSubmit(ajaxOpt);
        this.classList.add("was-validated");
    });


    $("#id_photo-clear").on("click", function () {
        $(".picture").attr("src", "/static/img/unknown_user.png");
    });

});
