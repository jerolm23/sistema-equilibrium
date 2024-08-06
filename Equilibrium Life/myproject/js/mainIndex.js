$(document).ready(function(){
    fetch("http://localhost:5000/obtenerUsuario/"+sessionStorage.getItem("key")).then(response=>{
        response.json().then(body=>{
            $("#emailFooter").val(body.correo);
        });
    });
});