function assigntoken(csrf){
  csrf_token=csrf;
  
}
var SiteType = function(data) {
    var self = this;
        this.id = ko.observable();
        this.name = ko.observable();
    
  
  for (var i in data){
       self[i] = ko.observable(data[i]);
              }

    };

var Site =function (data){
  self = this;
  self.id = ko.observable();
  self.identifier = ko.observable();
  self.name = ko.observable();
  self.type = ko.observable();
  self.address = ko.observable();
  self.phone = ko.observable();
  self.public_desc = ko.observable();
  self.additional_desc = ko.observable();
  self.project = ko.observable();
  self.logo = ko.observable();
  self.is_active = ko.observable();
  self.location = ko.observable();
  self.latitude = ko.observable();
  self.longitude = ko.observable();
  self.mapOne = ko.observable();

  self.save = function(){
    vm.site_modal_visibility(false);
  };
  for (var i in data){
    val = data[i] || "";
    clean_val = val == "undefined" ? "" :val;
    self[i] = ko.observable(val);
              }
  self.url= ko.observable("/fieldsight/site-dashboard/"+self.id()+"/");

  self.mapOne({'lat':ko.observable(self.latitude()),'lng':ko.observable(self.longitude())});


  // self.type(new SiteType({'id':self.type().id,'name':self.type().name}));
}



function SitesViewModel(project, url) {
  var self=this;
  self.project = project;
  self.allSites = ko.observableArray();
  self.sites = ko.observableArray();
  self.typeList = ko.observableArray();

  self.upload_file = ko.observable()

  self.modal_visibility = ko.observable(false);

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
    
   
    if (new Date(startdate) > new Date(enddate)){
      alert("Start Date cannot be greater than end date.");
      App.hideProcessing();
      return false;
    }

    if (!selectedFormids.length){
      alert("Please select atleast one form.");
      App.hideProcessing();
      return false;
    }

    self.data({'fs_ids':selectedFormids, 'startdate':startdate, 'enddate':enddate, 'csrfmiddlewaretoken':csrf_token});
    

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


  self.loadSites = function(){
    App.showProcessing();
        $.ajax({
            url: '/fieldsight/api/project-sites-list/'+self.project+'/',
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
               var mappedData = ko.utils.arrayMap(response, function(item) {
                        return new Site(item);
                    });
                self.allSites(mappedData);

                self.sites(mappedData);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };


  self.loadSites();

    self.loadTypes = function(){
    App.showProcessing();
        $.ajax({
            url: '/fieldsight/api/project-types/',
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
                 var mappedTypeData = ko.utils.arrayMap(response, function(item) {
                        return new SiteType(item);
                    });

                self.typeList(mappedTypeData);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };


  self.loadTypes();

  self.bulkUpload = function(){
      self.modal_visibility(true);

  };


self.save_file_acync = function(){
    App.showProcessing();
    var url = '/fieldsight/api/bulk_upload_site/'+self.project+'/';

    var success =  function (response) {
    self.modal_visibility(false);
      self.loadSites();
                App.hideProcessing();
                
                App.notifyUser(
                        'Sites Bulk Upload Sucess',
                        'success'
                    );

            };
    var failure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON.file;
                App.hideProcessing();
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };

            var formdata = new FormData();
            formdata.append('file', self.upload_file());
    App.remoteMultipartPost(url, formdata, success, failure);                                                                                                                    
  
  };


self.save_site_async = function(){
    App.showProcessing();
    var url = '/fieldsight/api/async_save_site/';

    var success =  function (response) {
    self.site_add_visibility(false);
    self.current_site("");
      self.loadSites();
                App.hideProcessing();
                
                App.notifyUser(
                        'Site Creation Sucess',
                        'success'
                    );

            };
    var failure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON.error;
                App.hideProcessing();
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };

            var formdata = new FormData();
            formdata.append('id', self.current_site().id());
            formdata.append('logo', self.current_site().logo());
            formdata.append('identifier', self.current_site().identifier());
            formdata.append('name', self.current_site().name());
            formdata.append('address', self.current_site().address());
            formdata.append('phone', self.current_site().phone());
            formdata.append('is_active', self.current_site().is_active());
            formdata.append('public_desc', self.current_site().public_desc());
            formdata.append('additional_desc', self.current_site().additional_desc());
            formdata.append('type', self.current_site().type().id());
            formdata.append('project', self.project);
            formdata.append('Latitude', self.current_site().mapOne().lat());
            formdata.append('Longitude', self.current_site().mapOne().lng());
    App.remoteMultipartPost(url, formdata, success, failure);                                                                                                                    
  
  };


  self.save_upload = function(){
    // self.modal_visibility(false);
    self.save_file_acync();
  };
  
  self.search_key = ko.observable();

  self.site_add_visibility = ko.observable(false);
  self.current_site = ko.observable();

  self.addSite = function(){
    self.site_add_visibility(true);
    self.current_site(new Site({'type':self.typeList()[0], 'latitude':27.7172, 'longitude':85.3240, 'is_active':true}));
  };

  self.saveSite = function(){
    self.save_site_async();
    self.site_add_visibility(false);
  };

  self.clearSite = function(){
  self.site_add_visibility(false);
    self.current_site(undefined);
  };

  self.search_key.subscribe(function (newValue) {
    if (!newValue) {
        self.sites(self.allSites());
    } else {
      newValue = newValue.toLowerCase();
        filter_sites = ko.utils.arrayFilter(self.allSites(), function(item) {
            return (ko.utils.stringStartsWith(item.name().toLowerCase(), newValue) || 
              ko.utils.stringStartsWith(item.address().toLowerCase(), newValue));
        });
        self.sites(filter_sites);
    }
    });

};


