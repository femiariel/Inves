import type {
  Signal, ProposalResponse, Holding, Settings, ETFMeta, BacktestResult,
} from '../types'

const BASE = ''  // Caddy proxies /api/* → FastAPI

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText)
    throw new Error(`${res.status} — ${text}`)
  }
  return res.json() as Promise<T>
}

export const api = {
  universe: () => req<ETFMeta[]>('/api/universe'),

  signals: () => req<Signal[]>('/api/signals'),

  proposal: () => req<ProposalResponse>('/api/proposal'),

  backtest: () => req<BacktestResult>('/api/backtest'),

  holdings: {
    list: () => req<Holding[]>('/api/holdings'),
    upsert: (body: { ticker: string; quantity: number; avg_cost: number }) =>
      req<Holding>('/api/holdings', { method: 'POST', body: JSON.stringify(body) }),
    delete: (ticker: string) =>
      req<{ ok: boolean }>(`/api/holdings/${ticker}`, { method: 'DELETE' }),
  },

  settings: {
    get: () => req<Settings>('/api/settings'),
    update: (body: Partial<Settings>) =>
      req<Settings>('/api/settings', { method: 'PUT', body: JSON.stringify(body) }),
  },

  cache: {
    clear: () => req<{ ok: boolean; message: string }>('/api/cache/clear', { method: 'POST' }),
  },
}
