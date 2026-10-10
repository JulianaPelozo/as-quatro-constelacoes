// Chamadas ao backend Flask. O cookie de sessão vai junto automaticamente,
// porque front e back estão no mesmo endereço.

async function chamar(caminho, { metodo = 'GET', corpo } = {}) {
  let resposta
  try {
    resposta = await fetch(`/api${caminho}`, {
      method: metodo,
      credentials: 'same-origin',
      headers: corpo ? { 'Content-Type': 'application/json' } : undefined,
      body: corpo ? JSON.stringify(corpo) : undefined,
    })
  } catch {
    throw new ErroApi('Não foi possível conectar. Confira sua internet e tente de novo.', 0)
  }

  if (resposta.status === 204) return null
  const dados = await resposta.json().catch(() => ({}))
  if (!resposta.ok) {
    throw new ErroApi(dados.erro || 'Algo deu errado. Tente de novo em instantes.', resposta.status)
  }
  return dados
}

export class ErroApi extends Error {
  constructor(mensagem, status) {
    super(mensagem)
    this.status = status
  }
}

export const auth = {
  entrar: (email, senha, lembrar) =>
    chamar('/auth/login', { metodo: 'POST', corpo: { email, senha, lembrar } }),
  sair: () => chamar('/auth/logout', { metodo: 'POST' }),
  eu: () => chamar('/auth/eu'),
}
