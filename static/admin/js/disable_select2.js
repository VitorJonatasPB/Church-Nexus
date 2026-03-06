document.addEventListener("DOMContentLoaded", function () {
    // Remove select2 de campos com a classe htmx-ignore-select2
    document.querySelectorAll("select.htmx-ignore-select2").forEach(function(el) {
        if (el.select2) {
            $(el).select2('destroy');  // destrói o select2
        }
    });
});