$( document ).ready(function() {

	$('.dropdown-content').on("click.bs.dropdown", function (e) {
	    e.stopPropagation();                 
	});

	$('.dropdown-item-close').click(function() {
		const notification_pk = $(this).attr('id');
		const url = '/notification/delete/'+notification_pk+'/';

		$.ajax({
			type: 'GET',
			url: url,
			data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
				'notification_pk':notification_pk,
			},
			success: function(response) {
				$(`#noti-${notification_pk}`).remove();
				$('#noti-count').text(response.notification_count);
			}
		})
	})

});

