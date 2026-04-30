import { useEffect, useMemo, useState } from 'react'
import { Plus, Trash2 } from 'lucide-react'
import { api } from '../api/client'
import { useApi } from '../hooks/useApi'
import { PageLoader } from '../components/Spinner'
import type { ETFMeta } from '../types'

type ExposureMap = Record<string, number>

interface AllocationLine {
  id: number
  ticker: string
  weight: string
}

interface Profile {
  regions: ExposureMap
  sectors: ExposureMap
  styles: ExposureMap
  currencies: ExposureMap
  footprint: string
}

const defaults: AllocationLine[] = [
  { id: 1, ticker: 'WPEA.PA', weight: '80' },
  { id: 2, ticker: 'PE500.PA', weight: '20' },
]

const fmt = (n: number) => `${n.toFixed(1)} %`

const optionLabel = (etf?: ETFMeta) => etf ? `${etf.ticker} - ${etf.name}` : ''
const searchableText = (etf: ETFMeta) => `${etf.ticker} ${etf.name} ${etf.category}`.toLowerCase()

function emptyProfile(): Profile {
  return {
    regions: { 'Non classé': 1 },
    sectors: { 'Non classé': 1 },
    styles: { 'Non classé': 1 },
    currencies: { Mixte: 1 },
    footprint: 'unknown',
  }
}

function addWeighted(target: ExposureMap, source: ExposureMap, weight: number) {
  Object.entries(source).forEach(([key, value]) => {
    target[key] = (target[key] ?? 0) + value * weight
  })
}

function clean(map: ExposureMap): Array<[string, number]> {
  return Object.entries(map)
    .filter(([, v]) => v > 0.005)
    .sort((a, b) => b[1] - a[1])
}

function bars(map: ExposureMap) {
  const rows = clean(map)
  return (
    <div className="space-y-2.5">
      {rows.map(([label, value]) => (
        <div key={label} className="space-y-1">
          <div className="flex justify-between gap-3 text-xs">
            <span className="text-ink font-medium truncate">{label}</span>
            <span className="text-graphite-muted tabular-nums">{fmt(value * 100)}</span>
          </div>
          <div className="h-2 rounded-full bg-black/5 overflow-hidden">
            <div
              className="h-full rounded-full bg-forest"
              style={{ width: `${Math.min(100, value * 100)}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  )
}

function exposureProfile(etf?: ETFMeta): Profile {
  if (!etf) return emptyProfile()

  const text = `${etf.ticker} ${etf.name} ${etf.category}`.toLowerCase()
  const category = etf.category.toLowerCase()

  const has = (...terms: string[]) => terms.some(t => text.includes(t))

  const profile: Profile = {
    regions: { 'Monde développé': 1 },
    sectors: { Diversifié: 1 },
    styles: { Large: 1 },
    currencies: { USD: 0.65, EUR: 0.20, JPY: 0.06, GBP: 0.04, Autres: 0.05 },
    footprint: 'world',
  }

  if (has('acwi', 'all country')) {
    profile.regions = { USA: 0.62, Europe: 0.15, Japon: 0.05, Emergents: 0.11, Autres: 0.07 }
    profile.footprint = 'acwi'
  } else if (category.includes('monde') || has('msci world', 'world')) {
    profile.regions = { USA: 0.72, Europe: 0.15, Japon: 0.06, Autres: 0.07 }
    profile.footprint = 'world'
  }

  if (category.includes('états-unis') || has('s&p 500', 'sp 500', 'msci usa', 'north america', 'russell 2000')) {
    profile.regions = { USA: 1 }
    profile.currencies = { USD: 1 }
    profile.footprint = has('russell 2000') ? 'usa_small' : 'usa_large'
  }
  if (category.includes('tech') || has('nasdaq')) {
    profile.regions = { USA: 1 }
    profile.sectors = { Technologie: 0.75, Communication: 0.15, Consommation: 0.10 }
    profile.styles = { Croissance: 0.85, Large: 0.15 }
    profile.currencies = { USD: 1 }
    profile.footprint = 'usa_growth_tech'
  }
  if (category.includes('europe') || has('stoxx europe', 'euro stoxx', 'eurozone')) {
    profile.regions = { Europe: 1 }
    profile.currencies = { EUR: 0.75, GBP: 0.15, CHF: 0.10 }
    profile.footprint = 'europe'
  }
  if (category.includes('france') || has('cac 40')) {
    profile.regions = { France: 1 }
    profile.currencies = { EUR: 1 }
    profile.footprint = 'france'
  }
  if (category.includes('allemagne') || has('dax')) {
    profile.regions = { Allemagne: 1 }
    profile.currencies = { EUR: 1 }
    profile.footprint = 'germany'
  }
  if (category.includes('royaume-uni') || has('ftse 100', 'uk')) {
    profile.regions = { 'Royaume-Uni': 1 }
    profile.currencies = { GBP: 1 }
    profile.footprint = 'uk'
  }
  if (category.includes('japon') || has('japan')) {
    profile.regions = { Japon: 1 }
    profile.currencies = { JPY: 1 }
    profile.footprint = 'japan'
  }
  if (category.includes('émergents') || has('emerging', 'em ', 'msci em')) {
    profile.regions = { Emergents: 1 }
    profile.currencies = { USD: 0.45, CNY: 0.25, INR: 0.10, TWD: 0.10, Autres: 0.10 }
    profile.footprint = 'emerging'
  }
  if (category.includes('asie')) {
    profile.regions = { 'Asie Pacifique': 1 }
    profile.currencies = { USD: 0.35, JPY: 0.25, CNY: 0.20, Autres: 0.20 }
    profile.footprint = 'asia'
  }

  if (has('technology', 'information technology', 'semiconductor', 'digital', 'ai ')) {
    profile.sectors = { Technologie: 0.85, Communication: 0.10, Autres: 0.05 }
    profile.styles = { Croissance: 0.75, Large: 0.25 }
    profile.footprint = profile.footprint.includes('usa') ? 'usa_growth_tech' : `${profile.footprint}_tech`
  } else if (has('health', 'health care')) {
    profile.sectors = { Santé: 0.90, Autres: 0.10 }
    profile.footprint = `${profile.footprint}_health`
  } else if (has('financial', 'banks', 'bank')) {
    profile.sectors = { Finance: 0.90, Autres: 0.10 }
    profile.footprint = `${profile.footprint}_financials`
  } else if (has('energy', 'oil', 'natural gas', 'clean energy')) {
    profile.sectors = { Energie: 0.90, Autres: 0.10 }
    profile.footprint = `${profile.footprint}_energy`
  } else if (has('real estate', 'property', 'epra', 'immobilier')) {
    profile.sectors = { Immobilier: 0.90, Autres: 0.10 }
    profile.footprint = `${profile.footprint}_realestate`
  } else if (category.includes('obligations') || has('bond', 'govt', 'yield')) {
    profile.sectors = { Obligations: 1 }
    profile.styles = { Défensif: 1 }
    profile.currencies = { EUR: 0.75, USD: 0.25 }
    profile.footprint = 'bonds'
  } else if (category.includes('monétaire') || has('cash', 'overnight')) {
    profile.sectors = { Monétaire: 1 }
    profile.styles = { Défensif: 1 }
    profile.currencies = { EUR: 1 }
    profile.footprint = 'cash'
  }

  if (has('small cap', 'small')) profile.styles = { 'Small cap': 0.85, Large: 0.15 }
  if (has('value')) profile.styles = { Value: 0.80, Large: 0.20 }
  if (has('quality')) profile.styles = { Quality: 0.80, Large: 0.20 }
  if (has('momentum')) profile.styles = { Momentum: 0.80, Large: 0.20 }
  if (has('dividend', 'high dividend')) profile.styles = { Dividendes: 0.80, Large: 0.20 }
  if (has('esg', 'sri', 'climate', 'pab', 'paris aligned')) {
    profile.styles = { ...profile.styles, ESG: 0.35 }
  }

  return profile
}

function redundancyAlerts(rows: Array<{ etf: ETFMeta; weight: number; profile: Profile }>) {
  const alerts: string[] = []
  const byFootprint = new Map<string, Array<{ ticker: string; weight: number }>>()

  rows.forEach(row => {
    const list = byFootprint.get(row.profile.footprint) ?? []
    list.push({ ticker: row.etf.ticker, weight: row.weight })
    byFootprint.set(row.profile.footprint, list)
  })

  byFootprint.forEach((list, footprint) => {
    const total = list.reduce((sum, item) => sum + item.weight, 0)
    if (list.length > 1 && total >= 0.20 && !['unknown', 'cash'].includes(footprint)) {
      alerts.push(`Doublon probable : ${list.map(i => i.ticker).join(' + ')} ciblent une exposition proche (${fmt(total * 100)}).`)
    }
  })

  const world = rows.filter(r => ['world', 'acwi'].includes(r.profile.footprint)).reduce((s, r) => s + r.weight, 0)
  const usa = rows.filter(r => r.profile.footprint.startsWith('usa')).reduce((s, r) => s + r.weight, 0)
  const tech = rows.filter(r => r.profile.footprint.includes('tech')).reduce((s, r) => s + r.weight, 0)

  if (world > 0.25 && usa > 0.10) alerts.push(`MSCI World + USA : le S&P 500 renforce surtout une exposition USA déjà présente dans le World.`)
  if (tech > 0.20) alerts.push(`Concentration croissance/tech élevée : Nasdaq, semiconducteurs ou tech mondiale peuvent se recouvrir fortement.`)

  return alerts
}

function FundPicker({
  etfs,
  value,
  onChange,
}: {
  etfs: ETFMeta[]
  value: string
  onChange: (ticker: string) => void
}) {
  const selected = etfs.find(etf => etf.ticker === value)
  const [query, setQuery] = useState(optionLabel(selected))
  const [open, setOpen] = useState(false)

  useEffect(() => {
    setQuery(optionLabel(selected))
  }, [selected?.ticker])

  const filtered = useMemo(() => {
    const terms = query.toLowerCase().trim().split(/\s+/).filter(Boolean)
    const matches = terms.length === 0
      ? etfs
      : etfs.filter(etf => terms.every(term => searchableText(etf).includes(term)))
    return matches.slice(0, 10)
  }, [etfs, query])

  const choose = (etf: ETFMeta) => {
    onChange(etf.ticker)
    setQuery(optionLabel(etf))
    setOpen(false)
  }

  return (
    <div className="relative min-w-0">
      <input
        value={query}
        onFocus={e => {
          e.currentTarget.select()
          setOpen(true)
        }}
        onBlur={() => window.setTimeout(() => {
          setOpen(false)
          setQuery(optionLabel(selected))
        }, 120)}
        onChange={e => {
          setQuery(e.target.value)
          setOpen(true)
        }}
        onKeyDown={e => {
          if (e.key === 'Enter' && filtered[0]) {
            e.preventDefault()
            choose(filtered[0])
          }
          if (e.key === 'Escape') {
            setOpen(false)
            setQuery(optionLabel(selected))
          }
        }}
        placeholder="Rechercher ticker ou nom..."
        className="w-full min-w-0 px-3 py-2 rounded-lg border border-black/10 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-forest/30"
      />

      {open && (
        <div className="absolute left-0 right-0 top-[calc(100%+4px)] z-20 max-h-72 overflow-y-auto rounded-lg border border-black/10 bg-white shadow-lg">
          {filtered.length > 0 ? filtered.map(etf => (
            <button
              key={etf.ticker}
              type="button"
              onMouseDown={e => {
                e.preventDefault()
                choose(etf)
              }}
              className="w-full px-3 py-2 text-left hover:bg-forest/8 focus:bg-forest/8 focus:outline-none"
            >
              <div className="text-sm font-medium text-ink">{etf.ticker}</div>
              <div className="text-xs text-graphite-muted truncate">{etf.name}</div>
              <div className="text-[11px] text-graphite-subtle">{etf.category}</div>
            </button>
          )) : (
            <div className="px-3 py-3 text-sm text-graphite-muted">Aucun ETF trouvé</div>
          )}
        </div>
      )}
    </div>
  )
}

export default function Allocation() {
  const { data: universe, loading, error } = useApi(() => api.universe())
  const [lines, setLines] = useState<AllocationLine[]>(defaults)

  const byTicker = useMemo(
    () => Object.fromEntries((universe ?? []).map(etf => [etf.ticker, etf])),
    [universe],
  )

  const selected = useMemo(() => {
    const parsed = lines
      .map(line => ({ ...line, etf: byTicker[line.ticker], rawWeight: Number(line.weight) || 0 }))
      .filter(line => line.etf && line.rawWeight > 0)
    const total = parsed.reduce((sum, line) => sum + line.rawWeight, 0)
    return parsed.map(line => ({
      etf: line.etf,
      weight: total > 0 ? line.rawWeight / total : 0,
      rawWeight: line.rawWeight,
      profile: exposureProfile(line.etf),
    }))
  }, [lines, byTicker])

  const exposure = useMemo(() => {
    const regions: ExposureMap = {}
    const sectors: ExposureMap = {}
    const styles: ExposureMap = {}
    const currencies: ExposureMap = {}
    selected.forEach(row => {
      addWeighted(regions, row.profile.regions, row.weight)
      addWeighted(sectors, row.profile.sectors, row.weight)
      addWeighted(styles, row.profile.styles, row.weight)
      addWeighted(currencies, row.profile.currencies, row.weight)
    })
    return { regions, sectors, styles, currencies }
  }, [selected])

  const alerts = useMemo(() => redundancyAlerts(selected), [selected])
  const totalRaw = selected.reduce((sum, line) => sum + line.rawWeight, 0)

  const addLine = () => {
    const fallback = universe?.[0]?.ticker ?? ''
    setLines(current => [...current, { id: Date.now(), ticker: fallback, weight: '10' }])
  }

  const updateLine = (id: number, patch: Partial<AllocationLine>) => {
    setLines(current => current.map(line => line.id === id ? { ...line, ...patch } : line))
  }

  const removeLine = (id: number) => {
    setLines(current => current.length > 1 ? current.filter(line => line.id !== id) : current)
  }

  if (loading) return <PageLoader label="Chargement de l’univers ETF…" />
  if (error) return <div className="text-danger p-6">{error}</div>

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-ink">Allocation</h1>
        <p className="text-sm text-graphite-muted mt-0.5">
          {selected.length} fonds · total saisi {fmt(totalRaw)} · estimation par profils ETF
        </p>
      </div>

      <div className="bg-ivory-light rounded-xl border border-black/5 p-5 space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-semibold uppercase tracking-widest text-graphite-muted">Fonds</h2>
          <button
            onClick={addLine}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-forest text-white text-xs font-medium hover:bg-forest-dark transition-colors"
          >
            <Plus size={14} />
            Ajouter
          </button>
        </div>

        <div className="space-y-2">
          {lines.map(line => (
            <div key={line.id} className="grid grid-cols-[minmax(0,1fr)_96px_32px] gap-2 items-center">
              <FundPicker
                etfs={universe ?? []}
                value={line.ticker}
                onChange={ticker => updateLine(line.id, { ticker })}
              />
              <input
                type="number"
                min="0"
                step="1"
                value={line.weight}
                onChange={e => updateLine(line.id, { weight: e.target.value })}
                className="px-3 py-2 rounded-lg border border-black/10 bg-white text-sm text-right tabular-nums focus:outline-none focus:ring-2 focus:ring-forest/30"
              />
              <button
                onClick={() => removeLine(line.id)}
                className="p-2 rounded-lg text-graphite-subtle hover:text-danger hover:bg-danger/5"
              >
                <Trash2 size={15} />
              </button>
            </div>
          ))}
        </div>
      </div>

      {alerts.length > 0 && (
        <div className="bg-amber/10 border border-amber/20 rounded-xl p-4 space-y-2">
          <h2 className="text-xs font-semibold uppercase tracking-widest text-amber">Redondances</h2>
          {alerts.map(alert => (
            <p key={alert} className="text-sm text-ink">{alert}</p>
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <section className="bg-ivory-light rounded-xl border border-black/5 p-5">
          <h2 className="text-xs font-semibold uppercase tracking-widest text-graphite-muted mb-4">Régions</h2>
          {bars(exposure.regions)}
        </section>
        <section className="bg-ivory-light rounded-xl border border-black/5 p-5">
          <h2 className="text-xs font-semibold uppercase tracking-widest text-graphite-muted mb-4">Secteurs</h2>
          {bars(exposure.sectors)}
        </section>
        <section className="bg-ivory-light rounded-xl border border-black/5 p-5">
          <h2 className="text-xs font-semibold uppercase tracking-widest text-graphite-muted mb-4">Styles</h2>
          {bars(exposure.styles)}
        </section>
        <section className="bg-ivory-light rounded-xl border border-black/5 p-5">
          <h2 className="text-xs font-semibold uppercase tracking-widest text-graphite-muted mb-4">Devises</h2>
          {bars(exposure.currencies)}
        </section>
      </div>
    </div>
  )
}
