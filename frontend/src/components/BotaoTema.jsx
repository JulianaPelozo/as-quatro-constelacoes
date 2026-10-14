import { useEffect, useState } from 'react'
import './BotaoTema.css'

const consultaEscuro = () => window.matchMedia('(prefers-color-scheme: dark)')

function temaAtual() {
  const escolhido = document.documentElement.dataset.tema
  if (escolhido) return escolhido
  return consultaEscuro().matches ? 'escuro' : 'claro'
}

export default function BotaoTema() {
  const [tema, setTema] = useState(temaAtual)

  // Acompanha a troca de tema do sistema enquanto ninguém escolheu um
  useEffect(() => {
    const consulta = consultaEscuro()
    const aoMudar = () => setTema(temaAtual())
    consulta.addEventListener('change', aoMudar)
    return () => consulta.removeEventListener('change', aoMudar)
  }, [])

  function alternar() {
    const novo = tema === 'escuro' ? 'claro' : 'escuro'
    document.documentElement.dataset.tema = novo
    try {
      localStorage.setItem('tema', novo)
    } catch {
      // Sem armazenamento (ex.: navegação privada): vale só para esta visita
    }
    setTema(novo)
  }

  const proximo = tema === 'escuro' ? 'claro' : 'escuro'
  return (
    <button type="button" className="botao-tema" onClick={alternar}>
      <span aria-hidden="true">{tema === 'escuro' ? '☀' : '☾'}</span>
      <span className="botao-tema__texto">Tema {proximo}</span>
    </button>
  )
}
