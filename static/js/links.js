$(document).ready(function(){
    $('.unfavorite_twit').click(function(){
        $(this).attr('src', 'https://si0.twimg.com/images/dev/cms/intents/icons/favorite.png');
        $.get('/unfavorite?t=twitter&id='+$(this).parent().parent().parent()[0].id, null, function(){
            // TODO
        });
        return false;
    })

    $('.retweet_twit').click(function(){
        $.get('/retweet?t=twitter&id='+$(this).parent().parent().parent()[0].id, null, function(){
            // TODO
        });
        return false;
    })
});