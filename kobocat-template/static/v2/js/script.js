(function($) {
    "use strict";
    $(document).ready(function() {
        //scroll bar
        function CustomScrollbar() {
            $("#siteinfo_table").slimscroll({
                height: "300px",
                color: "#8c909a",
                position: "right",
                size: "4px",
                alwaysVisible: !1,
                borderRadius: "3px",
                railBorderRadius: "0"
            }), 
            $(".invite-popup ul").slimscroll({
                height: "250px",
                color: "#8c909a",
                position: "right",
                size: "4px",
                alwaysVisible: !1,
                borderRadius: "3px",
                railBorderRadius: "0"
            }),  
            $(".submission-sidebar .thumb-list").slimscroll({
                height: "550px",
                color: "#8c909a",
                size: "3px",
                alwaysVisible: !1,
                borderRadius: "3px",
                railBorderRadius: "0"
            });
            $(".project-list .thumb-list").slimscroll({
                height: "500px",
                color: "#8c909a",
                size: "3px",
                alwaysVisible: !1,
                borderRadius: "3px",
                railBorderRadius: "0"
            });
            $(".recent-photo .gallery").slimscroll({
                height: "416px",
                color: "#8c909a",
                size: "3px",
                alwaysVisible: !1,
                borderRadius: "3px",
                railBorderRadius: "0"
            });
            $(".board-site-info ul").slimscroll({
                height: "424px",
                color: "#8c909a",
                size: "3px",
                alwaysVisible: !1,
                borderRadius: "3px",
                railBorderRadius: "0"
            });
            $(".admin .thumb-list").slimscroll({
                height: "232px",
                color: "#8c909a",
                size: "3px",
                alwaysVisible: !1,
                borderRadius: "3px",
                railBorderRadius: "0"
            });
            $(".mangager-list .thumb-list").slimscroll({
                height: "232px",
                color: "#8c909a",
                size: "3px",
                alwaysVisible: !1,
                borderRadius: "3px",
                railBorderRadius: "0"
            });
            $(".about-section .logs-list").slimscroll({
                height: "232px",
                color: "#8c909a",
                size: "3px",
                alwaysVisible: !1,
                borderRadius: "3px",
                railBorderRadius: "0"
            });
            $(".about-section .about-body").slimscroll({
                height: "276px",
                color: "#8c909a",
                size: "3px",
                alwaysVisible: !1,
                borderRadius: "3px",
                railBorderRadius: "0"
            });
            $(".submission-site-info ul").slimscroll({
                height: "282px",
                color: "#8c909a",
                size: "3px",
                alwaysVisible: !1,
                borderRadius: "3px",
                railBorderRadius: "0"
            });
            $(".popup-scroll").slimscroll({
                height: "500px",
                color: "#8c909a",
                size: "3px",
                alwaysVisible: !1,
                borderRadius: "3px",
                railBorderRadius: "0"
            });
        }
        CustomScrollbar();


        //popup modal show
        function showPopup(){
            $('.invite-popup').on('click', '.popup-close', function(e) {
                e.preventDefault();
                // var cardHide = $('.invite-popup .card').animate({width:"0"});
                // $(this).closest('.invite-popup').toggle(cardHide);
                $(this).closest('.invite-popup').toggleClass('hide');
            });
        }
        showPopup();

        //popclose
        function closePopup(){
            $('.fieldsight-popup').on('click', '.popup-close, .fieldsight-btn', function(e) {
                e.preventDefault();
                $(this).closest('.fieldsight-popup').removeClass('open');
            });
        }
        closePopup();

        //popup modal show
        function invitePop(){
            $('.add-btn').on('click', 'a', function(e) {
                e.preventDefault();
                var targetId = $(this).attr('data-tab');
                $('#' + targetId).addClass('open');
            });
        }
        invitePop();

        //Click event to scroll to top
        $('.scroll-up').on('click', function() {
            $('html, body').animate({ scrollTop: 0 }, 900);
            return false;
        });
        
        

        //site identiry dropdown show
        $(".photo-choose-form").on('click', '.list li:nth-child(2)', function() {
            $(this).closest('form').find('.hide-form').toggle(300);
          });
          $(".location-choose-form").on('click', '.list li:nth-child(2)', function() {
            $(this).closest('form').find('.hide-form').toggle(300);
          });

          //tooltip
          $('[data-toggle="tooltip"]').tooltip();

          $('a[data-toggle="tab"]').on('shown.bs.tab', function(e){
            $($.fn.dataTable.tables(true)).DataTable()
               .columns.adjust();
         });
         $('#accordion').on('shown.bs.collapse', function() {
            $.each($.fn.dataTable.tables(true), function(){
                $(this).DataTable()
                .columns.adjust()
                .responsive.recalc();
            });
        });

        $(".progress-bar").each(function () {
            var now=$(this).attr('aria-valuenow')
            var max=$(this).attr('aria-valuemax')
            var $percent = (now / max) * 100;
            // each_bar_width = $(this).attr('aria-valuenow');
            $(this).width(Math.round($percent) + '%');
            $(this).closest('.progress').find('.progress-count').html(Math.round($percent) + '%');
            $(this).parent().find('.progress-value').html(" " + now);
        });

        

         //nice select
        $('.wide').niceSelect();

        //select2
        $('.select2').select2();
        //  window.onresize = function() {
        //     $($.fn.dataTable.tables(true)).DataTable()
        //     .columns.adjust()
        //     .responsive.recalc();
        //     }

        $('.video-preview').magnificPopup({
            type: 'iframe',
            mainClass: 'mfp-fade',
            preloader: true,
        });

        $('.photo-item a.photo-preview').magnificPopup({
            type: 'image',
            gallery:{
              enabled:true
            }          
          });
        
    });
})(jQuery);

