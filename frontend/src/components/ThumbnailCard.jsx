function ThumbnailCard({prompt , imageUrl}) {
    return (
        <div className="thumbnail-card">
            <img src={imageUrl} alt={prompt} width="320" />
            <p>{prompt}</p>
        </div>
    )
}

export default ThumbnailCard