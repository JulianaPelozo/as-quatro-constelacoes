import { createContext, useContext } from 'react'

export const ContextoAuth = createContext(null)

/** Usuária logada (ou null), setUsuario e sair(). */
export function useAuth() {
  return useContext(ContextoAuth)
}

/** Página inicial de cada perfil depois do login. */
export function rotaInicial(usuario) {
  if (usuario.precisa_trocar_senha) return '/trocar-senha'
  return usuario.papel === 'administradora' ? '/admin' : '/painel'
}
