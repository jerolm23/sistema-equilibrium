$(document).ready(function(){
    fetch("http://localhost:5000/obtenerUsuario/"+sessionStorage.getItem("key")).then(response=>{
        response.json().then(body=>{
            $("#emailFooter").val(body.correo);
            $("#nombreFooter").val(body.nombre);
        });
    });

    $(".formularioFooter").submit(function(e){
        e.preventDefault();
        let data={to:$("#emailFooter").val(), name:$("#nombreFooter").val(), tel:$("#numeroFooter").val(), mss:$("#mensajeFooter").val()};
        document.getElementById("enviarFooter").disabled=true;
        fetch("http://localhost:5000/enviarMensaje", {headers:{'Content-Type':"application/json"}, method:"POST", body:JSON.stringify(data)}).then(res=>{
            $("#confirmacionFooter").css("color","white");
            setTimeout(()=>{
                window.location.reload();
            },1500)
        });

    });

});