$(document).ready(function(){
    var csrf_token = $('meta[name=csrf-token]').attr('content');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $("a.like").on("click", function(){
        var clicked_obj = $(this);
        var article_id = clicked_obj.attr("id");

        $.ajax({
            url: '/like',
            type: 'POST',
            data: JSON.stringify({ article_id: article_id }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response){
                console.log(response);
                clicked_obj.find("#likes").text("Likes: " + response.likes);
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});
