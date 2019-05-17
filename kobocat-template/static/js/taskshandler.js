
    var types = {
        0 : type0,
        1 : type1,
    }
// 0,1,2,4,7
// index starting from 4 are error notifications of equvalent notifications

//notification message list builder with ahref links
function type0(data, status){
    var additional_content = "";
    if (data.task_type in [3,6,8,9,10,11, 12]){
        if (data.status == 2){
            status = " is ready to download. "
            additional_content = "<br><a href='"+ data.file +"'>Download File</a>";
        }
    }
    content = data.get_task_type_display + status;
    return content + additional_content;
}












