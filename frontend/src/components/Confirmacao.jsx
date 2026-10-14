import { useState } from 'react'

/** Conteúdo padrão de um diálogo "Tem certeza?". */
export default function Confirmacao({ texto, botao, perigo, aoConfirmar, aoCancelar }) {
  const [enviando, setEnviando] = useState(false)
  const [erro, setErro] = useState('')

  async function confirmar() {
    setEnviando(true)
    setErro('')
    try {
      await aoConfirmar()
    } catch (e) {
      setErro(e.message)
      setEnviando(false)
    }
  }

  return (
    <>
      {erro && <p className="dialogo__erro" role="alert">{erro}</p>}
      <p className="dialogo__texto">{texto}</p>
      <div className="dialogo__acoes">
        <button type="button" className="botao botao--secundario" onClick={aoCancelar} autoFocus>
          Cancelar
        </button>
        <button
          type="button"
          className={perigo ? 'botao botao--perigo' : 'botao botao--principal'}
          onClick={confirmar}
          disabled={enviando}
        >
          {enviando ? 'Aguarde…' : botao}
        </button>
      </div>
    </>
  )
}
