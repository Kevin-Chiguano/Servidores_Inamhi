//manejo de las pestañas 
document.querySelectorAll('.menu p').forEach(button =>{
    button.addEventListener('click', () => {

        document.querySelectorAll('.menu p').forEach(btn =>{
            btn.classList.remove('active');
            btn.classList.add('inactive');
        });

        document.querySelectorAll('.tab-content').forEach(pane => pane.classList.remove('active'));

        button.classList.remove('inactive');
        button.classList.add('active');

        const targetId = button.getAttribute('data-target');
        document.querySelector(targetId).classList.add('active');
    }) 
})
//guardamos las pestañas 
document.querySelectorAll('.menu p').forEach(tab =>{
    tab.addEventListener('click', function(){
        const target = this.getAttribute('data-target');

        document.querySelectorAll('.tab-content').forEach(content =>{
            content.classList.remove('active');
        });

        document.querySelector(target).classList.add('active');
        sessionStorage.setItem('activeTab',target);
    });
});

//restauramos la pestaña activa al cargar la pagina 
document.addEventListener('DOMContentLoaded', function(){
    //obtengo el id
    const activeTab = sessionStorage.getItem('activeTab');
    if(activeTab){
        //elimino la clase activa de todas las pestañas 
        document.querySelectorAll('.tab-content').forEach(content =>{
            content.classList.remove('active');
        });

    //agrego la calse activa al contenido de la pestaña activa 
    document.querySelector(activeTab).classList.add('active');

    //marco la pestaña activa y als demas inactivas
    document.querySelectorAll('.menu p').forEach(tab => {
        if (tab.getAttribute('data-target') === activeTab){
            tab.classList.remove('inactive');
            tab.classList.add('active');
        }else{
            //si no esta activa se le agrega la calse inactive
            tab.classList.remove('active');
            tab.classList.add('inactive');
        }
    });
}
});

