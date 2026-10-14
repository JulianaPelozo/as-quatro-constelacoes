import { useEffect, useId, useState } from 'react'
import { admin } from '../../api'

const NOME_PAPEL = { administradora: 'administradora', autora: 'autora', participante: 'participante' }

/** Formulário de criar/editar história, usado dentro de um <Dialogo>. */
export default function FormHistoria({ historia, aoSalvar, aoCancelar }) {
  const editando = Boolean(historia)
  const [titulo, setTitulo] = useState(historia?.titulo ?? '')
  const [autoraId, setAutoraId] = useState(historia?.autora.id ?? '')
  const [link, setLink] = useState(historia?.link ?? '')
  const [noCirculo, setNoCirculo] = useState(historia?.no_circulo ?? true)
  const [contas, setContas] = useState(null)
  const [erro, setErro] = useState('')
  const [salvando, setSalvando] = useState(false)
  const id = useId()

  useEffect(() => {
    admin
      .contasAtivas()
      .then(({ contas }) => setContas(contas))
      .catch((e) => setErro(e.message))
  }, [])

  async function enviar(evento) {
    evento.preventDefault()
    setErro('')
    if (!titulo.trim() || !autoraId || !link.trim()) {
      setErro('Preencha o título, a autora e o link.')
      return
    }
    setSalvando(true)
    try {
      const dados = {
        titulo: titulo.trim(),
        autora_id: Number(autoraId),
        link: link.trim(),
        no_circulo: noCirculo,
      }
      const resposta = editando
        ? await admin.editarHistoria(historia.id, dados)
        : await admin.criarHistoria(dados)
      aoSalvar(resposta.historia)
    } catch (e) {
      setErro(e.message)
      setSalvando(false)
    }
  }

  return (
    <form onSubmit={enviar} noValidate>
      {erro && <p className="dialogo__erro" role="alert">{erro}</p>}

      <div className="campo">
        <label htmlFor={`${id}-titulo`}>Título</label>
        <input
          id={`${id}-titulo`}
          autoFocus
          autoComplete="off"
          maxLength={200}
          value={titulo}
          onChange={(e) => setTitulo(e.target.value)}
        />
      </div>

      <div className="campo">
        <label htmlFor={`${id}-autora`}>Autora</label>
        <select
          id={`${id}-autora`}
          value={autoraId}
          onChange={(e) => setAutoraId(e.target.value)}
          disabled={!contas}
        >
          <option value="">{contas ? 'Escolha…' : 'Carregando…'}</option>
          {contas?.map((c) => (
            <option key={c.id} value={c.id}>
              {c.nome} ({NOME_PAPEL[c.papel] ?? c.papel})
            </option>
          ))}
          {/* Autora desativada continua aparecendo ao editar */}
          {editando && contas && !contas.some((c) => c.id === historia.autora.id) && (
            <option value={historia.autora.id}>{historia.autora.nome} (conta desativada)</option>
          )}
        </select>
      </div>

      <div className="campo">
        <label htmlFor={`${id}-link`}>Link da história no Wattpad</label>
        <input
          id={`${id}-link`}
          type="url"
          inputMode="url"
          autoComplete="off"
          placeholder="https://www.wattpad.com/story/…"
          value={link}
          onChange={(e) => setLink(e.target.value)}
          aria-describedby={`${id}-link-dica`}
        />
        <p id={`${id}-link-dica`} className="campo__dica">
          Abra a história no Wattpad e copie o endereço da barra do navegador.
        </p>
      </div>

      <label className="caixa">
        <input type="checkbox" checked={noCirculo} onChange={(e) => setNoCirculo(e.target.checked)} />
        <span>
          Faz parte do círculo de leitura
          <small>Desmarque para tirar a história do cronograma sem apagar o cadastro.</small>
        </span>
      </label>

      <div className="dialogo__acoes">
        <button type="button" className="botao botao--secundario" onClick={aoCancelar}>
          Cancelar
        </button>
        <button type="submit" className="botao botao--principal" disabled={salvando}>
          {salvando ? 'Salvando…' : editando ? 'Salvar' : 'Cadastrar história'}
        </button>
      </div>
    </form>
  )
}
