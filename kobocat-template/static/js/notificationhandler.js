
    var data = "";
    var speed = 200;
    var types = {
        0 : type0,
        1 : type1,
        2 : type2,
        3 : type3,
        4 : type4,
        5 : type5,
        6 : type6,
        7 : type7,
        8 : type8,
        9 : type9,
        10 : type10,
        11 : type11,
        110 : type110,
        12 : type12,
        13 : type13,
        14 : type14,
        15 : type15,
        16 : type16,
        17 : type17,
        18 : type18,
        19 : type19,
        20 : type20,
        21 : type21,
        22 : type22,
        23 : type23,
        24 : type24,
        25 : type25,
        26 : type26,
        27 : type27,
        28 : type28,
        29 : type29,
        30 : type30,
        31 : type31,
        32 : type32,
        33 : type33,
        34 : type34,
        35 : type35,
        36 : type36,
        37 : type37,
        38 : type38,
        39 : type39,
        40 : type40,
        412: type412,
        421: type421,
        422: type422,
        429: type429,
        423: type430,
        432 : type432,

    }

// index starting from 4 are error notifications of equvalent notifications

//notification message list builder with ahref links
function type0(data){
    content = '<b><a href="'+ data.get_source_url +'">' + data.source_name +'</a></b> joined <b><a href="' +  data.get_event_url + '">' + data.event_name + '</a></b> as an Team Admin.';
    return content;
}
function type1(data){
    content = '<b><a href="'+ data.get_source_url +'">' + data.source_name +'</a></b> joined <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> as an Team Admin.';
    return content;
}

function type2(data){
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as the Project Manager of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    return content;
}
function type3(data){
    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as '+ data.terms_and_labels.site_reviewer +' of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as Reviewer of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';

    }
    return content;

}
function type4(data){
    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as '+ data.terms_and_labels.site_supervisor +' of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as Site Supervisor of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';

    }
    return content;

}
function type5(data){
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was assigned as an Team Admin in <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';
    return content;
}
function type6(data){
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was assigned as a Project Manager in <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    return content;
}
function type7(data){
    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was assigned as a '+ data.terms_and_labels.site_reviewer +' in <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was assigned as a Reviewer in <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';

    }
    return content;
}
function type8(data){
    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was assigned as a '+ data.terms_and_labels.site_supervisor +' in <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was assigned as a Site Supervisor in <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';

    }
    return content;
}

function type9(data){
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> created a new Team named <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';
    return content;
}


function type10(data){
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> created a new project named <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';
    return content;
}


function type11(data){
    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> created a new '+ data.terms_and_labels.site +' named <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> in Project named <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> created a new site named <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> in Project named <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';

    }
    return content;
}

function type110(data){
console.log(data.terms_and_labels);
    if(data.terms_and_labels!=null){
    console.log("tm and evel")
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> created a new Sub '+ data.terms_and_labels.site + ' named <b><a href="' + data.get_event_url + '">' + data.get_event_name + '</a></b>in Site named <b><a href="' + data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name+'</a></b> created a new sub site named <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> in Site named <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';

    }
    return content;
}

function type12(data){
    if(data.source_uid == user_id){
        content = '<span style="color:green;"><b>Sucessfully</b></span> ' + data.extra_message + ' in project <a href="' +  data.get_event_url + '"><b>' + data.get_event_name + '</a></b>.';
    }else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> '+ data.extra_message +' in <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';
    }
    return content;
}


function type13(data){
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> changed the details of Team named <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';
    return content;
}       

function type14(data){
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> changed the details of project named <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';
    return content;
} 

function type15(data, detail=false){

    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> changed the details of ' + data.terms_and_labels.site + ' named <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> changed the details of site named <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';

    }
    if (data.extra_json && detail) {
        const updated = data.extra_json;
        content += Object.keys(updated).map(
            key => '<li style="margin-left:60px;" ><b>' + updated[key].label + '</b> was updated from <b>' + (updated[key].data[0].length == 0 ? '<i>blank</i>' : updated[key].data[0]) + '</b> to <b>' + (updated[key].data[1].length == 0 ? '<i>blank</i>' : updated[key].data[1]) + '</b>.</li>',
        ).join(' ') + '</ul></div>';
    }
    return content;
}   

function type16(data){
    var formdetail = data.get_event_name.split("form");
    // var level = "site";
    // if (data.extra_message == "project"){ level="project"; }
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> submitted a response for '+ formdetail[0] +'form <b><a href="' +  data.get_event_url + '">' + formdetail[1] + '</a></b>' + '</a></b> in <b><a href="' + data.get_extraobj_url+ '">' + data.get_extraobj_name+'</a></b>.';
    return content;
}   

function type17(data){
    var formdetail = data.get_event_name.split("form");
    // var level = "site";
    // if (data.extra_message == "project"){ level="project"; }
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> reviewed a response for '+ formdetail[0] +'form <b><a href="' + data.get_event_url+ '">' + formdetail[1]+'</a></b> in <b><a href="' + data.get_extraobj_url+ '">' + data.get_extraobj_name+'</a></b>.';
    return content;
}   

function type18(data){
    var formdetail = data.get_event_name.split("form");  
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> assigned a new '+ formdetail[0] +'form <b><a href="' + data.get_event_url+ '">' + formdetail[1]+'</a></b> in project <b><a href="' + data.get_extraobj_url+ '">' + data.get_extraobj_name+'</a></b>.';
    return content;
}   

function type19(data){
    var formdetail = data.get_event_name.split("form");
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> assigned a new '+ formdetail[0] +'form <b><a href="' + data.get_event_url+ '">' + formdetail[1]+'</a></b> in site <b><a href="' + data.get_extraobj_url+ '">' + data.get_extraobj_name+'</a></b>.';
    return content;
}   


function type20(data){
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> edited <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> form.';
    return content;
}

function type21(data){
    if(data.source_uid == user_id){

        content = "<b>TASK INFO : </b>"+data.extra_message + ' of Team <a href="' +  data.get_event_url + '"><b>' + data.get_event_name + '</a></b> were created.';
    }else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> created '+ data.extra_message +' of Team <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';
    }
    return content;
}

function type22(data){
    if(data.source_uid == user_id){
        content = "<b>TASK INFO : </b>"+data.extra_message + ' of project <a href="' +  data.get_event_url + '"><b>' + data.get_event_name + '</a></b> were created.';
    }else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> created <b>'+ data.extra_message +' of project <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b>.';
    }
    return content;
}

function type23(data){

    content = "<b>TASK INFO : </b>"+data.extra_message + ' in <a href="' +  data.get_event_url + '"><b>' + data.get_event_name + '</a></b>.';
    return content;
}

function type24(data){
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added in <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    return content;

}

function type25(data){
    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as <b>'+ data.terms_and_labels.donor +'</b> of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as <b>Partner</b> of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';

    }
    return content;

}

function type26(data){
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as the Project Manager in '+ data.extra_message +' projects of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
        return content;
}

function type27(data){
    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as '+ data.terms_and_labels.site_reviewer +' in '+ data.extra_message +' sites of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as Reviewer in '+ data.extra_message +' sites of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';

    }
    return content;

}

function type28(data){
    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as '+ data.terms_and_labels.site_supervisor +' '+ data.extra_message +' sites of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as Site Supervisor in '+ data.extra_message +' sites of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';

    }
    return content;

}

function type29(data){
    content = 'Project Sites import from <a href="' +  data.get_extraobj_url + '"><b>' + data.get_extraobj_name + '</a></b> has <span style="color:green;"><b>completed successfully</b></span> in project <a href="' +  data.get_event_url + '"><b>' + data.get_event_name + '</a></b>.';
        return content;

}

function type30(data){
    content = data.extra_message + '<a href="' +  data.get_extraobj_url + '"><b>' + data.get_extraobj_name + '</a></b> has <span style="color:green;"><b>completed successfully</b></span> in project <a href="' +  data.get_event_url + '"><b>' + data.get_event_name + '</a></b>.'; 
        return content;
}

function type31(data){
    var formdetail = data.get_event_name.split("form");
    var level = "site";
    if (data.extra_message == "project"){ level="project"; }
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> edited a response in '+ formdetail[0] +'form <b><a href="' +  data.get_event_url + '">' + formdetail[1] + '</a></b>' + '</a></b> in '+ level +' <b><a href="' + data.get_extraobj_url+ '">' + data.get_extraobj_name+'</a></b>.';
    return content;
}

function type32(data){
    content = data.extra_message + ' <a href="' +  data.get_extraobj_url + '"><b>' + data.get_extraobj_name + '</a></b></a></b> has <span style="color:green;"><b>successfully</b></span> been completed.'; 
        return content;

}

function type33(data){
    var formdetail = data.get_event_name.split("form");
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> deleted a response submitted by '+ data.extra_json['submitted_by'] +' in '+ formdetail[0] +'form <b><a href="' +  data.get_event_url + '">' + formdetail[1] + '</a></b>' + '</a></b> in '+ data.extra_message +' <b><a href="' + data.get_extraobj_url+ '">' + data.get_extraobj_name+'</a></b>.';
    return content;
}

function type34(data){
    var formdetail = data.get_event_name.split("form");
    content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> deleted '+ formdetail[1] +' with '+ data.extra_json['submission_count'] +' submissions in <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    return content;
}

function type35(data){
    if(data.source_uid == user_id){
        content = '<span style="color:green;"><b>Sucessfully</b></span> '+ data.extra_message +' of <b><a href="' + data.get_event_url + '">'+ data.get_event_name +'</a></b>.';    
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> '+ data.extra_message +' of <b><a href="' + data.get_event_url + '">'+ data.get_event_name +'</a></b>.';
    }
    return content;
}

function type36(data){
    if(data.source_uid == user_id){
        content = '<span style="color:green;"><b>Sucessfully</b></span> deleted '+ data.extra_message +' named <b><a href="' + data.get_event_url + '">'+ data.get_event_name +'</a></b> of <b><a href="' + data.get_extraobj_url + '">'+ data.get_extraobj_name +'</a></b>.';    
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> deleted '+ data.extra_message +' named <b><a href="' + data.get_event_url + '">'+ data.get_event_name +'</a></b> of <b><a href="' + data.get_extraobj_url + '">'+ data.get_extraobj_name +'</a></b>.';
    }
    return content;
}

function type37(data){
    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as the '+ data.terms_and_labels.region_reviewer +' in region <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as the Region Reviewer in region <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';

    }
    return content;
}

function type38(data){
    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as the ' + data.terms_and_labels.region_supervisor +' in <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as the Region Supervisor in <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';

    }
    return content;
}

function type39(data){
    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as the '+ data.terms_and_labels.region_reviewer +' in <b>'+ data.extra_message + ' '+ data.terms_and_labels.region +'</b> of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as the Region Reviewer in <b>'+ data.extra_message +' Regions</b> of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';

    }
    return content;
}

function type40(data){
    if(data.terms_and_labels!=null){
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as the '+ data.terms_and_labels.region_supervisor +' in <b>'+ data.extra_message +' '+ data.terms_and_labels.region +'</b> of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';
    }
    else{
        content = '<b><a href="' + data.get_source_url + '">'+ data.source_name +'</a></b> was added as the Region Supervisor in <b>'+ data.extra_message +' Regions</b> of <b><a href="' +  data.get_event_url + '">' + data.get_event_name + '</a></b> by <b><a href="' +  data.get_extraobj_url + '">' + data.get_extraobj_name + '</a></b>.';

    }
    return content;
}

// ----------------Errors -------------------

function type412(data){
    var errormsg=data.extra_message;
    var messages = errormsg.split("@error");
    console.log(messages);
    var readableerror = "";
    if (messages.length > 1){

        errors = messages[1].split("DETAIL:");
        if(errors.length > 1){
            readableerror = errors[1];
        }
        else{
            readableerror = errors[0];  
        }

    }
    else{
        readableerror = messages[0];
    }
    console.log(readableerror);
    content = 'Bulk upload of ' + messages[0] + ' has <span style="color:maroon;""><b>failed</b></span> in project <a href="' +  data.get_event_url + '"><b>' + data.get_event_name + '</a></b>. <b>Error:  </b>'+readableerror;
    return content;
}

function type421(data){
    content = 'Multi Role assign for ' + data.extra_message + ' has <span style="color:maroon;"><b>failed</b></span> in Team <a href="' +  data.get_event_url + '"><b>' + data.get_event_name + '</a></b>.';
    return content;
}

function type422(data){
    content = data.extra_message + ' has <span style="color:maroon;"><b>failed</b></span> in project <a href="' +  data.get_event_url + '"><b>' + data.get_event_name + '</a></b>.';
    return content;
}

function type429(data){
    content = 'Project Sites import from <a href="' +  data.get_extraobj_url + '"><b>' + data.get_extraobj_name + '</a></b> has <span style="color:maroon;"><b>failed</b></span> in project <a href="' +  data.get_event_url + '"><b>' + data.get_event_name + '</a></b>.';
    return content;
}

function type430(data){
    content = data.extra_message + '<a href="' +  data.get_extraobj_url + '"><b>' + data.get_extraobj_name + '</a></b> has <span style="color:maroon;"><b>failed</b></span> in project <a href="' +  data.get_event_url + '"><b>' + data.get_event_name + '</a></b>.';
    return content;
}

function type432(data){
    content = data.title + ' <a href="' +  data.get_event_url + '"><b>' + data.get_event_name + '</a></b></a></b> has <span style="color:maroon;"><b>failed</b></span>. ' + data.extra_message; 
    return content;

}


function redirect(url){
    window.location = url;
}



function dateparser(date){
    let months = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ];

    var d = new Date(date);

    if (offSetTime.length > 3){

        offset_hours = offSetTime.slice(5, 7);
        offset_minutes = offSetTime.slice(8, 10);
        offset_type = offSetTime.slice(4, 5);


        if (offset_type == "+"){ 
            d.setUTCHours(d.getUTCHours() + parseInt(offset_hours));
            d.setUTCMinutes(d.getUTCMinutes() + parseInt(offset_minutes));
        }else{
            d.setUTCHours(d.getUTCHours() - parseInt(offset_hours));
            d.setUTCMinutes(d.getUTCMinutes() - parseInt(offset_minutes));
        }
    }
    month = d.getUTCMonth();
    time=d.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true, timeZone: 'UTC' });
    clean_date = months[month] +', '+ d.getUTCDate() +', '+ d.getUTCFullYear() +', '+ time.toLowerCase()+'.';
    return clean_date;
}


function dateTimeParser(date){
     let months = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ];
   
      var d = new Date(date);

      if (offSetTime.length > 3){

        offset_hours = offSetTime.slice(5, 7);
        offset_minutes = offSetTime.slice(8, 10);
        offset_type = offSetTime.slice(4, 5);


        if (offset_type == "+"){ 
            d.setUTCHours(d.getUTCHours() + parseInt(offset_hours));
            d.setUTCMinutes(d.getUTCMinutes() + parseInt(offset_minutes));
         }else{
            d.setUTCHours(d.getUTCHours() - parseInt(offset_hours));
            d.setUTCMinutes(d.getUTCMinutes() - parseInt(offset_minutes));
         }
       }
          month = d.getUTCMonth();
          time=d.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true, timeZone: 'UTC' });
          clean_date = months[month] +' '+ d.getUTCDate() +', '+ d.getUTCFullYear();
          time = time.toLowerCase()
          return {date:clean_date, time:time};
      }

  







