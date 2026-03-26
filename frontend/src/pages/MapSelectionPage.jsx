import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import MapSelector from '../components/MapSelector'
import AreaPreviewCard from '../components/AreaPreviewCard'

const cityCoordinates = {
  Nashik: [19.9975, 73.7898],
  Pune: [18.5204, 73.8567],
  Mumbai: [19.0760, 72.8777],
  Nagpur: [21.1458, 79.0882],
}

function MapSelectionPage() {
  const navigate = useNavigate()
  const [searchCity, setSearchCity] = useState('')
  const [mapCenter, setMapCenter] = useState([19.9975, 73.7898])
  const [selectedPosition, setSelectedPosition] = useState(null)

  const handleSearch = () => {
    const trimmedCity = searchCity.trim()
    const coords = cityCoordinates[trimmedCity]

    if (coords) {
      setMapCenter(coords)
      setSelectedPosition({
        lat: coords[0],
        lng: coords[1],
        regionName: trimmedCity,
      })
    } else {
      alert('City not found. Try: Nashik, Pune, Mumbai, Nagpur')
    }
  }

  const handleNext = () => {
    if (!selectedPosition) {
      alert('Please click on the map first to select an area.')
      return
    }

    navigate('/year-selection', {
      state: {
        selectedPosition,
      },
    })
  }

  return (
    <div className="page">
      <Navbar />

      <main className="page-content">
        <h1>Map Selection Page</h1>
        <p>Search a city or click directly on the map to select an area.</p>

        <div className="search-bar">
          <input
            type="text"
            placeholder="Enter city name (Nashik, Pune, Mumbai, Nagpur)"
            value={searchCity}
            onChange={(e) => setSearchCity(e.target.value)}
          />
          <button className="primary-btn" onClick={handleSearch}>
            Search
          </button>
        </div>

        <MapSelector
          selectedPosition={selectedPosition}
          setSelectedPosition={setSelectedPosition}
          mapCenter={mapCenter}
        />

        <AreaPreviewCard selectedPosition={selectedPosition} />

        <button className="primary-btn" onClick={handleNext}>
          Next
        </button>
      </main>

      <Footer />
    </div>
  )
}

export default MapSelectionPage