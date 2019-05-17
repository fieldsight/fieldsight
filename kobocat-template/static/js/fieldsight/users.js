var User = function (data){
  self = this;
  self.id = ko.observable();
  self.first_name = ko.observable();
  self.last_name = ko.observable();
  self.profile_picture = ko.observable();
  self.is_active = ko.observable();
  self.date_joined = ko.observable();
  self.last_login = ko.observable();
  
  for (var i in data){
    self[i] = ko.observable(data[i]);
              }
  self.edit_url= ko.observable("/users/edit/"+self.id()+"/");
  self.full_name = ko.computed(function() {
        return this.first_name() + " " + this.last_name();
    }, self);

 }


  var Group = function(name, level) {
    var self = this;
        self.name = name;
        self.level = level;
    };



function UsersViewModel() {
  
  var self=this;
  // self.allUsers = ko.observableArray();
  self.users = ko.observableArray();
  self.roleList =  ko.observableArray([
            new Group("Organization Admin", 1),
            new Group("Project Managers", 2),
            new Group("Reviewer", 3),
            new Group("Site Supervisor", 4)
        ]);
  self.selectedGroup = ko.observable();

self.reloadData = function(){
  var url = '/users/api/list/all/';

    if (self.selectedGroup() != undefined){
        url = url+self.selectedGroup().level +'/';
    }
    url = url + self.search_key();
     App.showProcessing();
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
               var mappedData = ko.utils.arrayMap(response, function(item) {
                        return new User(item);
                    });
                // self.allUsers(mappedData);

                self.users(mappedData);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });

    };

  self.loadList = function(){
    App.showProcessing();
        $.ajax({
            url: '/users/api/list/all/',
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
               var mappedData = ko.utils.arrayMap(response, function(item) {
                        return new User(item);
                    });
                // self.allUsers(mappedData);

                self.users(mappedData);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
  };


  self.loadList();
  
  self.search_key = ko.observable();

  self.activeInactivate = function(user_id){
    App.showProcessing();
        $.ajax({
            url: '/users/api/alter-status/'+user_id+'/',
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
              var message = response.msg;
                App.hideProcessing();
              App.notifyUser(
                        message,
                        'success'
                    );

            },
            error: function (errorThrown) {
                App.hideProcessing();
                var err_message = errorThrown.error;
                App.notifyUser(
                        err_message,
                        'error'
                    );
            }
        });
  };

   self.activeInactiveAction = function(current_user){
    self.selected_user = ko.utils.arrayFirst(self.users(), function(user) {
   return user.id() === current_user.id();
});
    var status = self.selected_user.is_active() == true ? false : true;
    self.selected_user.is_active(status);
    self.activeInactivate(self.selected_user.id());
  };

};


