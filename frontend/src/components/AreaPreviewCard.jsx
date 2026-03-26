function AreaPreviewCard({ selectedPosition }) {
  return (
    <div className="card">
      <h3>Selected Area Preview</h3>

      {selectedPosition ? (
        <>
          <p><strong>Region:</strong> {selectedPosition.regionName}</p>
          <p><strong>Latitude:</strong> {selectedPosition.lat.toFixed(6)}</p>
          <p><strong>Longitude:</strong> {selectedPosition.lng.toFixed(6)}</p>
        </>
      ) : (
        <p>No area selected yet. Click on the map to choose a location.</p>
      )}
    </div>
  )
}

export default AreaPreviewCard