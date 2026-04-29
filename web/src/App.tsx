import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Menu } from 'lucide-react'
import { Sidebar } from './components/Sidebar'
import Strategy  from './pages/Strategy'
import Signals   from './pages/Signals'
import Portfolio from './pages/Portfolio'
import Settings  from './pages/Settings'

export default function App() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-ivory flex font-sans">

        {/* Overlay mobile */}
        {menuOpen && (
          <div
            className="fixed inset-0 bg-black/50 z-20 md:hidden"
            onClick={() => setMenuOpen(false)}
          />
        )}

        <Sidebar open={menuOpen} onClose={() => setMenuOpen(false)} />

        <main className="flex-1 min-w-0 md:ml-56 flex flex-col">
          {/* Header mobile */}
          <div className="md:hidden sticky top-0 z-10 flex items-center justify-between px-4 py-3 bg-graphite border-b border-white/5">
            <div className="text-white font-semibold text-sm">PEA Radar</div>
            <button onClick={() => setMenuOpen(true)} className="text-white/70 hover:text-white p-1">
              <Menu size={20} />
            </button>
          </div>

          <div className="p-4 md:p-8 flex-1">
            <Routes>
              <Route path="/"          element={<Strategy />}  />
              <Route path="/signals"   element={<Signals />}   />
              <Route path="/portfolio" element={<Portfolio />} />
              <Route path="/settings"  element={<Settings />}  />
            </Routes>
          </div>
        </main>

      </div>
    </BrowserRouter>
  )
}
