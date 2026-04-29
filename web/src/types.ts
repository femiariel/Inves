export type Rec = 'buy' | 'hold' | 'trim' | 'avoid'

export interface Signal {
  ticker: string
  name: string
  sleeve: string
  category: string
  latest_price: number | null
  r1M: number | null
  r3M: number | null
  r6M: number | null
  r12M: number | null
  momentum_component: number
  trend_component: number
  risk_penalty: number
  score: number
  above_sma200: boolean
  annual_vol: number
  max_drawdown: number
  recommendation: Rec
  rec_label: string
  rec_color: string
  momentum_filter_ok: boolean
  lookback_summary: string
}

export interface ProposalLine {
  ticker: string
  name: string
  sleeve: string
  category: string
  weight: number
  value: number
  score: number | null
  rationale: string
}

export interface Proposal {
  lines: ProposalLine[]
  cash_reserve_pct: number
  cash_reserve_value: number
  capital: number
  n_satellites: number
  expected_return: number
  expected_vol: number
  expected_sharpe: number
  rationale: string
}

export interface Order {
  ticker: string
  name: string
  action: 'buy' | 'sell' | 'hold'
  current_weight: number
  target_weight: number
  current_value: number
  target_value: number
  delta_value: number
  priority: number
}

export interface ProposalResponse {
  proposal: Proposal
  orders: Order[]
}

export interface Holding {
  ticker: string
  name: string
  quantity: number
  avg_cost: number
  sleeve: string
  latest_price: number | null
  market_value: number
  cost_basis: number
  pnl: number
  pnl_pct: number
  day_change: number
  allocation_pct: number
  added_at: string
  updated_at: string
}

export interface Settings {
  data_source: string
  eodhd_api_key: string
  capital: string
  top_n: string
  history_years: string
}

export interface ETFMeta {
  ticker: string
  name: string
  sleeve: string
  category: string
  target_weight: number
  notes: string
}

export interface BacktestPoint {
  date: string
  value: number
}

export interface BacktestResult {
  equity_curve: BacktestPoint[]
  benchmark_curve: BacktestPoint[]
  ending_value: number
  benchmark_value: number
  cagr: number
  benchmark_cagr: number
  max_drawdown: number
  benchmark_max_dd: number
  sharpe: number
  benchmark_sharpe: number
  alpha: number
  trade_count: number
  n_days: number
}
