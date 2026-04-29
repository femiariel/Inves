import type { Rec } from '../types'

const styles: Record<Rec, string> = {
  buy:   'bg-forest/10 text-forest border border-forest/25',
  hold:  'bg-forest-light/10 text-forest-light border border-forest-light/25',
  trim:  'bg-amber/10 text-amber border border-amber/25',
  avoid: 'bg-danger/10 text-danger border border-danger/25',
}

interface Props {
  rec:   Rec
  label: string
}

export function ScoreBadge({ rec, label }: Props) {
  return (
    <span className={`inline-flex px-2 py-0.5 rounded text-[11px] font-semibold ${styles[rec]}`}>
      {label}
    </span>
  )
}
