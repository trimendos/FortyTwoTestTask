;(function () {
    if (!String.prototype.format) {
        /***
         * Usage: 'Give me a {what}'.format({what: 'power'})
         * @returns {string}
         */
        String.prototype.format = function () {
            let str, args, arg;
            str = this.toString();

            if (arguments.length === 0) {
                return str
            }

            args = typeof arguments[0];
            args = "string" === args || "number" === args ? arguments : arguments[0];

            for (arg in args) {
                if (args.hasOwnProperty(arg)) {
                    str = str.replace(new RegExp("\\{" + arg + "\\}", "gi"), args[arg]);
                }
            }
            return str
        }
    }
})();

let app = {};

app.Cookie = function (document) {

    function get(name) {
        let nameEQ = name + "=";
        let ca = document.cookie.split(";");

        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];

            while (c.charAt(0) == " ") {
                c = c.substring(1, c.length)
            }

            if (c.indexOf(nameEQ) == 0) {
                return c.substring(nameEQ.length, c.length)
            }
        }
        return null
    }

    function set(name, value, days, path) {
        let expires = "";
        path = path || "/";

        if (days) {
            let date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }

        document.cookie = name + "=" + value + expires + "; path=" + path;
    }

    function del(name) {
        set(name, "", -1)
    }

    return {
        set: set,
        get: get,
        del: del
    }

}(document);


app.Utils = function ($) {

    let csrftoken = app.Cookie.get("csrftoken");

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function setUpAjax() {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    }

    return {
        csrftoken: csrftoken,
        setUpAjax: setUpAjax
    }

}(jQuery);
