const booksData = {
    fiction: [
        { title: "The Great Gatsby", author: "F. Scott Fitzgerald", image: "assets/pj_lightning_thief.jpg" },
        { title: "1984", author: "George Orwell", image: "assets/pj_lightning_thief.jpg" },
    ],
    mystery: [
        { title: "The Girl with the Dragon Tattoo", author: "Stieg Larsson", image: "assets/pj_lightning_thief.jpg" },
        { title: "Gone Girl", author: "Gillian Flynn", image: "assets/pj_lightning_thief.jpg" },
    ],
    romance: [
        { title: "Pride and Prejudice", author: "Jane Austen", image: "assets/pj_lightning_thief.jpg" },
        { title: "The Notebook", author: "Nicholas Sparks", image: "assets/pj_lightning_thief.jpg" },
    ],
    fantasy: [
        { title: "Harry Potter and the Sorcerer's Stone", author: "J.K. Rowling", image: "assets/pj_lightning_thief.jpg" },
        { title: "The Hobbit", author: "J.R.R. Tolkien", image: "assets/pj_lightning_thief.jpg" },
    ],
    non_fiction: [
        { title: "Sapiens", author: "Yuval Noah Harari", image: "assets/pj_lightning_thief.jpg" },
        { title: "Educated", author: "Tara Westover", image: "assets/pj_lightning_thief.jpg" },
    ],
    biography: [
        { title: "Steve Jobs", author: "Walter Isaacson", image: "assets/pj_lightning_thief.jpg" },
        { title: "Becoming", author: "Michelle Obama", image: "assets/pj_lightning_thief.jpg" },
    ],
    science: [
        { title: "A Brief History of Time", author: "Stephen Hawking", image: "assets/pj_lightning_thief.jpg" },
        { title: "The Selfish Gene", author: "Richard Dawkins", image: "assets/pj_lightning_thief.jpg" },
    ],
};

// Function to display books based on selected genre
function showBooks(genre) {
    const bookListContainer = document.getElementById('book-list');
    bookListContainer.innerHTML = ''; // Clear current book list

    // Check if genre exists in the data
    if (booksData[genre]) {
        booksData[genre].forEach(book => {
            const bookItem = document.createElement('div');
            bookItem.classList.add('book-item');

            // Book cover image
            const img = document.createElement('img');
            img.src = book.image;
            img.alt = book.title;

            // Book details
            const bookDetails = document.createElement('div');
            bookDetails.classList.add('book-details');
            const title = document.createElement('h3');
            title.textContent = book.title;
            const author = document.createElement('p');
            author.textContent = `by ${book.author}`;

            bookDetails.appendChild(title);
            bookDetails.appendChild(author);
            bookItem.appendChild(img);
            bookItem.appendChild(bookDetails);

            // Append to the book list container
            bookListContainer.appendChild(bookItem);
        });
    }
}
