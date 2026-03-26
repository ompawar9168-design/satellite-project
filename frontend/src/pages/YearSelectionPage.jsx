import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

function YearSelectionPage() {
  const navigate = useNavigate()
  const location = useLocation()

  const selectedPosition = location.state?.selectedPosition || null

  const [oldYear, setOldYear] = useState('2020')
  const [newYear, setNewYear] = useState('2026')
  const [predictionEnabled, setPredictionEnabled] = useState(true)
  const [predictionYear, setPredictionYear] = useState('2028')
  const [errorMessage, setErrorMessage] = useState('')

  const availableYears = [
    '2018',
    '2019',
    '2020',
    '2021',
    '2022',
    '2023',
    '2024',
    '2025',
    '2026',
  ]

  const futureYears = [
    '2027',
    '2028',
    '2029',
    '2030',
    '2031',
    '2032',
    '2033',
    '2034',
    '2035',
  ]

  const handleRunAnalysis = () => {
    setErrorMessage('')

    if (!selectedPosition) {
      setErrorMessage('No area selected. Please go back and choose an area on map.')
      return
    }

    if (Number(oldYear) >= Number(newYear)) {
      setErrorMessage('Old year must be smaller than new year.')
      return
    }

    if (predictionEnabled && Number(predictionYear) <= Number(newYear)) {
      setErrorMessage('Prediction year must be greater than new year.')
      return
    }

    navigate('/processing', {
      state: {
        selectedPosition,
        oldYear,
        newYear,
        predictionEnabled,
        predictionYear: predictionEnabled ? predictionYear : null,
      },
    })
  }

  return (
    <div className="page">
      <Navbar />

      <main className="page-content">
        <h1>Year Selection Page</h1>
        <p>Select comparison years and optional future prediction year.</p>

        <div className="card">
          <h3>Selected Area</h3>
          {selectedPosition ? (
            <>
              <p><strong>Region:</strong> {selectedPosition.regionName}</p>
              <p><strong>Latitude:</strong> {selectedPosition.lat.toFixed(6)}</p>
              <p><strong>Longitude:</strong> {selectedPosition.lng.toFixed(6)}</p>
            </>
          ) : (
            <p>No area selected.</p>
          )}
        </div>

        <div className="card">
          <h3>Select Years</h3>

          <div className="form-grid">
            <div className="form-group">
              <label>Old Year</label>
              <select value={oldYear} onChange={(e) => setOldYear(e.target.value)}>
                {availableYears.map((year) => (
                  <option key={year} value={year}>
                    {year}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>New Year</label>
              <select value={newYear} onChange={(e) => setNewYear(e.target.value)}>
                {availableYears.map((year) => (
                  <option key={year} value={year}>
                    {year}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="toggle-row">
            <input
              type="checkbox"
              checked={predictionEnabled}
              onChange={(e) => setPredictionEnabled(e.target.checked)}
            />
            <span>Enable Future Prediction</span>
          </div>

          {predictionEnabled && (
            <div className="form-group prediction-box">
              <label>Prediction Year</label>
              <select
                value={predictionYear}
                onChange={(e) => setPredictionYear(e.target.value)}
              >
                {futureYears.map((year) => (
                  <option key={year} value={year}>
                    {year}
                  </option>
                ))}
              </select>
            </div>
          )}

          {errorMessage && <p className="error-text">{errorMessage}</p>}

          <button className="primary-btn" onClick={handleRunAnalysis}>
            Run Analysis
          </button>
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default YearSelectionPage