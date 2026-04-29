interface Props {
  label:  string
  value:  string
  sub?:   string
  trend?: 'up' | 'down' | 'neutral'
}

const trendColor = { up: 'text-forest', down: 'text-danger', neutral: 'text-ink' }

export function KpiCard({ label, value, sub, trend = 'neutral' }: Props) {
  return (
    <div className="bg-ivory-light rounded-xl border border-black/5 px-5 py-4">
      <div className="text-[11px] font-semibold uppercase tracking-widest text-graphite-muted mb-2">
        {label}
      </div>
      <div className={`text-2xl font-semibold tabular-nums ${trendColor[trend]}`}>
        {value}
      </div>
      {sub && <div className="text-xs text-graphite-subtle mt-1">{sub}</div>}
    </div>
  )
}
