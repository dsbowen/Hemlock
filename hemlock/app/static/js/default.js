// Default jquery

// LATER: Navigate without changing browser history
// $("form").submit( function(e) {
//     e.preventDefault();
//     if( $(this).hasClass("form-submitted") ){
//         return;
//     }
//     $(this).addClass("form-submitted");
//     $("input.btn[name='direction']").attr("disabled", true);
//     $.post(window.location.href, $(this).serialize(), function(data){
//         console.log(data);
//         window.location.replace(data);
//     })
// });

$("form").submit( function(e) {
    if( $(this).hasClass("form-submitted") ){
        e.preventDefault();
        return;
    }
    $(this).addClass("form-submitted");
    $("input.btn[name='direction']").attr("disabled", true);
});