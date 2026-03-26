import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

function LandingPage() {
  const navigate = useNavigate()

  return (
    <div className="page">
      <Navbar />

      <main className="page-content center-content">
        <h1>Satellite Land Use & Change Detection</h1>
        <p>
          Analyze land-use changes between selected years and view future prediction insights.
        </p>

        <button className="primary-btn" onClick={() => navigate('/map-selection')}>
          Start Analysis
        </button>
      </main>

      <Footer />
    </div>
  )
}

export default LandingPage