// codigo para que cuando de clic a registro o login se cambien de posicion 
// llama al boton y le agrega un evento y el evento es click
// se ejecuta las funciones 
document.getElementById("btn__registro").addEventListener("click",register);
document.getElementById("btn_inicio").addEventListener("click",InicioSesion);
// windows que ejecute la funcion añadiendo un evento 
// windows y le añadimos un evento y el evento es resize con la funcion de ancho pagina
window.addEventListener("resize",AnchoPa);
// declaracion de variables 
// document.queryselector me bsuca un elemento que tenga la etiqueta contenedor_login_Register
var contenedor_login_register = document.querySelector(".contenedor__login-register");
var formulario_login = document.querySelector(".formulario__login");
var formulario_register = document.querySelector(".formulario__registro");
var caja_trasera_login =document.querySelector(".caja__trasera-login");
var caja_trasera_registro = document.querySelector(".caja__trasera-registro");

// este condigo se ejecuta a medida que se va haciendo resize es lo que mueves la ventana 
function AnchoPa(){
    // cuando la ventana tenga un innerwidth mayor a 850  
    if(window.innerWidth > 850){
        
        caja_trasera_login.style.display = "block";
        caja_trasera_registro.style.display ="block";
          
    }else {
        //caso contrario si lo de arriba no se cumple que ejecute este codigo 
        // la caja trasera que se muestre con el block 
        caja_trasera_registro.style.display="block";
        // 
        caja_trasera_registro.style.opacity="1";
        caja_trasera_login.style.display="none";
        formulario_login.style.display ="block";
        formulario_register.style.display ="none";
        contenedor_login_register.style.left="0";
    }
}
// se ejecuta la funcion anchopa cada que recargo la pagina 
AnchoPa();
// funcion apara cuando de clic en el boton registrar
function InicioSesion(){
    // si el ancho del windows es mayor a 850 ejecuta el codigo que creamos 
    if(window.innerWidth > 850){
         // estilos en java script
    // cuando demos clic en registrar el formulario se va a mostrar 
    // por que en el css esta display none 
    formulario_register.style.display ="none";
    contenedor_login_register.style.left="10px";
    formulario_login.style.display ="block";
    caja_trasera_registro.style.opacity = "1";
    caja_trasera_login.style.opacity="0";

    }else{
        formulario_register.style.display ="none";
        // 0 para no tener ningun margin 
        contenedor_login_register.style.left="0px";
        formulario_login.style.display ="block";
        caja_trasera_registro.style.display = "block";
        caja_trasera_login.style.display="none";   
    }
   }
// todo lo contrario 
function register(){
    if(window.innerWidth > 850){
        // estilos en java script
    // cuando demos clic en registrar el formulario se va a mostrar 
    // por que en el css esta display none 
    formulario_register.style.display = "block";
    // es para cuando de clic se me baja a la izquierda 
    contenedor_login_register.style.left = "410px";
    formulario_login.style.display = "none";
    // para que el texto aparesca y desaparesca con el opacity 
    caja_trasera_registro.style.opacity = "0";
    caja_trasera_login.style.opacity = "1";


    }else {
        // dice lo contrario 
        formulario_register.style.display ="block";
        // 0 para no tener ningun margin 
        contenedor_login_register.style.left="0px";
        formulario_login.style.display ="none";
        caja_trasera_registro.style.display = "none";
        caja_trasera_login.style.display="block";
        caja_trasera_login.style.opacity = "1";  
    }
    }
