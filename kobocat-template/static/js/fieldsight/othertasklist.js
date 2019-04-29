window.app = new Vue({
  el: '#othertasklist',
  template: `
          <div style="height: 800px; overflow-x:auto;" @scroll="infiniteScroll">
            <div v-if="processed_data.length == 0" class="dropdown-header text-center mt-3 zeromytasks">No Task Notifications</div>  
            <template v-for="(value, key, index) in processed_data">
              <div class="task-item" v-html="value"></div>
            </template>
            <div class="container-fluid">
              <div class="row justify-content-center">
                <div class="col-md-6 col-lg-4">
                  <button v-if="load_next_url" v-on:click="loadDatas" class="btn btn-sm btn-block btn-primary margin-top">Load more</button>
                </div>
              </div>
            </div>
          </div>
          `,
  data: {
        raw_data: [],
        processed_data: [],
        dates:[],
        load_next_url:configure_settings.othertasks_url,
     },

  methods:{
    
    loadDatas : function (){
    var self = this;

    self.loading = true;
    

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

    

    self.$http.get(self.load_next_url).then(successCallback, errorCallback);

    },
    infiniteScroll: function (event) {
      var self = this;
      if (((event.target.scrollTop + event.target.offsetHeight) >= event.target.scrollHeight) && self.load_next_url) {
        this.loadDatas();
      }
    },

    tasklistgenerate: function(data, status){
      var additional_content = "";
      if (data.status == 2){
        if ([3,6,8,9,10].indexOf(data.task_type) >= 0){
              status = " is ready to download. "
              var url  = data.file
              if (data.task_type == 10){
                var new_url = url.split("/media/")
                url = "/media/" + new_url[1];
              }
              additional_content = "<br/><a href='"+ url +"'>Download File</a>";
          }
      }
      content = data.get_task_type_display + " of " +  "<a href='"+ data.get_event_url +"'>" + data.get_event_name + "</a>" + status;
      return content + additional_content;
    },

    createContent: function(data, index){
      var self = this;

      // function parseDate(str_date) {
      //   return new Date(Date.parse(str_date));
      // }

      var status = "";
      var icon = "";
      var title = "";
      var div_class = "";
      var div_subclass = "";
      var error_msg = "";

      if (data.status == 0){
          status = ' has been added to Queue.';
        icon = "la la-hourglass-1";
        title = "Added";
        div_class = "task-pending";
        div_subclass = "text-warning";
      }
      else if (data.status == 1){
          status = ' has been started.';       
        icon = "la la-hourglass-2";
        title = "Started";
        div_class = "task-ongoing";
        div_subclass = "text-info";
      }
      else if (data.status == 2){
          status = ' has completed.';
        icon = "la la-check-circle";
        title = "Completed";
        div_class = "task-success";
        div_subclass = "text-success";
      }
      else{
          status = ' has failed.';
        icon = "la la-times-circle";
        title = "Failed";
        div_class = "task-error";
        div_subclass = "text-danger";
        error_msg = "<b>Error message:</b> " + data.description + "<br/><br/>" ;
      }

      var task_content = self.tasklistgenerate(data, status);
      var new_li = `
                <div class="task-icon `+ div_subclass +`">
                  <i class="`+ icon +`"></i>
                </div>
                <div class="task-highlight">
                  <p class="task-title"><strong>`+title+`</strong></p>
                  <p class="task-highlight-excerpt">
                    `+ task_content +`
                  </p>
                  <p class="task-detail-handler">See Detail</p>
                  <p class="task-detail-content collapse">
                  `+ error_msg +`
                    Added on ` + dateparser(data.date_added) + `<br/>
                    `+ title +` on ` + dateparser(data.date_updateded) + `
                  </p>
            </div>`;

      self.processed_data.push(new_li);
          
      },

  processData : function (){
    var self = this;
    self.raw_data.forEach(self.createContent);
    $(".widget-scrolling-large-list > .widget-body, .widget-scrolling-list > .widget-body").getNiceScroll().resize();  
    },
  },

  created(){
    var self= this;
    self.loadDatas();
  },

  updated() {
      this.$nextTick(function () {
        $(".task-detail-handler").off("click");
              $('.task-detail-handler').on('click', function(event){
               event.stopPropagation();
               $(this).siblings('.task-detail-content').collapse('toggle');
               var hsText = $(this).text();
               if(hsText == 'See Detail'){
                  $(this).text('Hide Detail');
               }else{
                  $(this).text('See Detail');
               }
             });
          })
    }
})