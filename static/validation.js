$(document).ready(function(){
    $('.login').click(function(){
        var a = $('#username').val().length;
        var b = $('#password').val().length;

        if (a < 0 && b < 0){
          $('#username').focus();
          alert("fields should not be empty");
          return false;

        }else{
          return true;
        }
    });
    
});