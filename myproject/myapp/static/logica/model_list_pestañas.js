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

