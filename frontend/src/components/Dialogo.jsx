import { useEffect, useId, useRef } from 'react'
import './Dialogo.css'

/**
 * Janela modal com o <dialog> nativo: prende o foco, fecha com Esc e
 * devolve o foco ao botão que a abriu.
 */
export default function Dialogo({ aberto, aoFechar, titulo, children }) {
  const ref = useRef(null)
  const id = useId()

  useEffect(() => {
    const dialogo = ref.current
    if (aberto && !dialogo.open) dialogo.showModal()
    if (!aberto && dialogo.open) dialogo.close()
  }, [aberto])

  return (
    <dialog
      ref={ref}
      className="dialogo"
      aria-labelledby={`${id}-titulo`}
      onCancel={(e) => {
        e.preventDefault()
        aoFechar()
      }}
    >
      {aberto && (
        <>
          <div className="dialogo__topo">
            <h2 id={`${id}-titulo`}>{titulo}</h2>
            <button type="button" className="dialogo__fechar" onClick={aoFechar}>
              <span aria-hidden="true">×</span>
              <span className="visualmente-oculto">Fechar</span>
            </button>
          </div>
          {children}
        </>
      )}
    </dialog>
  )
}
