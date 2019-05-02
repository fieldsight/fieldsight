var url1 = ""
var orderby = "asce";
var sortbytext = "sitename";
function assignsite_id(url){

  url1 = url;
}

var Site =function (data){
  self = this;
  self.id = ko.observable();
  self.prog = ko.observable();
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
  self.get_site_submission_count = ko.observable();
  self.rejected = ko.observable();
  self.flagged = ko.observable();
  self.pending = ko.observable();
  self.approved = ko.observable();
  self.save = function(){
    vm.site_modal_visibility(false);
  };
  for (var i in data){
    self[i] = ko.observable(data[i]);
              }
  self.url= ko.observable("/fieldsight/site-dashboard/"+self.id()+"/");

  self.mapOne = ko.observable({
        lat: ko.observable(27.714875814507074),
        lng: ko.observable(85.3243088722229)});
}



function SitesViewModel() {
  var self=this;
  self.allSites = ko.observableArray();
  self.sites = ko.observableArray();


  self.loadSites = function(){

    App.showProcessing();


        $.ajax({
            url: url1,
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                
               var mappedData = ko.utils.arrayMap(response, function(item) {
                        response = item.get_site_submission_count;
                        item.get_site_submission_count = response;
                        item.rejected = response.rejected;
                        item.flagged = response.flagged;
                        item.pending = response.outstanding;
                        item.approved = response.approved;
                        return new Site(item);
                    });
                self.allSites(mappedData);

                self.sites(mappedData);
                
                sortnorderinit();
                App.hideProcessing();
            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };


  self.loadSites();
  
  self.search_key = ko.observable();



  self.site_modal_visibility = ko.observable(false);
  self.current_site = ko.observable();

  self.add_site = function(){
    self.current_site(new Site());
    self.site_modal_visibility(true);
  };

  self.search_key.subscribe(function (newValue) {
    if (!newValue) {
        self.sites(self.allSites());
    } else {
        filter_sites = ko.utils.arrayFilter(self.allSites(), function(item) {
            return ko.utils.stringStartsWith(item.name().toLowerCase(), newValue.toLowerCase());
        });
        self.sites(filter_sites);
    }
    });


  
  self.orderbyasce = ko.observable();
  self.orderbyasce.subscribe(function (newValue) {
        
       orderby = newValue;
       sortnorderinit();
   
    });


  self.sortby = ko.observable();
  self.sortby.subscribe(function (newValue) {

      sortbytext = newValue;
      sortnorderinit();
    
    });
  function sortnorderinit(){
    if (sortbytext == "approved"){
       sortbyapproved();
    }
    else if (sortbytext == "flagged"){
      sortbyflagged();
    }
    else if (sortbytext == "pending"){
      sortbypending();
    }
    else if (sortbytext == "rejected"){
      sortbyoutstanding();
    }
    else if (sortbytext == "progress"){
      sortbyprogress();
    }
    else if (sortbytext == "sitename"){
      sortbysitename();

    }
    else if (sortbytext == "identifier"){
      sortbyidentifier();
    }

  }

  function sortdata(x, y){
    if(orderby == "desc" ){
        return x < y ? 1 : x > y ? -1 : 0;
    }
    else{
        return x < y ? -1 : x > y ? 1 : 0; 
    }
  }


  function sortbyapproved(){
    sorted_sites = self.allSites().sort(
      function(a,b) {
            var x = a.approved();
            var y = b.approved();
            return sortdata(x, y);
          })
      self.sites(sorted_sites);

      return false;
  }
   function sortbyflagged(){
    sorted_sites = self.allSites().sort(
      function(a,b) {
            var x = a.flagged();
            var y = b.flagged();
            return sortdata(x, y);
          })
      self.sites(sorted_sites);
      return false;
  }
  function sortbypending(){
    sorted_sites = self.allSites().sort(
      function(a,b) {
            var x = a.pending();
            var y = b.pending();
            return sortdata(x, y);
          })
      self.sites(sorted_sites);
      return false;
  }
  function sortbyoutstanding(){
    sorted_sites = self.allSites().sort(
      function(a,b) {
            var x = a.rejected();
            var y = b.rejected();
            return sortdata(x, y);
          })
      self.sites(sorted_sites);
      return false;
  }
function sortbysitename(){
 
    sorted_sites = self.allSites().sort(
      function(a,b) {
            var x = a.name().toLowerCase();
            var y = b.name().toLowerCase();
            return sortdata(x, y);
          })
      self.sites(sorted_sites);
      return false;
  }
function sortbyidentifier(){
    sorted_sites = self.allSites().sort(
      function(a,b) {
            var x = a.identifier().toLowerCase();
            var y = b.identifier().toLowerCase();
            return sortdata(x, y);
          })
      self.sites(sorted_sites);
      return false;
  }
function sortbyprogress(){
    sorted_sites = self.allSites().sort(
      function(a,b) {
            var x = a.prog();
            var y = b.prog();
            return sortdata(x, y);
          })
      self.sites(sorted_sites);
      return false;
  }

 
// for sorting mechanicm
// self.sort_byflagged = function(){
    
//     sorted_sites = self.allSites().sort(
//       function(a,b) {
//             var x = a.name.toLowerCase();
//             var y = b.name.toLowerCase();
//             return x < y ? 1 : x > y ? -1 : 0;
//           })
//     self.sites(sorted_sites); 

//   };    


// self.sort_byrejected = function(){
    
//     sorted_sites = self.allSites().sort(
//       function(a,b) {
//             var x = a.name.toLowerCase();
//             var y = b.name.toLowerCase();
//             return x < y ? 1 : x > y ? -1 : 0;
//           })
//     self.sites(sorted_sites); 

//   };    

// self.sort_byoutstanding = function(){
    
//     sorted_sites = self.allSites().sort(
//       function(a,b) {
//             var x = a.name.toLowerCase();
//             var y = b.name.toLowerCase();
//             return x < y ? 1 : x > y ? -1 : 0;
//           })
//     self.sites(sorted_sites); 

//   };    

// self.sort_bypending = function(){
    
//     sorted_sites = self.allSites().sort(
//       function(a,b) {
//             var x = a.name.toLowerCase();
//             var y = b.name.toLowerCase();
//             return x < y ? 1 : x > y ? -1 : 0;
//           })
//     self.sites(sorted_sites); 

//   };    



    // self.search_key.subscribe(function (newValue) {
    // if (!newValue) {
       
    //     // function(a,b) {
    //     //     var x = a.name.toLowerCase();
    //     //     var y = b.name.toLowerCase();
    //     //     return x < y ? 1 : x > y ? -1 : 0;
    //     //   }

    //     filter_sites1 = self.allSites().sort(function(a,b) {
    //       var x = a.name.toLowerCase();
    //       var y = b.name.toLowerCase();
    //       return x < y ? 1 : x > y ? -1 : 0;
    //     });
    //     self.sites(filter_sites1);

    // } else {
    //    filter_sites1 = self.allSites().sort(function(a,b) {
    //       var x = a.name().toLowerCase();
    //       var y = b.name().toLowerCase();
    //       return x < y ? 1 : x > y ? -1 : 0;
    //     });
    //     self.sites(filter_sites1);

    //         }
    // });


};


