import { useState, useMemo } from 'react'
import { ExternalLink, Loader2 } from 'lucide-react'
import { api } from '../api/client'
import { useApi } from '../hooks/useApi'
import { PageLoader } from '../components/Spinner'
import type { NewsArticle } from '../types'

const PAGE_SIZE = 50

function timeAgo(dateStr: string): string {
  const diff = (Date.now() - new Date(dateStr).getTime()) / 1000
  if (diff < 3600)  return `${Math.floor(diff / 60)}min`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h`
  return `${Math.floor(diff / 86400)}j`
}

function ArticleCard({ article }: { article: NewsArticle }) {
  return (
    <a
      href={article.link}
      target="_blank"
      rel="noopener noreferrer"
      className="block bg-ivory-light rounded-xl border border-black/5 p-4 hover:bg-black/[0.02] hover:border-black/10 transition-all group"
    >
      <div className="flex items-start justify-between gap-3 mb-1.5">
        <h3 className="text-sm font-semibold text-ink leading-snug group-hover:underline">
          {article.title}
        </h3>
        <span className="text-[11px] text-graphite-subtle shrink-0 pt-0.5 flex items-center gap-1">
          {timeAgo(article.date)}
          <ExternalLink size={11} className="opacity-0 group-hover:opacity-60 transition-opacity" />
        </span>
      </div>
      {article.content && (
        <p className="text-xs text-graphite-muted leading-relaxed line-clamp-2 mb-2">
          {article.content}
        </p>
      )}
      {article.tags.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {article.tags.slice(0, 4).map(tag => (
            <span key={tag} className="text-[10px] px-1.5 py-0.5 rounded bg-black/5 text-graphite-muted uppercase tracking-wide">
              {tag}
            </span>
          ))}
        </div>
      )}
    </a>
  )
}

export default function News() {
  const [articles, setArticles] = useState<NewsArticle[]>([])
  const [offset, setOffset] = useState(0)
  const [loadingMore, setLoadingMore] = useState(false)
  const [hasMore, setHasMore] = useState(true)
  const [activeTag, setActiveTag] = useState<string | null>(null)

  const { loading, error } = useApi(async () => {
    const data = await api.news.market(PAGE_SIZE, 0)
    setArticles(data.articles)
    setOffset(PAGE_SIZE)
    setHasMore(data.articles.length === PAGE_SIZE)
    return data
  })

  async function loadMore() {
    setLoadingMore(true)
    try {
      const data = await api.news.market(PAGE_SIZE, offset)
      setArticles(prev => [...prev, ...data.articles])
      setOffset(prev => prev + PAGE_SIZE)
      setHasMore(data.articles.length === PAGE_SIZE)
    } finally {
      setLoadingMore(false)
    }
  }

  // Build tag frequency map from all loaded articles
  const tagCounts = useMemo(() => {
    const counts: Record<string, number> = {}
    for (const a of articles) {
      for (const tag of a.tags) {
        counts[tag] = (counts[tag] ?? 0) + 1
      }
    }
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 20)  // top 20 themes
  }, [articles])

  const filtered = useMemo(() =>
    activeTag ? articles.filter(a => a.tags.includes(activeTag)) : articles,
    [articles, activeTag]
  )

  if (loading) return <PageLoader label="Chargement des actualités…" />
  if (error)   return <div className="text-danger p-6">{error}</div>

  return (
    <div className="space-y-4 max-w-3xl">
      {/* Header */}
      <div>
        <h1 className="text-xl font-semibold text-ink">Actualités</h1>
        <p className="text-sm text-graphite-muted mt-0.5">
          {filtered.length} article{filtered.length > 1 ? 's' : ''}
          {activeTag ? ` · thème "${activeTag}"` : ` · ${articles.length} chargés`}
          {' '}· EODHD · cache 30 min
        </p>
      </div>

      {/* Theme bar */}
      {tagCounts.length > 0 && (
        <div className="bg-ivory-light rounded-xl border border-black/5 p-3">
          <div className="text-[10px] uppercase tracking-widest text-graphite-muted mb-2.5 px-1">
            Thèmes
          </div>
          <div className="flex flex-wrap gap-1.5">
            <button
              onClick={() => setActiveTag(null)}
              className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-colors ${
                activeTag === null
                  ? 'bg-ink text-white'
                  : 'bg-black/5 text-graphite-muted hover:text-ink hover:bg-black/8'
              }`}
            >
              Tous
              <span className="ml-1.5 opacity-60">{articles.length}</span>
            </button>
            {tagCounts.map(([tag, count]) => (
              <button
                key={tag}
                onClick={() => setActiveTag(activeTag === tag ? null : tag)}
                className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-colors ${
                  activeTag === tag
                    ? 'bg-ink text-white'
                    : 'bg-black/5 text-graphite-muted hover:text-ink hover:bg-black/8'
                }`}
              >
                {tag}
                <span className="ml-1.5 opacity-60">{count}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Articles */}
      <div className="space-y-2.5">
        {filtered.map((a, i) => <ArticleCard key={i} article={a} />)}
        {filtered.length === 0 && (
          <div className="text-graphite-muted text-sm py-8 text-center">
            Aucun article pour ce thème.
          </div>
        )}
      </div>

      {/* Load more — only when no tag filter active */}
      {hasMore && activeTag === null && (
        <button
          onClick={loadMore}
          disabled={loadingMore}
          className="w-full py-3 rounded-xl border border-black/8 bg-ivory-light text-sm font-medium text-graphite-muted hover:text-ink hover:border-black/15 transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {loadingMore
            ? <><Loader2 size={14} className="animate-spin" />Chargement…</>
            : `Charger ${PAGE_SIZE} articles de plus`
          }
        </button>
      )}
    </div>
  )
}