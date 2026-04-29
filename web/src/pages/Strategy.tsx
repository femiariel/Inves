import { useState } from 'react'
import {
  LineChart, Line, XAxis, YAxis, Tooltip,
  ResponsiveContainer, CartesianGrid, Legend,
} from 'recharts'
import { RefreshCw, ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react'
import { api } from '../api/client'
import { useApi } from '../hooks/useApi'
import { KpiCard } from '../components/KpiCard'
import { PageLoader } from '../components/Spinner'
import type { BacktestResult } from '../types'

const fmt = (n: number, dec = 2) =>
  n.toLocaleString('fr-FR', { minimumFractionDigits: dec, maximumFractionDigits: dec })

const pct = (n: number) => `${n >= 0 ? '+' : ''}${(n * 100).toFixed(1)} %`

const sleeveColor: Record<string, string> = {
  core:       '#156B49',
  aggressive: '#3A8C62',
  cash:       '#CBD5C0',
}

function AllocationBar({ lines }: { lines: Array<{ ticker: string; sleeve: string; weight: number; name: string }> }) {
  return (
    <div className="space-y-3">
      <div className="flex rounded-full overflow-hidden h-2.5">
        {lines.map((l) => (
          <div
            key={l.ticker}
            style={{ width: `${l.weight * 100}%`, backgroundColor: sleeveColor[l.sleeve] ?? '#CBD5C0' }}
            title={`${l.name} · ${(l.weight * 100).toFixed(1)} %`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-3">
        {lines.map((l) => (
          <div key={l.ticker} className="flex items-center gap-1.5 text-xs text-graphite-muted">
            <span
              className="w-2 h-2 rounded-full inline-block"
              style={{ backgroundColor: sleeveColor[l.sleeve] ?? '#CBD5C0' }}
            />
            {l.ticker} {(l.weight * 100).toFixed(0)} %
          </div>
        ))}
      </div>
    </div>
  )
}

function ActionIcon({ action }: { action: string }) {
  if (action === 'buy')  return <ArrowUpRight  size={14} className="text-forest" />
  if (action === 'sell') return <ArrowDownRight size={14} className="text-danger" />
  return <Minus size={14} className="text-graphite-subtle" />
}

export default function Strategy() {
  const { data, loading, error } = useApi(() => api.proposal())
  const [backtest, setBacktest] = useState<BacktestResult | null>(null)
  const [btLoading, setBtLoading] = useState(false)

  const runBacktest = async () => {
    setBtLoading(true)
    try { setBacktest(await api.backtest()) }
    catch (e) { console.error(e) }
    finally { setBtLoading(false) }
  }

  if (loading) return <PageLoader label="Calcul de la stratégie…" />
  if (error)   return <div className="text-danger p-6">{error}</div>
  if (!data)   return null

  const { proposal, orders } = data
  const visibleOrders = orders.filter(o => o.action !== 'hold')

  // Backtest chart data
  const chartData = backtest
    ? backtest.equity_curve.map((p, i) => ({
        date:       p.date,
        strategie:  p.value,
        benchmark:  backtest.benchmark_curve[i]?.value ?? null,
      }))
    : []

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-ink">Stratégie 80/20</h1>
        <p className="text-sm text-graphite-muted mt-0.5">{proposal.rationale}</p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
        <KpiCard
          label="Capital"
          value={`${fmt(proposal.capital, 0)} €`}
        />
        <KpiCard
          label="Rendement attendu"
          value={`${(proposal.expected_return * 100).toFixed(1)} %`}
          sub="estimation annuelle"
          trend="up"
        />
        <KpiCard
          label="Volatilité"
          value={`${(proposal.expected_vol * 100).toFixed(1)} %`}
          sub="annualisée"
        />
        <KpiCard
          label="Sharpe"
          value={proposal.expected_sharpe.toFixed(2)}
          sub={`${proposal.n_satellites} satellite${proposal.n_satellites > 1 ? 's' : ''} actif${proposal.n_satellites > 1 ? 's' : ''}`}
          trend={proposal.expected_sharpe >= 1 ? 'up' : 'neutral'}
        />
      </div>

      {/* Allocation */}
      <div className="bg-ivory-light rounded-xl border border-black/5 p-6">
        <h2 className="text-xs font-semibold uppercase tracking-widest text-graphite-muted mb-5">
          Allocation cible
        </h2>
        <AllocationBar lines={proposal.lines} />

        <div className="mt-5 divide-y divide-black/5">
          {proposal.lines.map((line) => (
            <div key={line.ticker} className="flex items-center justify-between py-3">
              <div className="flex items-center gap-3 min-w-0">
                <span
                  className="w-1.5 h-8 rounded-full flex-shrink-0"
                  style={{ backgroundColor: sleeveColor[line.sleeve] ?? '#CBD5C0' }}
                />
                <div className="min-w-0">
                  <div className="text-sm font-semibold text-ink">{line.ticker}</div>
                  <div className="text-xs text-graphite-muted truncate">{line.name}</div>
                </div>
              </div>
              <div className="text-right flex-shrink-0 ml-4">
                <div className="text-sm font-semibold text-ink tabular-nums">
                  {(line.weight * 100).toFixed(0)} %
                </div>
                <div className="text-xs text-graphite-subtle tabular-nums">
                  {fmt(line.value, 0)} €
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Rebalance orders */}
      {visibleOrders.length > 0 && (
        <div className="bg-ivory-light rounded-xl border border-black/5 p-6">
          <h2 className="text-xs font-semibold uppercase tracking-widest text-graphite-muted mb-4">
            Ordres de rééquilibrage
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-[11px] text-graphite-subtle uppercase tracking-wider border-b border-black/5">
                  <th className="pb-2 pr-4">Action</th>
                  <th className="pb-2 pr-4">Ticker</th>
                  <th className="pb-2 pr-4 text-right">Actuel</th>
                  <th className="pb-2 pr-4 text-right">Cible</th>
                  <th className="pb-2 text-right">Δ valeur</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-black/5">
                {visibleOrders.map((o) => (
                  <tr key={o.ticker} className="hover:bg-black/2">
                    <td className="py-2.5 pr-4">
                      <div className="flex items-center gap-1.5">
                        <ActionIcon action={o.action} />
                        <span className={`text-xs font-semibold uppercase ${
                          o.action === 'buy' ? 'text-forest' : 'text-danger'
                        }`}>{o.action}</span>
                      </div>
                    </td>
                    <td className="py-2.5 pr-4 font-medium text-ink">{o.ticker}</td>
                    <td className="py-2.5 pr-4 text-right text-graphite-muted tabular-nums">
                      {(o.current_weight * 100).toFixed(1)} %
                    </td>
                    <td className="py-2.5 pr-4 text-right text-graphite-muted tabular-nums">
                      {(o.target_weight * 100).toFixed(1)} %
                    </td>
                    <td className={`py-2.5 text-right font-medium tabular-nums ${
                      o.delta_value >= 0 ? 'text-forest' : 'text-danger'
                    }`}>
                      {o.delta_value >= 0 ? '+' : ''}{fmt(o.delta_value, 0)} €
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Backtest */}
      <div className="bg-ivory-light rounded-xl border border-black/5 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xs font-semibold uppercase tracking-widest text-graphite-muted">
            Backtest historique
          </h2>
          <button
            onClick={runBacktest}
            disabled={btLoading}
            className="flex items-center gap-2 text-xs font-medium px-3 py-1.5 rounded-lg bg-forest text-white hover:bg-forest-dark disabled:opacity-50 transition-colors"
          >
            <RefreshCw size={13} className={btLoading ? 'animate-spin' : ''} />
            {btLoading ? 'Calcul…' : 'Lancer'}
          </button>
        </div>

        {backtest ? (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
              <div>
                <div className="text-[11px] text-graphite-subtle uppercase tracking-wider">CAGR stratégie</div>
                <div className="text-lg font-semibold text-forest mt-1">{pct(backtest.cagr)}</div>
                <div className="text-xs text-graphite-subtle">vs {pct(backtest.benchmark_cagr)} bench</div>
              </div>
              <div>
                <div className="text-[11px] text-graphite-subtle uppercase tracking-wider">Max drawdown</div>
                <div className="text-lg font-semibold text-danger mt-1">{pct(backtest.max_drawdown)}</div>
                <div className="text-xs text-graphite-subtle">vs {pct(backtest.benchmark_max_dd)} bench</div>
              </div>
              <div>
                <div className="text-[11px] text-graphite-subtle uppercase tracking-wider">Sharpe</div>
                <div className="text-lg font-semibold text-ink mt-1">{backtest.sharpe.toFixed(2)}</div>
                <div className="text-xs text-graphite-subtle">α = {pct(backtest.alpha)}</div>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E8EDE9" />
                <XAxis
                  dataKey="date"
                  tick={{ fontSize: 10, fill: '#8BA898' }}
                  tickFormatter={d => d.slice(0, 7)}
                  interval="preserveStartEnd"
                />
                <YAxis
                  tick={{ fontSize: 10, fill: '#8BA898' }}
                  tickFormatter={v => `${(v / 1000).toFixed(0)}k`}
                  width={40}
                />
                <Tooltip
                  formatter={(v: number, name: string) => [`${fmt(v, 0)} €`, name]}
                  labelStyle={{ fontSize: 11, color: '#17201A' }}
                  contentStyle={{ border: '1px solid #E8EDE9', borderRadius: 8, fontSize: 12 }}
                />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Line dataKey="strategie" name="Stratégie 80/20" stroke="#156B49" dot={false} strokeWidth={2} />
                <Line dataKey="benchmark" name="Benchmark équipondéré" stroke="#BD6E1B" dot={false} strokeWidth={1.5} strokeDasharray="5 3" />
              </LineChart>
            </ResponsiveContainer>
          </>
        ) : (
          <div className="h-36 flex items-center justify-center text-sm text-graphite-subtle">
            Cliquer sur "Lancer" pour calculer le backtest sur l'historique disponible.
          </div>
        )}
      </div>
    </div>
  )
}
