window.DRApp = new DoTRoute.Application();

DRApp.load = function (name) {
    return $.ajax({url: name + ".html", async: false}).responseText;
}

$.ajaxPrefilter(function(options, originalOptions, jqXHR) {

});


DRApp.controller("Base",null,{
    rest: function(type,url,data) {
        var response = $.ajax({
            type: type,
            url: url,
            contentType: "application/json",
            data: (data === null) ? null : JSON.stringify(data),
            dataType: "json",
            async: false
        });
        if ((response.status != 200) && (response.status != 201) && (response.status != 202)) {
            alert(type + ": " + url + " failed");
            throw (type + ": " + url + " failed");
        }
        return response.responseJSON;
    },
    home: function() {
        this.it = {
            fields: this.rest("OPTIONS","/api/speak", {}).fields
        };
        this.application.render(this.it);
    },
    speak: function() {
        var speak = {
            text: $("#text").val(),
            language: $("#language").val(),
        };
        var node = $('input[name=node]:checked').val();
        if (node) {
            speak.node = node;
        }
        this.rest("POST","/api/speak",{speak: speak});
        this.it.message = "text sent for speech";
        this.application.render(this.it);
    },
});

DRApp.partial("Header",DRApp.load("header"));
DRApp.partial("Footer",DRApp.load("footer"));

DRApp.template("Home",DRApp.load("home"),null,DRApp.partials);

DRApp.route("home","/","Home","Base","home");
