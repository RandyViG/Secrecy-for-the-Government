
function cambiar(id){
    document.getElementById('change_form').setAttribute("action","/admin/changeData/"+id+"");
    $("#changeUser").modal();
    console.log(document.getElementById('change_form'))
}

function borrar(filename){
    document.getElementById('error_delete').setAttribute("href","/delete/"+filename+"");
    $("#confirmDeleteModal").modal();
}