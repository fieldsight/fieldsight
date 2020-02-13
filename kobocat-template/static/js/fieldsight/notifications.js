
			var noticount = 0;
    		var request_isfirst = "true";
    		var mytask_request_isfirst= "true";

			var othertask_request_isfirst= "true";

			document.onload = getnotifcount();

			function getnotifcount(){
				 $.ajax({
			        url: url_count,
			        type: 'GET',
			        success: function (data) {

			          if(data.count==0){
                          var element = document.getElementById("id_notif");
                          element.parentNode.removeChild(element);
			          }
			          else{
			              $( ".not_count" ).append( data.count );
			              noticount = parseInt(data.count);
			          }

			          if(data.task_count==0){
			              var element = document.getElementById("id_task");
                          element.parentNode.removeChild(element)
			          }
			          else{
			            $( ".task_count" ).append( data.task_count );
			          }
			          
			        }
			      });

			}


			function populatelist(data, index){


			    typeid = data.type;

                var readstatus='unread';
                if(data.seen_by.includes(user_id)){
                   readstatus='read';
                }
            // get description for notificationaccotding to its type id
                var content = types[typeid](data);
            //append the data in main notificatin div



                var new_li = '<div class="dropdown-item '+ readstatus +'"  id="'+data.id+'" onclick="redirect(`'+data.get_absolute_url+'`);">'+
                '<div class="notification-item">'+
                  '<div class="notification-avatar pull-left" href="">'+
                  '<i class="avatar-icon la la-info"></i>'+
                  '</div>'+
                  '<div class="notification-highlight">'+
                  '<p class="notification-highlight-excerpt">'+
                  content +
                  '</p>'+
                  '<p class="notification-highlight-time">'+ dateparser(data.date) +'</p></div></div></div>';


                // var div = document.getElementById('notifications');

                // div.innerHTML += new_li;
                speed = speed+100;


                $(new_li).appendTo("#notification-ul");
                $("#"+data.id).fadeIn(speed);

		}


	function prepend_populatelist(data, index){
                if(!data || data == "undefined" ){
                return
                }
	        console.log(data);

			    typeid = data.type;
			    var readstatus='unread';
			    if(data.seen_by.includes(user_id)){
			       readstatus='read';
			    }
			// get description for notificationaccotding to its type id
			    var content = types[typeid](data);
			//append the data in main notificatin div

			    var new_li = '<li class=" note-div-sm '+ readstatus +'" id="'+data.id+'" style="display:none;" onclick="redirect(`'+data.get_absolute_url+'`);">'+

                                '<div class="notification-item">' +
                                    '<div class="notification-avatar pull-left">' +
                                        '<i class="avatar-icon la la-info"></i>' +
                                    '</div>' +
                                    '<div class="notification-highlight">'+
										'<p class="notification-highlight-excerpt">'+
                                   content +
                                   		'</p>'+
                      '<p class="notification-highlight-time">' + dateparser(data.date) + '</p>' +
                                    '</div>'+
                                    '</div>' +
                                '</div>' +

							'</li>';


			    // var div = document.getElementById('notifications');

			    // div.innerHTML += new_li;
			    speed = speed+100;


				$(new_li).prependTo("#notification-ul");
				$("#"+data.id).fadeIn(speed);

		}

	function getnotifdata(){
		if(request_isfirst == "false"){
			return false;

		}
          $.ajax({
            url: url,
            type: 'GET',
            success: function (data) {
               $("#notification-ul").html( "" );
               new_data = data.results.slice(0, 4);
               new_data.forEach(populatelist);
               request_isfirst = "false";



               speed=0;


            }
          });
}


	function updateseen(){
      $.ajax({
        url: url_count,
        data: {'csrfmiddlewaretoken': csrf},
        type: 'POST',

        success: function (data) {
          console.log(data);
          noticount = 0;
//          $( ".not_count" ).html( noticount );
          var element = document.getElementById("id_notif");
          element.parentNode.removeChild(element);

        }
      });
}






var notificationCount = $('#noti-count').text() || "0";
notificationCount = parseInt(notificationCount);


		function tasklistgenerate(data, status){
		    var additional_content = "";
		    if (data.status == 2){
		    	if ([3,6,8,9,10,11,12,16, 26].indexOf(data.task_type) >= 0){
		            status = " is ready to download. "
		            
		            var url  = data.file
		            
		            additional_content = "<br/><a href='"+ url +"'>Download File</a>";
		        	
		        }
			}
			

			if (data.task_type == 0 && data.terms_and_labels!=null){
				content = "Bulk " + data.terms_and_labels.site + " Update " +  "<a href='"+ data.get_event_url +"'>" + data.get_event_name + "</a>" + status;
		
			  }
		
			else if (data.task_type == 2 && data.terms_and_labels!=null){
			content = "User Assign to " + data.terms_and_labels.site  +  "<a href='"+ data.get_event_url +"'>" + data.get_event_name + "</a>" + status;
	
			}
	
			else if (data.task_type == 3 && data.terms_and_labels!=null){
			content = data.terms_and_labels.site + " Response Xls Report " +  "<a href='"+ data.get_event_url +"'>" + data.get_event_name + "</a>" + status;
	
			}
			else if (data.task_type == 4 && data.terms_and_labels!=null){
			content = data.terms_and_labels.site + " Import " +  "<a href='"+ data.get_event_url +"'>" + data.get_event_name + "</a>" + status;
	
			}
	
			else if (data.task_type == 6 && data.terms_and_labels!=null){
			content = "Zip "+ data.terms_and_labels.site +" Image " +  "<a href='"+ data.get_event_url +"'>" + data.get_event_name + "</a>" + status;
	
			}
	
			else if (data.task_type == 10 && data.terms_and_labels!=null){
			content = data.terms_and_labels.site + " Progress Xls Report Image " +  "<a href='"+ data.get_event_url +"'>" + data.get_event_name + "</a>" + status;
	
			}
	
			else if (data.task_type == 8 && data.terms_and_labels!=null){
			content = data.terms_and_labels.site + " Data Export of " +  "<a href='"+ data.get_event_url +"'>" + data.get_event_name + "</a>" + status;
	
			}
			else if (data.task_type == 13 && data.terms_and_labels!=null){
			content = "User Assign to " + data.terms_and_labels.region +  "<a href='"+ data.get_event_url +"'>" + data.get_event_name + "</a>" + status;
	
			}
			else{
			content = data.get_task_type_display + " of " +  "<a href='"+ data.get_event_url +"'>" + data.get_event_name + "</a>" + status;
			}
		    return content + additional_content;
		}


		function populatemytasklist(data, index){
				var status = "";
				var icon = "";
				var title = "";
				var	div_class = "";
			    var	div_subclass = "";
			    var error_msg = "";

			    if (data.status == 0){
			        status = ' has been added to Queue.';
			    	icon = "la la-hourglass-1";
			    	title = "Added";
			    	div_class = "task-pending";
			    	div_subclass = "text-warning";
			    }
			    else if (data.status == 1){
			        status = ' has been started.';       
			    	icon = "la la-hourglass-2";
			    	title = "Started";
			    	div_class = "task-ongoing";
			    	div_subclass = "text-info";
			    }
			    else if (data.status == 2){
			        status = ' has completed.';
			    	icon = "la la-check-circle";
			    	title = "Completed";
			    	div_class = "task-success";
			    	div_subclass = "text-success";
			    }
			    else{
			        status = ' has failed.';
			    	icon = "la la-times-circle";
			    	title = "Failed";
			    	div_class = "task-error";
			    	div_subclass = "text-danger";
			    	error_msg = "<b>Error message:</b> " + data.description + "<br/><br/>" ;
			    }

				var task_content = tasklistgenerate(data, status);
			   
			    var new_li = `  <div class="task-item `+ div_class +`" id="mytask` + data.id + `">
										<div class="task-icon `+ div_subclass +`">
											<i class="`+ icon +`"></i>
										</div>
										<div class="task-highlight">
											<p class="task-title"><strong>`+title+`</strong></p>
											<p class="task-highlight-excerpt">
												`+ task_content +`
											</p>
											<p class="task-detail-handler">See Detail</p>
											<p class="task-detail-content collapse">
											`+ error_msg +`
											  Added on ` + dateparser(data.date_added) + `<br/>
											  `+ title +` on ` + dateparser(data.date_updateded) + `
											</p>
										</div>
								</div>`;
			    
			    speed = speed+100;
				$(new_li).appendTo("#mytasks-ul");
				$("#mytask"+data.id).fadeIn(speed);
		}

		function populateothertasklist(data, index){
				var status = "";
				var icon = "";
				var title = "";
				var	div_class = "";
			    var	div_subclass = "";
			    var error_msg = "";

			    if (data.status == 0){
			        status = ' has been added to Queue.';
			    	icon = "la la-hourglass-1";
			    	title = "Added";
			    	div_class = "task-pending";
			    	div_subclass = "text-warning";
			    }
			    else if (data.status == 1){
			        status = ' has been started.';       
			    	icon = "la la-hourglass-2";
			    	title = "Started";
			    	div_class = "task-ongoing";
			    	div_subclass = "text-info";
			    }
			    else if (data.status == 2){
			        status = ' has completed.';
			    	icon = "la la-check-circle";
			    	title = "Completed";
			    	div_class = "task-success";
			    	div_subclass = "text-success";
			    }
			    else{
			        status = ' has failed.';
			    	icon = "la la-times-circle";
			    	title = "Failed";
			    	div_class = "task-error";
			    	div_subclass = "text-danger";
			    	error_msg = "<b>Error message:</b> " + data.description + "<br/><br/>" ;
			    }

			    var task_content = tasklistgenerate(data, status);
			    var new_li = ` 		<div class="task-item `+ div_class +`" id="othertask` + data.id + `">
										<div class="task-icon `+ div_subclass +`">
											<i class="`+ icon +`"></i>
										</div>
										<div class="task-highlight">
											<p class="task-title"><strong>`+title+`</strong></p>
											<p class="task-highlight-excerpt">
												`+ task_content +`
											</p>
											<p class="task-detail-handler">See Detail</p>
											<p class="task-detail-content collapse">
											`+ error_msg +`
											  Added on ` + dateparser(data.date_added) + `<br/>
											  `+ title +` on ` + dateparser(data.date_updateded) + `
											</p>
									</div>
								</div>`;
			    
			    speed = speed+100;
				$(new_li).appendTo("#othertasks-ul");
				$("#othertask"+data.id).fadeIn(speed);
		}


	function getmytasksdata(){
		if(mytask_request_isfirst == "false"){
			return false;

		}
          $.ajax({
            url: '/events/api/mytasks/',
            type: 'GET',
            success: function (data) {
			   $("#mytasks-ul").html( "" );

			   var my_tasks_length = data.results.length;
			   if (my_tasks_length > 0){
				$(".zeromytasks").hide();	
					var new_data = data.results.slice(0, 4);

					new_data.forEach(populatemytasklist);
					mytask_request_isfirst = "false";
					speed=0;
					$(".task-detail-handler").off("click");
					$('.task-detail-handler').on('click', function(event){
						event.stopPropagation();
						$(this).siblings('.task-detail-content').collapse('toggle');
						var hsText = $(this).text();
						if(hsText == 'See Detail'){
								$(this).text('Hide Detail');
						}else{
								$(this).text('See Detail');
						}
					});
			   }
			}
          });
	}

	function getothertasksdata(){
		if(othertask_request_isfirst == "false"){
			return false;

		}
          $.ajax({
            url: '/events/api/othertasks/',
            type: 'GET',
            success: function (data) {
				var other_tasks_length = data.results.length;
				
				if (other_tasks_length > 0){
				$(".zeroothertasks").hide();	
				$("#othertasks-ul").html( "" );
				var new_data = data.results.slice(0, 4);
				new_data.forEach(populateothertasklist);
				othertask_request_isfirst = "false";
				speed=0;
				$(".task-detail-handler").off("click");
				$('.task-detail-handler').on('click', function(event){
						console.log(event);
					event.stopPropagation();
					$(this).siblings('.task-detail-content').collapse('toggle');
					var hsText = $(this).text();
					if(hsText == 'See Detail'){
							$(this).text('Hide Detail');
					}else{
							$(this).text('See Detail');
					}
					});
			}
		}
          });
}