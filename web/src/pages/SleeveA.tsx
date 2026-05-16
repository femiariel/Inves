import { TrendingUp, TrendingDown, Minus, AlertTriangle } from 'lucide-react'
import { api } from '../api/client'
import { useApi } from '../hooks/useApi'
import { PageLoader } from '../components/Spinner'
import type { SleeveAResult, SleeveASignal } from '../types'

// ── Helpers ───────────────────────────────────────────────────────────────────

const pct = (v: number | null) =>
  v == null ? '—' : `${v >= 0 ? '+' : ''}${v.toFixed(1)}%`

// ── Sub-components ────────────────────────────────────────────────────────────

function RegimeChip({ regime }: { regime: string }) {
  if (regime === 'on')
    return (
      <span className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full"
        style={{ color: '#156B49', background: '#156B4918', border: '1px solid #156B4930' }}>
        <span className="w-1.5 h-1.5 rounded-full bg-forest" />
        Régime ON
      </span>
    )
  if (regime === 'off')
    return (
      <span className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full"
        style={{ color: '#BD3A33', background: '#BD3A3318', border: '1px solid #BD3A3330' }}>
        <span className="w-1.5 h-1.5 rounded-full bg-danger" />
        Régime OFF
      </span>
    )
  return (
    <span className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full bg-black/5 text-graphite-muted">
      Données manquantes
    </span>
  )
}

function MomCell({ value }: { value: number | null }) {
  if (value === null) return <span className="text-graphite-subtle">—</span>
  const color = value >= 0 ? 'text-forest' : 'text-danger'
  const Icon = value > 5 ? TrendingUp : value < -5 ? TrendingDown : Minus
  return (
    <div className={`flex items-center justify-end gap-1.5 ${color} tabular-nums`}>
      <Icon size={12} strokeWidth={2} />
      <span className="font-medium text-xs">{pct(value)}</span>
    </div>
  )
}

function RegimeCard({ data }: { data: SleeveAResult }) {
  const { regime, allocation } = data
  const isOn = regime.regime === 'on'
  const isOff = regime.regime === 'off'

  const cardBg = isOn ? '#156B4908' : isOff ? '#BD3A3308' : 'transparent'
  const borderColor = isOn ? '#156B4920' : isOff ? '#BD3A3320' : 'rgba(0,0,0,0.05)'

  return (
    <div className="rounded-xl border p-5 space-y-4"
      style={{ backgroundColor: cardBg, borderColor }}>

      {/* Header row */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div className="flex items-center gap-3">
          <RegimeChip regime={regime.regime} />
          {regime.data_available && (
            <span className="text-sm text-graphite-muted tabular-nums">
              IWDA {regime.price?.toFixed(2)} · SMA200 {regime.sma200?.toFixed(2)}
            </span>
          )}
        </div>
        {regime.data_available && (
          <div className="text-right">
            <div className="text-[10px] uppercase tracking-widest text-graphite-muted mb-0.5">IWDA / SMA200</div>
            <div className={`text-2xl font-bold tabular-nums ${isOn ? 'text-forest' : 'text-danger'}`}
              style={{ color: isOn ? '#156B49' : '#BD3A33' }}>
              {((regime.ratio ?? 1) * 100 - 100).toFixed(1)}%
            </div>
          </div>
        )}
      </div>

      {/* Interpretation */}
      <p className="text-sm text-graphite-muted leading-relaxed">
        {isOn && 'IWDA au-dessus de sa moyenne 200 jours — tendance haussière confirmée. Les deux ETFs les mieux classés en momentum 6M sont actifs.'}
        {isOff && 'IWDA sous sa moyenne 200 jours — régime défensif actif. 100 % XEON (monétaire EUR) jusqu\'au prochain rebalancement mensuel.'}
        {!isOn && !isOff && 'Données IWDA insuffisantes pour évaluer le régime.'}
      </p>

      {/* Allocation cible */}
      <div>
        <div className="text-[10px] uppercase tracking-widest text-graphite-muted mb-2.5">Allocation cible</div>
        <div className="flex gap-3 flex-wrap">
          {allocation.positions.map(pos => (
            <div key={pos.ticker}
              className="flex-1 min-w-[160px] rounded-lg border border-black/5 bg-ivory-light px-4 py-3">
              <div className="flex items-baseline justify-between mb-0.5">
                <span className="font-semibold text-ink text-sm">{pos.ticker}</span>
                <span className="text-lg font-bold text-ink tabular-nums">
                  {(pos.weight * 100).toFixed(0)}%
                </span>
              </div>
              <div className="text-xs text-graphite-muted truncate">{pos.name}</div>
              {pos.mom_6m != null && (
                <div className={`text-xs mt-1.5 font-medium tabular-nums ${pos.mom_6m >= 0 ? 'text-forest' : 'text-danger'}`}
                  style={{ color: pos.mom_6m >= 0 ? '#156B49' : '#BD3A33' }}>
                  6M {pct(pos.mom_6m)}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Correlation */}
        {allocation.corr_pairs.length > 0 && (
          <div className="mt-2.5 flex items-center gap-2 text-xs text-graphite-muted">
            {allocation.corr_pairs.map(p => (
              <span key={`${p.t1}-${p.t2}`}>
                Corrélation {p.t1}/{p.t2} ={' '}
                <span className="font-mono tabular-nums text-ink">{p.corr.toFixed(2)}</span>
              </span>
            ))}
            {allocation.guardrail_applied && (
              <span className="ml-1 text-amber" style={{ color: '#BD6E1B' }}>
                · garde-fou corrélation activé
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

function SignalRow({ sig, rank }: { sig: SleeveASignal; rank: number | null }) {
  const isSelected = rank !== null && rank <= 2

  return (
    <tr className={`hover:bg-black/[0.03] transition-colors ${isSelected ? 'bg-forest/[0.03]' : ''}`}>
      <td className="py-3 px-5 pr-4 w-10">
        {rank != null ? (
          <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-[11px] font-bold ${
            rank === 1
              ? 'text-white'
              : rank === 2
                ? 'text-white'
                : 'text-graphite-muted bg-black/5'
          }`}
          style={rank === 1 ? { background: '#156B49' } : rank === 2 ? { background: '#156B4970' } : {}}>
            {rank}
          </span>
        ) : (
          <span className="text-graphite-subtle text-xs pl-1">—</span>
        )}
      </td>
      <td className="py-3 pr-4">
        <div className="font-semibold text-ink text-sm">{sig.ticker}</div>
      </td>
      <td className="py-3 pr-4">
        <div className="text-xs text-graphite-muted truncate max-w-[220px]">{sig.name}</div>
      </td>
      <td className="py-3 pr-4">
        <span className="text-xs text-graphite-muted">{sig.category}</span>
      </td>
      <td className="py-3 pr-5 text-right">
        {sig.data_available ? (
          <MomCell value={sig.mom_6m} />
        ) : (
          <span className="text-xs text-graphite-subtle">données manquantes</span>
        )}
      </td>
      <td className="py-3 pr-5 text-right tabular-nums text-xs text-graphite-muted">
        {sig.latest_price?.toFixed(2) ?? '—'}
      </td>
    </tr>
  )
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function SleeveA() {
  const { data, loading, error } = useApi(() => api.sleeveA())

  if (loading) return <PageLoader label="Calcul Sleeve A…" />
  if (error)   return <div className="text-danger p-6">{error}</div>
  if (!data)   return null

  const missing = data.data_coverage.total - data.data_coverage.available

  return (
    <div className="space-y-5 max-w-4xl">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-ink flex items-center gap-2">
            <TrendingUp size={18} className="text-forest" style={{ color: '#156B49' }} />
            Sleeve A — Momentum UCITS
          </h1>
          <p className="text-sm text-graphite-muted mt-0.5">
            Cross-sectionnel 6M · Filtre MM200 IWDA · Top 2 avec garde-fou corrélation
          </p>
        </div>
        <div className="text-right text-xs text-graphite-muted shrink-0 pt-1">
          <div className="font-medium text-ink">{data.data_coverage.available}/{data.data_coverage.total} ETFs</div>
          <div>Compte Saxo · non PEA</div>
        </div>
      </div>

      {/* Missing data warning */}
      {missing > 0 && (
        <div className="flex items-start gap-2.5 rounded-lg border border-amber/30 bg-amber/5 px-4 py-3 text-xs text-graphite-muted"
          style={{ borderColor: '#BD6E1B30', background: '#BD6E1B08' }}>
          <AlertTriangle size={13} className="mt-0.5 shrink-0" style={{ color: '#BD6E1B' }} />
          <span>
            <span className="font-semibold text-ink">{missing} ETF{missing > 1 ? 's' : ''} sans données.</span>
            {' '}Vérifier les symboles EODHD dans{' '}
            <code className="font-mono bg-black/5 px-1 rounded">data/sleeve_a_universe.py</code>.
          </span>
        </div>
      )}

      {/* Regime + allocation */}
      <RegimeCard data={data} />

      {/* Signals table */}
      <div className="bg-ivory-light rounded-xl border border-black/5 overflow-hidden">
        <div className="flex items-center justify-between px-5 py-4 border-b border-black/5">
          <h2 className="text-sm font-semibold text-ink">Classement momentum 6M</h2>
          <span className="text-xs text-graphite-muted">
            {data.signals.filter(s => s.data_available).length} / {data.signals.length} ETFs avec données
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="border-b border-black/5">
              <tr className="text-[11px] font-semibold uppercase tracking-wider text-graphite-subtle">
                <th className="py-3 px-5 pr-4 text-left">#</th>
                <th className="py-3 pr-4 text-left">Ticker</th>
                <th className="py-3 pr-4 text-left">Nom</th>
                <th className="py-3 pr-4 text-left">Catégorie</th>
                <th className="py-3 pr-5 text-right">Momentum 6M</th>
                <th className="py-3 pr-5 text-right">Prix</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-black/[0.04]">
              {data.signals.map(sig => (
                <SignalRow key={sig.ticker} sig={sig} rank={sig.rank} />
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}