function parse_form_response(main_question, type="all"){
    parsed_question={};
    lang_code=null;

    function set_language_code(obj){
        for(var key in obj){
            if(key.search(/en/i) > -1){
               lang_code = key;
            }
        }
    }

    function get_question_label(obj){
        if (lang_code == null){
            set_language_code(obj)
        }
        if (lang_code in obj){
            return obj[lang_code]
        }
        else{
            return obj[Object.keys(obj)[0]]
        }
    }

    function parse_group( prev_groupname, g_object){
         
        if (g_object['children'].length > 0){
            var g_question = prev_groupname+g_object['name'];

            g_object['children'].forEach(function(first_children){
            
                var question_name = g_question+"/"+first_children['name'];
                var question_label = question_name;

                if ('label' in first_children){
                    question_label = first_children['label'];
                    if (typeof question_label == "object"){
                        question_label = get_question_label(first_children['label'])
                    }
                }
                if (first_children['type'] == 'group'){
                    parse_group(g_question+"/",first_children)
                }else if(first_children['type'] != 'repeat'){
                    if (type == 'image' && first_children['type'] != "photo"){
                        return
                    }
                    if (type == 'location' && first_children['type'] != ""){
                        return
                    }           
                    parsed_question[question_name]={'label':question_label, 'type':first_children['type'], 'name':question_name}
                }
            });
        }
    }
    function parse_individual_questions(){
        console.log(main_question);
        if (main_question.length > 0){
            main_question.forEach(function(first_children){
                if (first_children['type'] == "repeat"){
                    
                }
                else if(first_children['type'] == 'group'){
                    parse_group("", first_children);
                }
                else{
                    var question_name = first_children['name'];
                    var question_label = question_name;

                    if ('label' in first_children){
                        question_label = first_children['label']
                        if (typeof question_label == "object"){
                            question_label = get_question_label(first_children['label'])
                        }
                    }
                if (type == 'image' && first_children['type'] != "photo"){
                    return
                }
                if (type == 'location' && first_children['type'] != ""){
                    return
                }    
                parsed_question[question_name]={'label':question_label, 'type':first_children['type'], 'name':question_name}
                }

            });
        }
    }    
    parse_individual_questions()
    return parsed_question
}      