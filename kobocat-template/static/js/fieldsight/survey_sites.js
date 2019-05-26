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
  self.create_surveys = ko.observableArray();
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
  self.is_survey = ko.observable();
  self.mapOne = ko.observable();

  self.save = function(){
    vm.site_modal_visibility(false);
  };
 
  for (var i in data){
    self[i] = ko.observable(data[i]);
  }
  self.mapOne({'lat':ko.observable(self.latitude()),'lng':ko.observable(self.longitude())});
  
  self.type(new SiteType({'id':self.type().id,'name':self.type().name}));
  self.is_survey(false);

};


function SitesViewModel(project) {
  var self=this;
  self.project = project;
  self.current_site = ko.observable();
  self.site_modal_visibility = ko.observable(false);
  self.allSites = ko.observableArray();
  self.sites = ko.observableArray();
  self.typeList =  ko.observableArray();
  
  self.detail_survey = function(site){
    self.site_modal_visibility(true);
  	self.current_site(site);
  };

  self.update_survey = function(update_site){
  App.showProcessing();
  var site = new Site({'type':{'id':update_site.type().id(),'name':update_site.type().name()}});
  site.id = update_site.id();
  site.identifier = update_site.identifier();
  site.name = update_site.name();
  site.public_desc = update_site.public_desc();
  site.additional_desc = update_site.additional_desc();
  site.latitude = update_site.mapOne().lat();
  site.longitude = update_site.mapOne().lng();
  site.type = update_site.type().id();
  site.is_survey = update_site.is_survey();

var url = '/fieldsight/api/survey-sites-review-update/'+site.id+'/';
var success =  function (response) {
                App.hideProcessing();
                self.current_site = ko.observable();
                self.site_modal_visibility(false);
                self.loadSites();
                App.notifyUser(
                        'Site Survey Saved',
                        'success'
                    );

            };
    
var failure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON.non_field_errors;
      if (err_message==undefined){
        err_message = "Failed To Save Data"
      }
                App.hideProcessing();
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };

    App.remotePost(url, site, success, failure);                                                                                                                    
  
  };


  self.save_detail = function(){
    self.update_survey(self.current_site());
    self.site_modal_visibility(false);
  	
  };

  self.close = function(){
    self.current_site = ko.observable();
      self.site_modal_visibility(false);
  };

  self.loadSites = function(){
    App.showProcessing();
        $.ajax({
            url: '/fieldsight/api/survey-sites-review/'+self.project+'/',
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

  self.loadSites();
  
  self.search_key = ko.observable();

  self.site_modal_visibility = ko.observable(false);
  self.current_site = ko.observable();


  self.search_key.subscribe(function (newValue) {
    if (!newValue) {
        self.sites(self.allSites());
    } else {
        filter_sites = ko.utils.arrayFilter(self.allSites(), function(item) {
            return ko.utils.stringStartsWith(item.name().toLowerCase(), newValue);
        });
        self.sites(filter_sites);
    }
    });

};


