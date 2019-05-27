(function($) {
    "use strict";
    $(document).ready(function() {
        //scroll bar
        function CustomScrollbar() {
            // $("#siteinfo_table").slimscroll({
            //     height: "300px",
            //     color: "#8c909a",
            //     position: "right",
            //     size: "2px",
            //     alwaysVisible: !1,
            //     borderRadius: "3px",
            //     railBorderRadius: "0"
            // }),  
            $(".navbar-right .dropdown-menu .body").slimscroll({
                height: "330px",
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
            $('.add-btn').on('click', 'a', function(e) {
                e.preventDefault();
                var targetId = $(this).attr('data-tab');
                $('#' + targetId).addClass('open');
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

        //Click event to scroll to top
        $('.scroll-up').on('click', function() {
            $('html, body').animate({ scrollTop: 0 }, 900);
            return false;
        });
        
        //nice select
        $('.wide').niceSelect();

        //site identiry dropdown show
        $(".photo-choose-form").on('click', '.list li:nth-child(2)', function() {
            $(this).closest('form').find('.hide-form').toggle(300);
          });
          $(".location-choose-form").on('click', '.list li:nth-child(2)', function() {
            $(this).closest('form').find('.hide-form').toggle(300);
          });

          //tooltip
          $('[data-toggle="tooltip"]').tooltip()
        
    });
})(jQuery);

