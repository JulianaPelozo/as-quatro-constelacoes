import { Navigate } from 'react-router'
import { rotaInicial, useAuth } from '../auth'

/**
 * Só mostra o conteúdo para quem está logada (e, se informado, com o papel certo).
 * Quem ainda está com senha temporária é levada para a troca de senha.
 */
export default function Exigir({ papel, telaDeTrocaDeSenha = false, children }) {
  const { usuario } = useAuth()
  if (!usuario) return <Navigate to="/entrar" replace />
  if (usuario.precisa_trocar_senha && !telaDeTrocaDeSenha) {
    return <Navigate to="/trocar-senha" replace />
  }
  if (papel && usuario.papel !== papel) return <Navigate to={rotaInicial(usuario)} replace />
  return children
}
