import { useCallback, useEffect, useState } from 'react'
import { auth } from '../api'
import { ContextoAuth } from '../auth'

export default function ProvedorAuth({ children }) {
  // undefined = ainda verificando; null = sem sessão
  const [usuario, setUsuario] = useState(undefined)

  useEffect(() => {
    auth
      .eu()
      .then(({ usuario }) => setUsuario(usuario))
      .catch(() => setUsuario(null))
  }, [])

  const sair = useCallback(async () => {
    try {
      await auth.sair()
    } finally {
      setUsuario(null)
    }
  }, [])

  if (usuario === undefined) return null
  return (
    <ContextoAuth.Provider value={{ usuario, setUsuario, sair }}>
      {children}
    </ContextoAuth.Provider>
  )
}
