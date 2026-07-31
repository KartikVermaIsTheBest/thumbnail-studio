import { useState } from 'react'

function CreateThumbnailForm({ token, onThumbnailCreated }) {
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/thumbnails/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ prompt, width: 1280, height: 720 }),
      })

      if (!response.ok) {
        throw new Error('Generation failed')
      }

      const newThumbnail = await response.json()
      onThumbnailCreated(newThumbnail)
      setPrompt('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Describe your thumbnail..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        disabled={loading}
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Generating...' : 'Generate'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  )
}

export default CreateThumbnailForm