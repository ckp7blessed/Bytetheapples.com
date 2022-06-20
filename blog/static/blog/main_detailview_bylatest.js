// js for post_detail.html

$( document ).ready(function() {

    // INFINITE SCROLL LOAD MORE COMMENTS
	var working = false;
	$(window).scroll(function() {
		console.log($(this).scrollTop());
		console.log('document height'+$(document).height()+' ---  window height'+ $(window).height())
		console.log('==' +($(document).height() - $(window).height()))
		console.log('scroll top' +$(this).scrollTop())
		// const comcount = $('.com-id').length;
		const comcount = $('.clist').length; 
		console.log('count='+comcount);
		const post_id = $('.content-section').attr('id');

		// if($(this).scrollTop() +1 >= $(document).height() - $(window).height())
		if($(this).scrollTop() + 100 >= $(document).height() - $(window).height()) {
			if (working == false) {
				working = true;
			
			$.ajax({
			type: 'POST',
			url: '/post/load-more-comments-detail-bylatest/',
			// url: '/post/load-more-comments-detail/',
			// url: "{% url 'load-more-comments-detail' %}",
			url: $('.infinite-scroll').data('url'),
			data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
				'post_id':post_id,
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
                comClone.attr("id", "clist");
                comClone.removeAttr("style");

                comClone.attr("class", "clist");

                comClone.find(".com-id-temp").attr("class", "com-id");

                comClone.find(".com-id").attr("id", "cl"+data.pk);
                console.log('comment id='+data.pk)
                comClone.find(".comment-user-pp").attr("href", user_url + response.username);
                comClone.find(".comment-img").attr("src", response.image);
                comClone.find(".comment-user").text(response.username);

                comClone.find(".comment-user").attr("href", user_url + response.username);

                comClone.find(".comment-created").text(response.created);
                comClone.find(".comment-content").text(data.fields.body);

                comClone.find(".comlike-form").attr("action", comment_like_url);
                comClone.find(".comlike-form").attr("id", data.pk);
                comClone.find(".cl-input").attr("value", data.pk);
                comClone.find(".com-like").attr("class", "btn btn-like0 btn-sm py-0 com-like");
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
				function checkValue(value,arr) {
				  var status = 'Not exist';
				 
				  for(var i=0; i<arr.length; i++) {
				    var name = arr[i];
				    if(name == value) {
				      status = 'Exist';
						comClone.find(".com-like").text("Liked ");
						$(`#like-btn${data.pk}`).removeClass('btn-like0').addClass('btn-liked1');
						$(`#like-btn${data.pk}`).append('<span class="like-icon"><i class="fa fa-heart"></i></span>');
				      break;
				    }
				    else {
						comClone.find(".com-like").text("Like ");
						$(`#like-btn${data.pk}`).removeClass('btn-liked1').addClass('btn-like0');
						$(`#like-btn${data.pk}`).append('<span class="like-icon"><i class="fa fa-heart"></i></span>');
				    }
				  }
				  return status;
				}
				checkValue(response.user, data.fields.liked);

				});

			}
			});

			}
		}
	});

});
