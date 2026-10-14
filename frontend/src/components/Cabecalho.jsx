import { useState } from 'react'
import { Link } from 'react-router'
import { rotaInicial, useAuth } from '../auth'
import BotaoTema from './BotaoTema'
import Logo from './Logo'
import './Cabecalho.css'

export default function Cabecalho() {
  const { usuario, sair } = useAuth()
  const [saindo, setSaindo] = useState(false)

  async function aoSair() {
    setSaindo(true)
    await sair()
  }

  return (
    <header className="cabecalho">
      <Link to={rotaInicial(usuario)} className="cabecalho__marca">
        <Logo tamanho={34} />
        <span>Constelação Literária</span>
      </Link>
      <div className="cabecalho__acoes">
        <span className="cabecalho__usuario" title={usuario.email}>{usuario.nome}</span>
        <BotaoTema />
        <button type="button" className="cabecalho__sair" onClick={aoSair} disabled={saindo}>
          {saindo ? 'Saindo…' : 'Sair'}
        </button>
      </div>
    </header>
  )
}
