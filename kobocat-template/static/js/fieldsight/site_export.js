
window.app = new Vue({
  el: '#export_button',
  <p v-if="this.terms_and_labels.length==0">
    template: `<a href="#" @click="generateXls" v-bind:class="[configure_settings.is_project_dashboard ? 'btn btn-primary' : 'btn btn-sm btn-primary']"><i class="la la-table"></i> Export {{this.terms_and_labels[0].site}} data</a>`,
  <p v-else="this.terms_and_labels.length==0">
      template: `<a href="#" @click="generateXls" v-bind:class="[configure_settings.is_project_dashboard ? 'btn btn-primary' : 'btn btn-sm btn-primary']"><i class="la la-table"></i> Export sites data</a>`,


  data: {
        load_next_url: configure_settings.url,
        configure_settings: configure_settings,
        terms_and_labels: [],
     },

  methods:{
    generateXls : function (){
    var self = this;
    self.loading = true;

    function successCallback(response) {
        alert(response.body.message);
        self.loading = false;
    }

    function errorCallback() {
        self.loading = false;
        alert("Error occured please try again.");
    }

    self.$http.get(self.load_next_url).then(successCallback, errorCallback);

    },
  },
  created(){
    var self= this;
  },

   mounted() {
     function errorCallback() {
            callback(new Error('Failed to load Project Terms and Labels data.'));
        }

     function successCallback(response) {
        this.terms_and_labels = response.body;
        if(response.body[0]){
             this.site=response.body[0].site;
             console.log('Site', this.site);

        }

    }
    this.$http.get('/fieldsight/api/project-terms-labels/'+ this.configure_settings.terms_and_labels_project_id).then(successCallback, errorCallback)

    },


})


window.app = new Vue({
  el: '#export_stage_progress_button',
  template: `<a href="#" @click="generateProgress" class="btn btn-primary"><i class="la la-table"></i> Progress Data </a>`,
  data: {
        genarete_excel_url: configure_settings.genarete_excel_url,
     },

  methods:{
    generateProgress : function (){
    var self = this;
    self.loading = true;

    function successCallback(response) {
        alert(response.body.message);
        self.loading = false;
    }

    function errorCallback() {
        self.loading = false;
        alert("Error occured please try again.");
    }

    self.$http.get(self.genarete_excel_url).then(successCallback, errorCallback);

    },
  },
  created(){
    var self= this;
  },

})

