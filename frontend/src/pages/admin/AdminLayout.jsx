import { NavLink, Outlet } from 'react-router'
import Cabecalho from '../../components/Cabecalho'
import './AdminLayout.css'

// Seções da área administrativa. As que ainda não existem aparecem
// desabilitadas, com "em breve", para mostrar o que vem por aí.
const SECOES = [
  { titulo: 'Início', rota: '/admin' },
  { titulo: 'Participantes' },
  { titulo: 'Histórias' },
  { titulo: 'Cronograma' },
  { titulo: 'Metas' },
  { titulo: 'Conteúdos' },
]

export default function AdminLayout() {
  return (
    <div className="admin">
      <Cabecalho />
      <div className="admin__corpo">
        <nav className="admin__menu" aria-label="Área administrativa">
          <ul>
            {SECOES.map((secao) => (
              <li key={secao.titulo}>
                {secao.rota ? (
                  <NavLink to={secao.rota} end className="admin__link">
                    {secao.titulo}
                  </NavLink>
                ) : (
                  <span className="admin__link admin__link--em-breve" aria-disabled="true">
                    {secao.titulo}
                    <small>em breve</small>
                  </span>
                )}
              </li>
            ))}
          </ul>
        </nav>
        <main className="admin__conteudo">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
