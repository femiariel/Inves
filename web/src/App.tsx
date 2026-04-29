import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Sidebar } from './components/Sidebar'
import Strategy  from './pages/Strategy'
import Signals   from './pages/Signals'
import Portfolio from './pages/Portfolio'
import Settings  from './pages/Settings'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-ivory flex font-sans">
        <Sidebar />
        <main className="ml-56 flex-1 p-8 min-w-0">
          <Routes>
            <Route path="/"          element={<Strategy />}  />
            <Route path="/signals"   element={<Signals />}   />
            <Route path="/portfolio" element={<Portfolio />} />
            <Route path="/settings"  element={<Settings />}  />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
