import { useState, useEffect } from "react";
import ThumbnailCard from "./components/ThumbnailCard";
import LoginForm from "./components/LoginForm";
import CreateThumbnailForm from "./components/CreateThumbnailForm";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [thumbnails, setThumbnails] = useState([]);

  useEffect(() => {
    if (!token) return;

    async function fetchThumbnails() {
      try {
        const response = await apiFetch("/thumbnails/");
        const data = await response.json();
        setThumbnails(data);
      } catch (err) {
        console.error(err);
      }
    }

    fetchThumbnails();
  }, [token]);

  if (!token) {
    return <LoginForm onLoginSuccess={(newToken) => setToken(newToken)} />;
  }

  function handleNewThumbnail(newThumbnail) {
    setThumbnails((prev) => [newThumbnail, ...prev]);
  }

  function handleLogout() {
    localStorage.removeItem("token");
    setToken(null);
  }

  async function apiFetch(path, options = {}) {
    const response = await fetch(`http://127.0.0.1:8000${path}`, {
      ...options,
      headers: {
        ...(options.headers || {}),
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status === 401) {
      localStorage.removeItem("token");
      setToken(null);
      throw new Error("Session expired, please log in again");
    }

    return response;
  }



  return (
    <div>
      <h1>Thumbnail Studio</h1>
      <button onClick={handleLogout}>Log Out</button>
      <CreateThumbnailForm
        apiFetch={apiFetch}
        onThumbnailCreated={handleNewThumbnail}
      />
      {thumbnails.map((thumb) => (
        <ThumbnailCard
          key={thumb.id}
          id={thumb.id}
          prompt={thumb.prompt}
          imageUrl={thumb.image_url}
          token={token}
        />
      ))}
    </div>
  );
}

export default App;
