import { useState } from "react";
import "./App.css";

function App_v1() {
    const [book, setBook] = useState("");
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const fetchRecs = async () => {
        if (!book.trim()) return;
        setLoading(true);
        setError("");
        try {
            const res = await fetch(`http://127.0.0.1:8000/recommend?book_name=${encodeURIComponent(book)}`);
            if (!res.ok) throw new Error(`HTTP error ${res.status}`);
            const data = await res.json();
            setRecommendations(data.recommendations);
        } catch (err) {
            console.error(err);
            setError("Failed to fetch recommendations.");
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

                {loading && <p>Loading...</p>}
                {error && <p style={{ color: "red" }}>{error}</p>}

            </div>
            <ul className="recommendations">
                {recommendations.map((r, i) => (
                    <li key={i}>
                        <b>{r.book}</b> — {r.corr}
                    </li>
                ))}
            </ul>
        </div>
    );
}
export default App_v1
