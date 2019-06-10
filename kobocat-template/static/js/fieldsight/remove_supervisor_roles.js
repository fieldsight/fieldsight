Vue.component('treeselect', VueTreeselect.Treeselect)
    var LOAD_CHILDREN_OPTIONS = this.VueTreeselect.LOAD_CHILDREN_OPTIONS
    var LOAD_ROOT_OPTIONS = this.VueTreeselect.LOAD_ROOT_OPTIONS
    window.exportSitesToProject=new Vue({
      el: '#removeSRole',
      template: `
      			<div>
      			<div>
		    		<treeselect :multiple="true"
					  :options="options"
					  :load-options="loadOptionsSupervisor"
					  :auto-load-root-options="false"
					  placeholder="Select Roles to remove ..."
					  v-model="values" />
		    	</div><br>
		    	<div>
			      <button class="btn btn-xs btn-danger" @click="removeRoles('4')">Remove Selected Supervisor Roles</button>
			    </div>
		    	<br>
			    </div>`,

	  data: () => ({
	    values: null,
	    options: null,
	  }),

	  methods: {
	    loadOptionsSupervisor({ action, parentNode, callback }) {
	      // Typically, do the AJAX stuff here.
	      // Once the server has responded,
	      // assign children options to the parent node & call the callback.


		function errorCallback() {
		    callback(new Error('Failed to load options: network error.'))
		}



		  if (action === LOAD_ROOT_OPTIONS) {
		  	function successCallback(response) {
	        		console.log(response);
	        		var projects = response.body
				    projects.forEach(function(val,index){ 
				       projects[index]['id'] = 'p'+val.id
					   projects[index]['level'] = "project"
					   projects[index]['label'] = '🇵' + ' ' + val.label
					   projects[index]['children'] = null 
					})
					this.options = projects
				    callback()
				}
	        	
	        	this.$http.get('/fieldsight/api/user/projects/' +  parseInt(configure_settings.user_id) + '/4/').then(successCallback, errorCallback);

		  }

	      else if (action === LOAD_CHILDREN_OPTIONS) {
	        if (parentNode.level == "project" && parentNode.cluster_sites === false)
	        {
	        	function successCallback(response) {
	        		console.log(response);
	        		parentNode.children = response.body
				    callback()
				}
	        	
	        	this.$http.get('/fieldsight/api/project/user/sites/' + parentNode.id.slice( 1 ) +'/' + configure_settings.user_id + '/4/').then(successCallback, errorCallback);

				

	        }
	        else if (parentNode.level == "project" && parentNode.cluster_sites === true)
	        {
	        	function successCallback(response) {
				    var regions = response.body.regions
				    regions.forEach(function(val,index){ 
					   regions[index]['id'] = 'r'+val.id
					   regions[index]['level'] = 'region'
					   regions[index]['label'] = '🇷' + ' ' + val.label
					   regions[index]['children'] = null 
					})
					parentNode.children = regions.concat(response.body.sites)
				    callback()
				}
	        	
	        	this.$http.get('/fieldsight/api/project/user/regions/' + parentNode.id.slice( 1 ) +'/' + configure_settings.user_id + '/4/').then(successCallback, errorCallback);

	        }
	        else if(parentNode.level == "region")
	        {
	        	function successCallback(response) {
	        		var regions = response.body.sub_regions
				    regions.forEach(function(val,index){ 
					   regions[index]['id'] = 'r'+val.id
					   regions[index]['level'] = 'region'
					   regions[index]['label'] = '🇷' + ' ' + val.label
					   regions[index]['children'] = null 
					})
					parentNode.children = regions.concat(response.body.sites)
				    callback()

				}
	        	
	        	this.$http.get('/fieldsight/api/region/' + parentNode.id.slice( 1 ) +'/subregionsandsites/' + configure_settings.user_id + '/4/').then(successCallback, errorCallback);
	        }

	      }
	    },

	  


	    removeRoles: function (group_id){
	    	function successCallback(response) {
	          alert(response.body.message);
	          
			}
			
			function errorCallback() {
			  alert('Failed to complete the request. Please try again.')
			  console.log('failed');
			}
			
			options = {headers: {'X-CSRFToken':configure_settings.csrf_token}};
			if (group_id == '3'){
				body = {'ids': this.valuesR, 'group': group_id }
			}
			else{
				body = {'ids': this.values, 'group': group_id }
			}
			console.log(body)
			this.$http.post('/fieldsight/api/remove_roles/'+configure_settings.user_id +'/', body, options).then(successCallback, errorCallback);     

			}
		},

	 })
