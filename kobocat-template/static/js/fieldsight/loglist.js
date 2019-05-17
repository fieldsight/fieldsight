window.app = new Vue({
  el: '#logdatas',
  template: `
    <div class="row">
            <div class="col-md-12">
              <div :class="is_full_log_page ? 'widget-info margin-top bg-white padding':'widget-info widget-scrolling-large-list margin-top bg-white padding'">
                <div class="widget-head">
                  <h4>Logs</h4>
                  <template v-if="!is_full_log_page">
                    <a v-bind:href="full_log_url" class="btn btn-xs btn-primary"><i class="la la-list"></i></a>
                  </template>
                </div>
                <div id="logbody" class="widget-body" @scroll="infiniteScroll">

                <div v-for="(value, key, index) in processed_data" v-bind:key="key" class="log-wrap">
                    <h6>{{ value.date }}</h6>
                    <ul class="log-list">
                     <li v-for="log in value.logs"  v-bind:key="log.id">
                        <span class="time">{{ log.datetime.time }}</span>
                        <img v-bind:src= "log.source_img" alt="Profile Pic">
                        <span v-html="log.content"></span>
                      </li>
                    </ul>
                  </div>
                  <div class="container-fluid">
                  <div class="row justify-content-center">
                    <div class="col-md-6 col-lg-4">
                      <button v-if="load_next_url" v-on:click="loadDatas" class="btn btn-sm btn-block btn-primary margin-top">Load more</button>
                    </div>
                  </div>
                  </div>
                </div>
              </div>
            </div>
          </div>`,
  data: {
        raw_data: [],
        processed_data: [],
        dates:[],
        load_next_url:configure_settings.log_url,
        full_log_url:configure_settings.full_log_url,
        is_full_log_page : 'is_full_log_page' in configure_settings,
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
        self.raw_data = response.body.results;
        self.loading = false;
        self.load_next_url = response.body.next;
        self.processData();
    }

    function errorCallback() {
        self.loading = false;
        console.log('failed');
    }

    

    self.$http.get(self.load_next_url, {
        params: options
    }).then(successCallback, errorCallback);

    },
    infiniteScroll: function (event) {
      var self = this;
      if (((event.target.scrollTop + event.target.offsetHeight) >= event.target.scrollHeight) && self.load_next_url) {
        this.loadDatas();
      }
    },
    datelogger: function(item, index){
      var self = this;

      // function parseDate(str_date) {
      //   return new Date(Date.parse(str_date));
      // }

     
      datetime = dateTimeParser(item.date);
      item.datetime =datetime;
      // console.log(item.type);
      item.content=types[item.type](item);
      
      // item.localtime=date_local;
      date_str = datetime.date;
      
      if (!self.dates.includes(date_str)){
          
          self.dates.push(date_str);
          var index = self.dates.indexOf(date_str);
          self.processed_data.splice(index, 0, {'date':item.datetime.date, 'logs':[item]});

        }
      else{
          var index = self.dates.indexOf(date_str);
          log_list = self.processed_data[index];
          
          log_list.logs.push(item);
          self.processed_data[index]=log_list; 
          //console.log(log_list.logs);

        }
      },

    processData : function (){
        var self = this;
        self.raw_data.forEach(self.datelogger);
        $(".widget-scrolling-large-list > .widget-body, .widget-scrolling-list > .widget-body").getNiceScroll().resize();  
        //console.log(self.processed_data);
        // console.log(self.dates);

    },


  },
  created(){
    var self= this;
    self.loadDatas();
  },

})