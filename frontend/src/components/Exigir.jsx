import { Navigate } from 'react-router'
import { rotaInicial, useAuth } from '../auth'

/** Só mostra o conteúdo para quem está logada (e, se informado, com o papel certo). */
export default function Exigir({ papel, children }) {
  const { usuario } = useAuth()
  if (!usuario) return <Navigate to="/entrar" replace />
  if (papel && usuario.papel !== papel) return <Navigate to={rotaInicial(usuario)} replace />
  return children
}
