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

$(document).ready(function() {
    $('#openForm').click(function(event) {
        event.preventDefault();
        $.ajax({
            url: "{% url 'model_create' %}",
            type: "GET",
            dataType: "html",
            success: function(data) {
                $('#formContainer').html(data);
                $('#formModal').modal('show');
            }
        });
    });

    // Handle form submission via AJAX
    $(document).on('submit', '#productForm', function(event) {
        event.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: "POST",
            data: new FormData(this),
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    $('#formModal').modal('hide');
                    location.reload(); // Reload to refresh the table
                } else {
                    // Handle errors if needed
                }
            },
            error: function(response) {
                console.log(response);
            }
        });
    });
});