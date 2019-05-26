function assigntoken(csrf){
  csrf_token=csrf;
  
}
is_siteselected=ko.observable(false);

is_regionselected=ko.observable(false);

all_selected_sites = ko.observableArray();
var Region =function (data, project){
  self = this;
  self.id = ko.observable();
  self.name = ko.observable();
  self.identifier = ko.observable();
  self.selected = ko.observable(false);
  for (var i in data){
    self[i] = ko.observable(data[i]);
      }
  self.url= ko.observable("/fieldsight/project/"+ project +"/regional-sites/"+self.id()+"/");
}



var Site = function(data){
  var self = this;
   
  self.id = ko.observable();
  self.type_label = ko.observable();
  self.name = ko.observable();
  self.identifier = ko.observable();
  self.type = ko.observable();
  self.region = ko.observable();
  
  for (var i in data){
    self[i] = ko.observable(data[i]);
      } 
   
  self.selected = ko.observable(
         all_selected_sites().some(function(item) {
            return (((item.id() != null && self.id() === item.id()) ? true:false));
            })
         
          );  
}



function RegionViewModel(next_url_region, next_url_site, site_query_url, region_query_url, project) {
  var self=this;
  self.allRegions = ko.observableArray();
  self.regions = ko.observableArray();
  self.next_page_region = ko.observable();
  self.prev_page_region = ko.observable();
  self.next_page_region = next_url_region;
  self.all_selected_regions = ko.observableArray();
  self.search_key_region = ko.observable();
  self.show_next_page_region = ko.observable(false);
  self.show_search_region_button = ko.observable(false);
  self.is_searching_regions = ko.observable(false);
  
function loadRegion(url){
    App.showProcessing();
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
               var all_regions_index = [];
               var all_selected_regions_index =[];
               
                for (var i = 0, j = self.allRegions().length; i < j; i++) {
                  all_regions_index["id="+self.allRegions()[i].id()]= i;
                }
                for (var i = 0, j = self.all_selected_regions().length; i < j; i++) {
                  all_selected_regions_index["id="+self.all_selected_regions()[i].id()]= i;
                }


                var mappedData = ko.utils.arrayMap(response.results, function(item) {
                        if(all_regions_index["id="+item.id] !== undefined){
                          index=all_regions_index["id="+item.id];
                          datas=self.allRegions()[index];
                        }else if(all_selected_regions_index["id="+item.id] !== undefined){
                          index=all_selected_regions_index["id="+item.id];
                          datas=self.all_selected_regions()[index];
                        }
                        else{
                          datas = new Region(item, project);
                        }

                        return datas;
                    });
               

                if(self.is_searching_regions() == false){
                self.allRegions.push.apply(self.allRegions, mappedData);
                if(response.next == null){
                    self.main_next_page_region = null;
                  }
                }

                self.regions.push.apply(self.regions, mappedData);
                console.log(mappedData);
                self.next_page_region = response.next;
                if (self.next_page_region != null){ 
                  self.show_next_page_region(true);
                   }
                else{ 
                  self.show_next_page_region(false);
                   }
              App.hideProcessing();
              },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };

  self.loadMoreRegions = function(){
    loadRegion(self.next_page_region);
  }; 

  loadRegion(self.next_page_region);

  self.dbsearchallRegions = function(){
  self.regions([]);

  if (self.is_searching_regions() == false){
      self.main_next_page_region = self.next_page_region;
      // console.log("in"+self.main_next_page_site);
  }
  // console.log("in"+self.main_next_page_site);
  self.is_searching_regions(true);
  url = region_query_url+"?q="+self.search_key_region();
  // alert(url);
  self.show_search_region_button(false);
  loadRegion(url);


  };

  self.setRegionSelected = function(selected_region){
      if (self.all_selected_regions.indexOf(selected_region) < 0){
        self.all_selected_regions([]);
        self.all_selected_regions.push(selected_region);
      }else{
        self.all_selected_regions([]);        
      }

      console.log(self.all_selected_regions());
      if(self.all_selected_regions().length == 0){
          is_regionselected(false);    
      }else{
        is_regionselected(true);
      }
               
      return true;
    
    };



   


    // if (self.all_selected_regions.indexOf(selected_region) < 0) {

    //   self.all_selected_regions([]);
    //   ko.utils.arrayForEach(self.regions(), function(region) {
      
    //   if(region.id() != selected_region.id()){ 
    //    region.selected(false);
    //   }
    //   });
      
    //   self.all_selected_regions.push(selected_region);
 
    //   }else{
    //     self.all_selected_regions.remove(selected_region);
        
    //   }
    //         console.log(self.all_selected_regions());
    //         return true;
    //   };


    
 

  // self.setAllRegionUnSelected = function(region){
   
  //  ko.utils.arrayForEach(self.regions(), function(region) {

  //  region.selected(false);
  //  // console.log(regions.selected());
  //  // console.log(all_selected_users());
  //   });   
  //   self.all_selected_regions([]);
   
  // };    
   

  // self.search_key_region.subscribe(function (newValue) {

  //   if (!newValue) {
  //       self.regions(self.allRegions());
  //   } else {
  //     newValue = newValue.toLowerCase();
  //       filter_regions = ko.utils.arrayFilter(self.allRegions(), function(item) {
  //           return (ko.utils.stringStartsWith(item.name().toLowerCase(), newValue) || 
  //             ko.utils.stringStartsWith(item.identifier().toLowerCase(), newValue));
  //       });
  //       self.regions(filter_regions);
  //   }
  //   });


self.search_key_region.subscribe(function (newValue) {
   // App.showProcessing();
    if (!newValue) {
        
        self.show_search_region_button(false);
        self.regions(self.allRegions().slice(0));
        if(self.is_searching_regions() == true){
        self.next_page_region = self.main_next_page_region;
        }
        self.is_searching_regions(false);
        // console.log(self.next_page_region);
        if (self.next_page_region != null){
          self.show_next_page_region(true);
        
        }
        // console.log(self.sites());

    } else {

      newValue = newValue.toLowerCase();
        filter_regions = ko.utils.arrayFilter(self.allRegions(), function(item) {
            // return item.name().split(" ").some(function(entry) {
            //       return ko.utils.stringStartsWith(entry.toLowerCase(), newValue);
            // });
            console.log(item.name());
            return (((item.name() != null) ? ko.utils.stringStartsWith(item.name().toLowerCase(), newValue):false) ||
              ko.utils.stringStartsWith(item.identifier().toLowerCase(), newValue));
        });
        self.regions(filter_regions);
        
    if(self.next_page_region != null){
      self.show_next_page_region(false);
      self.show_search_region_button(true);
        }

        console.log("main"+self.main_next_page_region)
    if(self.main_next_page_region != null){
      self.show_search_region_button(true);
    }
    }
    App.hideProcessing();

  
    });




  self.allSites = ko.observableArray();
  self.sites = ko.observableArray();
  self.next_page_site = ko.observable();
  self.prev_page_site = ko.observable();
  self.main_next_page_site = ko.observable();
  self.main_prev_page_site = ko.observable();
  self.next_page_site = next_url_site;
 
  self.search_key_site = ko.observable();
  self.show_next_page_site = ko.observable(false);
  self.show_search_site_button = ko.observable(false);
  self.is_searching_sites = ko.observable(false);
  self.all_selected_sites =ko.observableArray();
  self.main_next_page_site = null;

  function loadSites(url){
    App.showProcessing();
        $.ajax({
            url: url,

            success: function (response) {
               App.hideProcessing();
               var all_sites_index = [];
               var all_selected_sites_index =[];
               
                for (var i = 0, j = self.allSites().length; i < j; i++) {
                  all_sites_index["id="+self.allSites()[i].id()]= i;
                }
                for (var i = 0, j = self.all_selected_sites().length; i < j; i++) {
                  all_selected_sites_index["id="+self.all_selected_sites()[i].id()]= i;
                }



               
               var mappedData = ko.utils.arrayMap(response.results, function(item) {
                        if(all_sites_index["id="+item.id] !== undefined){
                          index=all_sites_index["id="+item.id];
                          datas=self.allSites()[index];
                        }else if(all_selected_sites_index["id="+item.id] !== undefined){
                          index=all_selected_sites_index["id="+item.id];
                          datas=self.all_selected_sites()[index];
                        }
                        else{
                          datas = new Site(item);
                        }

                        return datas;
                    });
                if(self.is_searching_sites() == false){
                self.allSites.push.apply(self.allSites, mappedData);
                if(response.next == null){
                    self.main_next_page_site = null;
                  }
                }
                self.sites.push.apply(self.sites, mappedData);
                
                self.next_page_site = response.next;
                self.prev_page_site = response.previous;
                if (self.next_page_site != null){ 
                  self.show_next_page_site(true);
                   }
                else{ 
                  self.show_next_page_site(false);
                   }
                
                
            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };

 


  self.loadMoreSites = function(){
    // console.log(self.sites());
    loadSites(self.next_page_site);
    // console.log(self.sites())
  };

  self.dbsearchallSites = function(){
    self.sites([]);

    if (self.is_searching_sites() == false){
        self.main_next_page_site = self.next_page_site;
        console.log("in"+self.main_next_page_site);
    }
    // console.log("in"+self.main_next_page_site);
    self.is_searching_sites(true);
    url = site_query_url+"?q="+self.search_key_site();
    // alert(url);
    self.show_search_site_button(false);
    loadSites(url);

  };

  loadSites(self.next_page_site);

  self.setSiteSelected = function(site){
   if (self.all_selected_sites.indexOf(site) < 0) {
    self.all_selected_sites.push(site);
        
  }else{
    self.all_selected_sites.remove(site);
    
  }
        console.log(self.all_selected_sites().length);
        if(self.all_selected_sites().length == 0){
          is_siteselected(false);
          
        }else{
          is_siteselected(true);
        }
                 
        return true;
  };

  self.setAllSiteUnSelected = function(site){
   // console.log(self.alluserid());
   ko.utils.arrayForEach(self.sites(), function(site) {

   site.selected(false);
   // console.log(site.selected());
   // console.log(all_selected_users());
    });   
    self.all_selected_sites([]);
    is_siteselected(false);
   
  };    

















function check(data, event) {
    console.log(event);
}  
   self.search_key_site.subscribe(function (newValue) {
   // App.showProcessing();
   console.log(self.next_page_site);
    if (!newValue) {
        
        self.show_search_site_button(false);
        self.sites(self.allSites().slice(0));
        if(self.is_searching_sites() == true){
        self.next_page_site = self.main_next_page_site;
        }
        self.is_searching_sites(false);
        // console.log(self.next_page_site);
        if (self.next_page_site != null){
          self.show_next_page_site(true);
        
        }
        // console.log(self.sites());

    } else {

      newValue = newValue.toLowerCase();
        filter_sites = ko.utils.arrayFilter(self.allSites(), function(item) {
            return ( ko.utils.stringStartsWith(item.identifier().toLowerCase(), newValue) || ((item.name().toLowerCase().search(newValue) == "-1") ? false:true) );


            

            // return ( ko.utils.stringStartsWith(item.identifier().toLowerCase(), newValue) || item.name().split(" ").some(function(entry) {
            //       return ko.utils.stringStartsWith(entry.toLowerCase(), newValue);
            // }));
            // return (ko.utils.stringStartsWith(item.name().toLowerCase(), newValue) || ko.utils.stringStartsWith(item.name().split(" ")[item.name().split(" ").length -1].toLowerCase(), newValue) ||
              // ko.utils.stringStartsWith(item.identifier().toLowerCase(), newValue));
        });
        self.sites(filter_sites);
        
    if(self.next_page_site != null){
      self.show_next_page_site(false);
      self.show_search_site_button(true);
        }

        console.log("main"+self.main_next_page_site)
    if(self.main_next_page_site != null){
      self.show_search_site_button(true);
    }
    }
    App.hideProcessing();

  
    });

  



  self.data = ko.observable();
  self.doAssign = function(){
    App.showProcessing();
    
    self.data({'region':[], 'sites':[]});
   
    if(self.all_selected_regions().length == 0 || self.all_selected_sites().length == 0)
      {
       alert("Please select atleast 1 site and 1 Region to assign to."); 
       App.hideProcessing();
       return false;
     }
    // if(all_selected_sites().length == 0){ alert("Please select atleast 1 site and 1 Region to assign to."); App.hideProcessing();return false;}
    
    ko.utils.arrayMap(self.all_selected_sites(), function(item) {
                    console.log(item.id());
                    self.data().sites.push(item.id);
                    });
    

    
    ko.utils.arrayMap(self.all_selected_regions(), function(item) {
                    console.log(item.id());
                    self.data().region.push(item.id);
                    });

    var url = "";
    console.log(ko.toJS(self.data()))
    

    var success =  function (response) {
                App.hideProcessing();

                App.notifyUser(
                        'Sites Assigned.',
                        'success'
                    );

            };
                App.hideProcessing();
   
    var failure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON[0];
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };
          console.log(csrf_token);
       App.remotePost(url, ko.toJS(self.data()), success, failure);  
};


self.unAssign = function(){
    App.showProcessing();
    
    self.data({'region':[], 'sites':[]});
    
   
    if(all_selected_sites().length == 0){ alert("Please select atleast 1 site to Unassign from Region."); App.hideProcessing();return false;}
    // if(all_selected_sites().length == 0){ alert("Please select atleast 1 site and 1 Region to assign to."); App.hideProcessing();return false;}
    
    ko.utils.arrayMap(all_selected_sites(), function(item) {
                    console.log(item.id());
                    self.data().sites.push(item.id);
                    });
    


    var url = "";
    console.log(ko.toJS(self.data()))
    

    var success =  function (response) {
                App.hideProcessing();

                App.notifyUser(
                        'Sites UnAssigned.',
                        'success'
                    );

            };
                App.hideProcessing();
   
    var failure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON[0];
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };
          console.log(csrf_token);
       App.remotePost(url, ko.toJS(self.data()), success, failure);  
};

};
