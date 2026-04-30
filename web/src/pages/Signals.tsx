import { useState, useMemo } from 'react'
import { ChevronUp, ChevronDown, ChevronsUpDown } from 'lucide-react'
import { api } from '../api/client'
import { useApi } from '../hooks/useApi'
import { ScoreBadge } from '../components/ScoreBadge'
import { PageLoader } from '../components/Spinner'
import type { Signal, Rec } from '../types'

const pct = (n: number | null) =>
  n == null ? '—' : `${n >= 0 ? '+' : ''}${(n * 100).toFixed(1)}%`

const price = (n: number | null) =>
  n == null ? '—' : `${n.toLocaleString('fr-FR', { maximumFractionDigits: 2 })} €`

type SortKey = 'score' | 'r1M' | 'r3M' | 'r6M' | 'r12_1M' | 'r12M' | 'annual_vol'
type Dir = 'asc' | 'desc'

function SortIcon({ col, active, dir }: { col: string; active: boolean; dir: Dir }) {
  if (!active) return <ChevronsUpDown size={13} className="text-graphite-subtle opacity-50" />
  return dir === 'desc'
    ? <ChevronDown size={13} className="text-forest" />
    : <ChevronUp   size={13} className="text-forest" />
}

export default function Signals() {
  const { data: signals, loading, error } = useApi(() => api.signals())

  const [category, setCategory] = useState('')
  const [rec, setRec]           = useState<Rec | ''>('')
  const [sort, setSort]         = useState<SortKey>('score')
  const [dir, setDir]           = useState<Dir>('desc')
  const [search, setSearch]     = useState('')

  const categories = useMemo(
    () => ['', ...Array.from(new Set((signals ?? []).map(s => s.category)))],
    [signals],
  )

  const filtered = useMemo(() => {
    let rows = signals ?? []
    if (category) rows = rows.filter(s => s.category === category)
    if (rec)      rows = rows.filter(s => s.recommendation === rec)
    if (search)   rows = rows.filter(s =>
      s.ticker.toLowerCase().includes(search.toLowerCase()) ||
      s.name.toLowerCase().includes(search.toLowerCase())
    )
    return [...rows].sort((a, b) => {
      const va = (a[sort] ?? -Infinity) as number
      const vb = (b[sort] ?? -Infinity) as number
      return dir === 'desc' ? vb - va : va - vb
    })
  }, [signals, category, rec, search, sort, dir])

  const toggleSort = (col: SortKey) => {
    if (sort === col) setDir(d => d === 'desc' ? 'asc' : 'desc')
    else { setSort(col); setDir('desc') }
  }

  const Th = ({ col, label }: { col: SortKey; label: string }) => (
    <th
      className="pb-3 pr-4 text-right cursor-pointer select-none hover:text-ink"
      onClick={() => toggleSort(col)}
    >
      <div className="flex items-center justify-end gap-1">
        {label}
        <SortIcon col={col} active={sort === col} dir={dir} />
      </div>
    </th>
  )

  if (loading) return <PageLoader label="Calcul des signaux pour 111 ETF…" />
  if (error)   return <div className="text-danger p-6">{error}</div>

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-xl font-semibold text-ink">Signaux ETF</h1>
        <p className="text-sm text-graphite-muted mt-0.5">
          {filtered.length} / {signals?.length ?? 0} ETF · Euronext Paris
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <input
          type="text"
          placeholder="Rechercher ticker ou nom…"
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="px-3 py-2 rounded-lg border border-black/10 bg-ivory-light text-sm focus:outline-none focus:ring-2 focus:ring-forest/30 w-56"
        />
        <select
          value={category}
          onChange={e => setCategory(e.target.value)}
          className="px-3 py-2 rounded-lg border border-black/10 bg-ivory-light text-sm focus:outline-none focus:ring-2 focus:ring-forest/30"
        >
          <option value="">Toutes catégories</option>
          {categories.filter(Boolean).map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
        <select
          value={rec}
          onChange={e => setRec(e.target.value as Rec | '')}
          className="px-3 py-2 rounded-lg border border-black/10 bg-ivory-light text-sm focus:outline-none focus:ring-2 focus:ring-forest/30"
        >
          <option value="">Toutes recommandations</option>
          <option value="buy">Fort</option>
          <option value="hold">Stable</option>
          <option value="trim">Faible</option>
          <option value="avoid">Éviter</option>
        </select>
      </div>

      {/* Table */}
      <div className="bg-ivory-light rounded-xl border border-black/5 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="border-b border-black/5">
              <tr className="text-[11px] font-semibold uppercase tracking-wider text-graphite-subtle">
                <th className="text-left py-3 px-5 pr-4">ETF</th>
                <th className="pb-3 pr-4 text-left pt-3">Catégorie</th>
                <th className="pb-3 pr-4 text-left pt-3">Signal</th>
                <Th col="score"      label="Score" />
                <Th col="r1M"        label="1M" />
                <Th col="r3M"        label="3M" />
                <Th col="r6M"        label="6M" />
                <Th col="r12_1M"     label="12-1M" />
                <Th col="r12M"       label="12M" />
                <Th col="annual_vol" label="Vol" />
                <th className="pb-3 pr-5 text-right pt-3">Prix</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-black/4">
              {filtered.map((s) => (
                <tr key={s.ticker} className="hover:bg-black/[0.02] transition-colors">
                  <td className="py-3 px-5 pr-4">
                    <div className="font-semibold text-ink">{s.ticker}</div>
                    <div className="text-xs text-graphite-subtle truncate max-w-[180px]">{s.name}</div>
                  </td>
                  <td className="py-3 pr-4 text-xs text-graphite-muted">{s.category}</td>
                  <td className="py-3 pr-4">
                    <ScoreBadge rec={s.recommendation} label={s.rec_label} />
                  </td>
                  <td className="py-3 pr-4 text-right font-semibold tabular-nums text-ink">
                    {s.score.toFixed(1)}
                  </td>
                  <td className={`py-3 pr-4 text-right tabular-nums text-xs ${
                    s.r1M == null ? 'text-graphite-subtle' : s.r1M >= 0 ? 'text-forest' : 'text-danger'
                  }`}>{pct(s.r1M)}</td>
                  <td className={`py-3 pr-4 text-right tabular-nums text-xs ${
                    s.r3M == null ? 'text-graphite-subtle' : s.r3M >= 0 ? 'text-forest' : 'text-danger'
                  }`}>{pct(s.r3M)}</td>
                  <td className={`py-3 pr-4 text-right tabular-nums text-xs ${
                    s.r6M == null ? 'text-graphite-subtle' : s.r6M >= 0 ? 'text-forest' : 'text-danger'
                  }`}>{pct(s.r6M)}</td>
                  <td className={`py-3 pr-4 text-right tabular-nums text-xs font-medium ${
                    s.r12_1M == null ? 'text-graphite-subtle' : s.r12_1M >= 0 ? 'text-forest' : 'text-danger'
                  }`}>{pct(s.r12_1M)}</td>
                  <td className={`py-3 pr-4 text-right tabular-nums text-xs font-medium ${
                    s.r12M == null ? 'text-graphite-subtle' : s.r12M >= 0 ? 'text-forest' : 'text-danger'
                  }`}>{pct(s.r12M)}</td>
                  <td className="py-3 pr-4 text-right tabular-nums text-xs text-graphite-muted">
                    {s.annual_vol ? `${(s.annual_vol * 100).toFixed(1)}%` : '—'}
                  </td>
                  <td className="py-3 pr-5 text-right tabular-nums text-xs text-graphite-muted">
                    {price(s.latest_price)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
