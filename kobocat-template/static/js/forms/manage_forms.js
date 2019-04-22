var bus = new Vue();

Vue.use(VueMultiselect);

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

Vue.filter('default_submission_status_label', function (value) {
  if (!value) return 'Pending'
  if(value==3) return 'Approved'
    return 'Pending'
})



window.app = new Vue({
  el: '#app',
  template: `
    <div class="row">
    <div class="col-md-4">
        <div class="widget-info bg-white padding">
            <div class="widget-head" v-show="!show_ad_stage_form">
                <h4>Stages</h4>
                <a href="javascript:void(0)"  title="" class="btn btn-sm btn-primary" @click="add_stage"><i class="la la-plus"></i> New Stage</a>
                <a v-if="stages.length>0 && !reorder_stages_mode" href="javascript:void(0)"  title="" class="btn btn-sm btn-primary" @click="reorderStages()"  v-show="!read_only"><i class="la la-reorder"></i> Reorder</a>
                <a v-if="stages.length>0" href="javascript:void(0)"  title="" class="btn btn-sm btn-success" @click="deployStages()" v-show="!read_only"><i class="la la-rocket"></i> Deploy</a>

            </div>
            <div class="widget-body">

                <ul class="stage-list"  v-if="!show_ad_stage_form && stages.length>0">

                    <li v-bind:class="{ active: activeStage(stage) }" v-for="stage, index in stages"><span>{{index+1}}.</span>
                     <a href="javascript:void(0)" @click="stageDetail(stage)" >{{stage.name}}</a> <span class="pull-right">{{stage.weight_calculated}} % </span></li>
                </ul>
                <ul class="stage-list" v-if="!show_ad_stage_form && stages.length==0 && !loading">
                    <li><span>There are no Stages.. Please Add Stages</span></li>
                </ul>



                <div class="margin-top" v-show="show_ad_stage_form">
                    <form class="padding-top" >
                        <div class="error" v-show="error">
                            {{error}}
                        </div>
                        <div class="form-group">
                            <label for="inputStageName">Name</label>
                            <input type="text" class="form-control" id="inputStageName" v-model="stage_form_obj.name">
                        </div>
                        <div class="form-group">
                            <label for="inputStageDescription">Description</label>
                            <textarea class="form-control" id="inputStageDescription" rows="3"
                                v-model="stage_form_obj.description"></textarea>
                        </div>
                        <div class="form-group" v-show="is_project==1">
                            <label for="inputSubStageTags">Site Types   </label>

                            <vselect :options="tags" label="name" :value="[]" v-model="stage_form_obj.tags" :allow-empty="true" :loading="loading"
                                 :select-label="''" :show-labels="false" :internal-search="true"
                                   :placeholder="'Select Site Types'" :multiple=true track-by="id" :hide-selected="true" :close-on-select="false">
                                <template slot="noResult">NO Types Available</template>
                                    <template slot="afterList" slot-scope="props">
                                    <a  href="javascript:void(0)" @click="newType()" class="btn btn-sm btn-primary"><i class="la la-plus"></i>Add</a></template>
                            </vselect>

                        </div>
                        <div class="form-group">
                            <a  href="javascript:void(0)" @click="save_stage" title=""  class="btn btn-sm btn-primary"><i class="la la-save"></i> Save</a>
                            <a  href="javascript:void(0)" @click="cancel_stage" class="btn btn-sm btn-light"><i class="la la-close"></i>Cancel</a>
                        </div>

                    </form>
                </div>

            </div>
        </div>
    </div>

    <div class="col-md-4">

        <div class="widget-info bg-white padding" v-if="current_stage && !(show_ad_stage_form || update_stage_mode || show_ad_substage_form) ">
            <div class="widget-head">
                <h4>{{current_stage.name | slice}}</h4>

                <a  href="javascript:void(0)" @click="update_stage" class="btn btn-sm btn-primary" v-show="!show_ad_substage_form && !update_stage_mode && !read_only_stage"><i class="la la-edit"></i>Edit</a>

                <a href="javascript:void(0)"  title="" class="btn btn-sm btn-success" v-show="!show_ad_substage_form && !update_stage_mode && substages.length && !read_only_stage>0" @click="deploySubStages()"><i class="la la-rocket"></i> Deploy</a>
            </div>
            <div class="widget-body">
                <div class="col-sm-12" v-show="current_stage.tags && current_stage.tags.length>0">
                   Types:  <label v-for="tag in current_stage.tags"> &nbsp; {{tag.name}}, </label>
                </div>
                <p>{{current_stage.description}}</p>

            </div>
            <div class="widget-head margin-top padding-left" v-show="!show_ad_substage_form">
                <h4 v-if="substages.length>0">Sub Stages</h4>
                <h4 v-if="substages.length==0">No SubStages In this Stage </h4>
                <a  href="javascript:void(0)"  title="" class="btn btn-sm btn-primary" v-show="!reorder_sub_stages_mode && !show_ad_substage_form && !update_stage_mode && substages.length && !read_only_stage>0" @click="reorderSubStages()"><i class="la la-reorder"></i> Reorder</a>
                <a href="javascript:void(0)" @click="add_substage" class="btn btn-sm btn-primary" v-show="!show_ad_substage_form && !update_stage_mode && !read_only_stage">
                <i class="la la-plus"></i> New</a>
            </div>
            <div class="widget-body overflow-auto">
                <ul class="stage-list padding-left" v-show="!show_ad_substage_form && !update_stage_mode">

                <li v-bind:class="{ active: activeSubStage(substage) }" v-for="substage, sindex in substages"><span>{{sindex+1}}.</span>
                     <a  href="javascript:void(0)" @click="substageDetail(substage)">{{substage.name}}</a>
                     <span class="pull-right">{{substage.weight}}</span>
                 </li>
                </ul>

            </div>

        </div>

        <div class="widget-info bg-white padding" v-if="show_ad_substage_form">
            <form class="padding-top">
                <div class="form-group">
                    <label for="inputSubStageName">Sub Stage Name <span class="error" v-show="add_sub_error"> {{add_sub_error}} </span></label>
                    <input type="text" v-model="substage_form_obj.name" class="form-control" id="inputSubStageName">
                </div>
                <div class="form-group">
                    <label for="inputSubStageDescription">Description</label>
                    <textarea class="form-control" v-model="substage_form_obj.description" id="inputSubStageDescription" rows="3"></textarea>
                </div>
                <div class="form-group">
                    <label for="inputSubStageForm">Form</label>
                    <vselect :options="forms" label="title" :value="''" v-model="substage_form_obj.xf" :allow-empty="true" :loading="loading"
                     :select-label="''" :show-labels="false" :internal-search="true"  :placeholder="'Select Form'" :multiple=false track-by="id" :hide-selected="true">
                    <template slot="noResult">Forms Available</template>
                    <template slot="afterList" slot-scope="props"><div v-show="forms.length==0" class="wrapper-sm bg-danger">
                    No Forms</div></template>
                </vselect>
                </div>
                <div class="form-group">
                    <label for="inputSubStageWeight">Weight</label>
                    <input type="number" min="0" max="100"  step="1"
                    onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57" v-model="substage_form_obj.weight" class="form-control" id="inputSubStageWeight">
                </div>
                <div class="form-group" v-show="is_project==1">
                    <label for="inputSubStageTags">Types</label>
                    <vselect :options="tags" label="name" :value="[]" v-model="substage_form_obj.tags" :allow-empty="true" :loading="loading"
                         :select-label="''" :show-labels="false" :internal-search="true"  :placeholder="'Select Types'" :multiple=true track-by="id" :hide-selected="true">
                        <template slot="noResult">NO Types Available</template>
                        <template slot="afterList" slot-scope="props"><div v-show="forms.length==0" class="wrapper-sm bg-danger">
                        No Types</div></template>
                    </vselect>

                </div>
                <div class="form-group">
                <label for="dfs">Default Submision Status</label>
                    <select v-model="substage_form_obj.selected" class="form-control">
                    <option disabled value="">Please select one</option>
                          <option>Pending</option>
                          <option>Approved</option>
                           </select>
                </div>
                <div class="form-group">
                    <a href="javascript:void(0)" @click="save_sub_stage" class="btn btn-sm btn-primary"><i class="la la-save"></i> Save</a>
                    <a href="javascript:void(0)" @click="cancel_sub_stage" class="btn btn-sm btn-light"><i class="la la-close"></i> Cancel</a>
                </div>

            </form>
        </div>
        <div class="widget-info bg-white padding" v-if="update_stage_mode &&  !show_ad_stage_form">
            <form class="padding-top">
                <div class="error" v-show="update_error">
                {{update_error}}
                </div>
                  <div class="form-group">
                  <label for="inputStageName">Stage Name</label>
                    <input v-model="stage_form_obj_edit.name" class="form-control" placeholder="Stage Name">
                  </div>
                  <div class="form-group">
                   <label for="inputStageDescription">Description</label>
                    <textarea v-model="stage_form_obj_edit.description" class="form-control" placeholder="Description" rows="3"></textarea>
                  </div>
                  <div class="form-group" v-show="is_project==1">
                    <label for="inputSubStageTags">Types</label>
                    <vselect :options="tags" label="name" :value="[]" v-model="stage_form_obj_edit.tags" :allow-empty="true" :loading="loading"
                         :select-label="''" :show-labels="false" :internal-search="true"  :placeholder="'Select Types'" :multiple=true track-by="id" :hide-selected="true">
                        <template slot="noResult">NO Types Available</template>
                        <template slot="afterList" slot-scope="props"><div v-show="tags.length==0" class="wrapper-sm bg-danger">
                        No Types</div></template>
                    </vselect>

                    </div>
                  <div class="form-group">
                    <a href="javascript:void(0)" @click="do_update_stage" class="btn btn-sm btn-primary"><i class="la la-save"></i> Save</a> &nbsp;
                    <a href="javascript:void(0)" @click="update_stage_done" class="btn btn-sm btn-light"><i class="la la-close"></i> Cancel</a>
                    </div>
            </form>
        </div>

        <div class="widget-info bg-white padding" v-if="reorder_stages_mode && !show_ad_stage_form">
            <div class="widget-head">
                <h4>Reorder  Stages </h4>
               <a href="javascript:void(0)"  title="" class="btn btn-sm btn-light" @click="reorderStagesCancel()"><i class="la la-close"></i>  Cancel Reorder</a>
                <a href="javascript:void(0)"  title="" class="btn btn-sm btn-primary" @click="reorderStagesSave()"><i class="la la-save"></i> Save Order</a>
            </div>
             <div id="main" class="widget-body">

                <div class="drag">
                    <draggable :list="stages_reorder" class="dragArea">
                        <div v-for="stage in stages_reorder" class="dragable-stage">{{stage.name}}</div>
                     </draggable>
                 </div>
             </div>

        </div>
    </div>

    <div class="col-md-4">
        <div class="widget-info bg-white padding" v-show="substage_detail && !update_substage_mode &&  !new_em && !show_ad_stage_form && !show_ad_substage_form">
            <div class="widget-head">
                <h4>{{substage_detail.order+1}} {{substage_detail.name}} </h4>
                <a href="javascript:void(0)" @click="loadEm" class="btn btn-primary  btn-sm" v-show="substage_detail.has_em"><i class="la la-eye"></i> View Material</a>
                <a href="javascript:void(0)" @click="newEm" class="btn btn-primary btn-sm" v-show="!substage_detail.has_em && !read_only_stage"><i class="la la-plus"></i> New Material</a>
                <a href="javascript:void(0)" @click="update_sub_stage" class="btn btn-primary  btn-sm" v-show="!read_only_stage"><i class="la la-edit"></i> Edit</a>
                <a href="javascript:void(0)"  title="" class="btn btn-sm btn-success" v-show="!show_ad_substage_form && !update_stage_mode && has_form && !substage_detail.is_deployed" @click="deploySubStage()"><i class="la la-rocket"></i> Deploy</a>
            </div>
            <div class="widget-body">
                <p>{{substage_detail.description}}</p>
                Responses : {{substage_detail.responses_count}} <br>
                Form Assigned : {{form_name}} <br>
                Weight : {{substage_detail.weight}} <br>
                Default Form Status : {{substage_detail.default_submission_status|default_submission_status_label}} <br>
                <div class="col-sm-12" v-show="substage_detail.tags && substage_detail.tags.length>0">
                   Types:  <label v-for="tag in substage_detail.tags"> &nbsp; {{tag.name}}, </label>
                </div>

            </div>
        </div>
        <div class="margin-top" v-show="update_substage_mode && substage_detail && !show_ad_stage_form">
                    <form class="padding-top">
                        <div class="form-group">
                            <label for="inputSubStageName">Name <span class="error" v-show="add_sub_error"> {{add_sub_error}} </span></label>
                            <input type="text" v-model="substage_detail.name" class="form-control" id="inputSubStageName">
                        </div>
                        <div class="form-group">
                            <label for="inputSubStageDescription">Description</label>
                            <textarea class="form-control" v-model="substage_detail.description" id="inputSubStageDescription" rows="3"></textarea>
                        </div>
                        <div class="form-group">
                            <label for="inputSubStageForm">Form</label>
                            <vselect :options="forms" label="title" :value="''" v-model="form" :allow-empty="true" :loading="loading"
                         :select-label="''" :show-labels="false" :internal-search="true"  :placeholder="'Select Form'" :multiple=false track-by="id" :hide-selected="true">
                        <template slot="noResult">Forms Available</template>
                        <template slot="afterList" slot-scope="props"><div v-show="forms.length==0" class="wrapper-sm bg-danger">
                        No Forms</div></template>
                        </vselect>
                        </div>
                        <div class="form-group">
                            <label for="inputSubStageWeight">Weight</label>
                            <input type="number" min="0" max="100"  step="1"
                            onkeypress="return (event.charCode == 8 || event.charCode == 0 || event.charCode == 13) ? null : event.charCode >= 48 && event.charCode <= 57" 
                             v-model="substage_detail.weight" class="form-control" id="inputSubStageWeight">
                        </div>
                        <div class="form-group" v-show="is_project==1">
                            <label for="inputSubStageTags">Types</label>
                            <vselect :options="tags" label="name" :value="[]" v-model="substage_detail.tags" :allow-empty="true" :loading="loading"
                                 :select-label="''" :show-labels="false" :internal-search="true"  :placeholder="'Select Types'" :multiple=true track-by="id" :hide-selected="true">
                                <template slot="noResult">NO Types Available</template>
                                <template slot="afterList" slot-scope="props"><div v-show="forms.length==0" class="wrapper-sm bg-danger">
                                No Types</div></template>
                            </vselect>
                            </div>

                              <div class="form-group">
                                <label for="dfs">Default Submision Status</label>
                                    <select v-model="substage_detail.selected" class="form-control">
                                    <option disabled value="">Please select one</option>
                                          <option>Pending</option>
                                          <option>Approved</option>
                                           </select>
                                </div>

                        <div class="form-group">
                            <a href="javascript:void(0)" @click="do_update_sub_stage" class="btn btn-sm btn-primary"><i class="la la-save"></i> Save</a>
                            <a href="javascript:void(0)" @click="cancel_sub_stage" class="btn btn-sm btn-light"><i class="la la-close"></i> Cancel</a>
                        </div>

                    </form>
                </div>
                <div class="widget-info bg-white padding" v-show="reorder_sub_stages_mode && !show_ad_stage_form">
                    <div class="widget-head">
                        <h4>Reorder  Sub Stages </h4>
                        <a href="javascript:void(0)"  title="" class="btn btn-sm btn-light" @click="reorderSubStagesCancel()"><i class="la la-close"></i> Cancel Reorder</a>
                <a href="javascript:void(0)"  title="" class="btn btn-sm btn-primary " @click="reorderSubStagesSave()"><i class="la la-save"></i> Save Order</a>
                    </div>
                     <div id="main" class="widget-body">

                        <div class="drag">
                            <draggable :list="substages_reorder" class="dragArea">
                                <div v-for="stage in substages_reorder" class="dragable-stage">{{stage.name}}</div>
                             </draggable>
                         </div>
                     </div>

                </div>

                <div class="widget-info bg-white padding" v-show="new_em && !show_ad_stage_form">
                    <form class="padding-top">
                    <div class="form-group">

                        <div>
                            <span><strong>PDF</strong></span>
                            <div v-show="new_em_obj.is_pdf"> <a target="_blank" v-bind:href="new_em_obj.pdf"> Pdf File </a> </div>
                            <input type="file" accept="application/pdf"  @change="onPDFChange">
                          </div>
                    </div>

                    <div class="form-group">
                            <label for="title">Title </label>
                            <input type="text" v-model="new_em_obj.title" class="form-control" id="inputSubStageName" @change="save_em">
                             <div class="invalid-feedback is-invalid" v-show="false">Eror occ</div>
                    </div>
                    <div class="form-group">
                            <label for="text">Description</label>
                            <textarea class="form-control" v-model="new_em_obj.text" id="text" rows="3" @change="save_em"></textarea>
                    </div>
                    <div class="form-group">
                        <div v-if="new_em_obj.em_images.length>0"><strong>Current Images</strong> </div>
                            <div class="row">
                                <div class="col-sm-6" v-for="i in new_em_obj.em_images" v-if="new_em_obj.em_images.length>0">
                                    <img :src="i.image" class="margin-top"/>

                                </div>
                            </div>
                    </div>

                    <div class="form-group">
                        <div>
                            <span>Upload Images</span>
                            <input type="file" multiple="true" @change="onImageChange" accept="image/*">
                          </div>
                    </div>

                      <div class="form-group">
                            <a href="javascript:void(0)" @click="cancel_em" class="btn btn-sm btn-light"><i class="la la-close"></i> Close</a>
                        </div>
                  </form>
                </div>
    </div>
    <new-show-time-modal :show="newShowTimeModal" @close="newShowTimeModal = false"></new-show-time-modal>
</div>`,
    components: {'vselect': VueMultiselect.default},
  data: {
        stages: [],
        stages_reorder: [],
        loading: false,
        is_project: configure_settings.is_project,
        pk: configure_settings.id,
        error: '',
        update_error: '',
        add_sub_error: '',
        update_sub_error: '',
        show_ad_stage_form: false,
        show_ad_substage_form: false,
        stage_form_obj: {'name': '', 'description':'', 'id':'','tags':[]},
        substage_form_obj: {'name': '', 'description':'', 'weight':0, tags:[],'xf':'','selected':''},
        current_stage: '',
        substages: [],
        substages_reorder: [],
        substage_detail: '',
        current_sub_stage: '',
        update_substage_mode: false,
        update_stage_mode: false,
        sub_stage_form: '',
        forms: [],
        tags: [],
        form: '',
        selected_tags: [],
        stage_form_obj_edit: '',
        reorder_stages_mode: false,
        reorder_sub_stages_mode: false,
        show_em :false,
        em :'',
        new_em :false,
        new_em_obj : {'title':'', 'text':'', 'em_images':[], 'pdf':''},
        image: '',
        newShowTimeModal : false,
  },

  methods:{

  loadSiteTypes : function(){
      var self = this;
      if(self.is_project == 0){

        return
      }
        var options = {};

        function successCallback(response) {
            self.tags = response.body;
            self.loading = false;
        }

            function errorCallback() {
                self.loading = false;
                console.log('failed');
            }
            self.$http.get('/fieldsight/api/site-types/'+self.pk+'/', {
                params: options
            }).then(successCallback, errorCallback);



  },
  newType: function(){
    var self = this;
    self.newShowTimeModal = true;
    bus.$emit('new_entry_for', self.pk, self.is_project);

  },
    onImageChange(e) {
    var self = this;
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length)
        return;
        if(files.length){
             self.uploadEmFiles(files, true);
        };
    },
    onPDFChange(e) {
    var self = this;
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length)
        return;
        if(files.length){

            let csrf = $('[name = "csrfmiddlewaretoken"]').val();
            let options = {headers: {'X-CSRFToken':csrf, 'Content-Type': 'application/x-www-form-urlencoded'}};

            var formdata = new FormData();
              formdata.append('is_pdf', true);
              formdata.append('pdf', files[0]);

            function successCallback (response){
                self.new_em_obj =response.body.em;
                self.error = "";
                    new PNotify({
                  title: 'saved',
                  text: 'PDf  Saved '
                });

            }

            function errorCallback (response){
              new PNotify({
              title: 'failed',
              text: 'Failed to Save PDF',
              type: 'error'
            });

            if(response.body.error){
            console.log(response.body.error)
            }else{

                }
            }
       self.$http.post('/forms/api/em/files/'+ self.substage_detail.id +'/', formdata, options)
        .then(successCallback, errorCallback);
            }

    },
    uploadEmFiles(files, is_pdf){
        var self = this;
        let csrf = $('[name = "csrfmiddlewaretoken"]').val();
            let options = {headers: {'X-CSRFToken':csrf, 'Content-Type': 'application/x-www-form-urlencoded'}};
            var formdata = new FormData();
            for( let i=0; i< files.length; i++){
                formdata.append('new_images_'+String(i), files[i])
            }
            function successCallback (response){
            self.new_em_obj =response.body.em;
                self.error = "";
                    new PNotify({
                  title: 'saved',
                  text: 'Images  Saved '
                });

            }

            function errorCallback (response){
            console.log(response);
              new PNotify({
              title: 'failed',
              text: 'Failed to Save Images',
              type: 'error'
            });

            if(response.body.error){
            console.log(response.body.error)
            }else{

                }
            }
       self.$http.post('/forms/api/em/files/'+ self.substage_detail.id +'/', formdata, options)
        .then(successCallback, errorCallback);

    },
    createImage(file) {
    var self = this;
      var image = new Image();
      var reader = new FileReader();
//      var vm = this;

//      reader.onload = (e) => {
//        self.image = e.target.result;
//      };
//      reader.readAsDataURL(file);

    },
    removeImage: function (e) {
    var self = this;
      self.image = '';
    },

    addImage: function (e) {
    var self = this;
    self.new_em_obj.em_images.push(self.image);
      self.image = '';
    },

    updateEm: function(){
        var self = this;
        self.new_em = true;
    },
    newEm: function(){
        var self = this;
        self.new_em = true;
        self.new_em_obj = {'title':'', 'text':'', 'em_images':[], 'pdf':''};
    },

    cancel_em: function(){
        var self = this;
        self.new_em = false;
        self.new_em_obj = {'title':'', 'text':'', 'em_images':[], 'pdf':''};
    },

    save_em: function(){
         var self = this;
        let csrf = $('[name = "csrfmiddlewaretoken"]').val();
        let options = {headers: {'X-CSRFToken':csrf}};
        let data = self.new_em_obj;
        function successCallback (response){
        self.new_em_obj = response.body.em;
            self.error = "";
                new PNotify({
              title: 'Material Saved',
              text: 'material Detail Saved'
            });

        }

        function errorCallback (response){
        console.log(response);
          new PNotify({
          title: 'failed',
          text: 'Failed to Save Em',
          type: 'error'
        });
            if(response.body.error){
            console.log(response.body.error)
            }else{

            }
        }
   self.$http.post('/forms/api/em/'+ self.substage_detail.id +'/', data, options)
    .then(successCallback, errorCallback);
//            self.new_em = false;
//            self.new_em_obj = {'title':'', 'text':'', 'files':[]};

    },

    heightLevel: function(){
      var self = this;
      Vue.nextTick(function () {
              var panelHeight = $(window).height() - $("#header").height() - 79;
            $(".widget-info" ).each(function() {
                $(this).css('min-height', panelHeight);
            });
            }.bind(self));
      },
    activeStage: function(stage){
    var self = this;
    if(self.current_stage.hasOwnProperty("id")){
    return self.current_stage.id == stage.id;

    }
    return false;

  },
    activeSubStage: function(stage){
    var self = this;
    if(self.current_sub_stage.hasOwnProperty("id")){
    return self.current_sub_stage.id == stage.id;

    }
    return false;

  },

    reorderStages: function (){
        var self = this;
        self.stages_reorder = [];
        for(let i=0; i< self.stages.length; i++){
            self.stages_reorder.push(self.stages[i]);
        }

        self.reorder_stages_mode = true;
        self.update_stage_mode = false;
        self.show_ad_substage_form = false;
        self.current_stage='';
        self.substages = [];
        self.heightLevel();

    },
    reorderStagesCancel: function (){
        var self = this;
        self.stages_reorder = [];

        self.reorder_stages_mode = false;

    },
    reorderStagesSave: function (){
        var self = this;
        let csrf = $('[name = "csrfmiddlewaretoken"]').val();
        let options = {headers: {'X-CSRFToken':csrf}};
        let data = {'stages':self.stages_reorder};

        function successCallback (response){
        self.stages = response.body.data;
        let total = 0
        self.stages.map(function (a) {
                total += parseInt(a.sub_stage_weight);
        });
        for(let i=0; i< self.stages.length; i++){
        console.log("here");
        console.log(self.stages[i].sub_stage_weight);
            self.stages[i].weight_calculated = Math.round((self.stages[i].sub_stage_weight) /
                    (total)* Math.pow(10, 2));
             if(!self.stages[i].weight_calculated){
                    self.stages[i].weight_calculated = 0;
             }

        }
        self.stages_reorder = [];
        self.reorder_stages_mode = false;


        self.error = "";
            new PNotify({
          title: 'saved',
          text: 'Ordering  Saved'
        });

        }

        function errorCallback (response){
        console.log(response);
          new PNotify({
          title: 'failed',
          text: 'Failed to Ordering',
          type: 'error'
        });
            if(response.body.error){
            console.log(response.body.error)
            }else{

            }
        }
       self.$http.post('/forms/api/stages-reorder/', data, options)
        .then(successCallback, errorCallback);
        },

    reorderSubStages: function (){
        var self = this;
        self.substages_reorder = [];
        for(let i=0; i< self.substages.length; i++){
            self.substages_reorder.push(self.substages[i]);
        }

        self.reorder_sub_stages_mode = true;
        self.update_substage_mode = false;
        self.current_sub_stage='';
        self.substage_detail='';

    },
    reorderSubStagesCancel: function (){
        var self = this;
        self.substages_reorder = [];

        self.reorder_sub_stages_mode = false;

    },
    reorderSubStagesSave: function (){
        var self = this;
        let csrf = $('[name = "csrfmiddlewaretoken"]').val();
    let options = {headers: {'X-CSRFToken':csrf}};
    let data = {'stages':self.substages_reorder};
    function successCallback (response){
    self.substages = response.body.data;
    self.substages_reorder = [];
    self.reorder_sub_stages_mode = false;


    self.error = "";
        new PNotify({
      title: 'saved',
      text: 'Ordering  Saved'
    });

    }

    function errorCallback (response){
    console.log(response);
      new PNotify({
      title: 'failed',
      text: 'Failed to Ordering',
      type: 'error'
    });
        if(response.body.error){
        console.log(response.body.error)
        }else{

        }
    }
   self.$http.post('/forms/api/substages-reorder/', data, options)
    .then(successCallback, errorCallback);
    },

    saveNewSubStage: function () {
    var self = this;
    let csrf = $('[name = "csrfmiddlewaretoken"]').val();
    let options = {headers: {'X-CSRFToken':csrf}};
    self.substage_form_obj.order = self.substages.length;
    var tags = self.substage_form_obj.tags.map(function (a) {
                    return parseInt(a.id);
                });
    self.substage_form_obj.tags = tags;
    var default_status = self.substage_form_obj.selected;
    if(default_status =="Approved"){
        self.substage_form_obj.default_submission_status =3;
    }else{
        self.substage_form_obj.default_submission_status =0;
    }

    function successCallback (response){


    self.error = "";
        new PNotify({
      title: 'Sub Stage Saved',
      text: 'Sub Stage '+ response.body.name + ' Saved'
    });
    self.substages.push(response.body);

    let index = self.stages.findIndex(x => x.id==self.current_stage.id);
    let stage = self.stages[index];
    stage.sub_stage_weight += response.body.weight;

    let total = 0
        self.stages.map(function (a) {
                total += parseInt(a.sub_stage_weight);
        });
        console.log(total);
        for(let i=0; i< self.stages.length; i++){
            self.stages[i].weight_calculated = Math.round((self.stages[i].sub_stage_weight) /
                    (total)* Math.pow(10, 2));
            if(!self.stages[i].weight_calculated){
                    self.stages[i].weight_calculated = 0;
             }

        }



    self.show_ad_substage_form = false;
    self.heightLevel();

    }

    function errorCallback (response){
    console.log(response);
      new PNotify({
      title: 'failed',
      text: 'Failed to Save Sub Stage',
      type: 'error'
    });
        if(response.body.error){
        console.log(response.body.error)
          self.error = response.bodyText;
        }else{
            self.error = "Form Contains Invalid Inputs";

        }
    }
   self.$http.post('/forms/api/sub-stage-detail-create/'+self.current_stage.id+'/', self.substage_form_obj, options)
    .then(successCallback, errorCallback);


},
    update_sub_stage: function (){
            var self = this;
            self.update_substage_mode = true;
            self.reorder_sub_stages_mode = false;
        },
    loadTagsFromArray: function (tags){
        if(!tags || tags=="null") return []
        var tags_array = [];
        var self = this;
        for (var i = 0; i < self.tags.length; i++) {
                if (tags.indexOf(self.tags[i].id) != -1) {
                    tags_array.push(self.tags[i]);
                }
            }

            return tags_array;

    },
    update_stage: function (){
            var self = this;
            self.update_error = "";
            var tags = [];
            self.stage_form_obj_edit = {'name':self.current_stage.name, 'id': self.current_stage.id, 'description':
                                        self.current_stage.description,'tags':self.current_stage.tags,
                                         'weight_calculated':self.current_stage.weight_calculated,
                                         'sub_stage_weight':self.current_stage.sub_stage_weight,
                                         };
            self.update_stage_mode = true;
            self.heightLevel();
        },
    update_sub_done: function (){
        var self = this;
        self.update_substage_mode = false;
    },
    update_stage_done: function (){
        var self = this;
        self.update_error = "";
        self.update_stage_mode = false;
        self.heightLevel();
    },
    loadSubStageDetail: function (sub_stage_id) {
        var self = this;
        self.loading = true;
        var options = {is_project:self.is_project, pk:self.pk};

        function successCallback(response) {
            self.substage_detail = response.body;
            self.substage_detail.selected =  (response.body.default_submission_status == 3) ? "Approved" : "Pending" ;
            self.substage_detail.tags = self.loadTagsFromArray(response.body.tags);
            self.loading = false;
        }

        function errorCallback() {
            self.loading = false;
            console.log('failed');
        }
        self.$http.get('/forms/api/sub-stage-detail/'+sub_stage_id+'/', {
            params: options
        }).then(successCallback, errorCallback);
    },
    loadSubStages: function (stage_id) {
        var self = this;
        self.loading = true;
        var options = {};

        function successCallback(response) {
            self.substages = response.body;
            self.loading = false;
        }

        function errorCallback() {
            self.loading = false;
            console.log('failed');
        }
        self.$http.get('/forms/api/sub-stage-list/'+stage_id+'/', {
            params: options
        }).then(successCallback, errorCallback);
    },
    loadKoboForms: function () {
            var self = this;
            self.loading = true;
            var options = {};

            function successCallback(response) {
                self.forms = response.body;
                self.loading = false;
            }

            function errorCallback() {
                self.loading = false;
                console.log('failed');
            }
            self.$http.get('/forms/api/xforms/', {
                params: options
            }).then(successCallback, errorCallback);
        },
    loadStages: function () {
            var self = this;
            self.loading = true;
            var options = {};

            function successCallback(response) {
                self.stages = response.body;
                let total = 0
                self.stages.map(function (a) {
                        total += parseInt(a.sub_stage_weight);
                });
                for(let i=0; i< self.stages.length; i++){
                    self.stages[i].weight_calculated = Math.round((self.stages[i].sub_stage_weight) /
                            (total)* Math.pow(10, 2));

                    if(!self.stages[i].weight_calculated){
                        self.stages[i].weight_calculated = 0;
                    }

                }

                self.loading = false;
            }

            function errorCallback() {
                self.loading = false;
                console.log('failed');
            }
            self.$http.get('/forms/api/stage-list/'+self.is_project+'/'+self.pk+'/', {
                params: options
            }).then(successCallback, errorCallback);
        },

    add_stage : function (){
            var self = this;
            self.error = "";
            self.stage_form_obj = {'name': '', 'description':'', 'id':'', 'tags':[]};
            self.show_ad_stage_form = true;
        },

    add_substage : function (){
            var self = this;
            self.error = "";
            self.update_stage_mode = false;
            self.substage_form_obj = {'name': '', 'description':'', 'id':'', 'weight':0, 'tags':self.current_stage.tags, 'xf':'', 'selected':'Pending'};
            self.show_ad_substage_form = true;
            self.heightLevel();
        },
    save_sub_stage : function (){
            var self = this;
            self.error = "";
            if(self.substage_form_obj.name.length >0){
                self.saveNewSubStage();
            }else{
            self.error = "Sub Stage Name Required";
            new PNotify({
          title: 'Required ',
          text: 'Sub Stage Name Required.',
          type: 'error'
        });

            }
        },
    do_update_sub_stage : function (){
            var self = this;
            self.error = "";
            self.saveExistingSubStage();

        },
    do_update_stage : function (){
            var self = this;
            self.error = "";
            self.saveExistingStage();

        },
    cancel_stage : function (){
            var self = this;
            self.show_ad_stage_form = false;
            self.stage_form_obj = {'name': '', 'description':'', 'id':''};
            self.heightLevel();
        },
    cancel_sub_stage : function (){
            var self = this;
            self.update_substage_mode = false;
            self.show_ad_substage_form = false;
            self.substage_form_obj = {'name': '', 'description':'', 'id':'', 'weight':0, 'tags':[], 'xf':''};;
            self.current_sub_stage = '';
            self.heightLevel();
        },

    saveNewStage: function () {
        var self = this;
        let csrf = $('[name = "csrfmiddlewaretoken"]').val();
        let options = {headers: {'X-CSRFToken':csrf}};
        self.stage_form_obj.order = self.stages.length;
        var tags = self.stage_form_obj.tags.map(function (a) {
                    return parseInt(a.id);
                });
        self.stage_form_obj.tags = tags;
        function successCallback (response){

        self.error = "";
            new PNotify({
          title: 'Stage Saved',
          text: 'Stage '+ response.body.name + ' Saved'
        });
        console.log(response.body);
        response.body.weight_calculated = 0;
        self.stages.push(response.body);
        self.show_ad_stage_form = false;
        self.heightLevel();
        }

        function errorCallback (response){
        console.log(response);
          new PNotify({
          title: 'failed',
          text: 'Failed to Save Stage',
          type: 'error'
        });
            if(response.body.error){
            console.log(response.body.error)
              self.error = 'Failed to Save Stage';
            }else{
                self.error = "Stage Name Required !.";

            }
        }
       self.$http.post('/forms/api/stage-list/'+self.is_project+'/'+self.pk+'/', self.stage_form_obj, options).then(successCallback, errorCallback);


    },

    saveExistingSubStage: function () {
        var self = this;
        let csrf = $('[name = "csrfmiddlewaretoken"]').val();
        let options = {headers: {'X-CSRFToken':csrf}};
        self.substage_detail.xf = self.form;

        var tags = self.substage_detail.tags.map(function (a) {
                    return parseInt(a.id);
                });
        self.substage_detail.tags = tags;

        var default_status = self.substage_detail.selected;
    if(default_status =="Approved"){
        self.substage_detail.default_submission_status =3;
    }else{
        self.substage_detail.default_submission_status =0;
    }

        function successCallback (response){

        self.error = "";
            new PNotify({
          title: 'Sub Stage Updated',
          text: 'Sub Stage '+ response.body.name + ' Updated'
        });
        var index = self.substages.findIndex(x => x.id==response.body.id);

        var updated_substage = response.body;
        updated_substage.tags = self.loadTagsFromArray(response.body.tags);

        Vue.set(self.substages, index, updated_substage);

        let index_stage = self.stages.findIndex(x => x.id==self.current_stage.id);
        let stage = self.stages[index_stage];

        console.log(self.current_sub_stage.weight);
        stage.sub_stage_weight =  stage.sub_stage_weight + response.body.weight - self.current_sub_stage.weight;

    let total = 0
        self.stages.map(function (a) {
                total += parseInt(a.sub_stage_weight);
        });
        for(let i=0; i< self.stages.length; i++){
            self.stages[i].weight_calculated = Math.round((self.stages[i].sub_stage_weight) /
                    (total)* Math.pow(10, 2));
            if(!self.stages[i].weight_calculated){
                    self.stages[i].weight_calculated = 0;
             }

        }

        self.update_substage_mode = false;
        self.current_sub_stage = response.body;
        self.substage_detail = response.body;
        self.heightLevel();
        }

        function errorCallback (response){
          new PNotify({
          title: 'failed',
          text: 'Failed to Update sub Stage',
          type: 'error'
        });
            if(response.body.error){
            console.log(response.body.error)
              self.error = response.body.error;
            }else{
                self.error = "Incorrect Form Data !.";

            }
        }
       self.$http.put('/forms/api/sub-stage-detail/'+self.substage_detail.id+'/', self.substage_detail, options).then(successCallback, errorCallback);


    },
    saveExistingStage: function () {
        var self = this;
        let csrf = $('[name = "csrfmiddlewaretoken"]').val();
        let options = {headers: {'X-CSRFToken':csrf}};

        var tags = self.stage_form_obj_edit.tags.map(function (a) {
                    return parseInt(a.id);
                });
        self.stage_form_obj_edit.tags = tags;

        var backup_sub_stage_weight_calculated = self.stage_form_obj_edit.weight_calculated;
        var backup_sub_stage_weight = self.stage_form_obj_edit.sub_stage_weight;

//        delete Object.getPrototypeOf(self.stage_form_obj_edit).sub_stage_weight;

        function successCallback (response){

        console.log(response);

        self.update_error = "";
            new PNotify({
          title: 'Stage Updated',
          text: 'Stage '+ response.body.name + ' Updated'
        });
        var index = self.stages.findIndex(x => x.id==response.body.id);


        response.body.weight_calculated = backup_sub_stage_weight_calculated;
        response.body.sub_stage_weight = backup_sub_stage_weight;
        console.log(response.body);


        Vue.set(self.stages, index, response.body);

        self.update_stage_mode = false;
        self.stage_form_obj_edit = '';
//        self.current_stage = self.stages[index];
//        let tags = self.loadTagsFromArray(response.body.tags);
//            self.current_stage.tags = tags;
            self.stageDetail(self.stages[index]);
            self.heightLevel();
        }

        function errorCallback (response){
          new PNotify({
          title: 'failed',
          text: 'Failed to Update Stage',
          type: 'error'
        });
        console.log(response.body);
            if(response.body.error){
            console.log(response.body.error)
              self.update_error = response.body.error;
            }else{
                self.update_error = "Incorrect Form Data !.";

            }
        }
       self.$http.put('/forms/api/configure-stage-update/'+self.stage_form_obj_edit.id+'/', self.stage_form_obj_edit, options).then(successCallback, errorCallback);


    },
    save_stage : function (){
        var self = this;
        if(!self.stage_form_obj.name){
        self.error = "Stage Name required";
        return;
        }
        self.error = "";
        if(!self.stage_form_obj.id){
            self.saveNewStage();
          }else{
          console.log("Update stage ");
          }
    },
    stageDetail : function (stage){
        var self = this;
            let tags = self.loadTagsFromArray(stage.tags);
        self.current_stage = Object.assign({}, stage);
        self.current_stage.tags = tags;
        self.reorder_stages_mode = false;
    },

    substageDetail : function (stage){
        var self = this;
        self.current_sub_stage = stage;
    },
    loadEm : function(){
        var self = this;
        self.new_em = true;
        self.show_ad_substage_form = false;
        self.update_substage_mode = false;
        self.reorder_stages_mode = false;
        if(self.substage_detail.has_em){
            self.getEm(self.substage_detail.id);
        }else{
            self.new_em_obj = {'title':'', 'text':'', 'em_images':[], 'pdf':''};
        }
    },
    hideEm : function(){
        var self = this;
        self.new_em = false;
        self.show_ad_substage_form = false;
        self.update_substage_mode = false;
        self.reorder_stages_mode = false;
        self.new_em_obj = {'title':'', 'text':'', 'em_images':[], 'pdf':''};

    },
    getEm : function(id){
        var self = this;
        self.loading = true;
        var options = {};

        function successCallback(response) {
            self.new_em_obj = response.body;
            self.loading = false;
        }

        function errorCallback() {
            self.loading = false;
            console.log('failed');
        }
        self.$http.get('/forms/api/get_em/'+id+'/', {
            params: options
        }).then(successCallback, errorCallback);

    },

    deployStages: function(){
                var self = this;

        self.$dialog.confirm('All Existing Stages Will be Deleted')
            .then(function () {


            var api_url = '/forms/api/set-deploy-all-stages/' + self.is_project + '/' + self.pk+'/'

            self.loading = true;
            var options = {};

            function successCallback(response) {
                console.log(response);

                new PNotify({
                      title: 'Stages Deployed',
                      text: 'Stages Deployed'
                    });
            }

            function errorCallback(errorThrown) {
                self.loading = false;

                console.log(errorThrown);
                 new PNotify({
                      title: 'Failed',
                      text: 'Stages Deployed Failed'
                    });
            }
            self.$http.get(api_url, {
                params: options
            }).then(successCallback, errorCallback);
        })
        .catch(function () {
            console.log('Clicked on cancel')
        });
    },

    deploySubStages: function(){
        var self = this;
        self.$dialog.confirm('All Existing SubStages Will be Deleted')
            .then(function () {


                var api_url = '/forms/api/set-deploy-main-stage/' + self.is_project + '/' + self.pk+'/' + self.current_stage.id + '/'

                self.loading = true;
                var options = {};

                function successCallback(response) {
                    console.log(response);
                    self.current_stage = response.body;
                    let tags = self.loadTagsFromArray(response.body.tags);
                    self.current_stage.tags = tags;
                    self.loading = false;
                    new PNotify({
                          title: 'Stage Deployed',
                          text: 'Stage Deployed'
                        });
                }

                function errorCallback(errorThrown) {
                    self.loading = false;

                    console.log(errorThrown);
                     new PNotify({
                          title: 'Failed',
                          text: 'Stage Deployed Failed'
                        });
                }
                self.$http.get(api_url, {
                    params: options
                }).then(successCallback, errorCallback);
    })
        .catch(function () {
            console.log('Clicked on cancel')
        });
    },

    deploySubStage: function(){
        var self = this;
        self.$dialog.confirm('Please Confirm Deployment')
            .then(function () {
            var api_url = '/forms/api/set-deploy-sub-stage/' + self.is_project + '/' + self.pk+'/' + self.current_sub_stage.id + '/'
            console.log(self.current_sub_stage.id);

            self.loading = true;
            var options = {};

            function successCallback(response) {
                self.current_sub_stage = response.body;
                self.loading = false;
                new PNotify({
                      title: 'Sub Stage Deployed',
                      text: 'Sub Stage Deployed'
                    });
            }

            function errorCallback(errorThrown) {
                self.loading = false;

                console.log(errorThrown);
                 new PNotify({
                      title: 'Failed',
                      text: 'Sub Stage Deployed Failed'
                    });
            }
            self.$http.get(api_url, {
                params: options
            }).then(successCallback, errorCallback);
        })
        .catch(function () {
            console.log('Clicked on cancel')
        });


    },
  },
  watch: {
    current_stage: function(newVal, oldVal) {
    var self = this;
    if (newVal){
//    console.log(newVal.tags);
    self.reorder_sub_stages_mode = false;
    self.reorder_stages_mode = false;
      self.substages = [];
      self.substage_detail = '';
      self.update_stage_mode = false;
      self.loadSubStages(newVal.id);
      self.heightLevel();
      }

    },
    current_sub_stage: function(newVal, oldVal) {
    var self = this;
    if (newVal){
    self.reorder_sub_stages_mode = false;
      self.substage_detail = '';
      self.loadSubStageDetail(newVal.id);
      self.heightLevel();
      }

    },
    substage_detail: function(newVal, oldVal) {
    var self = this;
    self.show_em = false;
    self.em = '';
    self.new_em = false;
    self.new_em_obj = {'title':'', 'text':'', 'em_images':[], 'pdf':''};
    if (newVal){
        self.reorder_sub_stages_mode = false;
        if(newVal.stage_forms){
            self.form = {'id':newVal.stage_forms.xf.id, 'title':newVal.stage_forms.xf.title};
       }else{
       self.form = '';
      }}else{
      self.form = '';
      }
      self.heightLevel();

    },
  },
    computed: {
    form_name: function() {
        var self = this;
        if(self.substage_detail.stage_forms){
            return self.substage_detail.stage_forms.xf.title;
            }
        return "No Form Assigned Yet";
    },

    has_form: function() {
        var self = this;
        if(self.substage_detail.stage_forms){
            return true;
            }
        return false;
    },

    read_only: function(){
        var self = this;
        if (self.is_project == '1'){return false}
        if(self.stages.length){
            for(var i=0; i < self.stages.length; i++){
                    if(self.stages[i].site == null){
                        return true;
                    }
            }
            
        }
        return false;

    },
    read_only_stage: function(){
        var self = this;
        if (self.is_project == '1'){return false}
        if (!self.current_stage){return false}
        console.log(self.current_stage);
        if(self.current_stage.site == null){
            return true;
        }
        return false;

    },

    },
  created(){
    var self= this;
    self.loadStages();
    self.loadKoboForms();
    self.loadSiteTypes();
    bus.$on('new_entry', function(new_entry){
        self.tags.push(new_entry);
        self.stage_form_obj.tags.push(new_entry);
        }.bind(self));
  },

  filters: {
  slice: function(value) {
    if (!value) return ''
    value = value.toString()
    if(value.length>13){
    return value.charAt(0).toUpperCase() + value.slice(1,12) + ".."
    }
    return value.charAt(0).toUpperCase() + value.slice(1)
  }
}

})