
$( document ).ready(function() {

	let display = false;
	$(".show-replies-button").click(function(e) {
		if (display===false) {
			$(this).next(".comment-box").show("slow");
			display=true;
			$(this).text('Hide replies');
		} else {
			$(this).next(".comment-box").hide("slow");
			display=false;
			$(this).text('Show replies');
		}  
	});

	// COMMENT POST
	$('.com-form').on("submit", function(e) {
		e.preventDefault();
	    const post_id = $(this).attr('id');
	    console.log(post_id)
		const comcountText = $(`.comment-count${post_id}`).text();
		const trim = $.trim(comcountText);
	    const url = $(this).attr('action');
	    const serializedData = $(this).serialize();

		let res;
		const comcount = $(`.comment-count${post_id}`).text();
		const trimCount = parseInt(comcount);

	    $.ajax({
	    	type: 'POST',
	        url: url,
			data: serializedData,
			dataType: 'json',
	        success: function(response) {
	            console.log('success')
	            console.log(response.username)
	            console.log(response.post_id+"post ID")

				const comClone = $("#clist00").clone(true, true).val(null);
	            // comClone.appendTo($(`.com-list${post_id}`));
	            comClone.prependTo($(`.com-list${post_id}`));

	            comClone.attr("id", "clist");
	            comClone.removeAttr("style");
	            comClone.find(".com-id-temp").attr("class", "com-id");
	            comClone.find(".com-id").attr("id", "cl"+response.comment.id);
	            comClone.find(".comment-img").attr("src", response.image);
	            comClone.find(".comment-user").text(response.username);
	            comClone.find(".comment-user").attr("href", response.user_url_start + response.username);
	            comClone.find(".comment-created").text("Just Now");
	            comClone.find(".comment-content").text(response.comment.body);

	            comClone.find(".comlike-form").attr("action", response.comment_like_url);
	            comClone.find(".comlike-form").attr("id", response.comment.id);
	            comClone.find(".cl-input").attr("value", response.comment.id);
	            comClone.find(".com-like").attr("class", "btn btn-like0 btn-sm py-0 com-like");


	            comClone.find(".com-like").attr("id", "like-btn" + response.comment.id);
	            comClone.find(".com-like").text("Like ");
	            comClone.find(".com-like").append('<span class="like-icon"><i class="fa fa-heart"></i></span>');


	            comClone.find(".com-modal").text("0 Likes");
	            comClone.find(".com-modal").attr("id", "clc" + response.comment.id);
	            comClone.find(".com-modal").attr("class", "btn btn-outline-dark btn-sm py-0 com-modal like-count" + response.comment.id);
	            comClone.find(".com-modal").attr("data-target", "#commentlikesModalLong-" + response.comment.id);

	            comClone.find(".cmodal").attr("id", "commentlikesModalLong-" + response.comment.id);

	            comClone.find(".liked-list00").attr("class", "modal-body liked-list" + response.comment.id);

	            comClone.find(".list-unstyled").remove();


	            comClone.find(".delete-btn").attr("id", response.comment.id);
	            comClone.find(".delete-btn").attr("data-target", "#commentdeleteModal-"+response.comment.id);
	            comClone.find(".comdelete").attr("id", "commentdeleteModal-"+response.comment.id);
	            comClone.find(".comdelete-form-temp").attr("action", response.delete_url_start+response.comment.id+response.delete_url_end);
	            comClone.find(".comdelete-form-temp").attr("id", response.comment.id);

	            console.log(response.delete_url_start+response.comment.id+response.delete_url_end)
	            console.log(response.comment.id)
	            console.log('success');
	            $('.com-form').each(function() { this.reset() });


	            res = trimCount + 1;
	            $(`.comment-count-small${post_id}`).text(res + ' ' + 'Comments');
	            console.log(res);

				if (display===false) {
					$(`#comment-box-${post_id}`).show("slow");
					display=true;
					$(this).text('Hide replies');
				};
	        },
	        error: function(error) {
	            console.log(error);
	        }
	    });
	});


	// LIKE/UNLIKE POSTS
	$('.like-form').submit(function(e){
		e.preventDefault();
		const post_id = $(this).attr('id');
		const likeText = $(`.like-btn${post_id}`).text();
		const trim = $.trim(likeText);
		const url = $(this).attr('action');

		let res;
		const likes = $(`.like-count${post_id}`).text();
		const trimCount = parseInt(likes);
		
		$.ajax({
			type: 'POST',
			url: url,
			data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
				'post_id':post_id,
			},
			success: function(response) {
				console.log('response.user_id'+response.user_id)
				// LIST OF USERS WHO LIKED THE POST
				var userlikeHTML =  
								'<div id="pl' +response.user_id + '">' +
								'<ul class="list-unstyled">' +
								'<li>' + 
								'<a href="/user/' +
								response.username + 
								'">' +
								'<img class="rounded-circle article-img" src="' + response.image + '">' +
								'<a class="mr-2 badge badge-light" href="/user/' +
								response.username +
								'">' +
								response.username +
								'</a>' +
								'</li>' +
								'</ul>' +
								'</div>';

				if(trim == "Liked") {
					$(`.like-btn${post_id}`).text('Like ');
					res = trimCount - 1;
					
					$(`.like-btn${post_id}`).removeClass('btn-liked1').addClass('btn-like0');
					$(`.like-btn${post_id}`).append('<span class="like-icon"><i class="fa fa-heart icn-spinner"></i></span>');

					$(`.liked-list${post_id}`).find('#pl'+response.user_id).remove();

					console.log(response.user_id)
					console.log('removed')

				} else {
					$(`.like-btn${post_id}`).text('Liked ');
					res = trimCount + 1;
					$(`.like-btn${post_id}`).removeClass('btn-like0').addClass('btn-liked1');
					$(`.like-btn${post_id}`).append('<span class="like-icon"><i class="fa fa-heart icn-spinner"></i></span>');

					$(`.liked-list${post_id}`).append(userlikeHTML);
				}
				console.log(response)
				console.log(response.username)
				console.log(response.image)

				$(`.like-count${post_id}`).text(res + ' ' + 'Likes');
			},
			error: function(response) {
				console.log('error', response);
			}
		});
	});

	// LIKE/UNLIKE COMMENTS
	$('.comlike-form').submit(function(e){
		e.preventDefault();
		const comment_id = $(this).attr('id');
		console.log(comment_id)
		const likeText = $(`#like-btn${comment_id}`).text();
		console.log(likeText)
		const trim = $.trim(likeText);
		// const url = $(this).attr('action')
		console.log(trim)
		// console.log(url)

		let res;
		const likes = $(`.like-count${comment_id}`).text();
		const trimCount = parseInt(likes);
		console.log(likes)
		console.log(trimCount)
		
		$.ajax({
			type: 'POST',
			url: '/post/comment/like/',
			data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
				'comment_id':comment_id,
			},
			success: function(response) {
				// LIST OF USERS WHO LIKED THE COMMENT
				var userlikeHTML =  
								'<div id="cl' +response.username + '">' +
								'<ul class="list-unstyled">' +
								'<li>' + 
								'<a href="/user/' +
								response.username + 
								'">' +
								'<img class="rounded-circle article-img" src="' + response.image + '">' +
								'<a class="mr-2 badge badge-light" href="/user/' +
								response.username +
								'">' +
								response.username +
								'</a>' +
								'</li>' +
								'</ul>' +
								'</div>';
				console.log(response)
				if(trim == "Liked") {
					$(`#like-btn${comment_id}`).text('Like ');
					res = trimCount - 1;
					
					$(`#like-btn${comment_id}`).removeClass('btn-liked1').addClass('btn-like0');
					$(`#like-btn${comment_id}`).append('<span class="like-icon"><i class="fa fa-heart icn-spinner"></i></span>');

					$(`.liked-list${comment_id}`).find('#cl'+response.username).remove();

				} else {
					$(`#like-btn${comment_id}`).text('Liked ');
					res = trimCount + 1;
					$(`#like-btn${comment_id}`).removeClass('btn-like0').addClass('btn-liked1');
					$(`#like-btn${comment_id}`).append('<span class="like-icon"><i class="fa fa-heart icn-spinner"></i></span>');

					$(`.liked-list${comment_id}`).append(userlikeHTML);

				}

				$(`.like-count${comment_id}`).text(res + ' ' + 'Likes');
			},
			error: function(response) {
				console.log('error', response);
			}
		});
	});

	// DELETE 'TEMPORARY' COMMENTS RENDERED BY JQUERY
    $('.comdelete-form-temp').on("submit", function(e) {
    	e.preventDefault();
        const comment_id = $(this).attr('id');
        console.log('delete success function - comment id '+comment_id)

        const url = $(this).attr('action');
        console.log(url)
        const serializedData = $(this).serialize();	
        console.log(serializedData)

        $.ajax({
        	type: 'POST',
            url: '/post/commenttemp/'+comment_id +'/delete/',
			data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
				'comment_id':comment_id,
			},
			// dataType: 'text',
            success: function(response) {
                $("#commentdeleteModal-"+response.comment_id).find('.close').click();

                $(`.com-list${response.post_id}`).find('#cl'+response.comment_id).remove();

                $(`.comment-count-small${response.post_id}`).text(response.num_comments + ' ' + 'Comments');
            },
			error: function(response) {
				console.log('error', response);
			}
        });
    });

    // DELETE COMMENTS
    $('.comdelete-form').on("submit", function(e) {
    	e.preventDefault();
        const comment_id = $(this).attr('id');
        console.log('delete success function - comment id '+comment_id)

        const url = $(this).attr('action');
        console.log(url)
        const serializedData = $(this).serialize();
        console.log(serializedData)

        $.ajax({
        	type: 'POST',
            url: url,
			data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
				'comment_id':comment_id,
			},
			// dataType: 'text',
            success: function(response) {
                $("#commentdeleteModal-"+response.comment_id).find('.close').click();

                $(`.com-list${response.post_id}`).find('#cl'+response.comment_id).remove();

                $(`.comment-count-small${response.post_id}`).text(response.num_comments + ' ' + 'Comments');
            },
			error: function(response) {
				console.log('error', response);
			}
        });
    });


});