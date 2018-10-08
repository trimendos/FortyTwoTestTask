$(function () {
    "use strict";

    $("#profile").submit(function () {
        if (this.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
        }
        this.classList.add("was-validated");

    });

    $("#id_birthday").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd/mm/yy",
        maxDate: '-16Y',
        yearRange : '1940:c'
    });

    $("#id_photo").on("change", function () {
        var input = this;

        if (input.files && input.files[0]) {
            var reader = new FileReader(),
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
    function simulateDataProcess() {
        var profile = {};
        disableEnableFields(true);
        $("input:not(:hidden, :button, :submit), textarea").each(
            function (i, el) {
                profile[el.name] = el.value;
            }
        );
        localStorage.setItem("profile", JSON.stringify(profile));
        setTimeout(function () {
            disableEnableFields(false);
        }, 3000);
    }

/*    $("#save").on("click", function () {
        simulateDataProcess();
        return false;
    });*/

});
