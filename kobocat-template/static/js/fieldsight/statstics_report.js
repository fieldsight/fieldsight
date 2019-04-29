

    // install plugin
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
  el: '#generateStatsticsReport',
  data: {
        buttonDisabled: false,
        date1: '',
        date2: '', 
        reportType: "Monthly",
        minDate: configure_settings.start_date_min_value,
        maxDate: configure_settings.end_date_max_value,
     },

  template: `
    
          
        <div class="modal-body p-3">
          <div class="form-group">
            <h5>Activity Report</h5>
              <div class="text-center">
                <div class="rounded-circle p-4 bg-light" style="height: 150px;width: 150px;margin: 32px auto;">
                  <i style="font-size: 52px;" class="la la-file-excel-o ml-2 text-success m-4"></i>
                </div>
                <p>
                                Export of site visits, submissions and active users <br> in a selected time interval.
                </p>
              </div>

          </div>
          <div class="form-item-wrapper checkbox-listing">
              <div class="row">
                  
                  <div class="col-md-12 col-lg-12">

                    <div class="form-group">
                      <label for="startdate">Select Report Type:</label>
                      <br>
                      <input type="radio" id="one" value="Daily" v-model="reportType">
                      <label for="one">Daily</label>
                     
                      <input type="radio" id="two" value="Weekly" v-model="reportType">
                      <label for="two">Weekly</label>
                     
                      <input type="radio" id="two" value="Monthly" v-model="reportType">
                      <label for="two">Monthly</label>
                  </div>
                </div>
              </div>

              <div class="row">
                  <div class="col-md-12 col-lg-12">
                    <div class="form-group">
                      <label for="startdate">Select Date Range:</label>
                      <div class="datepicker-trigger">
                      <input type="text" id="trigger-range" :value="date1 + ' - ' + date2" readonly>
                      <airbnb-style-datepicker
                        :trigger-element-id="'trigger-range'"
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
              <button type="button" :disabled="buttonDisabled" @click="generateStatsticsReport()" class="btn btn-success"> Generate Excel</button>
          </div>
        </div>

    

        
          `,
  

  methods:{
    
    generateStatsticsReport : function (){
      this.buttonDisabled = true;
    function successCallback(response) {
      alert(response.body.message);
      this.buttonDisabled = false;
    }
    
    function errorCallback() {
      alert('Failed to complete the request. Please try again.')
      this.buttonDisabled = false;
    }

    options = {headers: {'X-CSRFToken':configure_settings.csrf_token}};
    if (this.date1 == "" || this.date2 == ""){
      this.buttonDisabled = false;
      return alert("Please select date range to generate report from.");
      
    }
    body = {'startdate': this.date1, 'enddate': this.date2, 'type': this.reportType}
    
    console.log(body)
    this.$http.post(configure_settings.genarete_statstics_report_url, body, options).then(successCallback, errorCallback);     
    },
  }
})