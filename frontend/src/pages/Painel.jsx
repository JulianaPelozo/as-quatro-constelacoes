import { useAuth } from '../auth'
import Cabecalho from '../components/Cabecalho'
import './Painel.css'

const NOME_PAPEL = {
  administradora: 'Administradora',
  autora: 'Autora',
  participante: 'Participante do círculo de leitura',
}

// Página provisória das participantes e autoras. Será substituída pelo
// painel do círculo de leitura (RF-10.6).
export default function Painel() {
  const { usuario } = useAuth()

  return (
    <div className="painel">
      <Cabecalho />
      <main className="painel__conteudo">
        <h1>Olá, {usuario.nome}!</h1>
        <p className="painel__papel">{NOME_PAPEL[usuario.papel] ?? usuario.papel}</p>
        <p>Seu painel está em construção. Em breve, aqui vão aparecer o capítulo do dia e suas metas.</p>
      </main>
    </div>
  )
}
