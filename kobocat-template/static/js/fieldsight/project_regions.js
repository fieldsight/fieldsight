function assigntoken(csrf){
  csrf_token=csrf;
  
}
var Region =function (data, project){
  self = this;
  self.id = ko.observable();
  self.name = ko.observable();
  self.identifier = ko.observable();
  self.get_sites_count = ko.observable();
  
  for (var i in data){
    self[i] = ko.observable(data[i]);
      }
  self.url= ko.observable("/fieldsight/project/"+ project +"/regional-sites/"+self.id()+"/");
}



function RegionViewModel(project, url) {
  var self=this;
  self.allRegions = ko.observableArray();
  self.regions = ko.observableArray();
  
  self.generalforms = ko.observableArray();
  self.scheduledforms = ko.observableArray();
  self.stageforms = ko.observableArray();
  self.allformjson = ko.observableArray();
  self.stageForm = ko.observable();
  self.generalForm = ko.observable();
  self.scheduleForm = ko.observable();
  
  
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
    var filterRegion = $("#filterRegion").val();

    
    if (new Date(startdate) > new Date(enddate)){
      alert("Start Date cannot be greater than end date.");
      App.hideProcessing();
      return false;
    }

    // if (!selectedFormids.length){
    //   alert("Please select atleast one form.");
    //   App.hideProcessing();
    //   return false;
    // }

    self.data({'fs_ids':selectedFormids, 'startdate':startdate, 'enddate':enddate, 'filterRegion':filterRegion, 'csrfmiddlewaretoken':csrf_token});
    

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
       App.remotePost(url, ko.toJS(self.data()), success, failure); 

};


  self.loadData = function(url){
      // App.showProcessing();

          $.ajax({
              url: url,
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
    self.loadData(url);
  
  self.loadRegion = function(){
    App.showProcessing();
        $.ajax({
            url: '/fieldsight/api/project-regions/'+project+'/',
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
               
                var mappedData = ko.utils.arrayMap(response, function(item) {
                    datas = new Region(item, project);
                    return datas;
                });

                var filteredMappedData=mappedData.filter(r => !r.parent()
                );

                self.allRegions(mappedData);
                self.regions(filteredMappedData);
                $('#filterRegion').selectize({
                      
                  });
                },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };


  self.loadRegion();

  self.clearRegion = function(){
  self.region_add_visibility(false);
    self.current_region(undefined);
  };
  self.search_key = ko.observable();
  self.search_key.subscribe(function (newValue) {
    if (!newValue) {
        self.regions(self.allRegions());
    } else {
      newValue = newValue.toLowerCase();
        filter_regions = ko.utils.arrayFilter(self.allRegions(), function(item) {
            return (ko.utils.stringStartsWith(item.name().toLowerCase(), newValue) || 
              ko.utils.stringStartsWith(item.identifier().toLowerCase(), newValue));
        });
        self.regions(filter_regions);
    }
    });
};
