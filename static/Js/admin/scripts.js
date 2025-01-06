document.getElementById('create_post').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);

    fetch('/create', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload(); 
        }
    });
});


document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function () {
        const card = this.closest('.post');
        const id = card.getAttribute('id');

        fetch(`/delete/${id}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                card.remove(); 
            }
        });
    });
});

document.querySelectorAll('.edit-name').forEach(button => {
    button.addEventListener('click', function () {
        const card = this.closest('.post');
        const id = card.getAttribute('id');
        const name = prompt('Novo nome:', card.querySelector('#name').textContent);

        if (name) {
            const formData = new FormData();
            formData.append('name', name);

            fetch(`/update_name/${id}`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    card.querySelector('#name').textContent = name;
                }
            });
        }
    });
});


document.querySelectorAll('.edit-price').forEach(button => {
    button.addEventListener('click', function () {
        const card = this.closest('.post');
        const id = card.getAttribute('id');
        const price = prompt('Novo preço:', card.querySelector('#price').textContent);

        if (price) {
            const formData = new FormData();
            formData.append('price', price);

            fetch(`/update_price/${id}`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    card.querySelector('#price').textContent =`R$${price}`;
                }
            });
        }
    });
});

document.querySelectorAll('.edit-description').forEach(button => {
    button.addEventListener('click', function () {
        const card = this.closest('.post');
        const id = card.getAttribute('id');
        const description = prompt('Nova descrição:', card.querySelector('#description').textContent);

        if (description) {
            const formData = new FormData();
            formData.append('description', description);

            fetch(`/update_desc/${id}`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    card.querySelector('#description').textContent = description;
                }
            });
        }
    });
});

document.querySelectorAll('.change-image').forEach(button => {
    button.addEventListener('click', function () {
        const form = this.closest('.image-form');
        const fileInput = form.querySelector('input[type="file"]');
        const post = this.closest('.post');
        const id = post.getAttribute('id');

        fileInput.click();

        fileInput.addEventListener('change', function () {
            const formData = new FormData();
            formData.append('image', fileInput.files[0]);

            fetch(`/update-image/${id}`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    post.querySelector('img').src = data.new_image_url;
                } else {
                    alert('Erro ao trocar a imagem.');
                }
            });
        });
    });
});


document.getElementById("sair").addEventListener("click", () => {
    fetch('/logout', { method: 'GET' })
                .then(response => {
                    if (response.ok) {
                        window.location.href = '/login';
                    }
                }) 
            });