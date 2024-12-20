function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}

function addToBookshelf(button) {
    const bookId = button.getAttribute('data-book-id');  // Extract book ID from the button
    const csrfToken = getCookie('csrftoken');  // Get CSRF token
    console.log('CSRF Token:', csrfToken);


    // Send the book_id as a URL-encoded form data
    const formData = new URLSearchParams();
    formData.append('book_id', bookId);  // Append the book_id to the form data

    fetch('/bookshelf/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,  // Pass CSRF token in headers
            'Content-Type': 'application/x-www-form-urlencoded'  // Set the content type to URL-encoded form data
        },
        body: formData.toString()  // Send form data as a string
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);  // Display success message
        } else {
            console.log('Unexpected response:', data);
        }
    })
    .catch(error => console.error('Error:', error));
}


// Helper function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.body.contains(document.querySelector('.bookshelf-list'))) {
        const bookshelf = JSON.parse(localStorage.getItem('bookshelf')) || [];
        const bookshelfList = document.querySelector('.bookshelf-list');

        bookshelf.forEach(book => {
            const bookItem = document.createElement('div');
            bookItem.classList.add('book-item');
            bookItem.innerHTML = `
                <h3>${book.title}</h3>
                <p>${book.desc}</p>
            `;
            bookshelfList.appendChild(bookItem);
        });
    }
});

function toggleNav() {
    document.querySelector('nav').classList.toggle('collapsed');
}
