// js for post_comment_detail.html

$( document ).ready(function() {

    // INFINITE SCROLL LOAD MORE COMMENTS
	var working = false;
	$(window).scroll(function() {
		const comcount = $('.clist').length; 
		const post_id = $('.content-section').attr('id');
		const comment_parent_id = $('.comment-parent').attr('id');

		// if($(this).scrollTop() +1 >= $(document).height() - $(window).height())
		// if($(this).scrollTop() + 100 >= $(document).height() - $(window).height()) {
		if (($(window).scrollTop() + 150 + $(window).innerHeight()) >= $(document).height()-100){
			if (working == false) {
				working = true;
			
			$.ajax({
			type: 'POST',
			url: '/post/load-more-replies-detail-bylatest/',
			data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
				'post_id':post_id,
				'comment_parent_id': comment_parent_id, 
				'offset': comcount
			},
			dataType: 'json',
			success: function(response) {
                setTimeout(function() {
                	working = false;
                }, 300);

                var user_url = '/user/';
                var comment_like_url = '/post/comment/like/';
                var delete_url_start = '/post/commenttemp/';
                var delete_url_end = '/delete/';
				var json_data = $.parseJSON(response.comment);

				$.each(json_data,function(index,data) {

				const comClone = $("#clist00").clone(true, true).val(null);
                comClone.appendTo($(`.com-list${post_id}`));
                comClone.attr("id", "clist" + data.pk);
                comClone.removeAttr("style");

                comClone.attr("class", "clist");

                comClone.find(".comment-user-pp").attr("href", user_url + data.fields.username);
                comClone.find(".comment-img").attr("src", data.fields.user_pp);
                comClone.find(".comment-user").text(data.fields.username);

                comClone.find(".comment-user").attr("href", user_url + data.fields.username);

                comClone.find(".comment-created").text(data.fields.created_custom);
                comClone.find(".comment-content").text(data.fields.body);

                comClone.find(".comlike-form").attr("action", comment_like_url);
                comClone.find(".comlike-form").attr("id", data.pk);
                comClone.find(".cl-input").attr("value", data.pk);
                comClone.find(".com-like").attr("class", "btn btn-sm py-0 com-like");
                comClone.find(".com-like").append('<span class="like-icon"><i class="fa fa-heart"></i></span>');

                comClone.find(".com-like").attr("id", "like-btn" + data.pk);

                comClone.find(".com-modal").text(data.fields.liked.length+ " Likes");

                comClone.find(".com-modal").attr("id", "clc" + data.pk);
                comClone.find(".com-modal").attr("class", "btn btn-outline-dark btn-sm py-0 com-modal like-count" + data.pk);
                comClone.find(".com-modal").attr("data-target", "#commentlikesModalLong-" + data.pk);

                comClone.find(".cmodal").attr("id", "commentlikesModalLong-" + data.pk);
                comClone.find(".liked-list00").attr("class", "modal-body liked-list" + data.pk);

                // LIST OF USERS WHO LIKED THE COMMENT
				$.each(data.fields.liked_username, function(i, item) {

			  	var userlikeHTML =  
								'<div id="cl' +data.fields.liked_username[i] + '">' +
								'<ul class="list-unstyled">' +
								'<li>' + 
								'<a href="/user/' +
								data.fields.liked_username[i] + 
								'">' +
								'<img class="rounded-circle article-img" src="' + data.fields.liked_user_pp[i] + '"></a>' +
								'<a class="mr-2 badge badge-light" href="/user/' +
								data.fields.liked_username[i] + 
								'">' +
								data.fields.liked_username[i] +
								'</a>' +
								'</li>' +
								'</ul>' +
								'</div>';

                comClone.find($(`.liked-list${data.pk}`).append(userlikeHTML));
                });

				comClone.find($("#reply-btn00").remove());

				// IF request.user == comment.author: show delete button
                if (response.user == data.fields.user) {

                    comClone.find(".delete-btn").attr("id", data.pk);
                    comClone.find(".delete-btn").attr("data-target", "#commentdeleteModal-"+data.pk);
                    comClone.find(".comdelete").attr("id", "commentdeleteModal-"+data.pk);

                    comClone.find(".comdelete-form-temp").attr("action", delete_url_start+data.pk+delete_url_end);
                    comClone.find(".comdelete-form-temp").attr("id", data.pk);
            	}
            	else {
            		comClone.find(".delete-btn-dropdown").remove();
            	};

            	// IF request.user liked the comment
				function checkValue(value, arr) {
				  // var status = 'Not exist';
				 
				  for(var i=0; i<arr.length; i++) {
				    var name = arr[i];
				    if (name == value) {
				      // status = 'Exist';
				      console.log('EXIST');
						comClone.find($(`#like-btn${data.pk}`)).text("Liked ");
						comClone.find($(`#like-btn${data.pk}`).removeClass('btn-like0').addClass('btn-liked1'));
						comClone.find($(`#like-btn${data.pk}`).append('<span class="like-icon"><i class="fa fa-heart"></i></span>'));
				      break;
				    }
				    else {
				    	console.log('NONExist');
						comClone.find($(`#like-btn${data.pk}`)).text("Like ");
						// comClone.find($(`#like-btn${data.pk}`).removeClass('btn-liked1').addClass('btn-like0 '));
						comClone.find($(`#like-btn${data.pk}`).attr('class', "btn btn-like0 btn-sm py-0 com-like"));
						comClone.find($(`#like-btn${data.pk}`).append('<span class="like-icon"><i class="fa fa-heart"></i></span>'));
				    }
				  }
				  // return status;
				}
				checkValue(response.user, data.fields.liked);
				console.log(response.user);
				console.log(data.fields.liked);
				console.log('---NEW--');

				if (data.fields.liked.length == 0) {
					comClone.find($(`#like-btn${data.pk}`).attr('class', "btn btn-like0 btn-sm py-0 com-like"));
				};


				});

			}
			});

			}
		}
	});

});
