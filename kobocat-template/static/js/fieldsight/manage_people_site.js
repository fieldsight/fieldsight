
var csrf_token ="";
var group = "";

function assigntoken(csrf){
  csrf_token=csrf;

}



var all_selected_users = ko.observableArray();


function notFound(id, array){
var notFOund  = true;
  ko.utils.arrayFilter(array, function(item) {
            if (item.user().id() == id){
              notFOund = false;
              return;
            }
        });

return notFOund;
}


var User = function(data){
  var self = this;

  self.id =  ko.observable();
  self.username =  ko.observable();
  self.first_name =  ko.observable();
  self.last_name =  ko.observable();
  self.email =  ko.observable();
  self.password =  ko.observable();
  self.cpassword =  ko.observable();
  self.profile_picture = ko.observable();
  self.selected = ko.observable(false);

  for (var i in data){
    self[i] = ko.observable(data[i]);
      }

  self.full_name = ko.computed(function() {
        return self.first_name() + " " + this.last_name();
    }, self);
   
}

function usernameIsValid(username) {
    return /^[0-9a-zA-Z]+$/.test(username);
}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

var NewUser = function(){
  var self = this;

  self.id =  ko.observable("");
  self.username =  ko.observable("");
  self.first_name =  ko.observable("");
  self.last_name =  ko.observable("");
  self.email =  ko.observable("");
  self.password =  ko.observable("");
  self.cpassword =  ko.observable("");
  self.error = ko.observable();


   
   self.valid = ko.computed(function() {
    if (!self.username()){
      self.error("Username Required.")
      return false;
    }else if(!usernameIsValid(self.username())){
      self.error( "Username Invalid Characters.")
      return false;
    }
    self.error("");
    
    if (self.username().length <6){
      self.error("Username Must be at Least 6 Character long.")
      return false;
    }
    self.error("");
    if (!self.first_name()){
      self.error("First Name Required.")
      return false;
    }
    self.error("");
    
    if (!self.email()){
      self.error("Email Required.")
      return false;
    }else if(!validateEmail(self.email())){
      self.error("Email Invalid.")
      return false;
    }
    self.error("");
     if (self.password().length <6){
      self.error("Password Must be at Least 6 Character long.")
      return false;
    }
    self.error("");
    if(self.password() != self.cpassword()){
      self.error("Pasword Miss Match");
      return false;
    }
    self.error("");
    return true;
    }, self);
}

var Role = function (data){
  var self = this;
  self.id = ko.observable();
  self.user = ko.observable();
  self.users = ko.observableArray();
  self.group_name = ko.observable();
  self.started_at = ko.observable();
  self.group = ko.observable();
  self.site = ko.observable();
  self.project = ko.observable();
  self.organization = ko.observable();
  self.super_organization = ko.observable();

  for (var i in data){
    if(i == "user"){
      self.user(new User(data[i]));
     
    }else{
    self[i] = ko.observable(data[i]);
      }
    }
  
  self.rmrole = function(){
   vm.unAssignUserROle(self.id());
   
  };


  self.detail = function(){
    vm.showDetail(self);

  };

}



var Project = function(data){
  var self = this;
   
  self.id = ko.observable();
  self.type_label = ko.observable();
  self.organization_label = ko.observable();
  self.latitude = ko.observable();
  self.longitude = ko.observable();
  self.name = ko.observable();
  self.phone = ko.observable();
  self.fax = ko.observable();
  self.email = ko.observable();
  self.address = ko.observable();
  self.website = ko.observable();
  self.donor = ko.observable();
  self.public_desc = ko.observable();
  self.additional_desc = ko.observable();
  self.logo = ko.observable();
  self.is_active = ko.observable();
  self.location = ko.observable();
  self.date_created = ko.observable();
  self.type = ko.observable();
  self.organization = ko.observable();
  self.selected = ko.observable(false);

  for (var i in data){
    self[i] = ko.observable(data[i]);
      }   

 
}

var Region =function (data, project){
  self = this;
  self.id = ko.observable();
  self.name = ko.observable();
  self.identifier = ko.observable();
  self.selected = ko.observable(false);
  
  for (var i in data){
    self[i] = ko.observable(data[i]);
      }
  self.url= ko.observable("/fieldsight/api/project/"+ project +"/regional-sites/"+self.id()+"/");
}


var Site = function(data){
  var self = this;
   
  self.id = ko.observable();
  self.type_label = ko.observable();
  self.organization_label = ko.observable();
  self.latitude = ko.observable();
  self.longitude = ko.observable();
  self.name = ko.observable();
  self.phone = ko.observable();
  self.fax = ko.observable();
  self.email = ko.observable();
  self.address = ko.observable();
  self.website = ko.observable();
  self.donor = ko.observable();
  self.public_desc = ko.observable();
  self.additional_desc = ko.observable();
  self.logo = ko.observable();
  self.is_active = ko.observable();
  self.location = ko.observable();
  self.date_created = ko.observable();
  self.type = ko.observable();
  self.organization = ko.observable();
  self.selected = ko.observable(false);




  for (var i in data){
    self[i] = ko.observable(data[i]);
      }   
}

var SiteVM = function(level, pk){
  var self=this;
  self.group = ko.observable("Site Supervisor");

  self.search_key_supervisor = ko.observable();
  self.supervisors = ko.observableArray();
  self.allSupervisors = ko.observableArray();

  self.reviewers = ko.observableArray();
  self.allReviewers = ko.observableArray();
  
  self.available_supervisors = ko.observableArray(); 
  self.available_reviewers = ko.observableArray(); 
  // available ie users not in current list.
  self.search_key_supervisor = ko.observable();
  self.search_key_reviewer = ko.observable();

  self.setSelectedGroup = function(selected){
    self.group(selected);
    };


  self.add = function(){
    vm.addRole(self.group());  
  };
  
 

  self.loadSupervisor = function(){
    App.showProcessing();
        $.ajax({
            url: '/userrole/api/people/'+ String(level) + '/' + String(pk),
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                self.supervisors([]);
                self.reviewers([]);
                App.hideProcessing();
                ko.utils.arrayMap(response, function(item) {
                  if (item.group == "Site Supervisor"){
                        self.supervisors.push( new Role(item));
                      }else if (item.group == "Reviewer"){
                        self.reviewers.push(new Role(item));
                      }
                    });
                  
                self.allSupervisors(self.supervisors());
                self.allReviewers(self.reviewers());


            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };

  self.search_key_supervisor.subscribe(function (newValue) {
    if (!newValue) {
        self.supervisors(self.allSupervisors());
    } else {
        filter_data = ko.utils.arrayFilter(self.allSupervisors(), function(item) {
            return ko.utils.stringStartsWith(item.user().first_name().toLowerCase(), newValue);
        });
        self.supervisors(filter_data);
    }
    });

  self.search_key_reviewer.subscribe(function (newValue) {
    if (!newValue) {
        self.reviewers(self.allReviewers());
    } else {
        filter_data = ko.utils.arrayFilter(self.allReviewers(), function(item) {
            return ko.utils.stringStartsWith(item.user().first_name().toLowerCase(), newValue);
        });
        self.reviewers(filter_data);
    }
    });



  self.loadSupervisor();

};

var ProjectVM = function(level, pk){
  var self=this;
  self.group = ko.observable("Project Manager");

  self.search_key = ko.observable();
  self.projectManagers = ko.observableArray();
  self.allProjectManagers = ko.observableArray();
  self.allProjectDonors = ko.observableArray();
  self.projectDonors = ko.observableArray();
 
  
  self.available_projectManagers = ko.observableArray(); 



  self.new_role = ko.observable();
  self.new_invite = ko.observable();
  self.sites = ko.observableArray();
  self.site = ko.observableArray();
  self.allsites = ko.observableArray();
  
  self.allsiteid = ko.observableArray();
  self.allsiteid([]);
  self.all_selected_sites = ko.observableArray();
  self.all_selected_sites([]);
  


  self.add = function(){
    vm.addRole(self.group());  
  };
  
 

  self.loadProjectManagers = function(){
    App.showProcessing();
        $.ajax({
            url: '/userrole/api/people/'+ String(level) + '/' + String(pk),
            method: 'GET',
            dataType: 'json',
            success: function (response) {
                App.hideProcessing();
               var mappedData = ko.utils.arrayMap(response, function(item) {
                        return new Role(item);
                    });
                self.allProjectManagers(mappedData);

                self.projectManagers(mappedData);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };

self.loadProjectDonors = function(){
    App.showProcessing();
        $.ajax({
            url: '/userrole/api/doners/'+ String(pk),
            method: 'GET',
            dataType: 'json',
            success: function (response) {
                App.hideProcessing();
               var mappedData = ko.utils.arrayMap(response, function(item) {
                        return new Role(item);
                    });
                self.allProjectDonors(mappedData);

                self.projectDonors(mappedData);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };


  // self.search_key.subscribe(function (newValue) {
  //   if (!newValue) {
  //       self.projectManagers(self.allProjectManagers());
  //   } else {
  //       filter_data = ko.utils.arrayFilter(self.allProjectManagers(), function(item) {
  //           return ko.utils.stringStartsWith(item.user().first_name().toLowerCase(), newValue.toLowerCase());
  //       });
  //       self.projectManagers(filter_data);
  //   }
  //   });

  
  self.loadProjectManagers();
 self.loadProjectDonors();


  self.loadAllSites = function(){
    App.showProcessing();
        $.ajax({
            url: proj_site_url,
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
               var mappedData = ko.utils.arrayMap(response, function(item) {
                        
                        site = new Site(item);
                        self.allsiteid.push(site);
                        console.log(site.id());
                        return site;


                    });

                self.sites(mappedData);
                self.allsites(mappedData);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };

self.setSiteSelected = function(site){
 
   if (self.all_selected_sites.indexOf(site) < 0) {
    self.all_selected_sites.push(site);
        
  }else{
    self.all_selected_sites.remove(site);
    
  }
    console.log("site");
  console.log(self.all_selected_sites());
        return true;
  };    


  self.setAllAssignSiteAsSelected = function(site){
   // console.log(self.alluserid());
   self.all_selected_sites([]);
  
   ko.utils.arrayForEach(self.sites(), function(site) {

   site.selected(true);
   // console.log(site.selected());
   
   
    });  
   self.all_selected_sites(self.allsites().slice(0));
    
  }; 


  self.setAllSiteUnSelected = function(site){
   // console.log(self.alluserid());
   ko.utils.arrayForEach(self.sites(), function(site) {

   site.selected(false);
   // console.log(site.selected());
   // console.log(all_selected_users());
    });   
    self.all_selected_sites([]);
   
  };

  self.search_key.subscribe(function (newValue) {
   
    if (!newValue) {
        self.sites(self.allsites());
    } else {
        filter_data = ko.utils.arrayFilter(self.allsites(), function(item) {
            return ko.utils.stringStartsWith(item.name().toLowerCase(), newValue.toLowerCase());
        });
        self.sites(filter_data);
    }
    });
  

    var inviteurl = '/fieldsight/sendmultiusermultilevelinvite/';
   
    

    var invitepssuccess =  function (response) {
                App.hideProcessing();

                App.notifyUser(
                        'User Invited Sucess',
                        'success'
                    );

            };

    var invitepsfailure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON[0];
                App.hideProcessing();
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };



    self.invitereviewersSites = function(){
          group = 'Reviewer';
          self.inviteforemailsSites();
    }
    self.invitesupervisorsSites = function(){
        group = 'Site Supervisor';
        self.inviteforemailsSites();
    }

    self.invitereviewersRegions = function(){
          group = 'Reviewer';
          self.inviteforemailsRegions();
    }
    self.invitesupervisorsRegions = function(){
        group = 'Site Supervisor';
        self.inviteforemailsRegions();
    }

    self.invite_supervisors_regions = function(){
      group = 'Region Supervisor';
      self.invite_for_emails_regions();
   }

   self.invite_reviewers_regions = function(){
    group = 'Region Reviewer';
    self.invite_for_emails_regions();
}


function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

function validateemail(email) {
  if (validateEmail(email)) {
        return {
        multiemailstatus: true,
        email: email
        };

  } 
        return {
            multiemailstatus: false,
            email: email
            };
  
  
}


function multiemailvalidate(entry) {
  
    email_res = validateemail(entry);
    
    if(email_res.multiemailstatus == false){
      multiemailstatus=false;


      }
    }
  self.inviteforemailsSites = (function () {
    App.showProcessing();
    var emails = emails2;
    if (!emails[0]) {
      App.hideProcessing();
        alert("Please insert an email to invite.");
    } else {
          multiemailstatus=true;
          emails.forEach(multiemailvalidate);
  
            if(multiemailstatus == true ){ 
            self.new_invite({'group':group, 'emails':emails, 'levels':[], 'leveltype':'site'});
 
            if(!self.all_selected_sites()[0]){
              App.hideProcessing();
              alert("No Sites Selected to assign to.");
              return false;
            }    
             
            
            ko.utils.arrayMap(self.all_selected_sites(), function(item) {
                    self.new_invite().levels.push(item.id);
                    });
            console.log(ko.toJS(self.new_invite()));
   
             App.remotePost(inviteurl, ko.toJS(self.new_invite()), invitepssuccess, invitepsfailure);
           }
          else{ App.hideProcessing(); 
            alert('Contains Invalid Email'); }
    }
    });


  self.invite_for_emails_regions = (function () {
    App.showProcessing();
    var emails = emails2;
    if (!emails[0]) {
      App.hideProcessing();
        alert("Please insert an email to invite.");
    } else {
          multiemailstatus=true;
          emails.forEach(multiemailvalidate);
  
            if(multiemailstatus == true ){ 
            self.new_invite({'group':group, 'emails':emails, 'levels':[], 'leveltype':'region'});
 
            if(!self.all_selected_regions()[0]){
              App.hideProcessing();
              alert("No Regions Selected to assign to.");
              return false;
            }    
             
           
            ko.utils.arrayMap(self.all_selected_regions(), function(item) {
                    self.new_invite().levels.push(item.id);
                    });
            console.log(ko.toJS(self.new_invite()));
   
             App.remotePost(inviteurl, ko.toJS(self.new_invite()), invitepssuccess, invitepsfailure);
           }
          else{ App.hideProcessing(); 
            alert('Contains Invalid Email'); }
    }
    });

    self.inviteforemailsRegions = (function () {
      App.showProcessing();
      var emails = emails2;
      if (!emails[0]) {
        App.hideProcessing();
          alert("Please insert an email to invite.");
      } else {
            multiemailstatus=true;
            emails.forEach(multiemailvalidate);
    
              if(multiemailstatus == true ){ 
              self.new_invite({'group':group, 'emails':emails, 'levels':[], 'leveltype':'region'});
   
              if(!self.all_selected_regions()[0]){
                App.hideProcessing();
                alert("No Regions Selected to assign to.");
                return false;
              }    
               
             
              ko.utils.arrayMap(self.all_selected_regions(), function(item) {
                      self.new_invite().levels.push(item.id);
                      });
              console.log(ko.toJS(self.new_invite()));
     
               App.remotePost(inviteurl, ko.toJS(self.new_invite()), invitepssuccess, invitepsfailure);
             }
            else{ App.hideProcessing(); 
              alert('Contains Invalid Email'); }
      }
      });
    
  
  
                 

  // 
    
    

    self.allRegions = ko.observableArray();
    self.regions = ko.observableArray();
    self.all_selected_regions = ko.observableArray();
    self.all_selected_regions([]);
    self.loadRegionalSites = ko.observable();
    self.showsites = ko.observable(false);
    self.region_search_key = ko.observable();
      self.loadAllRegions = function(){
      App.showProcessing();
        $.ajax({
            url: proj_region_url,
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
               var mappedData = ko.utils.arrayMap(response, function(item) {
                        
                        region = new Region(item, pk);
                        return region;


                    });

                self.regions(mappedData);
                self.allRegions(mappedData);
            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };

self.loadRegionalSites.subscribe(function (newValue) {
    if(newValue){
        proj_site_url = newValue;
        self.loadAllSites();
        self.showsites(true);
      }
    else{
      self.showsites(false);
    }
    });

self.setRegionSelected = function(region){
 
   if (self.all_selected_regions.indexOf(region) < 0) {
    self.all_selected_regions.push(region);
        
  }else{
    self.all_selected_regions.remove(region);
    
  }
  console.log("region");
  console.log(self.all_selected_regions());
        return true;
  };    


  self.setAllAssignRegionAsSelected = function(region){
   self.all_selected_regions([]);
  
   ko.utils.arrayForEach(self.regions(), function(region) {

   region.selected(true);
    console.log(region.selected());
   
   
    });  
   self.all_selected_regions(self.allRegions().slice(0));
    
  }; 

  self.setAllRegionUnSelected = function(region){
   // console.log(self.alluserid());
   ko.utils.arrayForEach(self.regions(), function(region) {

   region.selected(false);
   // console.log(region.selected());
   // console.log(all_selected_users());
    });   
    self.all_selected_regions([]);
   
  };

  self.region_search_key.subscribe(function (newValue) {
   
    if (!newValue) {
        self.regions(self.allRegions());
    } else {
        filter_data = ko.utils.arrayFilter(self.allRegions(), function(item) {
            return (((item.name() != null) ? ko.utils.stringStartsWith(item.name().toLowerCase(), newValue):false) || ko.utils.stringStartsWith(item.identifier().toLowerCase(), newValue.toLowerCase()));
        });
        self.regions(filter_data);
    }
    });




    self.assignselectedreviewer = function(){
         
            
            self.doAssign('Reviewer');
         
    };
    self.assignselectedsupervisor = function(){
       
           
            self.doAssign('Site Supervisor');
       
    };

    self.assign_selected_region_supervisor = function(){
       
      self.doAssign('Region Supervisor');
 
  };

  self.assign_selected_reviewer = function(){
         
            
    self.doAssign('Region Reviewer');
 
  };

  self.assign_selected_to_project = function(){
       
    self.doAssignToEntireProject();

};

self.doAssignToEntireProject = function(){
  App.showProcessing();
  alert("You will be assign to this project.");


   if (!all_selected_users().length){
    alert("No Users Selected to Assign to.");
    App.hideProcessing();
    return false;
  }
  
  self.new_role({'users':[]});
  
  
  ko.utils.arrayMap(all_selected_users(), function(item) {
                  console.log(item.user().id);
                  self.new_role().users.push(item.user().id);
                  });

  var url = assign_users_to_entire_project_url;
  console.log('New roleeeeeeee', ko.toJS(self.new_role()));
  

  var success =  function (response) {
              App.hideProcessing();

              App.notifyUser(
                      'User Assigned Sucess',
                      'success'
                  );

          };
  var failure =  function (errorThrown) {
    var err_message = errorThrown.responseJSON[0];
              App.hideProcessing();
              App.notifyUser(
                      err_message,
                      'error'
                  );

          };

     App.remotePost(url, ko.toJS(self.new_role()), success, failure);  
};


    self.doAssign = function(group){
    App.showProcessing();

     if (!all_selected_users().length){
      alert("No Users Selected to Assign to.");
      App.hideProcessing();
      return false;
    }
    if(type == "region"){

    if (!self.all_selected_regions().length){
      alert("No Regions Selected to Assign to.");
      App.hideProcessing();
      return false;
    }
    self.new_role({'group':group, 'users':[], 'regions':[]});
    
    

    ko.utils.arrayMap(self.all_selected_regions(), function(item) {
                    console.log(item.id());
                    self.new_role().regions.push(item.id);
                    });
    }
    else{
    if (!self.all_selected_sites().length){
      alert("No Sites Selected to Assign to.");
      App.hideProcessing();
      return false;
    }
    
    self.new_role({'group':group, 'users':[], 'sites':[]});
    
    

    ko.utils.arrayMap(self.all_selected_sites(), function(item) {
                    console.log(item.id());
                    self.new_role().sites.push(item.id);
                    });
    }

    
    ko.utils.arrayMap(all_selected_users(), function(item) {
                    console.log(item.user().id);
                    self.new_role().users.push(item.user().id);
                    });

    var url = assignurl;
    console.log(ko.toJS(self.new_role()))
    

    var success =  function (response) {
                App.hideProcessing();

                App.notifyUser(
                        'User Assigned Sucess',
                        'success'
                    );

            };
    var failure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON[0];
                App.hideProcessing();
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };

       App.remotePost(url, ko.toJS(self.new_role()), success, failure);  
};
    

    if(type == "region"){
      self.loadAllRegions();
    }
    else{
      self.loadAllSites();
  
    }


}

var SuperOrgVM = function(level, pk){
  var self=this;
  self.group = ko.observable("Super Organization Admin");
  self.new_role = ko.observable();
  self.new_invite = ko.observable();
  self.admins = ko.observableArray();
  self.allAdmins = ko.observableArray();
  self.projects = ko.observableArray();
  self.project = ko.observableArray();
  self.allprojects = ko.observableArray();
  self.search_key = ko.observable();
  self.allprojectid = ko.observableArray();
  self.allprojectid([]);
  self.all_selected_projects = ko.observableArray();
  self.all_selected_projects([]);
  self.available_admins = ko.observableArray();
  self.add = function(){
    vm.addRole(self.group());
  };



  self.loadAdmins = function(){
    App.showProcessing();
        $.ajax({
            url: '/userrole/api/people/'+ String(level) + '/' + String(pk),
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
               var mappedData = ko.utils.arrayMap(response, function(item) {
                        return new Role(item);
                    });
                self.allAdmins(mappedData);

                self.admins(mappedData);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };







    self.loadAdmins();


    self.loadAllProjects = function(){
    App.showProcessing();
        $.ajax({
            url: proj_site_url,
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
               var mappedData = ko.utils.arrayMap(response, function(item) {

                        project = new Project(item);
                        self.allprojectid.push(project);
                        console.log(project.id());
                        return project;


                    });

                self.projects(mappedData);
                self.allprojects(mappedData);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };

  self.setSelected = function(project){
   if (self.all_selected_projects.indexOf(project) < 0) {
    self.all_selected_projects.push(project);

  }else{
    self.all_selected_projects.remove(project);

  }

        return true;
  };

  self.setAllAssignAsSelected = function(project){


   self.all_selected_projects([]);

   ko.utils.arrayForEach(self.projects(), function(project) {

   project.selected(true);
   // console.log(project.selected());


    });
   self.all_selected_projects(self.allprojects().slice(0));

  };

  self.setAllUnSelected = function(project){
   // console.log(self.alluserid());
   ko.utils.arrayForEach(self.projects(), function(project) {

   project.selected(false);
   // console.log(project.selected());
   // console.log(all_selected_users());
    });
    self.all_selected_projects([]);

  };

  self.search_key.subscribe(function (newValue) {

    if (!newValue) {
        self.projects(self.allprojects());
    } else {
        filter_data = ko.utils.arrayFilter(self.allprojects(), function(item) {
            console.log(item.name());
            return ko.utils.stringStartsWith(item.name().toLowerCase(), newValue.toLowerCase());
        });
        self.projects(filter_data);
    }
    });


    var inviteurl = '/fieldsight/sendmultiusermultilevelinvite/';



    var invitepssuccess =  function (response) {
                App.hideProcessing();

                App.notifyUser(
                        'User Invited Sucess',
                        'success'
                    );

            };

    var invitepsfailure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON[0];
                App.hideProcessing();
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };




function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

function validateemail(email) {
  if (validateEmail(email)) {
        return {
        multiemailstatus: true,
        email: email
        };

  }
        return {
            multiemailstatus: false,
            email: email
            };


}


function multiemailvalidate(entry) {

    email_res = validateemail(entry);

    if(email_res.multiemailstatus == false){
      multiemailstatus=false;


      }
    }


  self.inviteforemails = (function (newValue) {
    App.showProcessing();

    var emails = emails2;
    console.log(emails);
    if (!emails[0]) {
        App.hideProcessing();
        alert("Please insert an email to invite.");
        return false;

    } else {
          multiemailstatus=true;
          emails.forEach(multiemailvalidate);
          if(!self.all_selected_projects()[0])
          {
            App.hideProcessing();
            alert("No Teams Selected.");
            return false;
          }
          if(multiemailstatus == true ){
            self.new_invite({'group':'Project Manager', 'emails':emails, 'levels':[], 'leveltype':'project'});

            ko.utils.arrayMap(self.all_selected_projects(), function(item) {
                    self.new_invite().levels.push(item.id);
                    });
            console.log(ko.toJS(self.new_invite()));

             App.remotePost(inviteurl, ko.toJS(self.new_invite()), invitepssuccess, invitepsfailure);
           }
          else{ App.hideProcessing();
            alert('Contains Invalid Email'); }
    }
    });



  //
    self.loadAllProjects();
    self.doAssign = function(){
    App.showProcessing();
    self.new_role({'group':'Super Organization Admin', 'users':[], 'projects':[]});

    ko.utils.arrayMap(all_selected_users(), function(item) {
                    console.log(item.user().id);
                    self.new_role().users.push(item.user().id);
                    });

    ko.utils.arrayMap(self.all_selected_projects(), function(item) {
                    console.log(item.id());
                    self.new_role().projects.push(item.id);
                    });
       // App.showProcessing();

    var url = assignurl;
    console.log(ko.toJS(self.new_role()))


    var success =  function (response) {
                App.hideProcessing();

                App.notifyUser(
                        'User Assigned Sucess',
                        'success'
                    );

            };
    var failure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON[0];
                App.hideProcessing();
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };

       App.remotePost(url, ko.toJS(self.new_role()), success, failure);
};
}


var OrgVM = function(level, pk){
  var self=this;
  self.group = ko.observable("Organization Admin");
  self.new_role = ko.observable();
  self.new_invite = ko.observable();
  self.admins = ko.observableArray();
  self.allAdmins = ko.observableArray();
  self.projects = ko.observableArray();
  self.project = ko.observableArray();
  self.allprojects = ko.observableArray();
  self.search_key = ko.observable();
  self.allprojectid = ko.observableArray();
  self.allprojectid([]);
  self.all_selected_projects = ko.observableArray();
  self.all_selected_projects([]);
  self.available_admins = ko.observableArray(); 
  self.add = function(){
    vm.addRole(self.group());  
  };
  
 

  self.loadAdmins = function(){
    App.showProcessing();
        $.ajax({
            url: '/userrole/api/people/'+ String(level) + '/' + String(pk),
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
               var mappedData = ko.utils.arrayMap(response, function(item) {
                        return new Role(item);
                    });
                self.allAdmins(mappedData);

                self.admins(mappedData);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };




   
  
    
    self.loadAdmins();


    self.loadAllProjects = function(){
    App.showProcessing();
        $.ajax({
            url: proj_site_url,
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
               var mappedData = ko.utils.arrayMap(response, function(item) {
                        
                        project = new Project(item);
                        self.allprojectid.push(project);
                        console.log(project.id());
                        return project;


                    });

                self.projects(mappedData);
                self.allprojects(mappedData);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };

  self.setSelected = function(project){
   if (self.all_selected_projects.indexOf(project) < 0) {
    self.all_selected_projects.push(project);
        
  }else{
    self.all_selected_projects.remove(project);
    
  }
 
        return true;
  };    

  self.setAllAssignAsSelected = function(project){


   self.all_selected_projects([]);
  
   ko.utils.arrayForEach(self.projects(), function(project) {

   project.selected(true);
   // console.log(project.selected());
   
   
    });  
   self.all_selected_projects(self.allprojects().slice(0));
    
  }; 

  self.setAllUnSelected = function(project){
   // console.log(self.alluserid());
   ko.utils.arrayForEach(self.projects(), function(project) {

   project.selected(false);
   // console.log(project.selected());
   // console.log(all_selected_users());
    });   
    self.all_selected_projects([]);
   
  };

  self.search_key.subscribe(function (newValue) {
   
    if (!newValue) {
        self.projects(self.allprojects());
    } else {
        filter_data = ko.utils.arrayFilter(self.allprojects(), function(item) {
            console.log(item.name());
            return ko.utils.stringStartsWith(item.name().toLowerCase(), newValue.toLowerCase());
        });
        self.projects(filter_data);
    }
    });
  

    var inviteurl = '/fieldsight/sendmultiusermultilevelinvite/';
   
    

    var invitepssuccess =  function (response) {
                App.hideProcessing();

                App.notifyUser(
                        'User Invited Sucess',
                        'success'
                    );

            };

    var invitepsfailure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON[0];
                App.hideProcessing();
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };




function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

function validateemail(email) {
  if (validateEmail(email)) {
        return {
        multiemailstatus: true,
        email: email
        };

  } 
        return {
            multiemailstatus: false,
            email: email
            };
  
  
}


function multiemailvalidate(entry) {
  
    email_res = validateemail(entry);
    
    if(email_res.multiemailstatus == false){
      multiemailstatus=false;


      }
    }


  self.inviteforemails = (function (newValue) {
    App.showProcessing();

    var emails = emails2;
    console.log(emails);
    if (!emails[0]) {
        App.hideProcessing();
        alert("Please insert an email to invite.");
        return false;
        
    } else {
          multiemailstatus=true;
          emails.forEach(multiemailvalidate);
          if(!self.all_selected_projects()[0])
          {
            App.hideProcessing();
            alert("No Projects Selected.");
            return false;
          }
          if(multiemailstatus == true ){ 
            self.new_invite({'group':'Project Manager', 'emails':emails, 'levels':[], 'leveltype':'project'});
             
            ko.utils.arrayMap(self.all_selected_projects(), function(item) {
                    self.new_invite().levels.push(item.id);
                    });
            console.log(ko.toJS(self.new_invite()));
   
             App.remotePost(inviteurl, ko.toJS(self.new_invite()), invitepssuccess, invitepsfailure);
           }
          else{ App.hideProcessing();
            alert('Contains Invalid Email'); }
    }
    });
  
               

  // 
    self.loadAllProjects();
    self.doAssign = function(){
    App.showProcessing();
    self.new_role({'group':'Organization Admin', 'users':[], 'projects':[]});
    
    ko.utils.arrayMap(all_selected_users(), function(item) {
                    console.log(item.user().id);
                    self.new_role().users.push(item.user().id);
                    });

    ko.utils.arrayMap(self.all_selected_projects(), function(item) {
                    console.log(item.id());
                    self.new_role().projects.push(item.id);
                    });
       // App.showProcessing();
     
    var url = assignurl;
    console.log(ko.toJS(self.new_role()))
    

    var success =  function (response) {
                App.hideProcessing();

                App.notifyUser(
                        'User Assigned Sucess',
                        'success'
                    );

            };
    var failure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON[0];
                App.hideProcessing();
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };

       App.remotePost(url, ko.toJS(self.new_role()), success, failure);  
};
}

function ManagePeopleViewModel(pk, level, organization) {
  var self=this;
  self.pk = pk;
  self.organization = organization;
  self.level = level;
  self.users = ko.observableArray();
  self.available_users = ko.observableArray();
  
  self.add_people_form_visibility = ko.observable(false);
  self.add_user_form_visibility = ko.observable(false);
  
  self.detail_people_form_visibility = ko.observable(false);
  self.user = ko.observable();
  self.role = ko.observable();
  self.new_role = ko.observable();
  self.new_user = ko.observable();
  self.users = ko.observableArray();
  self.allusers = ko.observableArray();
  self.alluserid = ko.observableArray();
  self.alluserid([]);
  self.search_key = ko.observable();
  self.currentVm = ko.observable();
  
  self.siteVm = ko.observable();
  self.projectVm = ko.observable();
  self.orgVm = ko.observable();
  self.superOrgVm = ko.observable();

  self.addRole = function(group){
    

    var mapped_available_users = [];

    if(group == "Site Supervisor"){
      if(self.siteVm().allSupervisors().length <1){
        self.available_users(self.users());

      }else{


      mapped_available_users = ko.utils.arrayFilter(self.users(), function(item) {
            return notFound(item.id(), self.siteVm().allSupervisors());
        });
      self.available_users(mapped_available_users);

    }
  }else if(group == "Reviewer"){
      if(self.siteVm().allReviewers().length <1){
        self.available_users(self.users());

      }else{

      mapped_available_users = ko.utils.arrayFilter(self.users(), function(item) {
            return notFound(item.id(), self.siteVm().allReviewers());
        });
      self.available_users(mapped_available_users);

      }

     }else if(group == "Project Manager"){
      if(self.projectVm().allProjectManagers().length <1){
        self.available_users(self.users());

      }else{

      mapped_available_users = ko.utils.arrayFilter(self.users(), function(item) {
            return notFound(item.id(), self.projectVm().allProjectManagers());
        });
      self.available_users(mapped_available_users);

      }

     }else if(group == "Organization Admin"){
      if(self.orgVm().allAdmins().length <1){
        self.available_users(self.users());

      }else{

      mapped_available_users = ko.utils.arrayFilter(self.users(), function(item) {
            return notFound(item.id(), self.orgVm().allAdmins());
        });
      self.available_users(mapped_available_users);

      }

     }
    
    

   
    self.add_people_form_visibility(true);
    if(self.available_users().length<1){
      self.addUser();

    }

  };

  self.cancelAssign = function(){
    self.add_people_form_visibility(false);
    };

  self.cancelUser = function(){
    self.add_user_form_visibility(false);
    };

    
   
 

self.unAssignUserROle = function(role_id){

    var url = '/userrole/api/people/deactivate/';

   

    var success =  function (response) {
      var level = response.role_name;
      if (level == "Site Supervisor"){

         var rm_roles = ko.utils.arrayFilter(self.siteVm().allSupervisors(), function(item) {
            return item.id() != response.role;
        });
        self.siteVm().supervisors(rm_roles);                   
        self.siteVm().allSupervisors(rm_roles);                   
        
        
      }else if (level == "Reviewer"){

         var rm_roles = ko.utils.arrayFilter(self.siteVm().allReviewers(), function(item) {
            return item.id() != response.role;
        });
        self.siteVm().reviewers(rm_roles);                   
        self.siteVm().allReviewers(rm_roles);                   
        
        
      }else if (level == "Project Manager"){

       var rm_roles = ko.utils.arrayFilter(self.projectVm().allProjectManagers(), function(item) {
            return item.id() != response.role;
        });
        self.projectVm().projectManagers(rm_roles);                   
        self.projectVm().allProjectManagers(rm_roles);                   
        
        
      }else if (level == "Organization Admin"){

       var rm_roles = ko.utils.arrayFilter(self.orgVm().allAdmins(), function(item) {
            return item.id() != response.role;
        });
        self.orgVm().admins(rm_roles);                   
        self.orgVm().allAdmins(rm_roles);                   
        
        
      }
      var message = response.msg;
                App.hideProcessing();
               
                App.notifyUser(
                        message,
                        'success'
                    );

            };
    var failure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON;
      alert(err_message);
                App.hideProcessing();
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };
    // alert(csrf_token);
    App.remotePost(url, {'id':role_id,'level':self.level,'dashboard_pk':self.pk,}, success, failure);  

};


    self.assignreviewers = function(){
          group = 'Reviewer';
          self.doAssign();
    }
    self.assignsupervisors = function(){
        group = 'Site Supervisor';
        self.doAssign();
    }

    self.assignPM = function(){
        group = 'Project Manager';
        self.doAssign();
    }
    self.assignSuperOrgadmin = function(){
        group = 'Super Organization Admin';
        self.doAssign();
    }
    self.assignOadmin = function(){
        group = 'Organization Admin';
        self.doAssign();
    }

    self.assignDonor = function(){
        group = 'Project Donor';
        self.doAssign();
    }

  self.doAssign = function(){
    App.showProcessing();
    self.new_role(({'group':group, 'users':[]}));
    
    ko.utils.arrayMap(all_selected_users(), function(item) {
                    console.log('Userrrrrrrrrrrrrrrrrrr'+item.user().id);
                    self.new_role().users.push(item.user().id);
                    });
       // App.showProcessing();
     
    var url = '/userrole/api/people/'+ String(level) + '/' + String(pk);

    

    var success =  function (response) {
                App.hideProcessing();
                // if ((self.new_role().group() =='Site Supervisor') || self.new_role().group() =='Reviewer' ){
                //   vm.siteVm().loadSupervisor();

                // }else if(self.new_role().group() =='Project Manager'){
                //   vm.projectVm().loadProjectManagers();
                // }else if(self.new_role().group() =='Organization Admin'){
                //   vm.orgVm().loadAdmins();
                // }

                App.notifyUser(
                        'User Assigned Sucess',
                        'success'
                    );

            };
    var failure =  function (errorThrown) {
      var err_message = errorThrown.responseJSON[0];
                App.hideProcessing();
                App.notifyUser(
                        err_message,
                        'error'
                    );

            };
// console.log(self.new_role());
// console.log(CSRF_TOKEN);   
       App.remotePost(url, ko.toJS(self.new_role()), success, failure);  
    
// alert(JSON.stringify(self.new_role()));
//         $.ajax({

//             url: url,
//             type: 'POST',
//             contentType:"application/json; charset=utf-8",
//             dataType:"json",
//             data:JSON.stringify(self.new_role()),
//             // async: true,
//              beforeSend: function(request) {
//         return request.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
//     },     
//             success: function (response) {
//                 App.hideProcessing();
//                App.notifyUser(
//                         'People Assigned Sucess',
//                         'success'
//                     );


//             },
//             error: function (errorThrown) {
//                var err_message = errorThrown.responseJSON[0];
//                 App.hideProcessing();
//                 App.notifyUser(
//                         err_message,
//                         'error'
//                     );
//             }
//         });







    // self.selected_users([]);                                                                                                                  
  
    self.add_people_form_visibility(false);
    };

  self.addUser = function(){
    self.new_user(new NewUser());
    self.add_user_form_visibility(true);

  };

  self.saveUser = function(){
    if(self.new_user().valid()){
    self.saveUserData();
      
    }else{
      App.notifyUser(
                        "Please Correct form Data First",
                        'error'
                    );
    }
   };

  self.showDetail = function(role){
    self.role(role);

    self.detail_people_form_visibility(true);

  };


if (self.level == "0"){
  self.currentVm("site");
  self.siteVm(new SiteVM(level, pk));
}else if (self.level == "1"){
  self.currentVm("project");
  self.projectVm(new ProjectVM(level, pk));

}else if (self.level == "2"){
  self.currentVm("organization");
  self.orgVm(new OrgVM(level, pk));

}else if (self.level == "3"){
  self.currentVm("super_organization");
  self.superOrgVm(new SuperOrgVM(level, pk));

}  

  self.loadUsers = function(){
    App.showProcessing();
        $.ajax({
            url: '/users/list/'+ String(self.organization)+'/',
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                
                App.hideProcessing();
                var mappedData = ko.utils.arrayMap(response, function(item) {
                      return new User(item);
                    });

                self.users(mappedData);


            },
            error: function (errorThrown) {
                App.hideProcessing();
                //console.log(errorThrown);
            }
        });
  };

  //   self.saveUserData = function(){
  //   App.showProcessing();
  //   var url = '/users/list/'+ String(self.organization)+'/';
    

  //   var success =  function (response) {
  //               App.hideProcessing();
  //               self.users.push(new User(response));
  //               self.selected_users.push(new User(response));
  //               self.add_user_form_visibility(false);

  //               App.notifyUser(
  //                       'User '+response.username +'Created',
  //                       'success'
  //                   );

  //           };
  //   var failure =  function (errorThrown) {
  //     var err_message = errorThrown.responseJSON[0];
  //               App.hideProcessing();
  //               App.notifyUser(
  //                       err_message,
  //                       'error'
  //                   );

  //           };

  //   App.remotePost(url, ko.toJS(self.new_user()), success, failure);                                                                                                                    
  
  // };

  // self.loadUsers();



    self.loadAllUsers = function(){
    App.showProcessing();
        $.ajax({

            url: '/userrole/api/multiuserlist/'+ String(level) + '/' + String(pk),
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
               var mappedData = ko.utils.arrayMap(response, function(item) {
                        user = new User(item);
                        self.alluserid.push(user);
                        return user;

                    });
                self.users(mappedData);
                self.allusers(mappedData);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };

  self.setAllAssignAsSelected = function(user){
   // console.log(self.alluserid());
   all_selected_users([]);
   console.log(all_selected_users());
   console.log(self.allusers());
   ko.utils.arrayForEach(self.users(), function(user) {

   user.selected(true);
   // console.log(user.selected());
   
   
    });  
   all_selected_users(self.allusers().slice(0));
    // console.log(all_selected_users()); 
  }; 

  self.setAllUnSelected = function(user){
   // console.log(self.alluserid());
   ko.utils.arrayForEach(self.users(), function(user) {

   user.selected(false);
   // console.log(user.selected());
   // console.log(all_selected_users());
    });   
    all_selected_users([]);
   
  }; 
  self.search_key.subscribe(function (newValue) {
    // console.log(all_selected_users);
    if (!newValue) {
        self.users(self.allusers());
    } else {
        filter_data = ko.utils.arrayFilter(self.allusers(), function(item) {
            return ko.utils.stringStartsWith(item.user().email.toLowerCase(), newValue.toLowerCase());
        });
        self.users(filter_data);
    }
    });
  self.setSelected = function(user){
   // console.log(all_selected_users.indexOf(user));
   if (all_selected_users.indexOf(user) < 0) {
    all_selected_users.push(user);
        
  }else{
    all_selected_users.remove(user);
    
  }
  // console.log(all_selected_users());
        return true;
  };                                                                

  self.loadAllUsers();
};
