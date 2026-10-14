import { useEffect, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router'
import { admin } from '../../api'
import Dialogo from '../../components/Dialogo'
import Esqueleto from '../../components/Esqueleto'
import FormHistoria from './FormHistoria'
import './AdminHistorias.css'

const FILTROS = [
  { valor: 'circulo', rotulo: 'No círculo' },
  { valor: 'fora', rotulo: 'Fora do círculo' },
  { valor: 'todas', rotulo: 'Todas' },
]

const normalizar = (texto) =>
  texto.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()

const capitulos = (n) => (n === 1 ? '1 capítulo' : `${n} capítulos`)

export default function AdminHistorias() {
  const navegar = useNavigate()
  const local = useLocation()
  const [historias, setHistorias] = useState(null)
  const [erro, setErro] = useState('')
  const [busca, setBusca] = useState('')
  const [filtro, setFiltro] = useState('circulo')
  const [criando, setCriando] = useState(false)

  useEffect(() => {
    admin
      .historias()
      .then(({ historias }) => setHistorias(historias))
      .catch((e) => setErro(e.message))
  }, [])

  const noCirculo = historias?.filter((h) => h.no_circulo) ?? []
  const totalCapitulos = noCirculo.reduce((soma, h) => soma + h.total_capitulos, 0)

  const termo = normalizar(busca.trim())
  const visiveis = (historias ?? []).filter((h) => {
    if (filtro === 'circulo' && !h.no_circulo) return false
    if (filtro === 'fora' && h.no_circulo) return false
    return !termo || normalizar(`${h.titulo} ${h.autora.nome}`).includes(termo)
  })

  return (
    <div>
      <header className="pagina__topo">
        <div>
          <h1>Histórias</h1>
          {historias && (
            <p className="pagina__sub">
              {noCirculo.length} no círculo de leitura · {capitulos(totalCapitulos)}
            </p>
          )}
        </div>
        <button type="button" className="botao botao--principal" onClick={() => setCriando(true)}>
          <span aria-hidden="true">+</span> Cadastrar história
        </button>
      </header>

      <p className="pagina__aviso" role="status">
        {local.state?.aviso && <span className="aparecer">{local.state.aviso}</span>}
      </p>

      {!historias && !erro && <Esqueleto linhas={3} altura={118} colunas={260} />}

      {erro && <p className="alerta-erro" role="alert">{erro}</p>}

      {historias && historias.length > 0 && (
        <div className="ferramentas">
          <label className="busca">
            <span className="visualmente-oculto">Buscar por título ou autora</span>
            <input
              type="search"
              placeholder="Buscar por título ou autora"
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </label>
          <div className="segmentado" role="group" aria-label="Mostrar">
            {FILTROS.map((f) => (
              <button
                key={f.valor}
                type="button"
                aria-pressed={filtro === f.valor}
                onClick={() => setFiltro(f.valor)}
              >
                {f.rotulo}
              </button>
            ))}
          </div>
        </div>
      )}

      {historias && historias.length === 0 && (
        <div className="vazio">
          <p>
            Nenhuma história cadastrada ainda. Cadastre as histórias das participantes e, em
            seguida, os capítulos de cada uma.
          </p>
        </div>
      )}

      {historias && historias.length > 0 && visiveis.length === 0 && (
        <div className="vazio">
          <p>Nenhuma história encontrada com esses filtros.</p>
        </div>
      )}

      {visiveis.length > 0 && (
        <ul className="lista-historias">
          {visiveis.map((h, i) => (
            <li key={h.id} className="surgir" style={{ '--i': i }}>
              <Link to={`/admin/historias/${h.id}`} className="cartao-historia">
                <span className="cartao-historia__titulo">{h.titulo}</span>
                <span className="cartao-historia__autora">por {h.autora.nome}</span>
                <span className="cartao-historia__rodape">
                  <span>{capitulos(h.total_capitulos)}</span>
                  {!h.no_circulo && <span className="etiqueta etiqueta--desativada">Fora do círculo</span>}
                  {h.no_circulo && h.total_capitulos === 0 && (
                    <span className="etiqueta etiqueta--pendente">Sem capítulos</span>
                  )}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      )}

      <Dialogo aberto={criando} aoFechar={() => setCriando(false)} titulo="Cadastrar história">
        <FormHistoria
          aoCancelar={() => setCriando(false)}
          aoSalvar={(historia) => navegar(`/admin/historias/${historia.id}`, { state: { nova: true } })}
        />
      </Dialogo>
    </div>
  )
}
