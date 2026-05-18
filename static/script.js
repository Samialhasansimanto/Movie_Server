async function getMovies() {
    const genre = document.getElementById('genre').value;
    const type = document.getElementById('type').value;
    const rating = document.getElementById('rating').value;
    const moviesContainer = document.getElementById('movies');

    moviesContainer.innerHTML = `
    <div class="loader-wrapper">
        <div class="spinner"></div>
        <h3 class="pipeline-text">AI Matrix Core Processing Data Fields...</h3>
    </div>
    `;

    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ genre, type, rating })
        });

        const data = await response.json();
        moviesContainer.innerHTML = "";

        // if movie not matched
        if (!data || data.length === 0) {
            moviesContainer.innerHTML = `
            <div class="no-results-panel">
                <i class="fas fa-hourglass-empty text-orange" style="font-size: 3rem; margin-bottom: 1rem;"></i>
                <h2>No Matched Database Configurations Found 😢</h2>
                <p>Modify filtering dropdown criteria configurations.</p>
            </div>
            `;
            return;
        }

        // map() 
        const moviesHTML = data.map(movie => {
            // default poster if not available
            const imagePath = movie.poster ? `/static/posters/${movie.poster}` : 'https://images.unsplash.com/photo-1594909122845-11baa439b7bf?q=80&w=500';
            
            return `
            <div class="movie-card">
                <div class="poster-frame">
                    <img src="${imagePath}" onerror="this.src='https://images.unsplash.com/photo-1594909122845-11baa439b7bf?q=80&w=500'" alt="${movie.title}">
                    <div class="card-badge-rating">
                        <i class="fas fa-star text-gold"></i> ${movie.rating}
                    </div>
                </div>
                <div class="movie-info">
                    <h2>${movie.title}</h2>
                    <div class="card-meta-tags">
                        <span class="meta-tag context-origin">${movie.type}</span>
                        <span class="genre-sub-tag">${movie.genre}</span>
                    </div>
                    <div class="description">${movie.description}</div>
                </div>
            </div>
            `;
        }).join(''); // all element into one single string

        moviesContainer.innerHTML = moviesHTML;

    } catch (error) {
        console.error("Pipeline breakdown tracking state error:", error);
        moviesContainer.innerHTML = `
        <div class="no-results-panel">
            <h2 class="error-text">Network Synchronization Failure. Check Console Window Grid.</h2>
        </div>
        `;
    }
}
