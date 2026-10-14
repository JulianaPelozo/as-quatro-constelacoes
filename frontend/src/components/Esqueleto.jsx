/**
 * Blocos pulsando no formato do conteúdo que ainda está carregando.
 * Leitores de tela ouvem só "Carregando…".
 */
export default function Esqueleto({ linhas = 3, altura = 72, colunas }) {
  return (
    <div role="status">
      <span className="visualmente-oculto">Carregando…</span>
      <div
        className="esqueleto"
        aria-hidden="true"
        style={colunas ? { gridTemplateColumns: `repeat(auto-fill, minmax(${colunas}px, 1fr))` } : undefined}
      >
        {Array.from({ length: linhas }, (_, i) => (
          <div key={i} className="esqueleto__bloco" style={{ height: altura }} />
        ))}
      </div>
    </div>
  )
}
