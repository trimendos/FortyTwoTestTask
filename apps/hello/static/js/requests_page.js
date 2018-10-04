app = app || {};

app.Requests = function() {
    let options, store;

    options = {
        row_tpl: "<tr><td>{method}</td><td>{url}</td><td>{status_code}</td><td>{datetime}</td></tr>",
        title_msg: "Requests",

        updateInterval: 1000,

        tbody: $("tbody"),
        title: $("title")
    };

    store = {
        newRequests: 0,
        intervalId: 0,
        isPageInFocus: false
    };

    window.addEventListener("focus", handleOnFocus);
    window.addEventListener("blur", handleOnBlur);

    function isFocus() {
        return document.hasFocus();
    }

    function handleOnFocus() {
        options.title.text(options.title_msg);
        store.newRequests = 0;
    }

    function handleOnBlur() {
        let n = store.newRequests > 0 ? "(" + store.newRequests + ") " : "";
        options.title.text(n + options.title_msg);
    }

    function updateTitleOfPage() {
        isFocus() ? handleOnFocus() : handleOnBlur();
    }

    function makeUrl(base) {
        base = base || window.location.href;

        return base + "?infocus={infocus}".format({infocus: isFocus()});
    }

    function makeTemplate(args, template) {
        template = template || options.row_tpl;
        return template.format(args);
    }

    function insertRows(html) {
        options.tbody.html(html);
    }

    function handleResponse(response) {
        let html = "", webrequests, newRequests;

        newRequests = response.unviewed;
        store.newRequests = newRequests;

        webrequests = response.webrequests;
        webrequests.forEach(function (webrequest) {

            html += makeTemplate({
                "datetime": webrequest.datetime,
                "url": webrequest.url,
                "status_code": webrequest.status_code,
                "method": webrequest.method
            });
        });
        // Update table
        insertRows(html);

        // Update counter
        updateTitleOfPage();

    }

    function makeRequest() {
        let url;

        url = makeUrl();
        $.getJSON(url, handleResponse);
    }

    function autoUpdateOn() {
        console.debug("Auto update is turned On.");
        store.intervalId = window.setInterval(
            function () {
                makeRequest();
            },
        options.updateInterval);
    }

    function init() {
        // Turn auto update on
        autoUpdateOn();
        //
        updateTitleOfPage();
    }

    return {
        init: init
    }

}();
