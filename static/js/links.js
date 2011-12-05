$(document).ready(function(){
    $('.unfavorite_twit').click(function(){
        $(this).attr('src', 'https://si0.twimg.com/images/dev/cms/intents/icons/favorite.png');
        $.get('/unfavorite?t=twitter&id='+this.id, null, function(){
            // TODO
        });
        return false;
    })
});