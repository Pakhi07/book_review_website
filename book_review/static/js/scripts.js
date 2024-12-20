function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}

function addToBookshelf(button) {
    const bookId = button.dataset.bookId;

    if (!bookId) {
        alert("Book ID is missing!");
        return;
    }

    fetch("{% url 'bookshelf' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}", // Ensure this is available in your template
        },
        body: JSON.stringify({ book_id: bookId }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Failed to add book to bookshelf.");
            }
            return response.json();
        })
        .then((data) => {
            alert(data.message);
        })
        .catch((error) => {
            console.error(error);
            alert("An error occurred while adding the book.");
        });
}

// Helper function to get the CSRF token
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
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
