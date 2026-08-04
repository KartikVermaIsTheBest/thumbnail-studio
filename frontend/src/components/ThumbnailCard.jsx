import { useState } from 'react'

function ThumbnailCard({ id, prompt, imageUrl, token }) {
  const [isFavorited, setIsFavorited] = useState(false)
  const [loading, setLoading] = useState(false)

  async function toggleFavorite() {
    setLoading(true)
    const method = isFavorited ? 'DELETE' : 'POST'

    const response = await fetch(`http://127.0.0.1:8000/favorites/${id}`, {
      method,
      headers: { Authorization: `Bearer ${token}` },
    })

    if (response.ok) {
      setIsFavorited(!isFavorited)
    }
    setLoading(false)
  }

  return (
    <div className="thumbnail-card">
      <img src={imageUrl} alt={prompt} width="320" />
      <p>{prompt}</p>
      <button onClick={toggleFavorite} disabled={loading}>
        {isFavorited ? '★ Favorited' : '☆ Favorite'}
      </button>
    </div>
  )
}

export default ThumbnailCard