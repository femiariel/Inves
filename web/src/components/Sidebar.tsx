import { NavLink } from 'react-router-dom'
import { TrendingUp, BarChart2, Wallet, Settings } from 'lucide-react'

const links = [
  { to: '/',          icon: TrendingUp, label: 'Stratégie'    },
  { to: '/signals',   icon: BarChart2,  label: 'Signaux ETF'  },
  { to: '/portfolio', icon: Wallet,     label: 'Portefeuille' },
  { to: '/settings',  icon: Settings,   label: 'Réglages'     },
]

export function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 w-56 bg-graphite flex flex-col z-10">
      {/* Logo */}
      <div className="px-6 pt-8 pb-6 border-b border-white/5">
        <div className="text-xs font-semibold tracking-[0.2em] text-graphite-subtle uppercase mb-1">
          Alloc
        </div>
        <div className="text-white text-lg font-semibold leading-tight">
          PEA Radar
        </div>
        <div className="text-graphite-subtle text-xs mt-1">111 ETF · Euronext Paris</div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 space-y-0.5">
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
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
        Stratégie 80/20 · momentum
      </div>
    </aside>
  )
}
