$(function() {
    $(".dropdown-menu a").click(function (e) {
        console.log($(this).parents('.dropdown').find('.dropdown-toggle').text());
        let optionText = $(this).text();
        $(this).parents('.dropdown').find('.dropdown-toggle')
            .html(optionText);
        e.preventDefault();
    });
});