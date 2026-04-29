import { useState } from 'react'
import { Plus, Pencil, Trash2, X, Check } from 'lucide-react'
import { api } from '../api/client'
import { useApi } from '../hooks/useApi'
import { KpiCard } from '../components/KpiCard'
import { PageLoader } from '../components/Spinner'
import type { ETFMeta, Holding } from '../types'

const fmt  = (n: number, dec = 2) =>
  n.toLocaleString('fr-FR', { minimumFractionDigits: dec, maximumFractionDigits: dec })

const pctFmt = (n: number) =>
  `${n >= 0 ? '+' : ''}${(n * 100).toFixed(2)} %`

interface FormState {
  ticker: string
  quantity: string
  avg_cost: string
}

const emptyForm: FormState = { ticker: '', quantity: '', avg_cost: '' }

export default function Portfolio() {
  const { data: holdings, loading, error, refetch } = useApi(() => api.holdings())
  const { data: universe } = useApi(() => api.universe())

  const [form, setForm]       = useState<FormState>(emptyForm)
  const [editing, setEditing] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving]   = useState(false)

  const metaByTicker = Object.fromEntries(
    (universe ?? []).map((e: ETFMeta) => [e.ticker, e])
  )

  const totalMV  = (holdings ?? []).reduce((s, h) => s + h.market_value, 0)
  const totalCB  = (holdings ?? []).reduce((s, h) => s + h.cost_basis, 0)
  const totalPnl = totalMV - totalCB

  const openAdd = () => { setForm(emptyForm); setEditing(null); setShowForm(true) }

  const openEdit = (h: Holding) => {
    setForm({ ticker: h.ticker, quantity: String(h.quantity), avg_cost: String(h.avg_cost) })
    setEditing(h.ticker)
    setShowForm(true)
  }

  const onTickerChange = (ticker: string) => {
    const meta = metaByTicker[ticker]
    setForm(f => ({ ...f, ticker, avg_cost: meta ? '' : f.avg_cost }))
  }

  const save = async () => {
    const q  = parseFloat(form.quantity)
    const ac = parseFloat(form.avg_cost)
    if (!form.ticker || isNaN(q) || isNaN(ac) || q <= 0 || ac <= 0) return
    setSaving(true)
    try {
      await api.holdings.upsert({ ticker: form.ticker, quantity: q, avg_cost: ac })
      await refetch()
      setShowForm(false)
    } finally { setSaving(false) }
  }

  const remove = async (ticker: string) => {
    await api.holdings.delete(ticker)
    await refetch()
  }

  if (loading) return <PageLoader label="Chargement du portefeuille…" />
  if (error)   return <div className="text-danger p-6">{error}</div>

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-xl font-semibold text-ink">Portefeuille</h1>
          <p className="text-sm text-graphite-muted mt-0.5">
            {holdings?.length ?? 0} position{(holdings?.length ?? 0) > 1 ? 's' : ''}
          </p>
        </div>
        <button
          onClick={openAdd}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-forest text-white text-sm font-medium hover:bg-forest-dark transition-colors"
        >
          <Plus size={15} /> Ajouter
        </button>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-3 gap-4">
        <KpiCard
          label="Valeur marché"
          value={`${fmt(totalMV, 0)} €`}
        />
        <KpiCard
          label="P&L total"
          value={`${fmt(totalPnl, 0)} €`}
          sub={totalCB > 0 ? pctFmt(totalPnl / totalCB) : undefined}
          trend={totalPnl >= 0 ? 'up' : 'down'}
        />
        <KpiCard
          label="Prix de revient"
          value={`${fmt(totalCB, 0)} €`}
        />
      </div>

      {/* Add / Edit form */}
      {showForm && (
        <div className="bg-ivory-light rounded-xl border border-forest/20 p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-ink">
              {editing ? `Modifier ${editing}` : 'Nouvelle position'}
            </h3>
            <button onClick={() => setShowForm(false)} className="text-graphite-muted hover:text-ink">
              <X size={16} />
            </button>
          </div>
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-xs text-graphite-muted mb-1">Ticker</label>
              {editing ? (
                <div className="px-3 py-2 rounded-lg border border-black/10 bg-ivory text-sm font-medium text-ink">
                  {editing}
                </div>
              ) : (
                <select
                  value={form.ticker}
                  onChange={e => onTickerChange(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-black/10 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-forest/30"
                >
                  <option value="">Choisir…</option>
                  {(universe ?? []).map((e: ETFMeta) => (
                    <option key={e.ticker} value={e.ticker}>{e.ticker} — {e.name}</option>
                  ))}
                </select>
              )}
            </div>
            <div>
              <label className="block text-xs text-graphite-muted mb-1">Quantité (parts)</label>
              <input
                type="number"
                value={form.quantity}
                onChange={e => setForm(f => ({ ...f, quantity: e.target.value }))}
                placeholder="ex. 12"
                min="0.001"
                step="0.001"
                className="w-full px-3 py-2 rounded-lg border border-black/10 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-forest/30"
              />
            </div>
            <div>
              <label className="block text-xs text-graphite-muted mb-1">Prix de revient (€/part)</label>
              <input
                type="number"
                value={form.avg_cost}
                onChange={e => setForm(f => ({ ...f, avg_cost: e.target.value }))}
                placeholder="ex. 285.50"
                min="0.01"
                step="0.01"
                className="w-full px-3 py-2 rounded-lg border border-black/10 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-forest/30"
              />
            </div>
          </div>
          <div className="mt-4 flex justify-end">
            <button
              onClick={save}
              disabled={saving}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-forest text-white text-sm font-medium hover:bg-forest-dark disabled:opacity-50 transition-colors"
            >
              <Check size={14} />
              {saving ? 'Enregistrement…' : 'Enregistrer'}
            </button>
          </div>
        </div>
      )}

      {/* Holdings table */}
      {(holdings ?? []).length === 0 ? (
        <div className="bg-ivory-light rounded-xl border border-black/5 p-12 text-center text-sm text-graphite-subtle">
          Aucune position. Cliquer sur "Ajouter" pour commencer.
        </div>
      ) : (
        <div className="bg-ivory-light rounded-xl border border-black/5 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="border-b border-black/5">
                <tr className="text-[11px] font-semibold uppercase tracking-wider text-graphite-subtle">
                  <th className="text-left py-3 px-5 pr-4">ETF</th>
                  <th className="py-3 pr-4 text-right">Quantité</th>
                  <th className="py-3 pr-4 text-right">Prix actuel</th>
                  <th className="py-3 pr-4 text-right">Val. marché</th>
                  <th className="py-3 pr-4 text-right">P&L</th>
                  <th className="py-3 pr-4 text-right">Alloc.</th>
                  <th className="py-3 pr-5 text-right">Var. jour</th>
                  <th className="py-3 pr-5" />
                </tr>
              </thead>
              <tbody className="divide-y divide-black/4">
                {(holdings ?? []).map((h) => (
                  <tr key={h.ticker} className="hover:bg-black/[0.02]">
                    <td className="py-3 px-5 pr-4">
                      <div className="font-semibold text-ink">{h.ticker}</div>
                      <div className="text-xs text-graphite-subtle truncate max-w-[180px]">{h.name}</div>
                    </td>
                    <td className="py-3 pr-4 text-right tabular-nums text-graphite-muted">
                      {h.quantity}
                    </td>
                    <td className="py-3 pr-4 text-right tabular-nums text-graphite-muted">
                      {h.latest_price != null ? `${fmt(h.latest_price)} €` : '—'}
                    </td>
                    <td className="py-3 pr-4 text-right tabular-nums font-medium text-ink">
                      {fmt(h.market_value, 0)} €
                    </td>
                    <td className={`py-3 pr-4 text-right tabular-nums text-xs font-medium ${
                      h.pnl >= 0 ? 'text-forest' : 'text-danger'
                    }`}>
                      {fmt(h.pnl, 0)} €
                      <div className="text-[10px] opacity-75">{pctFmt(h.pnl_pct)}</div>
                    </td>
                    <td className="py-3 pr-4 text-right tabular-nums text-xs text-graphite-muted">
                      {(h.allocation_pct * 100).toFixed(1)} %
                    </td>
                    <td className={`py-3 pr-5 text-right tabular-nums text-xs font-medium ${
                      h.day_change >= 0 ? 'text-forest' : 'text-danger'
                    }`}>
                      {pctFmt(h.day_change)}
                    </td>
                    <td className="py-3 pr-5">
                      <div className="flex items-center justify-end gap-2">
                        <button onClick={() => openEdit(h)} className="text-graphite-subtle hover:text-ink p-1">
                          <Pencil size={14} />
                        </button>
                        <button onClick={() => remove(h.ticker)} className="text-graphite-subtle hover:text-danger p-1">
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
