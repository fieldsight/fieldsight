var inject_binding = function (allBindings, key, value) {
    //https://github.com/knockout/knockout/pull/932#issuecomment-26547528
    return {
        has: function (bindingKey) {
            return (bindingKey == key) || allBindings.has(bindingKey);
        },
        get: function (bindingKey) {
            var binding = allBindings.get(bindingKey);
            if (bindingKey == key) {
                binding = binding ? [].concat(binding, value) : value;
            }
            return binding;
        }
    };
}

ko.bindingHandlers.selectize = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
        if (!allBindingsAccessor.has('optionsText'))
            allBindingsAccessor = inject_binding(allBindingsAccessor, 'optionsText', 'name');
        if (!allBindingsAccessor.has('optionsValue'))
            allBindingsAccessor = inject_binding(allBindingsAccessor, 'optionsValue', 'id');
        if (typeof allBindingsAccessor.get('optionsCaption') == 'undefined')
            allBindingsAccessor = inject_binding(allBindingsAccessor, 'optionsCaption', 'Choose...');

        ko.bindingHandlers.options.update(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext);

        var options = {
            plugins: ['remove_button'],
            valueField: allBindingsAccessor.get('optionsValue'),
            labelField: allBindingsAccessor.get('optionsText'),
            searchField: allBindingsAccessor.get('optionsText')
        }

        if (allBindingsAccessor.has('selectize_options')) {
            var passed_options = allBindingsAccessor.get('selectize_options')
            for (var attr_name in passed_options) {
                options[attr_name] = passed_options[attr_name];
            }
        }
        var $select = $(element).selectize(options)[0].selectize;

        if (typeof allBindingsAccessor.get('value') == 'function') {
            $select.addItem(allBindingsAccessor.get('value')());
            allBindingsAccessor.get('value').subscribe(function (new_val) {
                $select.addItem(new_val);
            })
        }

        if (typeof allBindingsAccessor.get('selectedOptions') == 'function') {
            allBindingsAccessor.get('selectedOptions').subscribe(function (new_val) {
                // Removing items which are not in new value
                var values = $select.getValue();
                var items_to_remove = [];
                for (var k in values) {
                    if (new_val.indexOf(values[k]) == -1) {
                        items_to_remove.push(values[k]);
                    }
                }

                for (var k in items_to_remove) {
                    $select.removeItem(items_to_remove[k]);
                }

                for (var k in new_val) {
                    $select.addItem(new_val[k]);
                }

            });
            var selected = allBindingsAccessor.get('selectedOptions')();
            for (var k in selected) {
                $select.addItem(selected[k]);
            }
        }

        if (typeof init_selectize == 'function') {
            init_selectize($select);
        }

        // Selectize required field form submit focus fix
        // https://github.com/brianreavis/selectize.js/issues/733#issuecomment-145871854

        $select.$input.on('invalid', function (event) {
            event.preventDefault();
            $select.focus(true);
            $select.$wrapper.addClass('invalid');
        });

        $select.$input.on('change', function (event) {
            if (event.target.validity && event.target.validity.valid) {
                $select.$wrapper.removeClass('invalid');
            }
            // Force re-rendering of options by clearing render-cache
            $select.renderCache = {}
        });

        if (typeof valueAccessor().subscribe == 'function') {
            valueAccessor().subscribe(function (changes) {
                // To avoid having duplicate keys, all delete operations will go first
                var addedItems = new Array();
                changes.forEach(function (change) {
                    switch (change.status) {
                        case 'added':
                            addedItems.push(change.value);
                            break;
                        case 'deleted':
                            var itemId = change.value[options.valueField];
                            if (itemId != null) $select.removeOption(itemId);
                    }
                });
                addedItems.forEach(function (item) {
                    $select.addOption(item);
                });

            }, null, "arrayChange");
        }

    },
    update: function (element, valueAccessor, allBindingsAccessor) {

        if (allBindingsAccessor.has('object')) {
            var optionsValue = allBindingsAccessor.get('optionsValue') || 'id';

            if (typeof valueAccessor() == 'function') {
                var value_accessor = valueAccessor();
            } else {
                var value_accessor = valueAccessor;
            }

            var selected_obj = $.grep(value_accessor(), function (i) {

                if (typeof i[optionsValue] == 'function')
                    var id = i[optionsValue]
                else
                    var id = i[optionsValue]
                return id == allBindingsAccessor.get('value')();
            })[0];

            if (selected_obj) {
                allBindingsAccessor.get('object')(selected_obj);
            }
        }
    }
}

ko.bindingHandlers.autosize = {
    init: function (element, valueAccessor, allBindingsAccessor) {
        $(element).autosizeInput();
        var min_width = valueAccessor();
        if (min_width != 0) {
            if (!isNaN(min_width)) {
                min_width = min_width + 'em';
            }
            $(element).css({
                "min-width": min_width
            });
        }
    },
    update: function (element, valueAccessor, allBindingsAccessor) {
        $(element).data(Plugins.AutosizeInput.instanceKey).update();
    }
}

ko.bindingHandlers.localize = {
    init: function (element, valueAccessor, allBindingsAccessor) {

    },
    update: function (element, valueAccessor, allBindingsAccessor) {

        var lang_code = window.lang;

        if (allBindingsAccessor().editableText)
            var accessor = allBindingsAccessor().editableText;
        else if (allBindingsAccessor().value)
            var accessor = allBindingsAccessor().value;
        else if (allBindingsAccessor().text) {
            var original_text = allBindingsAccessor().text;
        }

        if (typeof accessor == 'function') {
            if (accessor() == null || typeof accessor() == 'undefined')
                return;
            var original_text = accessor();
        }

        var value = localize(original_text, lang_code, true);

        if (typeof accessor == 'function') {
            if (isAN(value)) {
                accessor(parseFloat(value));
            } else {
                accessor(value);
            }
        }

        var txt = localize(original_text, lang_code);

        $(element).html(txt);
        $(element).val(txt);

    }
}


ko.bindingHandlers.flash = {
    init: function (element) {
        $(element).hide().fadeIn('slow');
    }
};

ko.bindingHandlers.max = {
    init: function (element, valueAccessor) {
        $(element).attr('max', valueAccessor());
    },
    update: function (element, valueAccessor) {

        $(element).on('change', function (e) {
            if ($(element).val() > valueAccessor()) {
                $(element).val(null);
            }
        });
    }
};


ko.bindingHandlers.attachment = {
    init: function (element, valueAccessor) {
    },
    update: function (element, valueAccessor) {
        $(element).on('change', function () {
            var value = valueAccessor();
            value($(element)[0].files[0]);
        });
    },
};

ko.bindingHandlers.datepicker = {
    init: function (element) {
        if (element.classList.contains('ad-date')) {
            $(element).datepicker({
                format: 'yyyy-mm-dd',
            });
        } else if (element.classList.contains('bs-date')) {
            $(element).nepaliDatePicker();
        }
        ;
    },
    update: function (element, valueAccessor) {
    },
};


ko.bindingHandlers.editableText = {
    init: function (element, valueAccessor) {
        $(element).attr('contenteditable', true);
        $(element).on('blur', function () {
            var observable = valueAccessor();
            if (typeof (observable) == 'function') {
                observable($(this).text());
            }
        });
    },
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor());
        $(element).text(value);
    }
};

ko.bindingHandlers.numeric = {
    init: function (element, valueAccessor) {
        $(element).on('keydown', function (event) {

            // Allow: backspace, delete, tab, escape, and enter
            if (event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 13 ||
                    // Allow: Ctrl combinations
                (event.ctrlKey === true) ||
                    //Allow decimal symbol (.)
                (event.keyCode === 190 || event.keyCode === 110) ||
                    // Allow: home, end, left, right
                (event.keyCode >= 35 && event.keyCode <= 39)) {
                // let it happen, don't do anything
                return;
            }
            else {
                // Ensure that it is a number and stop the keypress
                if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                    event.preventDefault();
                }
            }
        });
    },
    update: function (element, valueAccessor) {
    }
};

ko.bindingHandlers.percentage_numeric = {
    init: function (element, valueAccessor) {
        $(element).on('keydown', function (event) {

            // Allow: backspace, delete, tab, escape, and enter
            if (event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 13 ||
                    // Allow: Ctrl combinations
                (event.ctrlKey === true) ||
                    //Allow decimal symbol (.)
                (event.keyCode === 190 || event.keyCode === 110) ||
                    // Allow: home, end, left, right
                (event.keyCode >= 35 && event.keyCode <= 39) ||
                event.keyCode == 53) {
                // let it happen, don't do anything
                return;
            }
            else {
                // Ensure that it is a number and stop the keypress
                if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                    event.preventDefault();
                }
            }
        });
    },
    update: function (element, valueAccessor) {
    }
};

//Custom Observable Extensions
ko.extenders.numeric = function (target, precision) {
    //create a writeable computed observable to intercept writes to our observable
    var result = ko.computed({
        read: target,  //always return the original observables value
        write: function (newValue) {
            var current = target(),
                roundingMultiplier = Math.pow(10, precision),
                newValueAsNum = isNaN(newValue) ? current : parseFloat(+newValue),
                valueToWrite = Math.round(newValueAsNum * roundingMultiplier) / roundingMultiplier;

            //only write if it changed
            if (valueToWrite !== current) {
                target(valueToWrite);
            } else {
                //if the rounded value is the same, but a different value was written, force a notification for the current field
                if (newValue !== current) {
                    target.notifySubscribers(valueToWrite);
                }
            }
        }
    });

    //initialize with current value to make sure it is rounded appropriately
    result(target());

    //return the new computed observable
    return result;
};

//Other useful KO-related functions
function setBinding(id, value) {
    var el = document.getElementById(id);
    if (el) {
        el.setAttribute('data-bind', value);
    }
}

ko.bindingHandlers.disable_content_editable = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
    },
    update: function (element, valueAccessor, allBindingsAccessor, viewModel) {
        if (valueAccessor()) {
//            $(element).text('');
            $(element).removeAttr('contenteditable');
        }
        else {
            $(element).attr('contenteditable', true);
        }
    }
}

ko.bindingHandlers.readOnly = {
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor());
        if (value) {
            element.setAttribute("readOnly", true);
        } else {
            element.removeAttribute("readOnly");
        }
    }
}

ko.bindingHandlers.toggle = {
    init: function (element, valueAccessor) {
        ko.utils.registerEventHandler(element, 'click', function (event) {
            var toggleValue = valueAccessor();
            toggleValue(!toggleValue());
            if (event.preventDefault)
                event.preventDefault();
            event.returnValue = false;
        });
    },
    update: function (element, valueAccessor) {
    }
};


ko.bindingHandlers.on_tab = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
        $(element).on('keydown', function (event) {
            if (event.keyCode == 9) {

                var fn = valueAccessor();
                fn(element, viewModel);
            }
        });
    },
    update: function (element, valueAccessor, allBindingsAccessor, viewModel) {

    }
}

// http://stackoverflow.com/a/18184016/328406
ko.subscribable.fn.subscription_changed = function (callback) {
    var oldValue;
    this.subscribe(function (_oldValue) {
        oldValue = _oldValue;
    }, this, 'beforeChange');

    this.subscribe(function (newValue) {
        callback(newValue, oldValue);
    });
};

ko.bindingHandlers.foreachprop = {
    transformObject: function (obj) {
        var properties = [];
        for (var key in obj) {
            if (obj.hasOwnProperty(key)) {
                if (key == '__ko_mapping__') continue;
                properties.push({key: key, name: key.toTitleCase().replaceAll('_', ' '), value: obj[key]});
            }
        }
        return properties;
    },
    init: function (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
        var value = ko.utils.unwrapObservable(valueAccessor()),
            properties = ko.bindingHandlers.foreachprop.transformObject(value);
        ko.applyBindingsToNode(element, {foreach: properties}, bindingContext);
        return {controlsDescendantBindings: true};
    }
};

ko.bindingHandlers.modal = {
    init: function (element, valueAccessor) {
        $(element).modal({
            show: false
        });

        var value = valueAccessor();
        if (ko.isObservable(value)) {
            $(element).on('hide.bs.modal', function() {
               value(false);
            });
        }

        // Update 13/07/2016
        // based on @Richard's finding,
        // don't need to destroy modal explicitly in latest bootstrap.
        // modal('destroy') doesn't exist in latest bootstrap.
        // ko.utils.domNodeDisposal.addDisposeCallback(element, function () {
        //    $(element).modal("destroy");
        // });

    },
    update: function (element, valueAccessor) {
        var value = valueAccessor();
        if (ko.utils.unwrapObservable(value)) {
            $(element).modal('show');
        } else {
            $(element).modal('hide');
        }
    }
}


ko.bindingHandlers.map = {
            init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
                $("#" + element.getAttribute("id")).data("mapObj","");
                mapObj = ko.utils.unwrapObservable(valueAccessor());
                var latLng = new google.maps.LatLng(
                    ko.utils.unwrapObservable(mapObj.lat),
                    ko.utils.unwrapObservable(mapObj.lng));
                var mapOptions = { center: latLng,
                                  zoom: 12, 
                                  mapTypeId: google.maps.MapTypeId.ROADMAP};
                
                mapObj.googleMap = new google.maps.Map(element, mapOptions);
                
                mapObj.marker = new google.maps.Marker({
                    map: mapObj.googleMap,
                    position: latLng,
                    title: "You Are Here",
                    draggable: true
                });     
                
                mapObj.onChangedCoord = function(newValue) {
                    var latLng = new google.maps.LatLng(
                        ko.utils.unwrapObservable(mapObj.lat),
                        ko.utils.unwrapObservable(mapObj.lng));

                    mapObj.googleMap.setCenter(latLng);
                    mapObj.marker.setPosition(latLng);                 
                };
                
                mapObj.onMarkerMoved = function(dragEnd) {
                    var latLng = mapObj.marker.getPosition();
                    mapObj.lat(latLng.lat());
                    mapObj.lng(latLng.lng());
                };
                
                mapObj.lat.subscribe(mapObj.onChangedCoord);
                mapObj.lng.subscribe(mapObj.onChangedCoord);  
                
                google.maps.event.addListener(mapObj.marker, 'dragend', mapObj.onMarkerMoved);
                
                $("#" + element.getAttribute("id")).data("mapObj",mapObj);
            }
        };


ko.bindingHandlers.datePicker = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel) {                    
        // Register change callbacks to update the model
        // if the control changes.       
        ko.utils.registerEventHandler(element, "change", function () {            
            var value = valueAccessor();
            value(new Date(element.value));            
        });
    },
    // Update the control whenever the view model changes
    update: function (element, valueAccessor, allBindingsAccessor, viewModel) {
        var value =  valueAccessor();        
        element.value = value().toISOString().slice(0,10);
    }
};

ko.bindingHandlers.confirmClick = {
    init: function(element, valueAccessor, allBindings, viewModel) {
        var value = valueAccessor();
        var message = ko.unwrap(value.message);
        var click = value.click;
        ko.applyBindingsToNode(element, { click: function () {
            if (confirm(message))
                return click.apply(this, Array.prototype.slice.apply(arguments));
        }}, viewModel);
    }
}

ko.bindingHandlers.fieldsightFormatDate = {
    update: function (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
        var value = valueAccessor();
        var newValueAccessor = ko.unwrap(value);
        var dt = new Date(newValueAccessor);
        if (newValueAccessor != null)
            $(element).text(dt.toDateString()+ "  " + dt.toLocaleTimeString());
    }
};



ko.bindingHandlers.fileUpload = {
    init: function (element, valueAccessor) {
        $(element).change(function () {
            valueAccessor()(element.files[0]);
        });
    },
    update: function (element, valueAccessor) {
        if (ko.unwrap(valueAccessor()) === null) {
            $(element).wrap('<form>').closest('form').get(0).reset();
            $(element).unwrap();
        }
    }
};