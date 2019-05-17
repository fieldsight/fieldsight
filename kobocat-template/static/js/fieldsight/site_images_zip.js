

window.app = new Vue({
  el: '#export_zip_imgs',
  template:`   <div class="pull-right">
                <span class="dropdown">
                  <a href="#" id="dropdownMenuButtonManage" class=" btn btn-sm btn-xs btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <i class="la la-download"></i> Download All
                  </a>
                  <div class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButtonManage">
                    <a class="dropdown-item" @click="generateZip('0')" v-bind:class=""><i class="la la-zip"></i> Low Quality </a>
                    <a class="dropdown-item" @click="generateZip('1')" v-bind:class=""><i class="la la-zip"></i> Medium Quality </a>
                    <a class="dropdown-item" @click="generateZip('2')" v-bind:class=""><i class="la la-zip"></i> Large Quality </a>
                  </div>
                </span>
              </div>
            `,
  data: {
        site_id: configure_settings.site_id,
     },

  methods:{
    generateZip : function (data){

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

    self.$http.get('/fieldsight/export/zip/site-images/' + self.site_id +'/' + data + '/').then(successCallback, errorCallback);

    },
  },
  created(){
    var self= this;
  },

})