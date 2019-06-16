Vue.component('treeselect', VueTreeselect.Treeselect)
    var LOAD_CHILDREN_OPTIONS = this.VueTreeselect.LOAD_CHILDREN_OPTIONS
    var LOAD_ROOT_OPTIONS = this.VueTreeselect.LOAD_ROOT_OPTIONS
    window.exportSitesToProject=new Vue({
      el: '#generateReport',
      template: `
					
			<div class="modal-body p-3">
				<div class="form-group">
					<h5>Data Export</h5>
					  <div class="text-center">
			              <div class="rounded-circle p-4 bg-light" style="height: 150px;width: 150px;margin: 32px auto;">
			                <i style="font-size: 52px;" class="la la-file-pdf-o ml-2 text-success m-4"></i>
			              </div>
			              <p v-if="this.terms_and_labels.length==0">
			                    Export of forms data and site information an PDF File, generated with filters in time range <br> and option to remove unanswered questions.
			              </p>
			              <p v-else>
			                    Export of forms data and {{this.terms_and_labels[0].site.toLowerCase().trim()}} information an PDF File, generated with filters in time range <br> and option to remove unanswered questions.
			              </p>
			            </div>

				</div>

				<div class="form-item-wrapper checkbox-listing">
			    	<div class="row">
					    <div class="form-row col-md-12 col-lg-12">
					        <div class="form-group col-md-6">
					          <label for="startdate">General Forms:</label>
						    	<treeselect :multiple="true"
								  :options="generalOptions"
								  :load-options="loadFormOptions"
								  :auto-load-root-options="false"
								  placeholder="Select General Forms"
								  v-model="generalValues" />
							</div>
						
						
							<div class="form-group col-md-6">
					          <label for="startdate">Scheduled Forms:</label>
						    	<treeselect :multiple="true"
								  :options="scheduledOptions"
								  :load-options="loadFormOptions"
								  :auto-load-root-options="false"
								  placeholder="Select Scheduled Forms"
								  v-model="scheduledValues" />
							</div>

							<div class="form-group col-md-6">
					            <label for="startdate">Stage Forms:</label>
								<treeselect :multiple="true"
								  :options="stageOptions"
								  :load-options="loadFormOptions"
								  :auto-load-root-options="false"
								  placeholder="Select Stage Forms"
								  v-model="stageValues" />

							</div>

							<div class="form-group col-md-6">
								<label>&nbsp;</label>

								<div class="form-group form-check" style="margin-top: 7px;">
									<input type="checkbox" v-model="removeNullField" class="form-check-input" id="removeNullField" /> <label class="form-check-label" for=
									"removeNullField">Hide Null Fields</label>
								</div>
							</div>
						</div>
					</div>

					<div class="row">
						<div class="col-md-12">
								<label>Filters:</label>
				
						</div>
					</div>

					<div class="p-3 border bg-light">
						<div class="row">
						<div class="col-md-6 col-lg-6">
							<div class="form-group">
								<label for="startdate">Start Date:</label> <input type="date" class=
								"form-control" v-model="start_date_value" v-bind:min="start_date_min_value" v-bind:max="start_date_max_value" name=
								"startdate" id="startdate" />
							</div>
						</div>

						<div class="col-md-6 col-lg-6">
							<div class="form-group">
								<label for="enddate">End Date:</label> <input type="date" class="form-control"
								v-model="end_date_value" v-bind:min="end_date_min_value" v-bind:max="end_date_max_value" name="enddate" id="enddate" />
							</div>
						</div>
						
						</div>
					</div>
					</div>
				
				<br>
				<button type="button" @click="generateReport()"  :disabled="buttonDisabled" class="btn btn-success"><i class="la la-file-pdf-o"></i> Generate PDF</button>
				
			</div>
			`,

	  data: () => ({
	  	buttonDisabled: false,
	    generalValues: [],
	    generalOptions: null,
	    stageValues: [],
	    stageOptions: null,
	    scheduledValues: [],
	    scheduledOptions: null,
	    removeNullField: false,
	    is_loading: false,
	    forms_loaded: false,
	    is_first_request: true,
	    start_date_value: configure_settings.start_date_value,
	    start_date_max_value: configure_settings.start_date_max_value,
	    start_date_min_value: configure_settings.start_date_min_value,
	    end_date_value: configure_settings.end_date_value,
	    end_date_max_value: configure_settings.end_date_max_value,
	    end_date_min_value: configure_settings.end_date_min_value,
	    terms_and_labels: [],
	    project_id: configure_settings.terms_and_labels_project_id,

	  }),

	  methods: {
	    loadFormOptions({ action, parentNode, callback }) {
	      // Typically, do the AJAX stuff here.
	      // Once the server has responded,
	      // assign children options to the parent node & call the callback.

	    const sleep = d => new Promise(r => setTimeout(r, d))

		function errorCallback() {
			this.is_loading = false
			this.forms_loaded = false
		    callback(new Error('Failed to load options: network error.'))
		}

		  
		  if (!this.forms_loaded  && !this.is_first_request){
		  		throw new Error('Failed to load options.')
		  	
		  }

		  if (this.forms_loaded  && this.is_first_request){
		  	console.log("loaded")
		  }

		  else if (action === "LOAD_ROOT_OPTIONS") {
		  	function successCallback(response) {
		  			this.is_loading = false
					this.forms_loaded = true

				    var processed_scheduled = [{'id':[0], 'label':'All scheduled Forms', 'children':[]} ]
				    response.body.schedule.forEach(function(val,index){ 
				       processed_scheduled[0]['id'].push(val.id)
				       var child = {'id':val.id, 'label':val.xf__title}
				       processed_scheduled[0]['children'].push(child)
					   
					})

					var processed_general = [{'id':[0], 'label':'All General Forms', 'children':[]} ]
				    response.body.general.forEach(function(val,index){ 
				       processed_general[0]['id'].push(val.id)
				       var child = {'id':val.id, 'label':val.xf__title}
				       processed_general[0]['children'].push(child)
					})

					var processed_stage = [{'id':[0], 'label':'All Stage Forms', 'children':[]} ]
				    
				    response.body.stage.forEach(function(val,index){ 
				       var id = [0]
				       var sub_children = []
				       val.sub_stages.forEach(function(sub_val, sub_index){
				       		id.push(sub_val.stage_forms__id)
				       		sub_children.push({'id':sub_val.stage_forms__id, 'label':sub_val.name})
				       })

				       var child = {'id':id, 'label':val.title, 'children':sub_children}
				       processed_stage[0]['id'].push(id)
				       processed_stage[0]['children'].push(child)

					})
		
					this.generalOptions = processed_general
					this.scheduledOptions = processed_scheduled
					this.stageOptions = processed_stage
				    callback()
				}
			this.is_first_request = false
	        this.is_loading = true
	        this.$http.get('/fieldsight/site/report/custom-responses/' + configure_settings.site_id + '/').then(successCallback, errorCallback);

	        	
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
			
			var all_ids = this.generalValues.concat(this.scheduledValues, [].concat.apply([], this.stageValues))
			
			if (all_ids.length == 0){
				this.buttonDisabled = false; 
				alert('Please Select atleast one form.');
				return
			}
	    	
	    	var pre_proccesed_ids = [].concat.apply([], all_ids)
	    	var proccesed_ids = pre_proccesed_ids.filter(id => id !== 0);
			
			
			options = {headers: {'X-CSRFToken':configure_settings.csrf_token}};
			body = {'fs_ids': proccesed_ids, 'removeNullField': this.removeNullField, 'startdate': this.start_date_value, 'enddate':this.end_date_value}
			
			console.log(body)
			this.$http.post('/fieldsight/site/report/custom-responses/'+configure_settings.site_id +'/', body, options).then(successCallback, errorCallback);     

			}
		},

		mounted() {
             function errorCallback() {
                    callback(new Error('Failed to load Project Terms and Labels data.'))
                }

             function successCallback(response) {
                this.terms_and_labels = response.body;
            }
            this.$http.get('/fieldsight/api/project-terms-labels/'+ this.project_id).then(successCallback, errorCallback)

            },

	 })

