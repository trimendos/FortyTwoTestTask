app = app || {};

app.Requests = function() {
    let options, store;

    options = {
        row_tpl: "<tr><td>{method}</td><td>{url}</td><td>{status_code}</td><td>{datetime}</td><td data-id='{id}'><button class='btn btn-light priority'>{priority}</button></td></tr>",
        priority_input: "<input type=number id=id_priority class=form-control max=999 min=1 value='{priority}'/>",
        title_msg: "Requests",
        bidi_arrow: "fas fa-sort-amount-down",

        updateInterval: 1000,

        priorityBtn: "button.priority",
        sort_ico: "fas fa-sort-amount-up",
        sort_ico_alt: "fas fa-sort-amount-down",


        tbody: $("tbody"),
        title: $("title"),
        sortPriorityBtn: $("thead th.sort__priority"),
        sortDatetimeBtn: $("thead th.sort__datetime")

    };

    store = {
        isAutoUpdate: true,
        newRequests: 0,
        intervalId: 0,
        isPageInFocus: false,
        prioritySortType: "high",
        isDatetimeSort: false,
        datetimeSortType: "last",
        forceUpdate: false
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
        return "{base}?infocus={infocus}&{sort_by}={sort}&force_update={force}"
            .format({
            base: base,
            infocus: isFocus(),
            sort_by: store.isDatetimeSort ? "sort_datetime" : "sort_priority",
            sort: store.isDatetimeSort ? store.datetimeSortType : store.prioritySortType,
            force: store.forceUpdate
        });
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
        if(webrequests){
            webrequests.forEach(function (webrequest) {

                html += makeTemplate({
                    "id": webrequest.id,
                    "datetime": webrequest.datetime,
                    "url": webrequest.url,
                    "status_code": webrequest.status_code,
                    "method": webrequest.method,
                    "priority": webrequest.priority
                });
            });
            // Update table
            insertRows(html);

            // Bind buttons
            priorityBtnHandler();

            // Update counter
            updateTitleOfPage();

        }

    }

    function makeRequest(isForceUpdate) {
        let url;

        isForceUpdate = isForceUpdate || false;
        store.forceUpdate = isForceUpdate;
        url = makeUrl();
        store.forceUpdate = false;
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

    function replaceBtnWithInput(btn) {
        var priority = btn.text().trim(),
            html = options.priority_input.format({priority: priority}),
            input;
        btn.hide();
        btn.after(html);

        input = $("input#id_priority")
            .focus()
            .blur(function (){
                input.remove();
                btn.show();
            });
        return input;
    }

    function sendInputtedData(input) {
        var parent, data;
        parent = $(input.parent());

        data = {
            priority: input.val(),
            rq_id: parent.attr("data-id")
        };

        $.ajax({
            method: "POST",
            data: data,
            url: makeUrl(),

            success: function (response) {
                var errorDict = response.errors || false,
                    joinedErrors = "",
                    field,
                    errors;

                if (errorDict) {
                    for (field in errorDict) {
                        if (errorDict.hasOwnProperty(field)) {
                            errors = errorDict[field].join(", ");
                            joinedErrors += field + ": " + errors;
                        }
                    }

                } else {
                    handleResponse(response);
                }
            },
            error: function (x, s, m) {
                console.log("Error! Message: " + m)
            }
        });
    }

    function priorityBtnHandler() {
        // Add event on the priority button
        $(options.priorityBtn).each(function () {
            var btn = $(this),
            keys = {
                enter: 13,
                up_arrow: 38,
                down_arrow: 40
            };

            btn.click(function () {
                var input = replaceBtnWithInput(btn);

                input.keypress(function (e) {
                    if (e.keyCode == keys.enter) {
                        sendInputtedData(input);
                    }
                });
                input.focusout(function () {
                    sendInputtedData(input);
                });
                input.keyup(function (e) {
                   if(e.keyCode == keys.up_arrow || e.keyCode == keys.down_arrow) {
                       sendInputtedData(input);
                   }
                });
            });
        });
    }

    function toggleSort() {
        options.sortPriorityBtn.click(function () {
            var self = $(this),
                arrow = self.find("i"),
                currClass = arrow.attr("class"),
                sortIco = store.prioritySortType == "high" ? options.sort_ico : options.sort_ico_alt;

            store.prioritySortType = store.prioritySortType == "high" ? "low" : "high";

            store.isDatetimeSort = false;

            options.sortDatetimeBtn.removeClass("link").addClass("text-muted");
            options.sortDatetimeBtn.find("i").removeClass().addClass(options.bidi_arrow);

            self.removeClass("text-muted").addClass("link");
            arrow.removeClass(currClass).addClass(sortIco);

            makeRequest(true);
        });
    }

    function toggleDatetimeSort() {
        options.sortDatetimeBtn.click(function () {
            var self = $(this),
                arrow = self.find("i"),
                currClass = arrow.attr("class"),
                sortIco = store.datetimeSortType == "last" ? options.sort_ico : options.sort_ico_alt;

            store.datetimeSortType = store.datetimeSortType == "last" ? "first" : "last";
            store.isDatetimeSort = true;

            options.sortPriorityBtn.removeClass("link").addClass("text-muted");
            options.sortPriorityBtn.find("i").removeClass().addClass(options.bidi_arrow);

            self.removeClass("text-muted").addClass("link");
            arrow.removeClass(currClass).addClass(sortIco);

            makeRequest(true);
        });
    }

    function init() {
        // Turn auto update on
        autoUpdateOn();
        //
        updateTitleOfPage();

        priorityBtnHandler();

        toggleDatetimeSort();
        // Bind priority sort button
        toggleSort();

        app.Utils.setUpAjax();

        updateTitleOfPage();
    }

    return {
        init: init
    }

}();
