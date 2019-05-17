    Vue.component('treeselect', VueTreeselect.Treeselect)
    var LOAD_CHILDREN_OPTIONS = this.VueTreeselect.LOAD_CHILDREN_OPTIONS
    var LOAD_ROOT_OPTIONS = this.VueTreeselect.LOAD_ROOT_OPTIONS

    window.generateProgressReport=new Vue({
      el: '#generateProgressReport',
      template: `
      		
					
				<div class="modal-body p-3">

					<div class="form-group">
						<h5>Progress Report</h5>
		  				<div class="text-center">
							<div class="rounded-circle p-4 bg-light" style="height: 150px;width: 150px;margin: 32px auto;">
								<i style="font-size: 52px;" class="la la-file-excel-o ml-2 text-success m-4"></i>
							</div>
							<p>
												  		Export of key progress indicators like submission count,status and site <br> visits generated from Staged Forms.
							</p>
						</div>

					</div>
					<br>
					<div class="row">
							<div class="col-md-12">
									<label>Filters:</label>
							</div>
					</div>
					<div class="p-3 border bg-light">
					<div class="form-row">
					    
				        <div class="form-group col-md-6">
								<label for="startdate">Region:</label>
							<treeselect :multiple="true"
								  :options="regionOptions"
								  :load-options="loadRegionOptions"
								  :auto-load-root-options="false"
								  placeholder="Select Regions"
								  v-model="regionValues" />

						</div>
				        <div class="form-group col-md-6">
								<label for="startdate">Site Type:</label>
							<treeselect :multiple="true"
								  :options="siteTypeOptions"
								  :load-options="loadSiteTypeOptions"
								  :auto-load-root-options="false"
								  placeholder="Select Types"
								  v-model="siteTypeValues" />
								

						</div>
						  
					    </div>
					  </div>
					<br>
					<button type="button" :disabled="buttonDisabled" @click="generateReport()" class="btn btn-success"> Generate Excel</button>		
					</div>
				</div>
				
			`,

	  data: () => ({
	  	buttonDisabled: false,
	    regionValues: null,
	    regionOptions: null,
	    siteTypeValues: null,
	    siteTypeOptions: null,
	    is_loading: false,
	  }),

	  methods: {
	    loadRegionOptions({ action, parentNode, callback }) {
			function errorCallback() {
			    callback(new Error('Failed to load options: network error.'))
			}
		  	if (action === LOAD_ROOT_OPTIONS) {
		  	function successCallback(response) {
		  			console.log(response);
	        		var regions = response.body
				    regions.forEach(function(val,index){ 
				       regions[index]['id'] = val.id
					   regions[index]['label'] = val.name + " -- " + val.identifier
					 })
					this.regionOptions = regions
				    callback()
				}
	        this.$http.get(configure_settings.regions_url).then(successCallback, errorCallback);

		  }
	    },

		loadSiteTypeOptions({ action, parentNode, callback }) {
			function errorCallback() {
			    callback(new Error('Failed to load options: network error.'))
			}
		  	if (action === LOAD_ROOT_OPTIONS) {
		  	function successCallback(response) {
		  			console.log(response);
	        		var site_types = response.body
				    site_types.forEach(function(val,index){ 
				       site_types[index]['id'] = val.id
					   site_types[index]['label'] = val.name
					})
					this.siteTypeOptions = site_types
				    callback()
				}
	        this.$http.get(configure_settings.site_types_url).then(successCallback, errorCallback);

		  }
	    },

	  


	    generateReport: function (){
	    	this.buttonDisabled = true;
	    	function successCallback(response) {
	          alert(response.body.message);
			  this.buttonDisabled = false;
			}
			
			function errorCallback() {
			  alert('Failed to complete the request. Please try again.')
			  console.log('failed');
			  this.buttonDisabled = false;
			}
			
			options = {headers: {'X-CSRFToken':configure_settings.csrf_token}};
			body = {'regions': this.regionValues, 'siteTypes': this.siteTypeValues}
			
			console.log(body)
			this.$http.post(configure_settings.progress_report_url, body, options).then(successCallback, errorCallback);     

			}
		},

	 })
