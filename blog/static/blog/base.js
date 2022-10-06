
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


	// Detects if user is on a mobile device and alerts
	function detectMob() {
	    return ( ( window.innerWidth <= 391 ) && ( window.innerHeight <= 845 ) );
	  };

	  var alerted = sessionStorage.getItem('alerted') || '';
	  if (detectMob()){
	    if (alerted != 'yes') {
	     alert("Detected a mobile device. Please use a desktop browser or use in portrait mode for best experience");
	     sessionStorage.setItem('alerted','yes');
	    };
	};
	detectMob();

	// Enlarges images
	$('img[data-enlargeable]').addClass('img-enlargeable').click(function() {
	  var src = $(this).attr('src');
	  var modal;

	  function removeModal() {
	    modal.remove();
	    $('body').off('keyup.modal-close');
	  }
	  modal = $('<div>').css({
	    background: 'RGBA(0,0,0,.5) url(' + src + ') no-repeat center',
	    backgroundSize: 'contain',
	    width: '100%',
	    height: '100%',
	    position: 'fixed',
	    zIndex: '10000',
	    top: '0',
	    left: '0',
	    cursor: 'zoom-out'
	  }).click(function() {
	    removeModal();
	  }).appendTo('body');
	  //handling ESC
	  $('body').on('keyup.modal-close', function(e) {
	    if (e.key === 'Escape') {
	      removeModal();
	    }
	  });
	});

	// COMMENT ON A POST
	$('.com-form').on("submit", function(e) {
		e.preventDefault();
	    const post_id = $(this).attr('id');
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

				const comClone = $("#clist00").clone(true, true).val(null);
	            comClone.prependTo($(`.com-list${post_id}`));

	            comClone.attr("id", "clist"+response.comment.id);
	            comClone.removeAttr("style");
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

	            comClone.find(".com-modal").text("0 ");
	            comClone.find(".com-modal").append('<small><i class="fa fa-heart fa-heart-blue"></i></small>');
	            comClone.find(".com-modal").attr("id", "clc" + response.comment.id);
	            comClone.find(".com-modal").attr("class", "btn btn-outline-dark btn-sm py-0 com-modal like-count" + response.comment.id);
	            comClone.find(".com-modal").attr("data-target", "#commentlikesModalLong-" + response.comment.id);

	            comClone.find(".cmodal").attr("id", "commentlikesModalLong-" + response.comment.id);

	            comClone.find(".liked-list00").attr("class", "modal-body liked-list" + response.comment.id);

	            comClone.find(".list-unstyled").remove();

	            comClone.find($("#reply-btn00").attr("href", '/post/'+ post_id + '/comment/'+response.comment.id));
	            comClone.find($("#reply-btn00").text("0 "));
	            comClone.find($("#reply-btn00").append('<small><i class="fa fa-solid fa-comment"></i></small>'));

	            comClone.find(".delete-btn").attr("id", response.comment.id);
	            comClone.find(".delete-btn").attr("data-target", "#commentdeleteModal-"+response.comment.id);
	            comClone.find(".comdelete").attr("id", "commentdeleteModal-"+response.comment.id);
	            comClone.find(".comdelete-form-temp").attr("action", response.delete_url_start+response.comment.id+response.delete_url_end);
	            comClone.find(".comdelete-form-temp").attr("id", response.comment.id);

	            $('.com-form').each(function() { this.reset() });

	            res = trimCount + 1;
	            $(`.comment-count-small${post_id}`).text(res + ' ');

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

				} else {
					$(`.like-btn${post_id}`).text('Liked ');
					res = trimCount + 1;
					$(`.like-btn${post_id}`).removeClass('btn-like0').addClass('btn-liked1');
					$(`.like-btn${post_id}`).append('<span class="like-icon"><i class="fa fa-heart icn-spinner"></i></span>');

					$(`.liked-list${post_id}`).append(userlikeHTML);
				}

				$(`.like-count${post_id}`).text(res +' ');
				$(`.like-count${post_id}`).append('<i class="fa fa-heart fa-heart-blue"></i>');
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
		const likeText = $(`#like-btn${comment_id}`).text();
		const trim = $.trim(likeText);

		let res;
		const likes = $(`.like-count${comment_id}`).text();
		const trimCount = parseInt(likes);
		
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

				$(`.like-count${comment_id}`).text(res + ' ');
				$(`.like-count${comment_id}`).append('<small><i class="fa fa-heart fa-heart-blue"></i></small>');
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

        const url = $(this).attr('action');
        const serializedData = $(this).serialize();	

        $.ajax({
        	type: 'POST',
            url: '/post/commenttemp/'+comment_id +'/delete/',
			data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
				'comment_id':comment_id,
			},
            success: function(response) {
                $("#commentdeleteModal-"+response.comment_id).find('.close').click();
                $(`.com-list${response.post_id}`).find('#clist'+response.comment_id).remove();
                $(`.comment-count-small${response.post_id}`).text(response.num_comments + ' ');

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
        const url = $(this).attr('action');
        const serializedData = $(this).serialize();

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
                $(`.com-list${response.post_id}`).find('#clist'+response.comment_id).remove();
                $(`.comment-count-small${response.post_id}`).text(response.num_comments + ' ');
            },
			error: function(response) {
				console.log('error', response);
			}
        });
    });

});