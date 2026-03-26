import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import MapSelectionPage from './pages/MapSelectionPage'
import YearSelectionPage from './pages/YearSelectionPage'
import ProcessingPage from './pages/ProcessingPage'
import DashboardPage from './pages/DashboardPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/map-selection" element={<MapSelectionPage />} />
        <Route path="/year-selection" element={<YearSelectionPage />} />
        <Route path="/processing" element={<ProcessingPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App