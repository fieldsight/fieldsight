function assigntoken(csrf){
  csrf_token=csrf;
  
}
var Images =function (data){
  self = this;
  self.fs_uuid = ko.observable();
  self._attachments = ko.observable();
  
  for (var i in data){
    self[i] = ko.observable(data[i]);
      }
}
function StageViewModel(url1, url2) {
 
  var self=this;
  self.generalforms = ko.observableArray();
  self.scheduledforms = ko.observableArray();
  self.stageforms = ko.observableArray();
  self.allformjson = ko.observableArray();
  self.stageForm = ko.observable();
  self.generalForm = ko.observable();
  self.scheduleForm = ko.observable();

  self.allImages = ko.observable();
  
  
  self.setSelected = function(item){
          console.log(item.selected());

          ko.utils.arrayForEach(item.forms, function(child) {
             
              child.selected((item.selected()));
              ko.utils.arrayForEach(child.forms, function(subchild) {
             
              subchild.selected((child.selected()));
             
             });
             
             });

          ko.utils.arrayForEach(self.allformjson(), function(item) {


                  select_status1 = false;

                    ko.utils.arrayForEach(item().forms, function(child) {
                        
                        if (child.selected() === true && item().xf_title != "Stage Forms"){
                              select_status1=true;
                        }

                            else{
                                select_status2 = false;
                                ko.utils.arrayForEach(child.forms, function(subchild) {
                                    if (subchild.selected() === true){
                                      select_status2 = true;        
                                      select_status1 = true;
                                    }                                             
                                });
                                child.selected(select_status2);    
                            }
                        item().selected(select_status1);    
                            
                                  
                    });           

             });

  return true;
          
     
    
  }; 

  self.data = ko.observable();
  self.generateReport = function(){
    App.showProcessing();
    var selectedFormids = [];
          ko.utils.arrayForEach(self.allformjson(), function(item) {
            
                if (item().selected() === true){
                    ko.utils.arrayForEach(item().forms, function(child) {

                        if (child.selected() === true){

                            if (item().xf_title != "Stage Forms"){

                                selectedFormids.push(child.id);
                            }
                            else{

                                ko.utils.arrayForEach(child.forms, function(subchild) {
                                    if (subchild.selected() === true){
                                      selectedFormids.push(subchild.id);        
                                    }                                             
                                });    
                            }
                        }          
                    });           
                }  
             });
    // console.log(selectedFormids);
    
    var startdate = document.getElementById("startdate").value;
    var enddate = document.getElementById("enddate").value;
    var removeNullField = document.getElementById("removeNullField").checked;
    
    // if (new Date(startdate) > new Date(enddate)){
    //   alert("Start Date cannot be greater than end date.");
    //   App.hideProcessing();
    //   return false;
    // }

    // if (!selectedFormids.length){
    //   alert("Please select atleast one form.");
    //   App.hideProcessing();
    //   return false;
    // }
    self.data({'fs_ids':selectedFormids, 'startdate':startdate, 'enddate':enddate, 'removeNullField':removeNullField, 'csrfmiddlewaretoken':csrf_token});
    
    //self.data({'fs_ids':selectedFormids, 'startdate':startdate, 'enddate':enddate, 'csrfmiddlewaretoken':csrf_token});
    

    var success =  function (response) {
                alert(response.message);
                App.notifyUser(
                        'Generating',
                        'Will be notified when ready.'
                    );

            };
            $('#exportModal').modal('hide');
            App.hideProcessing();
   
    var failure =  function (errorThrown) {
      alert(response.message);
      var err_message = errorThrown.responseJSON[0];
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };
          console.log(csrf_token);
       App.remotePost(url1, ko.toJS(self.data()), success, failure); 

    //   var xhr = new XMLHttpRequest();
    //   xhr.open("POST", url1, true);
    //   App.showProcessing();
    //   $('#exportModal').modal('hide');
    //   xhr.setRequestHeader('Content-Type', 'application/json');
    //   xhr.setRequestHeader('X-CSRFToken', csrf_token);
    //   xhr.responseType = 'blob';
    //   xhr.send(JSON.stringify(self.data())); 
    //   xhr.onload = function(e) {
    //     if (this.status == 200) {
    //         App.hideProcessing();
    //         alert("PDF is Ready, downloading now.");
    //         // Create a new Blob object using the response data of the onload object
    //         var blob = new Blob([this.response], {type: 'image/pdf'});
    //         //Create a link element, hide it, direct it towards the blob, and then 'click' it programatically
    //         let a = document.createElement("a");
    //         a.style = "display: none";
    //         document.body.appendChild(a);
    //         //Create a DOMString representing the blob and point the link element towards it
    //         let url = window.URL.createObjectURL(blob);
    //         a.href = url;
    //         a.download = 'Custom_Report.pdf';
    //         //programatically click the link to trigger the download
    //         a.click();
    //         //release the reference to the file by revoking the Object URL
    //         window.URL.revokeObjectURL(url);
    //     }else{
    //         //deal with your error state here
    //     }
    // };
};


  self.loadData = function(url1){
      // App.showProcessing();

          $.ajax({
              url: url1,
              method: 'GET',
              dataType: 'json',
              

              success: function (response) {
                 self.generalForm({'xf_title':'General Forms', 'level':'1', 'forms':[], 'selected': ko.observable(false) });
                 var mappedGeneralData = ko.utils.arrayMap(response.general, function(item) {
                            datas = {'id': item.id, 'xf_title': item.xf__title, 'level':'2', 'forms':[], 'selected': ko.observable(false)};
                            return datas;
                        });
                 self.generalForm().forms.push.apply(self.generalForm().forms, mappedGeneralData);

                 self.scheduleForm({'xf_title':'Schedule Forms', 'level':'1', 'forms':[], 'selected': ko.observable(false)});
                 var mappedScheduleData = ko.utils.arrayMap(response.schedule, function(item) {
                            datas = {'id': item.id, 'xf_title': item.schedule__name, 'level':'2', 'forms':[], 'selected': ko.observable(false)};
                            return datas;
                        });
                 self.scheduleForm().forms.push.apply(self.scheduleForm().forms, mappedScheduleData);

                 self.stageForm({'xf_title':'Stage Forms', 'level':'1', 'forms':[], 'selected': ko.observable(false)});
                 var mappedStageData = ko.utils.arrayMap(response.stage, function(item) {
                        var sub_stages = ko.utils.arrayMap(item.sub_stages, function(subitem) {
                            sub_datas = {'id': subitem.stage_forms__id, 'xf_title': subitem.name, 'forms':[], 'level':'3', 'selected': ko.observable(false)};
                            return sub_datas;
                        });
                        stage_data = {'id': item.id, 'xf_title': item.title, 'level':'2', 'forms':sub_stages, 'selected': ko.observable(false)};                      
                        return stage_data;
                    });
                 self.stageForm().forms.push.apply(self.stageForm().forms, mappedStageData);

                 self.allformjson.push(self.generalForm);
                 self.allformjson.push(self.scheduleForm);
                 self.allformjson.push(self.stageForm); 

                App.hideProcessing();
                },
              error: function (errorThrown) {
                  App.hideProcessing();
                  console.log(errorThrown);
              }
          });
    };

  

  

   self.loadImageData = function(url2){
       App.showProcessing();

          $.ajax({
              url: url2,
              method: 'GET',
              dataType: 'json',
              

              success: function (response) {
                console.log(response);
                var mappedData = ko.utils.arrayMap(response.images, function(item) {
                        datas = new Images(item);
                        return datas;
                    });
                self.allImages(mappedData);
                $('.scrollingSlider').slick({
                slidesToShow: 4,
                arrows: false,
                autoplay : true,
                infinite: false,
                responsive: [
                {
                  breakpoint: 768,
                  settings: {
                  arrows: false,
                  slidesToShow: 3
                  }
                },
                {
                  breakpoint: 480,
                  settings: {
                  arrows: false,
                  centerMode: true,
                  slidesToShow: 1
                  }
                }
                ]
              });
              $('.photo-item img').on('click',function(){
                    var title = $(this).attr('img-title');
                    var submitted_by = $(this).attr('submission_by');
                    var submission_url = $(this).attr('submission_url');
                    var src = $(this).attr('src');
                    var img = '<img src="' + src + '" class="img-responsive"/>';
                    var html = '';
                    html += img;    
                    $('#myModalLabel').modal();
                    $('#myModalLabel').on('shown.bs.modal', function(){
                      $('#myModalLabel .modal-header .modal-title').html('By: '+submitted_by +'<a href="'+ submission_url +'"> (View Submission) </a>');
                      $('#myModalLabel .modal-body').html(html);
                    })
                $('#myModalLabel').on('hidden.bs.modal', function(){
                  $('#myModalLabel .modal-header .modal-title').html('');
                  $('#myModalLabel .modal-body').html('');
                });
              });

              var height = 0;
              $(".gh-col" ).each(function() {
                height += $(this).height();
              });
              height = height + 14;
              $(".ah-col" ).height(height);

              var rpHeight = $("#recentPicutres").height();
              var tbHeight = $(".tab-custom-height>.active").height();
              if(rpHeight > tbHeight){
                $(".tab-custom-height>.tab-pane" ).each(function() {
                  $(this).height(rpHeight - 51);
                });
              }

                App.hideProcessing();
                // self.loadData(url1);
                },
              error: function (errorThrown) {
                  App.hideProcessing();
                  console.log(errorThrown);
              }
          });
    };

  

  self.loadImageData(url2);
}



