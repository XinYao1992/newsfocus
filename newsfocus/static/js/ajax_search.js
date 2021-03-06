var page = 0;
var total_page;
var success_action = function(data) {
	page = 0;
	news = data;
	if(data.length % 10 != 0){
		total_page = data.length / 10 +1;
	} else {
		total_page = data.length / 10;
	}
	display(page);
};

$("#nextpage").on("click", function(e){
	e.preventDefault();
	if(page < total_page - 1) {
		page += 1;
		display(page);
	}
});

$("#previouspage").on("click", function(e){
	e.preventDefault();
	if(page > 0) {
		page += -1;
		display(page);
	}
});

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



function display(start) {
	$("#results").html("");
	$("#text-field").html("");
	index = 0;
	// data.forEach(function(e)
	news.slice(start,start+10).forEach(function(e) {
		console.log(e)
		$("#results").append(
			'<div class="row">' +
				'<div class="col-md-1">' +
					'<a href="#newsModal' + index + '" class="newsfield-link" data-toggle="modal">' +
						'<img class="img-responsive" src="'+e['thumbnail_standard']+'" style="width:75px;height:75px;margin-top:20px" alt="">' +
					'</a>' +
				'</div>' +
				'<div class="col-md-11">'+
					'<h3>' + e['title'] + '</h3>'+
					'<h4>' + e['byline'] + '</h4>'+
					'<p>' + e['abstract'] + '</p>'+
					'<a class="btn btn-primary" href="#newsModal' + index + '" data-toggle="modal">View News<span class="glyphicon glyphicon-chevron-right"></span></a>' +
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
									'<p class="item-intro text-muted">Date: '+e['published_date']+'</p>'+
									'<p>' + e['content'] + '</p>' +
									'<ul class="list-inline" id="related'+index+'">' +
										'<li>Category: ' + e['section'] + '</li>' +
									'</ul>' +
									'<button type="button" class="btn btn-primary" data-dismiss="modal"><i class="fa fa-times"></i> Close Project</button>'+
								'</div>' +
							'</div>' +
						'</div>' +
					'</div>' +
				'</div>' +
			'</div>'
		);

		// function get_related(relateds) {
		// 	var links = '';
		// 	for(i = 0; i < e['related_urls'].length; i++){
		// 		links += '<li>Related: <a href="'+relateds['related_urls'][i]['url']+'">'+relateds['related_urls'][i]['suggested_link_text']+'</a></li>';
		// 	}
		// 	return links;
		// }
		var len = e['related_urls'].length;
		for(j = 0; j < len; j++){
			$("#related"+index).append(
				// get_related(e);
				'<li>Related: <a href="'+e['related_urls'][j]['url']+'">'+e['related_urls'][j]['suggested_link_text']+'</a></li>'
			);
		}

		index += 1;
	});
}
