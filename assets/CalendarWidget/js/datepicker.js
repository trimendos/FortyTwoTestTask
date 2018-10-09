$(document).ready(function () {
    $("#id_birthday").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd/mm/yy",
        maxDate: '-16Y',
        yearRange : '1940:c'
    });
});
