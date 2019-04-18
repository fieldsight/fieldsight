
var bus = new Vue();


Vue.component('Modal', {
  template: '#modal-template',
  props: ['show'],
  methods: {
    close: function () {
      this.$emit('close');
    }
  },
  mounted: function () {
    document.addEventListener("keydown", (e) => {
      if (this.show && e.keyCode == 27) {
        this.close();
      }
    });
  }
});

Vue.component('NewShowTimeModal', {
  template: '#new-show-time-modal-template',
  props: ['show'],
  data: function () {
    return {
      new_type_id: '',
      new_type_name: '',
      error: '',
    };
  },
  methods: {
    close: function () {
    var self = this;
      self.$emit('close');
      self.pk = '';
      self.is_project = '';
      self.new_type_id = '';
      self.new_type_name = '';
    },
    saveNewEntry: function () {
       var self = this;
        let csrf = $('[name = "csrfmiddlewaretoken"]').val();
        let options = {headers: {'X-CSRFToken':csrf}};
        let body = {};
        body.project = self.pk;
        body.identifier = self.new_type_id;
        body.name = self.new_type_name;
        function successCallback (response){
             bus.$emit('new_entry', response.body)
            self.close();
        }

        function errorCallback (response){
            console.log(response);
            self.error = "Failed to save site type.";
        }
       self.$http.post('/fieldsight/api/site-types/', body, options).then(successCallback, errorCallback);
    }
  },
  created() {
    var self = this;
    bus.$on('new_entry_for', function(pk, is_project){
         self.pk = pk;
         self.is_project = is_project;
        }.bind(self));


  },
});


window.app = new Vue({
  el: '#app',
  template: `
  <form>
  <div class="form-group">
    <label for="exampleInputPassword1">Form Name</label>
    <input type="text" class="form-control" id="exampleInputPassword1" placeholder="New Form" v-model="kobo_form.name">
  </div>

  <a href="javascript:void(0)"   class="btn btn-primary" @click="saveForm" v-show="kobo_form.name.length>0">Create</a>
</form>

    `,
  data: {
        kobo_form : {'name': '',
        'asset_type':'survey',
         'settings': {
            "description":
            "No Description",
            "sector":"",
            "country":"",
            "share-metadata":false},
             },
             token_key : settings.token_key,
             kpi_url : settings.kpi_url,
  },

  methods:{
    saveForm: function(){
         var self = this;
         var asset_url = self.kpi_url + 'assets/';
         console.log('ASSSSSets', asset_url);
        let csrf = $('[name = "csrfmiddlewaretoken"]').val();
        let options = {headers: {'X-CSRFToken':csrf ,'Content-Type':'application/json', 'Authorization':'Token '+self.token_key}};

        function successCallback (response){
        console.log(response.body.uid);
                new PNotify({
              title: 'Form Saved',
              text: 'New Form Saved'
            });
             window.location = self.kpi_url + '#/forms/' + response.body.uid + '/edit';

        }

        function errorCallback (response){
        console.log(response.body);
          new PNotify({
          title: 'failed',
          text: 'Failed to Save Form',
          type: 'error'
        });
        }

   self.$http.post(asset_url, self.kobo_form, options)
    .then(successCallback, errorCallback);
    },


  },

  created(){
    var self= this;

  },

})