import { useState, useEffect } from 'react'
import ThumbnailCard from './components/ThumbnailCard'
import LoginForm from './components/LoginForm'
import CreateThumbnailForm from './components/CreateThumbnailForm'

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [thumbnails, setThumbnails] = useState([])

  useEffect(() => {
    if (!token) return

    async function fetchThumbnails() {
      const response = await fetch('http://127.0.0.1:8000/thumbnails/', {
        headers: { Authorization: `Bearer ${token}` },
      })
      const data = await response.json()
      setThumbnails(data)
    }

    fetchThumbnails()
  }, [token])

  if (!token) {
    return <LoginForm onLoginSuccess={(newToken) => setToken(newToken)} />
  }

  function handleNewThumbnail(newThumbnail) {
    setThumbnails((prev) => [newThumbnail, ...prev])
  }

  function handleLogout(){
    localStorage.removeItem('token')
    setToken(null)
  }

  return (
    <div>
      <h1>Thumbnail Studio</h1>
      <button onClick={handleLogout}>Log Out</button>
      <CreateThumbnailForm token={token} onThumbnailCreated={handleNewThumbnail} />
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
  )
}


export default App