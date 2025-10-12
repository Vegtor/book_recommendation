import { useState } from "react";
import BookGrid from "./BookGrid";
import "./App.css";

function App() {
    const [book, setBook] = useState("");
    const [author, setAuthor] = useState("");
    const [publisher, setPublisher] = useState("");
    const [year, setYear] = useState("");
    const [isbn, setIsbn] = useState("");

    const [showAdvanced, setShowAdvanced] = useState(false);
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const fetchRecs = async () => {
        if (!book.trim()) return;
        setLoading(true);
        setError("");
        setRecommendations([]);

        try {
            const params = new URLSearchParams({ book_name: book });
            if (showAdvanced) {
                if (author.trim()) params.append("author", author);
                if (publisher.trim()) params.append("publisher", publisher);
                if (year.trim()) params.append("year", year);
                if (isbn.trim()) params.append("isbn", isbn);
            }

            const res = await fetch(`http://127.0.0.1:8000/recommend_v3?${params.toString()}`);
            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.detail || `HTTP error ${res.status}`);
            }
            setRecommendations(data.recommendations || []);
        } catch (err) {
            console.error(err.message);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <div className="recommend-box">
                <h2>Book Recommender</h2>

                <div className="input-group">
                    <input
                        value={book}
                        onChange={(e) => setBook(e.target.value)}
                        placeholder="Enter book name"
                    />
                    <button onClick={fetchRecs}>Recommend</button>
                </div>

                <div className="advanced-toggle">
                    <label>
                        <input
                            type="checkbox"
                            checked={showAdvanced}
                            onChange={() => setShowAdvanced(!showAdvanced)}
                        />
                        &nbsp;Advanced search
                    </label>
                </div>

                {showAdvanced && (
                    <div className="advanced-fields">
                        <input
                            value={author}
                            onChange={(e) => setAuthor(e.target.value)}
                            placeholder="Author"
                        />
                        <input
                            value={publisher}
                            onChange={(e) => setPublisher(e.target.value)}
                            placeholder="Publisher"
                        />
                        <input
                            value={year}
                            onChange={(e) => setYear(e.target.value)}
                            placeholder="Year"
                        />
                        <input
                            value={isbn}
                            onChange={(e) => setIsbn(e.target.value)}
                            placeholder="ISBN"
                        />
                    </div>
                )}

                {loading && <p>Loading...</p>}
                {error && <p style={{ color: "red" }}>{error}</p>}
            </div>

            {recommendations.length > 0 && <BookGrid books={recommendations} />}
        </div>
    );
}

export default App;