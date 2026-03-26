import { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import axios from 'axios'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

function ProcessingPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const data = location.state || null

  const [error, setError] = useState('')
  const [currentStep, setCurrentStep] = useState(0)

  const steps = [
    '📡 Checking backend health...',
    '🛰️ Fetching real Sentinel imagery...',
    '🧠 Running land classification...',
    '🔍 Detecting land-use changes...',
    '📊 Generating stats, graphs, and insights...',
    '🔮 Predicting 2028 trends...',
    '✅ Finalizing dashboard...',
  ]

  useEffect(() => {
    const runAnalysis = async () => {
      try {
        if (!data) {
          navigate('/year-selection')
          return
        }

        setCurrentStep(0)
        const health = await axios.get('http://127.0.0.1:5000/api/health')

        if (health.data.status !== 'success') {
          throw new Error('Backend is not healthy')
        }

        for (let i = 1; i < steps.length - 1; i++) {
          setCurrentStep(i)
          await new Promise((res) => setTimeout(res, 600))
        }

        const res = await axios.post('http://127.0.0.1:5000/api/run-analysis', data)

        setCurrentStep(steps.length - 1)
        await new Promise((res) => setTimeout(res, 800))

        navigate('/dashboard', {
          state: {
            ...data,
            images: res.data.result,
          },
        })
      } catch (err) {
        console.error('Run analysis error:', err)
        setError('Failed to run full analysis. Please check backend, internet, API, and Sentinel configuration.')
      }
    }

    runAnalysis()
  }, [data, navigate])

  return (
    <div className="page">
      <Navbar />

      <main className="page-content center-content">
        <h1>Running Full Analysis...</h1>

        <div className="card" style={{ maxWidth: '700px', width: '100%' }}>
          {steps.map((step, index) => (
            <div
              key={index}
              style={{
                padding: '10px',
                marginBottom: '8px',
                borderRadius: '8px',
                background:
                  index === currentStep
                    ? '#2563eb'
                    : index < currentStep
                    ? '#16a34a'
                    : '#1f2937',
                color: '#ffffff',
                fontWeight: index === currentStep ? 'bold' : 'normal',
                transition: 'all 0.3s ease',
              }}
            >
              {index < currentStep ? '✔️ ' : ''}
              {step}
            </div>
          ))}
        </div>

        {!error && (
          <div style={{ marginTop: '20px' }}>
            <div className="loader"></div>
          </div>
        )}

        {error && (
          <div className="card" style={{ maxWidth: '700px', marginTop: '20px' }}>
            <h3>Analysis Error</h3>
            <p>{error}</p>

            <button className="primary-btn" onClick={() => navigate('/year-selection')}>
              Restart Analysis
            </button>
          </div>
        )}
      </main>

      <Footer />
    </div>
  )
}

export default ProcessingPage