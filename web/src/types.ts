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
  r12_1M: number | null
  momentum_component: number
  trend_component: number
  risk_penalty: number
  score: number
  above_sma200: boolean
  annual_vol: number
  max_drawdown: number
  data_quality_ok: boolean
  allocation_eligible: boolean
  factor_score: number
  momentum_z: number
  momentum_12_1m_z: number
  momentum_6m_z: number
  momentum_3m_z: number
  trend_z: number
  vol_z: number
  drawdown_z: number
  overheat_penalty: number
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

export interface StressIndicator {
  id: string
  label: string
  description: string
  value: number | null
  value_label: string | null
  percentile: number | null
  stress: number
  status: 'green' | 'orange' | 'red' | 'unknown'
  interpretation: string
  weight: number
}

export interface StressDashboard {
  composite_score: number
  composite_status: 'green' | 'orange' | 'red'
  composite_label: string
  indicators: StressIndicator[]
  computed_at: number
}

export type SensitivityLevel = 'very_high' | 'high' | 'medium' | 'low'

export interface ETFCrashProfile {
  level: SensitivityLevel
  label: string
  color: string
  bg_color: string
  multiplier: number
  relevant_indicators: string[]
  crash_context: string
  description: string
  warning_threshold: number
}

export interface ETFStressAnalysis {
  ticker: string
  crash_profile: ETFCrashProfile
  stress: StressDashboard
  risk_score: number
  risk_status: 'green' | 'orange' | 'red'
  risk_label: string
  risk_summary: string
}

// ── News ──────────────────────────────────────────────────────────────────────

export type SentimentLabel = 'positive' | 'negative' | 'neutral'

export interface NewsArticle {
  date: string
  title: string
  content: string
  link: string
  symbols: string[]
  tags: string[]
  sentiment: { polarity: number | null; label: SentimentLabel }
}

export interface NewsFeed {
  articles: NewsArticle[]
  source: string
  us_benchmark?: string
  cached_at: number
}

// ── Sleeve A ──────────────────────────────────────────────────────────────────

export interface SleeveARegime {
  regime: 'on' | 'off' | 'unknown'
  filter_ticker: string
  price: number | null
  sma200: number | null
  ratio: number | null
  data_available: boolean
}

export interface SleeveASignal {
  ticker: string
  name: string
  category: string
  mom_6m: number | null
  latest_price: number | null
  data_available: boolean
  rank: number | null
}

export interface SleeveAPosition {
  ticker: string
  name: string
  category: string
  weight: number
  mom_6m?: number | null
  rank?: number | null
  rationale: string
  latest_price: number | null
}

export interface SleeveACorrPair {
  t1: string
  t2: string
  corr: number
}

export interface SleeveAAllocation {
  regime: SleeveARegime
  positions: SleeveAPosition[]
  corr_pairs: SleeveACorrPair[]
  guardrail_applied: boolean
  corr_threshold?: number
}

export interface SleeveAResult {
  regime: SleeveARegime
  signals: SleeveASignal[]
  allocation: SleeveAAllocation
  data_coverage: { available: number; total: number }
  computed_at: number
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
