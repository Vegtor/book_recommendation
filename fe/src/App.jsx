import { useState } from "react";
import BookGrid from "./BookGrid";
import BookGridGoodreads from "./BookGridGoodreads";
import { SearchedBook, SearchedBookGoodreads } from "./SearchedBook";
import "./App.css";


function App() {
    const [book, setBook] = useState("");
    const [author, setAuthor] = useState("");
    const [publisher, setPublisher] = useState("");
    const [year, setYear] = useState("");
    const [isbn, setIsbn] = useState("");

    const [showAdvanced, setShowAdvanced] = useState(false);
    const [recommendations, setRecommendations] = useState([]);
    const [searchedBook, setSearchedBook] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [selectedVersion, setSelectedVersion] = useState("v1");

    const fetchRecs = async () => {
        if (!book.trim()) return;
        setLoading(true);
        setError("");
        setRecommendations([]);
        setSearchedBook(null);

        try {
            const params = new URLSearchParams({ book_name: book, version: selectedVersion });
            if (showAdvanced) {
                if (author.trim()) params.append("author", author);
                if (publisher.trim()) params.append("publisher", publisher);
                if (year.trim()) params.append("year", year);
                if (isbn.trim()) params.append("isbn", isbn);
            }

            const backendUrl = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:8000";
            let backendCall;

            if (selectedVersion === "v1" || selectedVersion === "v1_1"){
                backendCall = `${backendUrl}/recommend_v1?${params.toString()}`;
            }
            else{
                backendCall = `${backendUrl}/recommend_v2?${params.toString()}`;
            }
            const res = await fetch(backendCall);
            
            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.detail || `HTTP error ${res.status}`);
            }
            setSearchedBook(data.searched_book?.[0] || null);
            if (!data.recommendations || data.recommendations.length === 0) {
                console.error("No usable data for recommendation for this search query");
                setError("No usable data for recommendation for this search query");
            } else {
                setRecommendations(data.recommendations);
            }
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
                            disabled={selectedVersion === "v2" || selectedVersion === "v2_1"}
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
                        <div className="version-checkboxes">
                            <label>
                                <input
                                    type="radio"
                                    name="version"
                                    value="v1"
                                    checked={selectedVersion === "v1"}
                                    onChange={() => setSelectedVersion("v1")}
                                />
                                &nbsp;v1
                            </label>
                            <label>
                                <input
                                    type="radio"
                                    name="version"
                                    value="v1_1"
                                    checked={selectedVersion === "v1_1"}
                                    onChange={() => setSelectedVersion("v1_1")}
                                />
                                &nbsp;v1.1
                            </label>
                            <label>
                                <input
                                    type="radio"
                                    name="version"
                                    value="v2"
                                    checked={selectedVersion === "v2"}
                                    onChange={() => {
                                        setSelectedVersion("v2");
                                        setPublisher("");
                                    }}
                                />
                                &nbsp;v2
                            </label>
                            <label>
                                <input
                                    type="radio"
                                    name="version"
                                    value="v2_1"
                                    checked={selectedVersion === "v2_1"}
                                    onChange={() => {
                                        setSelectedVersion("v2_1");
                                        setPublisher("");
                                    }}
                                />
                                &nbsp;v2.1
                            </label>
                        </div>
                    </div>
                )}

                {loading && <p>Loading...</p>}
                {error && <p style={{ color: "red" }}>{error}</p>}
            </div>

            {searchedBook && (selectedVersion === "v1" || selectedVersion === "v1_1") && <SearchedBook book={searchedBook} />}
            {searchedBook && (selectedVersion === "v2" || selectedVersion === "v2_1") && <SearchedBookGoodreads book={searchedBook} />}

            {recommendations.length > 0 && (selectedVersion === "v1" || selectedVersion === "v1_1") && <BookGrid books={recommendations} />}
            {recommendations.length > 0 && (selectedVersion === "v2" || selectedVersion === "v2_1") && <BookGridGoodreads books={recommendations} />}
        </div>
    );
}

export default App;