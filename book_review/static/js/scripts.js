function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
}

function addToBookshelf(button) {
    const bookItem = button.parentElement.parentElement;
    const title = bookItem.dataset.title;
    const desc = bookItem.dataset.desc;

    // Retrieve bookshelf from localStorage
    let bookshelf = JSON.parse(localStorage.getItem('bookshelf')) || [];
    
    // Add new book
    bookshelf.push({ title, desc });

    // Save back to localStorage
    localStorage.setItem('bookshelf', JSON.stringify(bookshelf));

    alert(`${title} has been added to your bookshelf!`);
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
