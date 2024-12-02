$(document).ready(function(){
    var csrf_token = $('meta[name=csrf-token]').attr('content');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    $("a.react").on("click", function(){
        var clicked_obj = $(this);
        var article_id = clicked_obj.attr("id")
        let reactionType = '';
        if ($(this).find('i').hasClass('fa-thumbs-up')) {
            reactionType = 'likes';
        } else if ($(this).find('i').hasClass('fa-grin-squint-tears')) {
            reactionType = 'laughs';
        } else if ($(this).find('i').hasClass('fa-grimace')) {
            reactionType = 'grimaces';
        } else if ($(this).find('i').hasClass('fa-meh')) {
            reactionType = 'blanks';
        } else if ($(this).find('i').hasClass('fa-surprise')) {
            reactionType = 'surprises';
        }

        $.ajax({
            url: '/react',
            type: 'POST',
            data: JSON.stringify({article_id: article_id, reaction: reactionType}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(response){
                console.log(response);
                if (reactionType === "likes") {
                    clicked_obj.find("#likes").text(" "+response.likes+"  ");
                } else if (reactionType === "laughs") {
                    clicked_obj.find("#laughs").text(" "+response.laughs);
                } else if (reactionType === "grimaces") {
                    clicked_obj.find("#grimaces").text(" "+response.grimaces);
                } else if (reactionType === "blanks") {
                    clicked_obj.find("#blanks").text(" "+response.blanks);
                } else if (reactionType === "surprises") {
                    clicked_obj.find("#surprises").text("      "+response.surprises);
                }
            },
            error: function(error){
                console.log(error);
            }
        });
        
    });
});
