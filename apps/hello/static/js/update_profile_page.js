$(function () {
    "use strict";

    $("#profile").submit(function () {
        if (this.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
        }
        this.classList.add("was-validated");

    });

    $("#birthday").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd/mm/yy",
        maxDate: '-16Y',
        yearRange : '1940:c'
    });
});