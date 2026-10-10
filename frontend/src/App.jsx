import { useEffect, useState } from 'react'
import { auth } from './api'
import Login from './pages/Login'
import Painel from './pages/Painel'

export default function App() {
  // undefined = ainda verificando; null = sem sessão
  const [usuario, setUsuario] = useState(undefined)

  useEffect(() => {
    auth
      .eu()
      .then(({ usuario }) => setUsuario(usuario))
      .catch(() => setUsuario(null))
  }, [])

  if (usuario === undefined) return null
  if (!usuario) return <Login aoEntrar={setUsuario} />
  return <Painel usuario={usuario} aoSair={() => setUsuario(null)} />
}
