Vue.use(VueHighcharts);


window.app = new Vue({
  el: '#peoples',
  template: `
    <div class="widget-info widget-scrolling-large-list margin-top bg-white padding" data-mh="eq111">
        <div class="widget-head">
            <h4> Users </h4>
            <a class="btn btn-xs btn-primary" :href="new_people_url"><i class="la la-plus"></i></a>

            <a class="btn btn-xs btn-primary" data-toggle="collapse" href="#searchProjectManager" aria-expanded="false" aria-controls="searchProjectManager"><i class="la la-search"></i></a>
        </div>
        <div class="widget-body">
            <div class="collapse margin-bottom" id="searchProjectManager">
			<form>
				<div class="input-group input-group-sm">
					<input type="text"  v-model="search_key" @change="searchChange()" class="form-control" placeholder="Search for..." aria-label="Search for...">
					<span class="input-group-btn">
						<button class="btn btn-primary" type="button"><i class="la la-search"></i>Search</button>
					</span>
				</div>
			</form>
		    </div>

		    <a href="#" class="project-item-wrap margin-top clearfix" v-for="u in peoples"  v-on:click="profile_page(u)">
			<div class="project-logo">
				<img :src="u.image" alt="" width="50" height="50">
			</div>
			<div class="project-basic-info" >
				<h4>{{u.name}}</h4>
				<p>{{ u.email }}</p>
                <p>{{ u.phone }}</p>
			</div>
		    </a>

        </div>

    </div> `,
  data: {
        peoples: [],
        new_people_url :'',
        search_key :'',
        loading: false,
        project_id: configure_settings.project_id,
  },

  methods:{
    loadDatas : function (){
    var self = this;

    var self = this;
    self.loading = true;
    if(self.search_key){
        var options = {'name':self.search_key};

    }else{
        var options = {};

    }

    function successCallback(response) {
        self.new_people_url = response.body.new_people_url;
        self.peoples = response.body.peoples;
        self.loading = false;
    }

    function errorCallback() {
        self.loading = false;
        console.log('failed');
    }
    self.$http.get('/fieldsight/api/project_peoples/'+self.project_id+'/', {
        params: options
    }).then(successCallback, errorCallback);

    },
    heightLevel: function(){
      var self = this;
      Vue.nextTick(function () {
              $(".widget-scrolling-large-list > .widget-body, .widget-scrolling-list > .widget-body").
              niceScroll({cursorborder:"",cursorcolor:"#00628e"});
            }.bind(self));
      },
    searchChange : function (){
        var self = this;
        self.loadDatas();

    },
    profile_page : function(user){
        window.location.href = user.url;
    },
  },
  created(){
    var self= this;
    self.loadDatas();
    self.heightLevel();
  },

})

window.app = new Vue({
  el: '#graphs',
  template: `
    <div class="row">
        <div class="col-md-6">
							<div class="widget-info margin-top bg-white padding">
								<div class="widget-head">
									<h4>Form Submissions</h4>
								</div>
								<div class="widget-body">
									 <highcharts :options="submissions_data" ref="highcharts"></highcharts>
                                       <!-- <button @click="updateCredits">update credits</button> -->
								</div>
							</div>
						</div>
						<div class="col-md-6">
							<div class="widget-info margin-top bg-white padding">
								<div class="widget-head">
									<h4 v-if="this.terms_and_labels.length==0">School Progress</h4>
									<h4 v-else >{{this.terms_and_labels[0].site}} Progress</h4>
								</div>
								<div class="widget-body">
									 <highcharts :options="progress_data" ref="highcharts"></highcharts>
                                        <!-- <button @click="updateCredits">update credits</button> -->
								</div>
							</div>
						</div>

    </div> `,
  data: {
        progress_data: {},
        submissions_data :{},
        loading: false,
        project_id: configure_settings.project_id,
        scrolled: false,
        terms_and_labels: [],
        site: "School"
  },

  methods:{
    loadDatas : function (){
    var self = this;

    var self = this;
    self.loading = true;
    var options = {};



    function successCallback(response) {
        self.progress_data = {
                chart: {
                    type: 'column'
                },
              title: {
                text: this.site + ' Progress',
                x: -20 //center
              },
              subtitle: {
                text: '',
                x: -20
              },
              xAxis: {
                categories: response.body.pl
              },
              yAxis: {
                title: {
                  text: 'Progress'
                },
                plotLines: [{
                  value: 0,
                  width: 1,
                  color: '#808080'
                }]
              },
              tooltip: {
                valueSuffix: ' Site(s)'
              },
              credits: {
                enabled : false
                },
              legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0,
                enabled: false,
              },
              series: [{
                name: 'Progress',
                data: response.body.pd,
              },]
            };

        self.submissions_data = {
              title: {
                text: 'Form Submissions',
                x: -20 //center
              },
              subtitle: {
                text: 'Number of form submissions in different timeline',
                x: -20
              },
              xAxis: {
                categories: response.body.sl
              },
              yAxis: {
                title: {
                  text: 'Submissions'
                },
                plotLines: [{
                  value: 0,
                  width: 1,
                  color: '#808080'
                }]
              },
              credits: {
                enabled : false
                },
              tooltip: {
            //    valueSuffix: '°C'
              },
              legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0,
                enabled: false,
              },
              series: [{
                name: 'No OF Submissions',
                data: response.body.sd,
              }]
            };
        self.loading = false;
    }

    function errorCallback(errorResponse) {
        self.loading = false;
        console.log(errorResponse);
    }
    self.$http.get('/fieldsight/api/project_graphs/'+self.project_id+'/', {
        params: options
    }).then(successCallback, errorCallback);

    },
    updateCredits: function() {
    	var chart = this.$refs.highcharts.chart;
      chart.credits.update({
        style: {
          color: '#' + (Math.random() * 0xffffff | 0).toString(16)
        }
      });
    },
    handleScroll: function () {
        var self = this;
        if(window.scrollY>500){
//            console.log(window.scrollY);
            if(!self.loading && !self.submissions_data.hasOwnProperty("title")){
                self.loadDatas();
            }
        }
        self.scrolled = window.scrollY > 0;
  },
  heightLevel: function(){
      var self = this;
      Vue.nextTick(function () {
              $(".widget-scrolling-large-list > .widget-body, .widget-scrolling-list > .widget-body").
              niceScroll({cursorborder:"",cursorcolor:"#00628e"});
            }.bind(self));
      },


  },
  created(){
    var self= this;

    window.addEventListener('scroll', this.handleScroll);
    self.heightLevel();
  },

  mounted() {
     function errorCallback() {
            callback(new Error('Failed to load Project Terms and Labels data.'))
        }

     function successCallback(response) {
        this.terms_and_labels = response.body;
        if(response.body[0]){
             this.site=response.body[0].site;

        }

    }
    this.$http.get('/fieldsight/api/project-terms-labels/'+ this.project_id).then(successCallback, errorCallback)

    },

  destroyed () {
  window.removeEventListener('scroll', this.handleScroll);
    }

})


window.app = new Vue({
  el: '#stagedatas',
  template: `
    <div class="row"><div class="col-md-12">
              <div class="widget-info margin-top bg-white padding">
                <div class="widget-head">
                  <h4>Tabular Report</h4>
                  <a class="btn btn-xs btn-primary" v-bind:href="'/fieldsight/project/report/stage-table/'+ project_id +'/'"><i class="la la-list"></i></a>
                </div>
                <div class="widget-body">
                  <template v-if="sub_headers.length > 0 && rows.length > 0 ">
                  <div class="table-responsive">
                      <table class="table table-bordered table-hover tabular-report">
                        <thead class="thead-default">
                          <tr>
                          <template v-for="header in headers">
                            <th v-if="header['stage_order']" scope="col" :colspan="header['colspan']" :rowspan="header['rowspan']">{{ header['name'] }}</th>
                            <th v-else scope="col" :colspan="header['colspan']" :rowspan="header['rowspan']">{{ header['name'] }}</th>
                          </template>
                          </tr>
                          <tr>
                          <template v-for="sub_header in sub_headers">
                            <th scope="col">{{ sub_header[1] }}</th>
                          </template>
                          </tr>
                        </thead>
                        <tbody>

                          <tr v-for="row in rows">
                          <template v-for="cell in row">
                            <template v-if="typeof cell === 'string'">
                              <th class="cell-inactive" v-html="cell"></th>
                            </template>
                            <template v-else>
                              <th :class="cell[2]">{{ cell[1] }}</th>
                            </template>
                          </template>
                          </tr>
                        
                        </tbody>
                      </table>
                     
                  </div>
                  </template>
                  <template v-else>
                    <span>No Data</span>
                  </template>
                </div>
              </div>
            </div>
            </div>`,
  data: {
        headers: [],
        sub_headers :[],
        rows :[],
        loading: false,
        project_id: configure_settings.project_id,
        load_next_url : '/fieldsight/ProjectDashboardStageResponsesStatus/'+configure_settings.project_id+'/',
        
     },

  methods:{
    loadDatas : function (){
    var self = this;

    var self = this;
    self.loading = true;
    if(self.search_key){
        var options = {'name':self.search_key};

    }else{
        var options = {};

    }

    function successCallback(response) {
        self.headers = response.body.content.head_cols;
        self.sub_headers = response.body.content.sub_stages;
        self.rows = self.rows.concat(response.body.content.rows);
        self.load_next_url = response.body.next_page;
        self.loading = false;
    }

    function errorCallback() {
        self.loading = false;
        console.log('failed');
    }

    self.$http.get(self.load_next_url, {
        params: options
    }).then(successCallback, errorCallback);

    },
    heightLevel: function(){
      var self = this;
      Vue.nextTick(function () {
              $(".widget-scrolling-large-list > .widget-body, .widget-scrolling-list > .widget-body").
              niceScroll({cursorborder:"",cursorcolor:"#00628e"});
            }.bind(self));
      },
    searchChange : function (){
        var self = this;
        self.loadDatas();

    },
  },
  created(){
    var self= this;
    self.loadDatas();
    self.heightLevel();
  },

})

//<input v-for="(meta, index) in project.site_meta_attributes" type="checkbox" v-bind:id="meta" v-bind:value="meta" v-model="checkedNames">
                //  <label v-bind:for="meta">{{ meta }}</label>
                
window.exportSitesToProject = new Vue({
  el: '#exportSitesToProject',
  template: `
          <div>
          <div class="modal-header">
                <h5 class="modal-title" id="exportModalLabel">Import Sites</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body widget-info bg-white padding">
             
                
                <div class="widget-head">
                  <h4>Select a Project</h4>
                </div>
                <div id="logbody" class="widget-body">
                  <select v-model = "selected_project" v-on:change="loadProjectDetail">
                    <option v-for="(option, index) in projects" v-bind:value="index">
                      {{ option.name }}
                    </option>
                  </select>
                  <div>
                  <br>

                  <template v-if="project.hasOwnProperty('site_meta_attributes') && project.site_meta_attributes.length > 0 ">
                      <div class="widget-head">
                        <h4>Select Attributes you want to import</h4>
                      </div>
                      
                      <li>
                       <input type="checkbox" id="all_regions_metas" value="all_metas_selected" v-model="all_selected" v-on:change="selectAllMetas">
                        <label for="all_regions_metas">All</label>
                      </li>
                      <br>
                      <li v-for="(meta, index) in project.site_meta_attributes">
                      <input type="checkbox" v-bind:id="meta.question_name" v-bind:value="meta.question_name" v-model="selected_meta_attribs">
                        <label v-bind:for="meta.question_name">{{ meta.question_name }}</label>
                      </li>
                  </template>
                  <template v-else>
                    

                  </template>
                  <br>
                  <br>    
                  <template v-if="regions.length > 0 ">   

                      
                    <div class="widget-head">
                       <input type="checkbox" id="ignore_site_cluster" value="true" v-model="ignore_site_cluster">
                        <label for="ignore_site_cluster">Discard Regional Clustering</label>
                     <br>
                    </div>
                    
                 
                    <div class="widget-head">
                      <h4>Select Regions you want to import</h4>
                      
                    </div>
                    <li><input type="checkbox" id="all_regions_selected" value="all_regions_selected" v-model="all_selected" v-on:change="selectAllRegions">
                      <label for="all_regions_selected">All</label>
                    </li>
                    <br>
                    
                    <input type="checkbox" id="Region0" value="0" v-model="selected_region_ids">
                      <label for="Region0">UnRegioned Sites</label>
                    </li>
                    <li v-for="region in regions">
                    <input type="checkbox" v-bind:id="'Region'+region.id" v-bind:value="region.id" v-model="selected_region_ids">
                      <label v-bind:for="'Region'+region.id">{{ region.identifier }}</label>
                    </li>
                  </template>
                  <template v-else>
                   
                  </template>
                    
              
              </div>
              
            </div>
          
                        </div>
              
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-primary" v-on:click="importSites">Import</button>
              </div>
              </div>`,

  data: {
        all_selected: [],
        selected_project: -1,
        projects:[],
        project:{},
        selected_meta_attribs:[],
        regions:[],
        selected_region_ids:[],
        project_id: configure_settings.project_id,
        load_all_projects_url:'/fieldsight/api/my_projects/'+configure_settings.project_id+'/',
        ignore_site_cluster: [],
        csrf: configure_settings.csrf_token,
     },

  methods:{
    loadDatas : function (){
    var self = this;
    self.loading = true;
    if(self.search_key){
        var options = {'name':self.search_key};
    }else{
        var options = {};
    }

    function successCallback(response) {
        self.projects = response.body;
        self.loading = false;
    }

    function errorCallback() {
        self.loading = false;
        console.log('failed');
    }

    

    self.$http.get(self.load_all_projects_url, {
        params: options
    }).then(successCallback, errorCallback);
    },

    selectAllMetas: function(){
      var self= this;
      self.selected_meta_attribs = []
      if (self.all_selected.indexOf("all_metas_selected") >= 0){
      self.project.site_meta_attributes.forEach(function(obj) {
        self.selected_meta_attribs.push(obj.question_name);
      });
      }
    },

    selectAllRegions: function(){
      var self= this;
      self.selected_region_ids = []
      if (self.all_selected.indexOf("all_regions_selected") >= 0){
      self.regions.forEach(function(obj) {
        self.selected_region_ids.push(obj.id);
      });
      self.selected_region_ids.push(0);
      }
    },

    importSites: function(){
      var self = this;
      if (!self.project.hasOwnProperty('id')){
        alert("Select a project.");
        return false;
      }
      
      if (self.project.cluster_sites === true && self.selected_region_ids.length < 1){
        alert("Select atleast 1 Region to import sites from.");
        return false;
      }
      
      function successCallback(response) {
          alert(response.body);
          self.loading = false;
      }
      function errorCallback() {
          self.loading = false;
          console.log('failed');
      }
      options = {headers: {'X-CSRFToken':self.csrf}};
      body = {'regions': self.selected_region_ids, 'meta_attributes': self.selected_meta_attribs, 'ignore_region': self.ignore_site_cluster }
      self.$http.post('/fieldsight/export/clone/project/from/'+ self.project.id +'/to/'+ self.project_id +'/', body, options).then(successCallback, errorCallback);     

    },

    loadRegions: function(id){
    var self= this;

    function successCallback(response) {
        self.regions = response.body;
        self.loading = false;
    }
    function errorCallback() {
        self.loading = false;
        console.log('failed');
    }

    self.$http.get('/fieldsight/api/project/'+ id +'/regions/').then(successCallback, errorCallback);

    },
    

    loadProjectDetail: function(){
    var self= this;
    self.all_selected= [];
    self.project={};
    self.selected_meta_attribs=[];
    self.regions=[];
    self.selected_region_ids=[];
    self.project = self.projects[self.selected_project];
    if (self.project.cluster_sites === true){
      self.loadRegions(self.project.id);
      }
    },
    
   },
  created(){
    var self= this;
    self.loadDatas();
  },

})