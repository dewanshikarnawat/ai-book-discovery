
const API_URL = 'http://127.0.0.1:5000/recommend';


async function getBookCoverByTitle(title) {
    try {
        const response = await fetch(`https://www.googleapis.com/books/v1/volumes?q=intitle:${encodeURIComponent(title.substring(0, 40))}`);
        const data = await response.json();
        return data.items?.[0]?.volumeInfo?.imageLinks?.thumbnail || 
               data.items?.[0]?.volumeInfo?.imageLinks?.smallThumbnail || '';
    } catch {
        return '';
    }
}

document.getElementById('bookInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') getRecommendations();
});

async function getRecommendations() {
    const query = document.getElementById('bookInput').value.trim();
    if (!query) return;
    saveSearch(query);
    showLoading();
    hideError();

    try {
        const response = await fetch(`${API_URL}?book=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        console.log('Fetching book covers...');
        const enhancedBooks = await Promise.all(data.map(async (book) => {
            const coverUrl = await getBookCoverByTitle(book.title);
            return { ...book, cover_url: coverUrl };
        }));

        displayResults(enhancedBooks, query);
        const email = localStorage.getItem('currentUser');
        if (email) {
            await fetch('http://127.0.0.1:5000/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, query })
            });
            console.log('✅ Search history saved');
        }
    } catch (error) {
        showError('Backend not running! Run: cd backend && python app.py');
    }
}

function displayResults(books, query) {
    hideLoading();
    document.getElementById('results').style.display = 'block';
    document.getElementById('resultsTitle').textContent = `Books like "${query}" (${books.length} found)`;
    
    document.getElementById('booksGrid').innerHTML = books.map(book => `
        <div class="book-card">
            ${book.cover_url ? `
                <img src="${book.cover_url}" alt="${escapeHtml(book.title)}" class="book-cover" onerror="this.style.display='none'">
            ` : ''}
            <div style="flex: 1;">
                <div class="book-title">${escapeHtml(book.title)}</div>
                <div class="book-author">${escapeHtml(book.author)}</div>
                <div class="book-meta">
                    <div class="rating">⭐ ${book.rating.toFixed(2)}</div>
                    <div class="match">${(book.similarity_score * 100).toFixed(1)}% Match</div>
                </div>
            </div>
        </div>
    `).join('');
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showError(message) {
    hideLoading();
    document.getElementById('error').innerHTML = `<h3>⚠️ Error</h3><p>${message}</p>`;
    document.getElementById('error').style.display = 'block';
}

function hideError() {
    document.getElementById('error').style.display = 'none';
}

function clearResults() {
    document.getElementById('results').style.display = 'none';
    document.getElementById('bookInput').value = '';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function saveSearch(query) {
    let history = JSON.parse(localStorage.getItem('searchHistory')) || [];

    // duplicate remove
    history = history.filter(item => item.toLowerCase() !== query.toLowerCase());

    history.unshift(query);

    // limit to last 5 searches
    if (history.length > 5) history = history.slice(0, 5);

    localStorage.setItem('searchHistory', JSON.stringify(history));
    renderSearchHistory();
}

function renderSearchHistory() {
    const history = JSON.parse(localStorage.getItem('searchHistory')) || [];
    const container = document.getElementById('searchHistory');
    const list = document.getElementById('historyList');

    if (history.length === 0) {
        container.style.display = 'none';
        return;
    }

    container.style.display = 'block';
    list.innerHTML = history.map(item => `
        <span class="history-item" onclick="searchFromHistory('${item.replace(/'/g, "\\'")}')">
            ${item}
        </span>
    `).join('');
}

function searchFromHistory(query) {
    document.getElementById('bookInput').value = query;
    getRecommendations();
}

window.onload = () => {
    renderSearchHistory();
};

async function loadPopularBooks() {
    try {
        const response = await fetch('http://127.0.0.1:5000/popular');
        const data = await response.json();

        displayBooks(data.most_recommended, 'mostRecommended');
        displayBooks(data.top_rated, 'topRated');
    } catch (error) {
        console.error("Error fetching popular books:", error);
    }
}

function displayBooks(books, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = books.map(book => `
        <div class="book-card">
            <div style="flex:1;">
                <div class="book-title">${escapeHtml(book.title)}</div>
                <div class="book-author">${escapeHtml(book.author)}</div>

                <div class="book-meta">
                    <div class="rating">⭐ ${book.rating.toFixed(2)}</div>
                </div>
            </div>
        </div>
    `).join('');
}

// call on page load
loadPopularBooks();

function startVoiceSearch() {
    if (!('webkitSpeechRecognition' in window)) {
        alert("Voice search not supported in this browser");
        return;
    }

    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    showListeningUI();

    recognition.start();

    recognition.onresult = function (event) {
        const voiceText = event.results[0][0].transcript;
        console.log("🎤 Voice input:", voiceText);

        document.getElementById("bookInput").value = voiceText;
        hideListeningUI();

        getRecommendations(); // auto search
    };

    recognition.onerror = function (event) {
        console.error("Voice error:", event.error);
        hideListeningUI();
    };

    recognition.onend = function () {
        hideListeningUI();
    };
}

function showListeningUI() {
    document.getElementById("loading").innerHTML =
        `<i class="fas fa-microphone fa-beat"></i><br>Listening...`;
    document.getElementById("loading").style.display = "block";
}

function hideListeningUI() {
    document.getElementById("loading").style.display = "none";
}