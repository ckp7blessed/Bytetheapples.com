    // DELETE COMMENTS
    $('.add-follower-form').on("submit", function(e) {
    	e.preventDefault();
        const profile_id = $(this).attr('id');
        console.log(profile_id)

        const url = $(this).attr('action');
        console.log(url)
        const serializedData = $(this).serialize();
        console.log(serializedData)

        $.ajax({
        	type: 'POST',
            url: url,
			data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
				'profile_id':profile_id,
			},
			// dataType: 'text',
            success: function(response) {
                $(`.add-follow-div-${profile_id}`).attr('class',`remove-follow-div-${profile_id}`);


                $("#follow-button-"+profile_id).attr("id");

                $(`.com-list${response.post_id}`).find('#clist'+response.comment_id).remove();

                $(`.comment-count-small${response.post_id}`).text(response.num_comments + ' ' + 'Comments');
            },
			error: function(response) {
				console.log('error', response);
			}
        });
    });