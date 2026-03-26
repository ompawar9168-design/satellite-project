function AreaPreviewCard({ selectedPosition }) {
  if (!selectedPosition) return null

  return (
    <div className="card">
      <h3>Selected Area Preview</h3>
      <p><strong>Region:</strong> {selectedPosition.regionName}</p>
      <p>
        <strong>Coordinates:</strong> {selectedPosition.lat.toFixed(6)}, {selectedPosition.lng.toFixed(6)}
      </p>
    </div>
  )
}

export default AreaPreviewCard