import { useLocation } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

function DashboardPage() {
  const location = useLocation()
  const data = location.state || {}

  const oldImg = data.images?.old_image
  const newImg = data.images?.new_image
  const changeMap = data.images?.change_map_base64
  const thresholdMap = data.images?.threshold_map_base64
  const changePercent = data.images?.change_percent

  const oldClassification = data.images?.old_classification || {}
  const newClassification = data.images?.new_classification || {}
  const classComparison = data.images?.class_comparison || {}
  const transitionStats = data.images?.transition_stats || {}
  const insights = data.images?.insights || []

  const prediction2028 = data.images?.prediction_2028 || {}
  const predictionInsights = data.images?.prediction_insights || []

  const advancedStats = data.images?.advanced_stats || {}
  const zonewiseChange = advancedStats.zonewise_change || {}

  const oldClassifiedMap = oldClassification?.classified_map_base64
  const newClassifiedMap = newClassification?.classified_map_base64

  const imgStyle = {
    width: '100%',
    height: '420px',
    objectFit: 'cover',
    borderRadius: '14px',
  }

  const maskStyle = {
    width: '100%',
    height: '460px',
    objectFit: 'contain',
    borderRadius: '14px',
    background: '#0b1220',
  }

  const comparisonChartData = [
    {
      name: 'Urban',
      before: oldClassification.urban_percent || 0,
      after: newClassification.urban_percent || 0,
    },
    {
      name: 'Vegetation',
      before: oldClassification.vegetation_percent || 0,
      after: newClassification.vegetation_percent || 0,
    },
    {
      name: 'Water',
      before: oldClassification.water_percent || 0,
      after: newClassification.water_percent || 0,
    },
    {
      name: 'Other',
      before: oldClassification.other_percent || 0,
      after: newClassification.other_percent || 0,
    },
  ]

  const trendChartData = [
    {
      year: data.oldYear || '2020',
      urban: oldClassification.urban_percent || 0,
      vegetation: oldClassification.vegetation_percent || 0,
      water: oldClassification.water_percent || 0,
      other: oldClassification.other_percent || 0,
    },
    {
      year: data.newYear || '2024',
      urban: newClassification.urban_percent || 0,
      vegetation: newClassification.vegetation_percent || 0,
      water: newClassification.water_percent || 0,
      other: newClassification.other_percent || 0,
    },
    {
      year: '2028',
      urban: prediction2028.urban_percent || 0,
      vegetation: prediction2028.vegetation_percent || 0,
      water: prediction2028.water_percent || 0,
      other: prediction2028.other_percent || 0,
    },
  ]

  const zoneChartData = [
    { name: 'North', change: zonewiseChange.north || 0 },
    { name: 'South', change: zonewiseChange.south || 0 },
    { name: 'East', change: zonewiseChange.east || 0 },
    { name: 'West', change: zonewiseChange.west || 0 },
  ]

  const downloadPdfReport = async () => {
    const reportElement = document.getElementById('report-section')
    if (!reportElement) return

    const canvas = await html2canvas(reportElement, {
      scale: 2,
      useCORS: true,
      backgroundColor: '#0f172a',
    })

    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF('p', 'mm', 'a4')

    const pdfWidth = pdf.internal.pageSize.getWidth()
    const pdfHeight = pdf.internal.pageSize.getHeight()

    const imgWidth = pdfWidth
    const imgHeight = (canvas.height * imgWidth) / canvas.width

    let heightLeft = imgHeight
    let position = 0

    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
    heightLeft -= pdfHeight

    while (heightLeft > 0) {
      position = heightLeft - imgHeight
      pdf.addPage()
      pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight)
      heightLeft -= pdfHeight
    }

    pdf.save(`satellite_report_${data.oldYear}_${data.newYear}.pdf`)
  }

  return (
    <div className="page dashboard-page">
      <Navbar />

      <main className="page-content">
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            gap: '12px',
            flexWrap: 'wrap',
            marginBottom: '20px',
            alignItems: 'flex-start',
          }}
        >
          <div>
            <h1 className="page-title">Satellite Comparison Dashboard</h1>
            <p className="page-subtitle">
              Real Sentinel imagery + spectral analysis + change prediction
            </p>
          </div>

          <button className="primary-btn" onClick={downloadPdfReport}>
            Download PDF Report
          </button>
        </div>

        <div id="report-section">
          <div className="dashboard-grid">
            <div className="card stat-card">
              <h3>Selected Area</h3>
              <p>{data.selectedPosition?.regionName || 'Selected Area'}</p>
            </div>

            <div className="card stat-card">
              <h3>Coordinates</h3>
              <p>
                {data.selectedPosition?.lat?.toFixed(6)}, {data.selectedPosition?.lng?.toFixed(6)}
              </p>
            </div>

            <div className="card stat-card">
              <h3>Compared Years</h3>
              <p>{data.oldYear} vs {data.newYear}</p>
            </div>

            <div className="card stat-card highlight-card">
              <h3>Total Change Detected</h3>
              <p>{changePercent ?? 'N/A'}%</p>
            </div>
          </div>

          <div className="dashboard-grid">
            <div className="card stat-card">
              <h3>Total Area</h3>
              <p>{advancedStats.total_area_sqkm ?? 'N/A'} sq km</p>
            </div>

            <div className="card stat-card">
              <h3>Changed Area</h3>
              <p>{advancedStats.changed_area_sqkm ?? 'N/A'} sq km</p>
            </div>

            <div className="card stat-card">
              <h3>Annual Urban Rate</h3>
              <p>{advancedStats.annual_urban_growth_rate ?? 'N/A'}% / year</p>
            </div>

            <div className="card stat-card">
              <h3>Annual Vegetation Rate</h3>
              <p>{advancedStats.annual_vegetation_change_rate ?? 'N/A'}% / year</p>
            </div>
          </div>

          <div className="dashboard-grid">
            <div className="card stat-card">
              <h3>Urban Growth</h3>
              <p>{classComparison.urban_growth_percent ?? 'N/A'}%</p>
            </div>

            <div className="card stat-card">
              <h3>Vegetation Change</h3>
              <p>{classComparison.vegetation_change_percent ?? 'N/A'}%</p>
            </div>

            <div className="card stat-card">
              <h3>Water Change</h3>
              <p>{classComparison.water_change_percent ?? 'N/A'}%</p>
            </div>

            <div className="card stat-card">
              <h3>Other Change</h3>
              <p>{classComparison.other_change_percent ?? 'N/A'}%</p>
            </div>
          </div>

          <div className="card insight-card">
            <h3>AI Insights</h3>
            {insights.length > 0 ? (
              insights.map((item, index) => (
                <div key={index} className="insight-item">
                  {item}
                </div>
              ))
            ) : (
              <p>No insights available.</p>
            )}
          </div>

          <div className="card">
            <h3>Land Cover Comparison Graph</h3>
            <div style={{ width: '100%', height: '320px' }}>
              <ResponsiveContainer>
                <BarChart data={comparisonChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="name" stroke="#cbd5e1" />
                  <YAxis stroke="#cbd5e1" />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="before" name={`Before (${data.oldYear})`} />
                  <Bar dataKey="after" name={`After (${data.newYear})`} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card prediction-card">
            <h3>2028 Prediction</h3>
            <div className="dashboard-grid">
              <div className="card mini-card">
                <h3>Urban (2028)</h3>
                <p>{prediction2028.urban_percent ?? 'N/A'}%</p>
              </div>

              <div className="card mini-card">
                <h3>Vegetation (2028)</h3>
                <p>{prediction2028.vegetation_percent ?? 'N/A'}%</p>
              </div>

              <div className="card mini-card">
                <h3>Water (2028)</h3>
                <p>{prediction2028.water_percent ?? 'N/A'}%</p>
              </div>

              <div className="card mini-card">
                <h3>Other (2028)</h3>
                <p>{prediction2028.other_percent ?? 'N/A'}%</p>
              </div>
            </div>
          </div>

          <div className="card">
            <h3>Trend Graph (2020 → 2024 → 2028)</h3>
            <div style={{ width: '100%', height: '340px' }}>
              <ResponsiveContainer>
                <BarChart data={trendChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="year" stroke="#cbd5e1" />
                  <YAxis stroke="#cbd5e1" />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="urban" name="Urban" />
                  <Bar dataKey="vegetation" name="Vegetation" />
                  <Bar dataKey="water" name="Water" />
                  <Bar dataKey="other" name="Other" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card">
            <h3>Zone-wise Change</h3>
            <div style={{ width: '100%', height: '320px' }}>
              <ResponsiveContainer>
                <BarChart data={zoneChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="name" stroke="#cbd5e1" />
                  <YAxis stroke="#cbd5e1" />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="change" name="Change %" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card">
            <h3>Land Transition Stats</h3>
            <div className="dashboard-grid">
              <div className="card mini-card">
                <h3>Vegetation → Urban</h3>
                <p>{transitionStats.vegetation_to_urban ?? 'N/A'}%</p>
              </div>

              <div className="card mini-card">
                <h3>Water → Urban</h3>
                <p>{transitionStats.water_to_urban ?? 'N/A'}%</p>
              </div>

              <div className="card mini-card">
                <h3>Water → Other</h3>
                <p>{transitionStats.water_to_other ?? 'N/A'}%</p>
              </div>

              <div className="card mini-card">
                <h3>Other → Urban</h3>
                <p>{transitionStats.other_to_urban ?? 'N/A'}%</p>
              </div>

              <div className="card mini-card">
                <h3>Vegetation → Other</h3>
                <p>{transitionStats.vegetation_to_other ?? 'N/A'}%</p>
              </div>

              <div className="card mini-card">
                <h3>No Change</h3>
                <p>{transitionStats.no_change ?? 'N/A'}%</p>
              </div>
            </div>
          </div>

          <div className="card insight-card">
            <h3>2028 Prediction Insights</h3>
            {predictionInsights.length > 0 ? (
              predictionInsights.map((item, index) => (
                <div key={index} className="insight-item">
                  {item}
                </div>
              ))
            ) : (
              <p>No prediction insights available.</p>
            )}
          </div>

          <div className="dashboard-grid">
            <div className="card">
              <h3>Before ({data.oldYear})</h3>
              {oldImg ? (
                <img
                  src={`data:image/png;base64,${oldImg}`}
                  alt="Old satellite"
                  style={imgStyle}
                />
              ) : (
                <p>No old image available.</p>
              )}
            </div>

            <div className="card">
              <h3>After ({data.newYear})</h3>
              {newImg ? (
                <img
                  src={`data:image/png;base64,${newImg}`}
                  alt="New satellite"
                  style={imgStyle}
                />
              ) : (
                <p>No new image available.</p>
              )}
            </div>
          </div>

          <div className="dashboard-grid">
            <div className="card">
              <h3>Before Classification ({data.oldYear})</h3>
              {oldClassifiedMap ? (
                <img
                  src={`data:image/png;base64,${oldClassifiedMap}`}
                  alt="Old classified map"
                  style={maskStyle}
                />
              ) : (
                <p>No old classified map available.</p>
              )}
              <div className="stats-list">
                <p>Urban: {oldClassification.urban_percent ?? 'N/A'}%</p>
                <p>Vegetation: {oldClassification.vegetation_percent ?? 'N/A'}%</p>
                <p>Water: {oldClassification.water_percent ?? 'N/A'}%</p>
                <p>Other: {oldClassification.other_percent ?? 'N/A'}%</p>
              </div>
            </div>

            <div className="card">
              <h3>After Classification ({data.newYear})</h3>
              {newClassifiedMap ? (
                <img
                  src={`data:image/png;base64,${newClassifiedMap}`}
                  alt="New classified map"
                  style={maskStyle}
                />
              ) : (
                <p>No new classified map available.</p>
              )}
              <div className="stats-list">
                <p>Urban: {newClassification.urban_percent ?? 'N/A'}%</p>
                <p>Vegetation: {newClassification.vegetation_percent ?? 'N/A'}%</p>
                <p>Water: {newClassification.water_percent ?? 'N/A'}%</p>
                <p>Other: {newClassification.other_percent ?? 'N/A'}%</p>
              </div>
            </div>
          </div>

          <div className="dashboard-grid">
            <div className="card">
              <h3>Change Heatmap</h3>
              {changeMap ? (
                <img
                  src={`data:image/png;base64,${changeMap}`}
                  alt="Change heatmap"
                  style={maskStyle}
                />
              ) : (
                <p>No change map available.</p>
              )}
            </div>

            <div className="card">
              <h3>Threshold Change Mask</h3>
              {thresholdMap ? (
                <img
                  src={`data:image/png;base64,${thresholdMap}`}
                  alt="Threshold change mask"
                  style={maskStyle}
                />
              ) : (
                <p>No threshold mask available.</p>
              )}
            </div>
          </div>

          <div className="card legend-card">
            <h3>Classification Legend</h3>
            <p>🟩 Vegetation | 🟦 Water | ⬜ Urban/Built-up | 🟨 Other/Barren</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default DashboardPage