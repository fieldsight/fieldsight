
    window.generateGsuitReport=new Vue({
      el: '#driveLink',
      template: `
      			<div class="modal-body">
      				<div class="form-group">
						<h5>Standard Reports</h5>
							<div>
					        	<table class="table table-striped table-bordered table-hover margin-top table-sync" id="dynamic-table2">
									<thead>
										<tr>
											<th>Report Name</th>
											<th>Sync</th>
										</tr>
									</thead>
									<tbody>
										<tr>
											<td>
												<h6 v-if="this.terms_and_labels.length==0"> Site Information </h6>
												<h6 v-else > {{this.terms_and_labels[0].site}} Information </h6>
												<p v-if="details_updated_at != null"><a :href="details_link" target="_blank"> View in Google sheets <i class="la la-external-link"></i></a><br>

												Last synced at {{ details_updated_at }}</p>
												<p v-else>Report has not been synced with google sheets. Try syncing now by clicking Sync now. It might take some time.</p>
											</td>
											<td>
												<button type="button" :disabled="buttonDisabled1" @click="generateSitesExportReport()" class="btn btn-success"><i class="la la-refresh ml-2"></i> Sync now</button>
											</td>
										</tr>

										<tr>
											<td>
												<h6> Progress Report </h6>
												<p v-if="progress_updated_at != null"><a :href="progress_link" target="_blank"> View in Google sheets <i class="la la-external-link"></i></a><br>

												Last synced at {{ progress_updated_at }}</p>
												<p v-else>Report has not been synced with google sheets. Try syncing now by clicking Sync now. It might take some time.</p>
											</td>
											<td>
												<button type="button" :disabled="buttonDisabled2" @click="generateProgressReport()" class="btn btn-success"><i class="la la-refresh ml-2"></i> Sync now</button>
											</td>
										</tr>					
									</tbody>
								</table>      
					        </div>
					</div>

					<br>
					<hr>
					<br>
					
					<a :href="'/fieldsight/sync_schedule/' + project_id + '/'" target="_blank"><button type="button" class="btn btn-primary"><i class="la la-refresh ml-2"></i> Add Sync Schedule</button></a>

					<br>
					<hr>
					<br>

					<div class="form-group">
						<h5>General Report</h5>
							<div>
					        	<table class="table table-striped table-bordered table-hover margin-top table-sync" id="dynamic-table2">
									<thead>
										<tr>
											<th>Form Name</th>
											<th>Sync</th>
										</tr>
									</thead>
									<tbody>
										<tr v-for="form in general_forms">
											<td><h6>{{ form.xf__title }}</h6>
												<p v-if="form.id.toString() + '_' + form.xf__title + '_' + form.xf__id_string in gsuit_metas"><a :href="gsuit_metas[form.id.toString() + '_' + form.xf__title + '_' + form.xf__id_string].link" target="_blank"> View in Google sheets <i class="la la-external-link"></i></a><br> Last synced at {{ dateparse(gsuit_metas[form.id.toString() + '_' + form.xf__title + '_' + form.xf__id_string].updated_at) }}</p>
												<p v-else>Report has not been synced with google sheets. Try syncing now by clicking Sync now. It might take some time.</p>
											</td>
											<td>
												<button type="button" :disabled="buttonDisabled3" @click="syncFormXls(form.id, form.xf__user__username, form.xf__id_string)" class="btn btn-success"><i class="la la-refresh ml-2"></i> Sync now</button>
											</td>
										</tr>
									 

									</tbody>
								</table>      
					        </div>

					</div>
					<br>
					<hr>
					<br>
					<div class="form-group">
						<h5>Scheduled Forms Report</h5>
							<div>
					        	<table class="table table-striped table-bordered table-hover margin-top table-sync" id="dynamic-table2">
									<thead>
										<tr>
											<th>Form Name</th>
											<th>Sync</th>
										</tr>
									</thead>
									<tbody>
										<tr v-for="form in scheduled_forms">
											<td><h6>{{ form.xf__title }}</h6>
												<p v-if="form.id.toString() + '_' + form.xf__title + '_' + form.xf__id_string in gsuit_metas"><a :href="gsuit_metas[form.id.toString() + '_' + form.xf__title + '_' + form.xf__id_string].link" target="_blank"> View in Google sheets <i class="la la-external-link"></i></a><br> Last synced at {{ dateparse(gsuit_metas[form.id.toString() + '_' + form.xf__title + '_' + form.xf__id_string].updated_at) }}</p>
												<p v-else>Report has not been synced with google sheets. Try syncing now by clicking Sync now. It might take some time.</p>
											</td>
											<td>
												<button type="button" :disabled="buttonDisabled3" @click="syncFormXls(form.id, form.xf__user__username, form.xf__id_string)" class="btn btn-success"><i class="la la-refresh ml-2"></i> Sync now</button>
											</td>
										</tr>
									 

									</tbody>
								</table>      
					        </div>

					</div>
					<br>
					<hr>
					<br>
					<div class="form-group">
						<h5>Survey Report</h5>
							<div>
					        	<table class="table table-striped table-bordered table-hover margin-top table-sync" id="dynamic-table2">
									<thead>
										<tr>
											<th>Form Name</th>
											<th>Sync</th>
										</tr>
									</thead>
									<tbody>
										<tr v-for="form in survey_forms">
											<td><h6>{{ form.xf__title }}</h6>
												<p v-if="form.id.toString() + '_' + form.xf__title + '_' + form.xf__id_string in gsuit_metas">
													<a :href="gsuit_metas[form.id.toString() + '_' + form.xf__title + '_' + form.xf__id_string].link" target="_blank"> View in Google sheets <i class="la la-external-link"></i></a><br> Last synced at {{ dateparse(gsuit_metas[form.id.toString() + '_' + form.xf__title + '_' + form.xf__id_string].updated_at) }}
												</p>
												<p v-else>Report has not been synced with google sheets. Try syncing now by clicking Sync now. It might take some time.</p>
											</td>
											<td>
												<button type="button" :disabled="buttonDisabled3" @click="syncFormXls(form.id, form.xf__user__username, form.xf__id_string)" class="btn btn-success"><i class="la la-refresh ml-2"></i> Sync now</button>
											</td>
										</tr>
									 

									</tbody>
								</table>      
					        </div>

					</div>
					<br>
					<hr>
					<br>
					<div class="form-group">
						<h5>Staged Report</h5>
							<div>
					        	<table class="table table-striped table-bordered table-hover margin-top table-sync" id="dynamic-table2">
									<thead>
										<tr>
											<th>Form Name</th>
											<th>Sync</th>
										</tr>
									</thead>
									<tbody>
										<template v-for="staged_form in staged_forms">
										<tr>
											<td><h6><strong>{{ 'Stage:' + staged_form.title }}</strong></h6></td>
											<td></td>
										</tr>

										<tr v-for="form in staged_form.sub_stages">
											<td><h6>{{ form.name }}</h6>
												<p v-if="form.stage_forms__id.toString() + '_' + form.name + '_' + form.stage_forms__xf__id_string in gsuit_metas"><a :href="gsuit_metas[form.stage_forms__id.toString() + '_' + form.name + '_' + form.stage_forms__xf__id_string].link" target="_blank"> View in Google sheets <i class="la la-external-link"></i></a><br> Last synced at {{ dateparse(gsuit_metas[form.stage_forms__id.toString() + '_' + form.name + '_' + form.stage_forms__xf__id_string].updated_at) }}</p>
												<p v-else>Report has not been synced with google sheets. Try syncing now by clicking Sync now. It might take some time.</p>
											</td>
											<td>
												<button type="button" :disabled="buttonDisabled3" @click="syncFormXls(form.stage_forms__id, form.stage_forms__xf__user__username, form.stage_forms__xf__id_string)" class="btn btn-success"><i class="la la-refresh ml-2"></i> Sync now</button>
											</td>
										</tr>
										</template>
									 

									</tbody>
								</table>      
					        </div>

					</div>


				</div>
			`,

	  data: () => ({
	    is_loading: false,
	    buttonDisabled1: false, 
	    buttonDisabled2: false,
	    buttonDisabled3: false, 
	    progress_updated_at: null,
	    progress_link: null,
	    progress_created_by: null,
	    details_updated_at: null,
	    details_link: null,
	    details_created_by: null,
	    scheduled_forms: [],
	    general_forms: [],
	    survey_forms: [],
	    staged_forms: [],
	    gsuit_metas: configure_settings.gsuit_metas,
	    terms_and_labels: [],
	    project_id: configure_settings.terms_and_labels_project_id,
	  }),
	  created: function (){
	  		
	  		if('Site Information' in configure_settings.gsuit_metas && 'link' in configure_settings.gsuit_metas['Site Information']){
	  			this.details_updated_at = dateparser(configure_settings.gsuit_metas['Site Information']['updated_at']);
	  			this.details_link = configure_settings.gsuit_metas['Site Information']['link']
	  			this.details_created_by = configure_settings.gsuit_metas['Site Information']['user']
	  		}


	        if('Site Progress' in configure_settings.gsuit_metas && 'link' in configure_settings.gsuit_metas['Site Progress']){
	  			this.progress_updated_at = dateparser(configure_settings.gsuit_metas['Site Progress']['updated_at']);
	  			this.progress_link = configure_settings.gsuit_metas['Site Progress']['link']
	  			this.details_created_by = configure_settings.gsuit_metas['Site Information']['user']
	  		}

	  		function successCallback(response) {
				this.scheduled_forms = response.body.schedule;
				this.general_forms = response.body.general;
				this.survey_forms = response.body.survey;
				this.staged_forms = response.body.stage;
			}
			
			function errorCallback() {
			  alert('Failed to complete the request. Please try again.')
			  console.log('failed');
			  this.buttonDisabled1 = false;
			}

	  		this.$http.get('/fieldsight/export/xls/project/responses/' + configure_settings.project_id + '/').then(successCallback, errorCallback);
   	    },
	  methods: {

	  	dateparse: function (date) {
	      // `this` points to the vm instance
	      return dateparser(date)
	    },
	    generateSitesExportReport: function (){
	    	this.buttonDisabled1 = true;
	    	function successCallback(response) {
	          alert(response.body.message);
			  this.buttonDisabled1 = false;
			}
			
			function errorCallback() {
			  alert('Failed to complete the request. Please try again.')
			  console.log('failed');
			  this.buttonDisabled1 = false;
			}
			
			options = {headers: {'X-CSRFToken':configure_settings.csrf_token}};
			body = {'regions': [], 'siteTypes': [], 'sync_to_drive': true}
			
			console.log(body)
			this.$http.post(configure_settings.genarete_sites_export_url, body, options).then(successCallback, errorCallback);     

			},

		generateProgressReport: function (){
			this.buttonDisabled2 = true;
	    	function successCallback(response) {
	          alert(response.body.message);
	          this.buttonDisabled2 = false;
			}
			
			function errorCallback() {
			  alert('Failed to complete the request. Please try again.')
			  console.log('failed');
			  this.buttonDisabled2 = false;
			}
			
			options = {headers: {'X-CSRFToken':configure_settings.csrf_token}};
			body = {'regions': [], 'siteTypes': [], 'sync_to_drive': true}
			
			console.log(body)
			this.$http.post(configure_settings.progress_report_url, body, options).then(successCallback, errorCallback);     

			},

		syncFormXls: function (form_id, username, id_string){
			this.buttonDisabled3 = true;
	    	function successCallback(response) {
	          alert('Success, sync has been queued and soon will be updated.');
	          this.buttonDisabled3 = false;
			}
			
			function errorCallback() {
			  alert('Failed to complete the request. Please try again.')
			  console.log('failed');
			  this.buttonDisabled3 = false;
			}
			
			options = {headers: {'X-CSRFToken':configure_settings.csrf_token}};
			body = {}
			
			console.log(body)
			this.$http.post('/'+ username +'/exports/'+ id_string +'/xls/1/'+ form_id +'/0/0/1/new', body, options).then(successCallback, errorCallback);     

			},
		
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
