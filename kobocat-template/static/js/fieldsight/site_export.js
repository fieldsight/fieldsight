
window.app = new Vue({
  el: '#export_button',
  template: `<a href="#" @click="generateXls" v-bind:class="[configure_settings.is_project_dashboard ? 'btn btn-primary' : 'btn btn-sm btn-primary']"><i class="la la-table"></i> Export sites data</a>`,
  data: {
        load_next_url: configure_settings.url,
        configure_settings: configure_settings
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

