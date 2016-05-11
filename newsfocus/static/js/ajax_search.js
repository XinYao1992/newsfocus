var success_action = function(data) {
	$("#results").html("");
	index = 0;
	data.forEach(function(e) {
		console.log(e)
		$("#results").append(
			'<div class="row">' +
				'<div class="col-md-1">' +
					'<a href="#newsModal' + index + '" class="newsfield-link" data-toggle="modal">' +
						'<img class="img-responsive" src="/static/img/newsfield/art.jpg" style="width:75px;height:75px;margin-top:20px" alt="">' +
					'</a>' +
				'</div>' +
				'<div class="col-md-11">'+
					'<h3>' + e['title'] + '</h3>'+
					'<h4>' + e['byline'] + '</h4>'+
					'<p>' + e['abstract'] + '</p>'+
					'<a class="btn btn-primary" href="#newsModal' + index + '" data-toggle="modal">View Project <span class="glyphicon glyphicon-chevron-right"></span></a>' +
				'</div>' +
			'</div>' + '<hr>'
		);
		$("#text-field").append(
			'<div class="newsfield-modal modal fade" id="newsModal' + index + '" tabindex="-1" role="dialog" aria-hidden="true">' +
				'<div class="modal-content">' +
					'<div class="close-modal" data-dismiss="modal">' +
						'<div class="lr">' +
							'<div class="rl">' +
							'</div>' +
						'</div>' +
					'</div>' +
					'<div class="container">' +
						'<div class="row">' +
							'<div class="col-lg-8 col-lg-offset-2">' +
								'<div class="modal-body">'+
									'<h2>' + e['title'] + '</h2>' +
									'<p class="item-intro text-muted">' + e['byline'] + '</p>' +
									'<p class="item-intro text-muted"><a href="'+e['url']+'">go to original website</a></p>'+
									'<p>' + e['content'] + '</p>' +
									'<ul class="list-inline">' +
										'<li>Date: ' + e['published_date'] + '</li>' +
										'<li>Category: ' + e['section'] + '</li>' +
									'</ul>' +
									'<button type="button" class="btn btn-primary" data-dismiss="modal"><i class="fa fa-times"></i> Close Project</button>'+
								'</div>' +
							'</div>' +
						'</div>' +
					'</div>' +
				'</div>' +
			'</div>'
		)
		index += 1;
	});
};

$("#ordinary-search").on("click", function(e){
	e.preventDefault();
	$.ajax({
		type: "POST",
		url: "/ordinary_search/",
		data: {
			csrfmiddlewaretoken: csrf_token,
			'keywords': $('#ordinary-key-words').val(),
		},
		success: success_action
	});
});

$("#advanced-search").on("click", function(e){
	e.preventDefault();
	var categories = grab_selected();
	$.ajax({
		type: "POST",
		url: "/advanced_search/",
		data: {
			csrfmiddlewaretoken: csrf_token,
			'keywords': $('#advanced-key-words').val(),
			'daterange': $('#date-range').val(),
			'categories[]': categories,
		},
		success: success_action
	});
});

function grab_selected() {
	var tasks = [];
	$('input:checked').each(function() {
		tasks.push(this.id);
	});
	return tasks;
}
