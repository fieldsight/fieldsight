/**
 * Created by wrufesh on 10/3/16.
 */
var App = (function () {
    var remotePostProcessing = function (url, data, defaultCallback, failureCallback) {
        data['csrfmiddlewaretoken'] = $('[name = "csrfmiddlewaretoken"]').val();
        $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", data['csrfmiddlewaretoken']);
            }
        })
            .done(defaultCallback)
            .fail(failureCallback);
    };

    // Post with file data
    var remoteMultipartPostProcessing = function (url, data, defaultCallback, failureCallback) {
        data['csrfmiddlewaretoken'] = $('[name = "csrfmiddlewaretoken"]').val();
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", data['csrfmiddlewaretoken']);
            }
        })
            .done(defaultCallback)
            .fail(failureCallback);
    };
    // Post with file data end

    // Remote patch
    var remotePatchProcessing = function (url, data, defaultCallback, failureCallback) {
        data['csrfmiddlewaretoken'] = $('[name = "csrfmiddlewaretoken"]').val();
        $.ajax({
            url: url,
            type: 'PATCH',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", data['csrfmiddlewaretoken']);
            }
        })
            .done(defaultCallback)
            .fail(failureCallback);
    };
    // End Remote Patch

    var remotePutProcessing = function (url, data, defaultCallback, failureCallback) {
        data['csrfmiddlewaretoken'] = $('[name = "csrfmiddlewaretoken"]').val();
        $.ajax({
            url: url,
            type: 'PUT',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", data['csrfmiddlewaretoken']);
            }
        })
            .done(defaultCallback)
            .fail(failureCallback);
    };

    var remoteDeleteProcessing = function (url, data, defaultCallback, failureCallback) {
        data['csrfmiddlewaretoken'] = $('[name = "csrfmiddlewaretoken"]').val();
        $.ajax({
            url: url,
            type: 'DELETE',
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", data['csrfmiddlewaretoken']);
            }
        })
            .done(defaultCallback)
            .fail(failureCallback);
    };

    var remoteGetProcessing = function (url, data, defaultCallback, failureCallback) {
        $.get(url, JSON.stringify(data), defaultCallback).fail(failureCallback).done();
    };

    return {
        remotePost: function (url, data, defaultCallback, failureCallback) {
            return remotePostProcessing(url, data, defaultCallback, failureCallback);
        },
        remoteMultipartPost: function (url, data, defaultCallback, failureCallback) {
            return remoteMultipartPostProcessing(url, data, defaultCallback, failureCallback);
        },
        remotePatch: function (url, data, defaultCallback, failureCallback) {
            return remotePatchProcessing(url, data, defaultCallback, failureCallback);
        },
        remotePut: function (url, data, defaultCallback, failureCallback) {
            return remotePutProcessing(url, data, defaultCallback, failureCallback);
        },
        remoteDelete: function (url, data, defaultCallback, failureCallback) {
            return remoteDeleteProcessing(url, data, defaultCallback, failureCallback);
        },
        remoteGet: function (url, data, defaultCallback, failureCallback) {
            return remoteGetProcessing(url, data, defaultCallback, failureCallback)
        },
        showProcessing: function (options) {
            var options = $.extend(true, {}, options);
            html = '<h5 class="loader"><img src="/static/images/input-spinner.gif" />';

            if (options.target) { // element blocking
                var el = $(options.target);
                if (el.height() <= ($(window).height())) {
                    options.cenrerY = true;
                }
                el.block({
                    message: html,
                    baseZ: options.zIndex ? options.zIndex : 1000,
                    centerY: options.cenrerY !== undefined ? options.cenrerY : false,
                    css: {
                        top: '10%',
                        border: '0',
                        padding: '0',
                        backgroundColor: 'none'
                    },
                    overlayCSS: {
                        backgroundColor: options.overlayColor ? options.overlayColor : '#555',
                        opacity: options.boxed ? 0.05 : 0.1,
                        cursor: 'wait'
                    }
                });
            } else { // page blocking
                $.blockUI({
                    message: html,
                    baseZ: options.zIndex ? options.zIndex : 1000,
                    css: {
                        border: '0',
                        padding: '0',
                        backgroundColor: 'none'
                    },
                    overlayCSS: {
                        backgroundColor: options.overlayColor ? options.overlayColor : '#555',
                        opacity: options.boxed ? 0.05 : 0.1,
                        cursor: 'wait'
                    }
                });
            }
        },
        hideProcessing: function (target) {
            if (target) {
                $(target).unblock({
                    onUnblock: function () {
                        $(target).css('position', '');
                        $(target).css('zoom', '');
                    }
                });
            } else {
                $.unblockUI();
            }
        },
        validationSettings: function () {
            var validationSettings = {
                registerExtenders: true,
                messagesOnModified: true,
                insertMessages: true,
                parseInputAttributes: true,
                messageTemplate: null,
                errorElementClass: 'has-error',
                errorClass: 'errorlist',
                decorateInputElement: true,
                grouping: {
                    deep: true,
                    live: true,
                    observable: true
                }
            };
            ko.validation.init(validationSettings, true);
        },
         /**
         * Created by wrufesh on 11/24/16.
         */
         // Dependencies:
         //     <link rel="stylesheet" href="{% static 'hr/css/plugins/toastr/toastr.css' %}">
         //     <script src="{% static 'hr/js/plugins/toastr/toastr.js' %}"></script>
        notifyUser: function (message, type, layout) {
            toastr.options = {
                "closeButton": true,
                "debug": false,
                "newestOnTop": true,
                "progressBar": true,
                "positionClass": "toast-bottom-right",
                "preventDuplicates": false,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "20000",
                "extendedTimeOut": "1000",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            };
            if (type == 'success') {
                toastr.success(message, 'Successful');
            }
            if (type == 'info') {
                toastr.success(message, 'Successful');
            }
            if (type == 'error') {
                toastr.error(message, 'Error');
            }
            if (type == 'warning') {
                toastr.warning(message, 'Warning');
            }
        },
        confirmAlert: function (message, okCallback) {
            var r = confirm(message);
            if (r == true) {
                okCallback()
            }

        },
        redirectTo: function (path, timeout) {
            if (timeout)
                setTimeout(function () {
                    window.location.href = path
                }, timeout);
            else
                window.location.href = path
        },
        getUrlParameterByName: function (name) {
            name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
            var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
                results = regex.exec(location.search);
            return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
        },
        linkBaseUrl: function (link) {
            if (!link) {
                var raw_link = document.URL.split('/');
                var link = '/' + raw_link[3] + '/' + raw_link[4] + '/';
            }
            return link;
        },
        // Initialize user profile details and urls
        username: '',
        profile_url: '',
        user_group: ''
    }
})();


function Pagination(paginate, data) {
    var self = this;

    self.visits = paginate;
    self.data = data;
    self.next_url = ko.observable(self.data.next);
    self.previous_url = ko.observable(self.data.previous);
    self.current = ko.observable(self.data.current);

    self.next = function (self) {
        App.remoteGet(self.next_url(), {},
            function (res) {
                App.hideProcessing();
                self.data = res;
                self.next_url(self.data.next);
                self.previous_url(self.data.previous);
                self.visits(self.data.results);
                self.current(self.data.current);
            },
            function (err) {
                var err_message = err.responseJSON.detail;
                var error = App.notifyUser(
                    err_message,
                    'error'
                );
                App.hideProcessing();
            }
        );
    }

    self.has_next = ko.computed(function () {
        if (self.next_url() != null) {
            return 'visible'
        } else {
            return 'hidden'
        }
    });


    self.has_previous = ko.computed(function () {
        return self.previous_url() != null;
    });

    self.previous = function () {
        App.remoteGet(self.previous_url(), {},
            function (res) {
                App.hideProcessing();
                self.data = res;
                self.next_url(self.data.next);
                self.previous_url(self.data.previous);
                self.visits(self.data.results);
                self.current(self.data.current);
            },
            function (err) {
                var err_message = err.responseJSON.detail;
                var error = App.notifyUser(
                    err_message,
                    'error'
                );
                App.hideProcessing();
            }
        );
    }

    self.compute_paginate = ko.computed(function () {
        self.visits(self.data.results);
    });

}
