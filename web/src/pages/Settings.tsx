import { useState, useEffect } from 'react'
import { Save, Check } from 'lucide-react'
import { api } from '../api/client'
import { useApi } from '../hooks/useApi'
import { PageLoader } from '../components/Spinner'
import type { Settings } from '../types'

const SOURCE_LABELS: Record<string, string> = {
  eodhd: 'EODHD',
}

export default function SettingsPage() {
  const { data, loading, error } = useApi(() => api.settings.get())

  const [form, setForm]         = useState<Partial<Settings>>({})
  const [saving, setSaving]     = useState(false)
  const [saved, setSaved]       = useState(false)

  useEffect(() => { if (data) setForm(data) }, [data])

  const save = async () => {
    setSaving(true)
    try {
      await api.settings.update({
        capital:       form.capital,
        top_n:         form.top_n,
      })
      setSaved(true)
      setTimeout(() => setSaved(false), 2500)
    } finally { setSaving(false) }
  }

  const set = (k: keyof Settings, v: string) => setForm(f => ({ ...f, [k]: v }))

  if (loading) return <PageLoader label="Chargement des réglages…" />
  if (error)   return <div className="text-danger p-6">{error}</div>

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-xl font-semibold text-ink">Réglages</h1>
        <p className="text-sm text-graphite-muted mt-0.5">Configuration de la stratégie et des données</p>
      </div>

      {/* Source de données */}
      <div className="bg-ivory-light rounded-xl border border-black/5 p-6 space-y-4">
        <h2 className="text-xs font-semibold uppercase tracking-widest text-graphite-muted">
          Source de données
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div className="rounded-lg border border-black/8 bg-white px-3 py-2">
            <div className="text-xs text-graphite-muted">Source active</div>
            <div className="text-sm font-medium text-ink">
              {SOURCE_LABELS[String(form.data_source)] ?? form.data_source ?? 'Cache'}
            </div>
          </div>
          <div className="rounded-lg border border-black/8 bg-white px-3 py-2">
            <div className="text-xs text-graphite-muted">Historique</div>
            <div className="text-sm font-medium text-ink">{form.history_years ?? '—'} ans</div>
          </div>
        </div>
        <p className="text-xs text-graphite-subtle">
          Les prix sont chargés hors interface par <code>scripts/fetch_market_data.py</code>.
        </p>
      </div>

      {/* Stratégie */}
      <div className="bg-ivory-light rounded-xl border border-black/5 p-6 space-y-4">
        <h2 className="text-xs font-semibold uppercase tracking-widest text-graphite-muted">
          Paramètres stratégie
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs text-graphite-muted mb-1.5">Capital (€)</label>
            <input
              type="number"
              value={form.capital ?? ''}
              onChange={e => set('capital', e.target.value)}
              min="100"
              step="100"
              className="w-full px-3 py-2 rounded-lg border border-black/10 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-forest/30"
            />
          </div>
          <div>
            <label className="block text-xs text-graphite-muted mb-1.5">
              Satellites (top N)
              <span className="text-graphite-subtle ml-1">max pour le 20%</span>
            </label>
            <input
              type="number"
              value={form.top_n ?? ''}
              onChange={e => set('top_n', e.target.value)}
              min="1"
              max="10"
              step="1"
              className="w-full px-3 py-2 rounded-lg border border-black/10 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-forest/30"
            />
          </div>
        </div>

        <div className="bg-black/3 rounded-lg p-3 text-xs text-graphite-muted">
          <strong className="text-ink">Rappel stratégie :</strong> 80% ancre MSCI World (DCAM.PA)
          + 20% répartis sur les top-N satellites avec momentum 12M positif.
          Si aucun satellite éligible → 20% en liquidités.
        </div>
      </div>

      {/* Save */}
      <div className="flex items-center gap-3">
        <button
          onClick={save}
          disabled={saving}
          className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-forest text-white text-sm font-medium hover:bg-forest-dark disabled:opacity-50 transition-colors"
        >
          {saved ? <Check size={15} /> : <Save size={15} />}
          {saved ? 'Enregistré !' : saving ? 'Enregistrement…' : 'Enregistrer'}
        </button>
        <p className="text-xs text-graphite-subtle">
          Les prix affichés viennent uniquement du cache SQLite.
        </p>
      </div>
    </div>
  )
}
