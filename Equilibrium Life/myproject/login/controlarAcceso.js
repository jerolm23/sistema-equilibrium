$(document).ready(function(){
    if(sessionStorage.getItem("key")==undefined){
        window.location.href="login.html";
    }
});