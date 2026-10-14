import { useEffect, useState } from 'react'
import { flushSync } from 'react-dom'
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

  function alternar(evento) {
    const novo = tema === 'escuro' ? 'claro' : 'escuro'
    const aplicar = () => {
      document.documentElement.dataset.tema = novo
      try {
        localStorage.setItem('tema', novo)
      } catch {
        // Sem armazenamento (ex.: navegação privada): vale só para esta visita
      }
      flushSync(() => setTema(novo))
    }

    const semMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (!document.startViewTransition || semMovimento) {
      aplicar()
      return
    }

    // O novo tema se espalha em círculo a partir do botão
    const botao = evento.currentTarget.getBoundingClientRect()
    const x = botao.left + botao.width / 2
    const y = botao.top + botao.height / 2
    const raio = Math.hypot(Math.max(x, window.innerWidth - x), Math.max(y, window.innerHeight - y))

    const transicao = document.startViewTransition(aplicar)
    transicao.ready.then(() => {
      document.documentElement.animate(
        { clipPath: [`circle(0px at ${x}px ${y}px)`, `circle(${raio}px at ${x}px ${y}px)`] },
        {
          duration: 550,
          easing: 'cubic-bezier(0.2, 0.8, 0.2, 1)',
          pseudoElement: '::view-transition-new(root)',
        },
      )
    })
  }

  const proximo = tema === 'escuro' ? 'claro' : 'escuro'
  return (
    <button type="button" className="botao-tema" onClick={alternar}>
      <span aria-hidden="true">{tema === 'escuro' ? '☀' : '☾'}</span>
      <span className="botao-tema__texto">Tema {proximo}</span>
    </button>
  )
}
