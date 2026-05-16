import { NavLink } from 'react-router-dom'
import { TrendingUp, PieChart, Wallet, Settings, X, Layers, Newspaper } from 'lucide-react'

const links = [
  { to: '/',               icon: TrendingUp, label: 'Stratégie'    },
  { to: '/sleeve-a',       icon: Layers,     label: 'Sleeve A'     },
  { to: '/news',           icon: Newspaper,  label: 'Actualités'   },
  { to: '/concentration',  icon: PieChart,   label: 'Concentration' },
  { to: '/portfolio',      icon: Wallet,     label: 'Portefeuille' },
  { to: '/settings',       icon: Settings,   label: 'Réglages'     },
]

interface Props {
  open:    boolean
  onClose: () => void
}

export function Sidebar({ open, onClose }: Props) {
  return (
    <aside className={`
      fixed inset-y-0 left-0 w-56 bg-graphite flex flex-col z-30
      transition-transform duration-200
      ${open ? 'translate-x-0' : '-translate-x-full'}
      md:translate-x-0
    `}>
      {/* Close button — mobile only */}
      <button
        className="md:hidden absolute top-4 right-4 text-white/50 hover:text-white"
        onClick={onClose}
      >
        <X size={18} />
      </button>

      {/* Logo */}
      <div className="px-6 pt-8 pb-6 border-b border-white/5">
        <div className="text-xs font-semibold tracking-[0.2em] text-graphite-subtle uppercase mb-1">
          Alloc
        </div>
        <div className="text-white text-lg font-semibold">PEA Radar</div>
        <div className="text-graphite-subtle text-xs mt-1">Euronext Paris · 80/20</div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-0.5">
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            onClick={onClose}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-forest text-white'
                  : 'text-graphite-subtle hover:text-white hover:bg-white/8'
              }`
            }
          >
            <Icon size={17} strokeWidth={1.75} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-6 py-5 text-graphite-muted text-[11px]">
        Stratégie momentum · factor investing
      </div>
    </aside>
  )
}
