$(function () {
    console.log("menu");
    let title = document.title;
    // let html;
    $(".navbar-nav li").each( function () {
        let current = $(this).find("a");
        if(title === current.text()) {
            console.log()
            $(this).addClass("active");
             current.html( `${current.text()} <span class=\"sr-only\">(current)</span>`);
        }


    });


});