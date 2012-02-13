$(document).ready(function(){
    $('.unfavorite_twit').click(function(){
        $(this).attr('src', 'https://si0.twimg.com/images/dev/cms/intents/icons/favorite.png');
        $(this).attr('class', 'favorite_twit')
        $.get('/unfavorite?t=twitter&id='+$(this).parent().parent().parent()[0].id, null, function(){
            // TODO
        });
        return false;
    })

    $('.retweet_twit').click(function(){
        $.get('/retweet?t=twitter&id='+$(this).parent().parent().parent()[0].id, null, function(){
            this.src = '/static/img/twitter/retweet_on.png'
        });
        return false;
    })

    $('.undo_retweet_twit').mouseover(function() {
        this.src = '/static/img/twitter/retweet_hover.png'
    })

    $('.undo_retweet_twit').mouseleave(function() {
        this.src = '/static/img/twitter/retweet_on.png'
    })

    $('.retweet_twit').mouseover(function() {
        this.src = '/static/img/twitter/retweet_hover.png'
    })

    $('.retweet_twit').mouseleave(function() {
        this.src = '/static/img/twitter/retweet.png'
    })

    $('.unfavorite_twit').mouseover(function() {
        this.src = '/static/img/twitter/favorite_hover.png'
    })

    $('.unfavorite_twit').mouseleave(function() {
        this.src = '/static/img/twitter/favorite_on.png'
    })

});
