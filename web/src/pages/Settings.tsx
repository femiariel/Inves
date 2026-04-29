import { useState, useEffect } from 'react'
import { Save, Trash2, Check } from 'lucide-react'
import { api } from '../api/client'
import { useApi } from '../hooks/useApi'
import { PageLoader } from '../components/Spinner'
import type { Settings } from '../types'

const SOURCE_OPTIONS = [
  { value: 'mock',  label: 'Hors-ligne (démo)',  desc: 'Données simulées — instantané' },
  { value: 'yahoo', label: 'Yahoo Finance',       desc: 'Données réelles gratuites — ~30s pour 111 ETF' },
  { value: 'eodhd', label: 'EODHD',              desc: 'Données premium — rapide et fiable' },
]

export default function SettingsPage() {
  const { data, loading, error } = useApi(() => api.settings.get())

  const [form, setForm]         = useState<Partial<Settings>>({})
  const [saving, setSaving]     = useState(false)
  const [saved, setSaved]       = useState(false)
  const [clearing, setClearing] = useState(false)
  const [cleared, setCleared]   = useState(false)

  useEffect(() => { if (data) setForm(data) }, [data])

  const save = async () => {
    setSaving(true)
    try {
      await api.settings.update({
        data_source:   form.data_source,
        eodhd_api_key: form.eodhd_api_key,
        capital:       form.capital,
        top_n:         form.top_n,
        history_years: form.history_years,
      })
      setSaved(true)
      setTimeout(() => setSaved(false), 2500)
    } finally { setSaving(false) }
  }

  const clearCache = async () => {
    setClearing(true)
    try {
      await api.cache.clear()
      setCleared(true)
      setTimeout(() => setCleared(false), 2500)
    } finally { setClearing(false) }
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
        <div className="space-y-2">
          {SOURCE_OPTIONS.map(opt => (
            <label
              key={opt.value}
              className={`flex items-start gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${
                form.data_source === opt.value
                  ? 'border-forest/40 bg-forest/5'
                  : 'border-black/8 hover:border-black/15'
              }`}
            >
              <input
                type="radio"
                name="data_source"
                value={opt.value}
                checked={form.data_source === opt.value}
                onChange={e => set('data_source', e.target.value)}
                className="mt-0.5 accent-forest"
              />
              <div>
                <div className="text-sm font-medium text-ink">{opt.label}</div>
                <div className="text-xs text-graphite-muted mt-0.5">{opt.desc}</div>
              </div>
            </label>
          ))}
        </div>

        {form.data_source === 'eodhd' && (
          <div>
            <label className="block text-xs text-graphite-muted mb-1.5">Clé API EODHD</label>
            <input
              type="text"
              value={form.eodhd_api_key ?? ''}
              onChange={e => set('eodhd_api_key', e.target.value)}
              placeholder="votre-clé-api"
              className="w-full px-3 py-2 rounded-lg border border-black/10 bg-white text-sm font-mono focus:outline-none focus:ring-2 focus:ring-forest/30"
            />
          </div>
        )}
      </div>

      {/* Stratégie */}
      <div className="bg-ivory-light rounded-xl border border-black/5 p-6 space-y-4">
        <h2 className="text-xs font-semibold uppercase tracking-widest text-graphite-muted">
          Paramètres stratégie
        </h2>

        <div className="grid grid-cols-3 gap-4">
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
          <div>
            <label className="block text-xs text-graphite-muted mb-1.5">Historique (années)</label>
            <select
              value={form.history_years ?? '2'}
              onChange={e => set('history_years', e.target.value)}
              className="w-full px-3 py-2 rounded-lg border border-black/10 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-forest/30"
            >
              <option value="1">1 an</option>
              <option value="2">2 ans</option>
              <option value="3">3 ans</option>
              <option value="5">5 ans</option>
            </select>
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
          Les changements de source de données invalident le cache au prochain chargement.
        </p>
      </div>

      {/* Danger zone */}
      <div className="bg-ivory-light rounded-xl border border-danger/20 p-6 space-y-3">
        <h2 className="text-xs font-semibold uppercase tracking-widest text-danger/70">
          Zone de maintenance
        </h2>
        <p className="text-sm text-graphite-muted">
          Vider le cache SQLite force le rechargement de tous les prix au prochain appel.
          Utile si les données semblent incohérentes.
        </p>
        <button
          onClick={clearCache}
          disabled={clearing}
          className="flex items-center gap-2 px-4 py-2 rounded-lg border border-danger/30 text-danger text-sm font-medium hover:bg-danger/5 disabled:opacity-50 transition-colors"
        >
          {cleared ? <Check size={14} /> : <Trash2 size={14} />}
          {cleared ? 'Cache vidé !' : clearing ? 'Vidage…' : 'Vider le cache des prix'}
        </button>
      </div>
    </div>
  )
}
