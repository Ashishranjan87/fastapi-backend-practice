// =========================
// ADD TODO
// =========================

const todoForm = document.getElementById('todoForm');

if (todoForm) {
    todoForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(todoForm);

        const payload = {
            title: formData.get('title'),
            description: formData.get('description'),
            priority: parseInt(formData.get('priority')),
            complete: false
        };

        try {
            const token = getCookie('access_token');

            const response = await fetch('/todos/create_todos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                window.location.reload();
            } else {
                const errorData = await response.json();
                alert(errorData.detail);
            }

        } catch (error) {
            console.error(error);
        }
    });
}


// =========================
// EDIT TODO
// =========================

const editTodoForm = document.getElementById('editTodoForm');

if (editTodoForm) {

    editTodoForm.addEventListener('submit', async function (event) {

        event.preventDefault();

        const formData = new FormData(editTodoForm);

        const todoId = window.location.pathname.split('/').pop();

        const payload = {
            title: formData.get('title'),
            description: formData.get('description'),
            priority: parseInt(formData.get('priority')),
            complete: formData.get('complete') === 'on'
        };

        try {

            const token = getCookie('access_token');

            const response = await fetch(`/todos/update/${todoId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                window.location.href = '/todos/todo-page';
            } else {
                const errorData = await response.json();
                alert(errorData.detail);
            }

        } catch (error) {
            console.error(error);
        }
    });


    // =========================
    // DELETE TODO
    // =========================

    const deleteButton = document.getElementById('deleteButton');

    if (deleteButton) {

        deleteButton.addEventListener('click', async function () {

            const todoId = window.location.pathname.split('/').pop();

            try {

                const token = getCookie('access_token');

                const response = await fetch(`/todos/delete/${todoId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    window.location.href = '/todos/todo-page';
                } else {
                    const errorData = await response.json();
                    alert(errorData.detail);
                }

            } catch (error) {
                console.error(error);
            }
        });
    }
}



// =========================
// LOGIN
// =========================

const loginForm = document.getElementById('loginForm');

if (loginForm) {

    loginForm.addEventListener('submit', async function (event) {

        event.preventDefault();

        const formData = new FormData(loginForm);

        const payload = new URLSearchParams();

        for (const pair of formData.entries()) {
            payload.append(pair[0], pair[1]);
        }

        try {

            const response = await fetch('/auth/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: payload.toString()
            });

            if (response.ok) {

                const data = await response.json();

                document.cookie = `access_token=${data.access_token}; path=/`;

                window.location.href = '/todos/todo-page';

            } else {

                const errorData = await response.json();

                alert(errorData.detail);
            }

        } catch (error) {
            console.error(error);
        }
    });
}



// =========================
// REGISTER
// =========================

const registerForm = document.getElementById('registerForm');

if (registerForm) {

    registerForm.addEventListener('submit', async function (event) {

        event.preventDefault();

        const formData = new FormData(registerForm);

        if (formData.get('password') !== formData.get('password2')) {
            alert('Passwords do not match');
            return;
        }

        const payload = {
            email: formData.get('email'),
            username: formData.get('username'),
            firstname: formData.get('firstname'),
            lastname: formData.get('lastname'),
            role: formData.get('role'),
            phone_number: formData.get('phone_number'),
            dateofbirth: formData.get('dateofbirth') || null,
            password: formData.get('password')
        };

        try {

            const response = await fetch('/auth/createUser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {

                window.location.href = '/auth/login-page';

            } else {

                const errorData = await response.json();

                alert(errorData.detail);
            }

        } catch (error) {
            console.error(error);
        }
    });
}



// =========================
// GET COOKIE
// =========================

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + '=')) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }
        }
    }

    return cookieValue;
}



// =========================
// LOGOUT
// =========================

function logout() {

    document.cookie =
        "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

    window.location.href = '/auth/login-page';
}