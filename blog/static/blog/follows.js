$( document ).ready(function() {

// FOR FOLLOWERS.HTML, FOLLOWING.HTML

    $('.follower-form').on("submit", function(e) {
    e.preventDefault();

    let countFollowing;
    const following = $('.following-count').text();
    const trimFollowing = parseInt(following);
    const url = $(this).attr('action');
    const profile_id = $(this).attr('id');

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'profile_id':profile_id,
        },
        success: function(response) {
            if(response == "Follow") {
                $(`#unfollow-button-${profile_id}`).attr('class', "btn btn-follow btn-light side-link");
                $(`#unfollow-button-${profile_id}`).text('Follow');
                $(`#unfollow-button-${profile_id}`).attr('id', "follow-button-"+profile_id);
                countFollowing = trimFollowing - 1; 
            } else {
                $(`#follow-button-${profile_id}`).attr('class',"btn btn-unfollow unfollow-link");
                $(`#follow-button-${profile_id}`).empty();
                $(`#follow-button-${profile_id}`).append("<span>Following</span>");
                $(`#follow-button-${profile_id}`).attr('id',"unfollow-button-"+profile_id);
                countFollowing = trimFollowing + 1;            
            }
            $('.following-count').text(countFollowing)

        },
        error: function(response) {
            console.log('error', response);
        },    
        });
    });

});



