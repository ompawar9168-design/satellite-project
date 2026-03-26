import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet'
import L from 'leaflet'
import { useEffect } from 'react'

delete L.Icon.Default.prototype._getIconUrl

L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

function LocationMarker({ selectedPosition, setSelectedPosition }) {
  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng
      setSelectedPosition({
        lat,
        lng,
        regionName: 'Selected Region',
      })
    },
  })

  if (!selectedPosition) return null

  return (
    <Marker position={[selectedPosition.lat, selectedPosition.lng]}>
      <Popup>
        Selected Location <br />
        Lat: {selectedPosition.lat.toFixed(4)} <br />
        Lng: {selectedPosition.lng.toFixed(4)}
      </Popup>
    </Marker>
  )
}

function RecenterMap({ center }) {
  const map = useMapEvents({})

  useEffect(() => {
    if (center) {
      map.setView(center, 11)
    }
  }, [center, map])

  return null
}

function MapSelector({ selectedPosition, setSelectedPosition, mapCenter }) {
  return (
    <div className="map-wrapper">
      <MapContainer
        center={mapCenter || [19.9975, 73.7898]}
        zoom={11}
        scrollWheelZoom={true}
        className="leaflet-map"
      >
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <RecenterMap center={mapCenter} />
        <LocationMarker
          selectedPosition={selectedPosition}
          setSelectedPosition={setSelectedPosition}
        />
      </MapContainer>
    </div>
  )
}

export default MapSelector