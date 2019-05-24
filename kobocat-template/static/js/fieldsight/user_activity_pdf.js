Vue.component('treeselect', VueTreeselect.Treeselect)
var LOAD_CHILDREN_OPTIONS = this.VueTreeselect.LOAD_CHILDREN_OPTIONS
var LOAD_ROOT_OPTIONS = this.VueTreeselect.LOAD_ROOT_OPTIONS

Vue.use(window.AirbnbStyleDatepicker, {
  sundayFirst: true,
  colors: {
    selected: '#00628e',
    inRange: '#00628e',
    selectedText: '#fff',
    text: '#565a5c',
    inRangeBorder: '#00628e',
    disabled: '#fff',

  }
})

window.app = new Vue({
  el: '#generateUserActivityPDFReport',
  data: {
        buttonDisabled: false,
        date1: '',
        date2: '', 
        minDate: configure_settings.start_date_min_value,
        maxDate: configure_settings.end_date_max_value,
        users: null,
        selected_user: null,
        project_id: null,
     },

  template: `
        <div class="modal-body p-3">
          <div class="form-group">
            <h5>Individual Activity Report</h5>
              <div class="text-center">
                <div class="rounded-circle p-4 bg-light" style="height: 150px;width: 150px;margin: 32px auto;">
                  <i style="font-size: 52px;" class="la la-file-excel-o ml-2 text-success m-4"></i>
                </div>
                <p>
                  Export of User's Activities <br> in a selected time interval.
                </p>
              </div>

          </div>
          <div class="form-item-wrapper checkbox-listing">
              <div class="row">
                  <div class="col-md-12 col-lg-12">
                    <div class="form-group">
                      <label for="startdate">Select Date Range:</label>
                      <div class="datepicker-trigger">
                      <input type="text" id="trigger-range1" :value="date1 + ' - ' + date2" readonly>
                      <airbnb-style-datepicker
                        :trigger-element-id="'trigger-range1'"
                        :date-one="date1"
                        :date-two="date2"
                        :min-date="minDate"
                        :end-date="maxDate"
                        v-on:date-one-selected="function(val) { date1 = val }"
                        v-on:date-two-selected="function(val) { date2 = val }"
                      ></airbnb-style-datepicker>
                      </div>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 col-lg-12">
                  <div class="form-group">
                    <label for="startdate">Select User:</label>
                      <treeselect :multiple="false"
                      :options="users"
                      :load-options="loadOptions"
                      :auto-load-root-options="false"
                      placeholder="Select User"
                      v-model="selected_user" />
                  </div>
                </div>
              </div>
              <a :disabled="(date1 == '' || date2 == '' || selected_user == null) ? true : false " :href="'/fieldsight/user/report/activity/' + project_id + '/'+ selected_user + '/' + date1 + '/' + date2 + '/'"><button type="button" class="btn btn-success"> Preview PDF</button></a>
          </div>
        </div>
          `,
  

  methods:{

    loadOptions({ action, parentNode, callback }) {
      function successCallback(response) {
        this.users = response.body
        if(response.body[0].project_id){
                this.project_id = response.body[0].project_id;

        }

        callback()
      }
      
      function errorCallback() {
         callback(new Error('Failed to load options: network error.'))
      }
   
      if (action === LOAD_ROOT_OPTIONS) {
          this.$http.get(configure_settings.project_managers).then(successCallback, errorCallback);          
      }
    }
  }
})