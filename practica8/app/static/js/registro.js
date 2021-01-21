function comprobarPwd(){
  if(document.forms["formRegistro"]["pwd"].value !== document.forms["formRegistro"]["pwdR"].value){
    alert("Las contraseñas no coinciden")
    return false
  }
  return true
}
function comprobarPwdPerfil(){
  if(document.forms["formPerfil"]["pwd"].value !== document.forms["formPerfil"]["pwdR"].value){
    alert("Las contraseñas no coinciden" + document.forms["formPerfil"]["pwd"].value +" - "+document.forms["formPerfil"]["pwdR"].value)
    return false
  }
  return true
}
