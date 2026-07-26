import { useState, useEffect } from 'react'
import ThumbnailCard from './components/ThumbnailCard'

function App() {
  const [thumbnails, setThumbnails] = useState([])

  useEffect(() => {
    async function fetchThumbnails() {
      const response = await fetch('http://127.0.0.1:8000/thumbnails/', {
        headers: {
          Authorization: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzg1MDkxODgyfQ.jOnzQ0EUI2tmxNJBVP3vavl-InfrEL2HDFN1J_idu9E',
        },
      })
      const data = await response.json()
      setThumbnails(data)
    }

    fetchThumbnails()
  }, [])

  return (
    <div>
      <h1>Thumbnail Studio</h1>
      {thumbnails.map((thumb) => (
        <ThumbnailCard key={thumb.id} prompt={thumb.prompt} imageUrl={thumb.image_url} />
      ))}
    </div>
  )
}

export default App