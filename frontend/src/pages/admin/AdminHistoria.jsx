import { useEffect, useId, useState } from 'react'
import { Link, useLocation, useNavigate, useParams } from 'react-router'
import { admin } from '../../api'
import Confirmacao from '../../components/Confirmacao'
import Dialogo from '../../components/Dialogo'
import Esqueleto from '../../components/Esqueleto'
import FormHistoria from './FormHistoria'
import './AdminHistorias.css'

const EXEMPLO_LOTE = `https://www.wattpad.com/111-capitulo-1
Capítulo 2 – O encontro | https://www.wattpad.com/222-o-encontro
Epílogo: https://www.wattpad.com/333-epilogo`

export default function AdminHistoria() {
  const { id } = useParams()
  const navegar = useNavigate()
  const local = useLocation()
  const [historia, setHistoria] = useState(null)
  const [erro, setErro] = useState('')
  const [aviso, setAviso] = useState(local.state?.nova ? 'História cadastrada. Agora adicione os capítulos.' : '')
  // { tipo: 'editar' | 'excluir' | 'capitulo' | 'lote' | 'excluir-capitulo', capitulo }
  const [dialogo, setDialogo] = useState(null)

  useEffect(() => {
    admin
      .historia(id)
      .then(({ historia }) => setHistoria(historia))
      .catch((e) => setErro(e.message))
  }, [id])

  const fechar = () => setDialogo(null)

  function atualizarCapitulos(funcao) {
    setHistoria((h) => {
      const lista = funcao(h.capitulos).sort((a, b) => a.numero - b.numero)
      return { ...h, capitulos: lista, total_capitulos: lista.length }
    })
  }

  if (erro) {
    return (
      <div>
        <Link to="/admin/historias" className="voltar">← Histórias</Link>
        <p className="alerta-erro" role="alert">{erro}</p>
      </div>
    )
  }
  if (!historia) {
    return (
      <div>
        <Link to="/admin/historias" className="voltar">← Histórias</Link>
        <Esqueleto linhas={1} altura={84} />
        <div style={{ height: 24 }} />
        <Esqueleto linhas={4} altura={62} />
      </div>
    )
  }

  const n = historia.capitulos.length

  return (
    <div>
      <Link to="/admin/historias" className="voltar">← Histórias</Link>

      <header className="pagina__topo">
        <div>
          <h1>{historia.titulo}</h1>
          <p className="historia__meta">
            <span>por {historia.autora.nome}</span>
            <a href={historia.link} target="_blank" rel="noopener noreferrer">
              Abrir no Wattpad<span aria-hidden="true"> ↗</span>
              <span className="visualmente-oculto"> (abre em nova aba)</span>
            </a>
            {!historia.no_circulo && <span className="etiqueta etiqueta--desativada">Fora do círculo</span>}
          </p>
        </div>
        <div className="historia__acoes">
          <button type="button" className="botao botao--secundario" onClick={() => setDialogo({ tipo: 'editar' })}>
            Editar história
          </button>
          <button type="button" className="botao botao--secundario" onClick={() => setDialogo({ tipo: 'excluir' })}>
            Excluir
          </button>
        </div>
      </header>

      <p className="pagina__aviso" role="status">
        <span key={aviso} className="aparecer">{aviso}</span>
      </p>

      <section className="secao-capitulos" aria-labelledby="titulo-capitulos">
        <div className="secao-capitulos__topo">
          <h2 id="titulo-capitulos">
            Capítulos <span className="pagina__sub">({n})</span>
          </h2>
          <div className="secao-capitulos__botoes">
            <button type="button" className="botao botao--secundario" onClick={() => setDialogo({ tipo: 'lote' })}>
              Adicionar vários
            </button>
            <button type="button" className="botao botao--principal" onClick={() => setDialogo({ tipo: 'capitulo' })}>
              <span aria-hidden="true">+</span> Adicionar capítulo
            </button>
          </div>
        </div>

        {n === 0 ? (
          <div className="vazio">
            <p>
              Nenhum capítulo ainda. Use <strong>Adicionar vários</strong> para colar os links de
              todos os capítulos de uma vez.
            </p>
          </div>
        ) : (
          <ol className="lista-capitulos">
            {historia.capitulos.map((c, i) => (
              <li key={c.id} className="capitulo surgir" style={{ '--i': i }}>
                <span className="capitulo__numero" aria-label={`Capítulo ${c.numero}`}>{c.numero}</span>
                <span className={c.titulo ? 'capitulo__titulo' : 'capitulo__titulo capitulo__titulo--vazio'}>
                  {c.titulo || 'Sem título'}
                </span>
                <div className="acoes-linha">
                  <a href={c.link} target="_blank" rel="noopener noreferrer">
                    Abrir<span className="visualmente-oculto"> capítulo {c.numero} no Wattpad (nova aba)</span>
                    <span aria-hidden="true">&nbsp;↗</span>
                  </a>
                  <button type="button" onClick={() => setDialogo({ tipo: 'capitulo', capitulo: c })}>
                    Editar<span className="visualmente-oculto"> capítulo {c.numero}</span>
                  </button>
                  <button type="button" onClick={() => setDialogo({ tipo: 'excluir-capitulo', capitulo: c })}>
                    Excluir<span className="visualmente-oculto"> capítulo {c.numero}</span>
                  </button>
                </div>
              </li>
            ))}
          </ol>
        )}
      </section>

      <Dialogo aberto={dialogo?.tipo === 'editar'} aoFechar={fechar} titulo="Editar história">
        <FormHistoria
          historia={historia}
          aoCancelar={fechar}
          aoSalvar={(atualizada) => {
            setHistoria(atualizada)
            setAviso('Alterações salvas.')
            fechar()
          }}
        />
      </Dialogo>

      <Dialogo aberto={dialogo?.tipo === 'excluir'} aoFechar={fechar} titulo="Excluir história?">
        <Confirmacao
          texto={`"${historia.titulo}" e seus ${n} capítulos vão ser apagados do site (nada muda no Wattpad). Se a ideia é só tirar a história do cronograma, prefira editar e desmarcar "Faz parte do círculo de leitura".`}
          botao="Excluir história"
          perigo
          aoCancelar={fechar}
          aoConfirmar={async () => {
            await admin.excluirHistoria(historia.id)
            navegar('/admin/historias', { replace: true, state: { aviso: `"${historia.titulo}" foi excluída.` } })
          }}
        />
      </Dialogo>

      <Dialogo
        aberto={dialogo?.tipo === 'capitulo'}
        aoFechar={fechar}
        titulo={dialogo?.capitulo ? `Editar capítulo ${dialogo.capitulo.numero}` : 'Adicionar capítulo'}
      >
        <FormCapitulo
          historiaId={historia.id}
          capitulo={dialogo?.capitulo}
          proximoNumero={(historia.capitulos.at(-1)?.numero ?? 0) + 1}
          aoCancelar={fechar}
          aoSalvar={(capitulo) => {
            atualizarCapitulos((lista) => [...lista.filter((c) => c.id !== capitulo.id), capitulo])
            setAviso(dialogo?.capitulo ? `Capítulo ${capitulo.numero} salvo.` : `Capítulo ${capitulo.numero} adicionado.`)
            fechar()
          }}
        />
      </Dialogo>

      <Dialogo aberto={dialogo?.tipo === 'lote'} aoFechar={fechar} titulo="Adicionar vários capítulos">
        <FormLote
          historiaId={historia.id}
          aoCancelar={fechar}
          aoSalvar={(novos) => {
            atualizarCapitulos((lista) => [...lista, ...novos])
            setAviso(novos.length === 1 ? '1 capítulo adicionado.' : `${novos.length} capítulos adicionados.`)
            fechar()
          }}
        />
      </Dialogo>

      <Dialogo aberto={dialogo?.tipo === 'excluir-capitulo'} aoFechar={fechar} titulo="Excluir capítulo?">
        {dialogo?.tipo === 'excluir-capitulo' && (
          <Confirmacao
            texto={`O capítulo ${dialogo.capitulo.numero}${dialogo.capitulo.titulo ? ` ("${dialogo.capitulo.titulo}")` : ''} vai ser removido do site. Os outros capítulos mantêm a numeração.`}
            botao="Excluir capítulo"
            perigo
            aoCancelar={fechar}
            aoConfirmar={async () => {
              await admin.excluirCapitulo(dialogo.capitulo.id)
              atualizarCapitulos((lista) => lista.filter((c) => c.id !== dialogo.capitulo.id))
              setAviso(`Capítulo ${dialogo.capitulo.numero} excluído.`)
              fechar()
            }}
          />
        )}
      </Dialogo>
    </div>
  )
}

function FormCapitulo({ historiaId, capitulo, proximoNumero, aoSalvar, aoCancelar }) {
  const [numero, setNumero] = useState(String(capitulo?.numero ?? proximoNumero))
  const [titulo, setTitulo] = useState(capitulo?.titulo ?? '')
  const [link, setLink] = useState(capitulo?.link ?? '')
  const [erro, setErro] = useState('')
  const [salvando, setSalvando] = useState(false)
  const id = useId()

  async function enviar(evento) {
    evento.preventDefault()
    setErro('')
    const n = Number(numero)
    if (!Number.isInteger(n) || n < 1) return setErro('O número precisa ser um número inteiro a partir de 1.')
    if (!link.trim()) return setErro('Informe o link do capítulo.')
    setSalvando(true)
    try {
      const dados = { numero: n, titulo: titulo.trim(), link: link.trim() }
      const resposta = capitulo
        ? await admin.editarCapitulo(capitulo.id, dados)
        : await admin.criarCapitulo(historiaId, dados)
      aoSalvar(resposta.capitulo)
    } catch (e) {
      setErro(e.message)
      setSalvando(false)
    }
  }

  return (
    <form onSubmit={enviar} noValidate>
      {erro && <p className="dialogo__erro" role="alert">{erro}</p>}
      <div className="campo">
        <label htmlFor={`${id}-numero`}>Número</label>
        <input
          id={`${id}-numero`}
          type="number"
          inputMode="numeric"
          min="1"
          step="1"
          value={numero}
          onChange={(e) => setNumero(e.target.value)}
          style={{ maxWidth: 120 }}
        />
      </div>
      <div className="campo">
        <label htmlFor={`${id}-titulo`}>
          Título <span className="campo__opcional">(opcional)</span>
        </label>
        <input
          id={`${id}-titulo`}
          autoComplete="off"
          maxLength={200}
          value={titulo}
          onChange={(e) => setTitulo(e.target.value)}
        />
      </div>
      <div className="campo">
        <label htmlFor={`${id}-link`}>Link do capítulo no Wattpad</label>
        <input
          id={`${id}-link`}
          type="url"
          inputMode="url"
          autoComplete="off"
          autoFocus
          placeholder="https://www.wattpad.com/…"
          value={link}
          onChange={(e) => setLink(e.target.value)}
        />
      </div>
      <div className="dialogo__acoes">
        <button type="button" className="botao botao--secundario" onClick={aoCancelar}>
          Cancelar
        </button>
        <button type="submit" className="botao botao--principal" disabled={salvando}>
          {salvando ? 'Salvando…' : capitulo ? 'Salvar' : 'Adicionar'}
        </button>
      </div>
    </form>
  )
}

function FormLote({ historiaId, aoSalvar, aoCancelar }) {
  const [texto, setTexto] = useState('')
  const [erro, setErro] = useState(null)
  const [salvando, setSalvando] = useState(false)
  const id = useId()
  const linhas = texto.split('\n').filter((l) => l.trim()).length

  async function enviar(evento) {
    evento.preventDefault()
    setErro(null)
    setSalvando(true)
    try {
      const { capitulos } = await admin.criarCapitulosEmLote(historiaId, texto)
      aoSalvar(capitulos)
    } catch (e) {
      setErro({ mensagem: e.message, detalhes: e.detalhes ?? [] })
      setSalvando(false)
    }
  }

  return (
    <form onSubmit={enviar} noValidate>
      {erro && (
        <div className="dialogo__erro" role="alert">
          {erro.mensagem}
          {erro.detalhes.length > 0 && (
            <ul>
              {erro.detalhes.map((d) => <li key={d}>{d}</li>)}
            </ul>
          )}
        </div>
      )}
      <p className="dialogo__texto">
        Cole um link por linha, na ordem dos capítulos. Se quiser, escreva o título antes do link. Eles
        entram numerados depois do último capítulo já cadastrado.
      </p>
      <div className="exemplo-lote" aria-label="Exemplo">{EXEMPLO_LOTE}</div>
      <div className="campo">
        <label htmlFor={`${id}-texto`}>Links dos capítulos</label>
        <textarea
          id={`${id}-texto`}
          rows={8}
          autoFocus
          spellCheck="false"
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
        />
      </div>
      <div className="dialogo__acoes">
        <button type="button" className="botao botao--secundario" onClick={aoCancelar}>
          Cancelar
        </button>
        <button type="submit" className="botao botao--principal" disabled={salvando || linhas === 0}>
          {salvando ? 'Adicionando…' : linhas > 1 ? `Adicionar ${linhas} capítulos` : 'Adicionar'}
        </button>
      </div>
    </form>
  )
}
