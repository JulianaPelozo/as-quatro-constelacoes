import { useState } from 'react'
import { auth } from '../api'
import BotaoTema from '../components/BotaoTema'
import Logo from '../components/Logo'
import './Painel.css'

const NOME_PAPEL = {
  administradora: 'Administradora',
  autora: 'Autora',
  participante: 'Participante do círculo de leitura',
}

// Página provisória após o login. Será substituída pelo painel do círculo
// de leitura (RF-10.6) e pela área administrativa (RF-10.10).
export default function Painel({ usuario, aoSair }) {
  const [saindo, setSaindo] = useState(false)

  async function sair() {
    setSaindo(true)
    try {
      await auth.sair()
    } finally {
      aoSair()
    }
  }

  return (
    <div className="painel">
      <header className="painel__topo">
        <div className="painel__marca">
          <Logo tamanho={36} />
          <span>Constelação Literária</span>
        </div>
        <div className="painel__acoes">
          <BotaoTema />
          <button type="button" className="painel__sair" onClick={sair} disabled={saindo}>
            {saindo ? 'Saindo…' : 'Sair'}
          </button>
        </div>
      </header>

      <main className="painel__conteudo">
        <h1>Olá, {usuario.nome}!</h1>
        <p className="painel__papel">{NOME_PAPEL[usuario.papel] ?? usuario.papel}</p>
        <p>Seu painel está em construção. Em breve, aqui vão aparecer o capítulo do dia e suas metas.</p>
      </main>
    </div>
  )
}
