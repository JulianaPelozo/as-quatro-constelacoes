import { useId, useRef, useState } from 'react'
import { useNavigate } from 'react-router'
import { auth } from '../api'
import { rotaInicial, useAuth } from '../auth'
import BotaoTema from '../components/BotaoTema'
import Logo from '../components/Logo'
import './Acesso.css'

const SENHA_MIN = 8

export default function TrocarSenha() {
  const { usuario, setUsuario, sair } = useAuth()
  const navegar = useNavigate()
  const temporaria = usuario.precisa_trocar_senha

  const [atual, setAtual] = useState('')
  const [nova, setNova] = useState('')
  const [repetida, setRepetida] = useState('')
  const [mostrar, setMostrar] = useState(false)
  const [erros, setErros] = useState({})
  const [erroGeral, setErroGeral] = useState('')
  const [enviando, setEnviando] = useState(false)

  const id = useId()
  const refs = { atual: useRef(null), nova: useRef(null), repetida: useRef(null) }

  function validar() {
    const e = {}
    if (!atual) e.atual = temporaria ? 'Informe a senha temporária.' : 'Informe sua senha atual.'
    if (nova.length < SENHA_MIN) e.nova = `A nova senha precisa ter pelo menos ${SENHA_MIN} caracteres.`
    else if (nova === atual) e.nova = 'A nova senha precisa ser diferente da atual.'
    if (!e.nova && repetida !== nova) e.repetida = 'As senhas não são iguais.'
    return e
  }

  async function enviar(evento) {
    evento.preventDefault()
    setErroGeral('')
    const e = validar()
    setErros(e)
    const primeiro = ['atual', 'nova', 'repetida'].find((campo) => e[campo])
    if (primeiro) return refs[primeiro].current.focus()

    setEnviando(true)
    try {
      const { usuario: atualizado } = await auth.trocarSenha(atual, nova)
      setUsuario(atualizado)
      navegar(rotaInicial(atualizado), { replace: true })
    } catch (erro) {
      setErroGeral(erro.message)
      setAtual('')
      refs.atual.current.focus()
    } finally {
      setEnviando(false)
    }
  }

  const campo = (nome, rotulo, valor, setValor, autoComplete, dica) => (
    <div className="campo">
      <label htmlFor={`${id}-${nome}`}>{rotulo}</label>
      <input
        ref={refs[nome]}
        id={`${id}-${nome}`}
        type={mostrar ? 'text' : 'password'}
        autoComplete={autoComplete}
        value={valor}
        onChange={(e) => setValor(e.target.value)}
        aria-invalid={Boolean(erros[nome])}
        aria-describedby={[dica && `${id}-${nome}-dica`, erros[nome] && `${id}-${nome}-erro`]
          .filter(Boolean)
          .join(' ') || undefined}
      />
      {dica && <p id={`${id}-${nome}-dica`} className="campo__dica">{dica}</p>}
      {erros[nome] && <p id={`${id}-${nome}-erro`} className="campo__erro">{erros[nome]}</p>}
    </div>
  )

  return (
    <div className="acesso">
      <div className="acesso__ceu" aria-hidden="true" />
      <div className="acesso__topo">
        <BotaoTema />
      </div>

      <main className="acesso__conteudo">
        <header className="acesso__marca">
          <Logo tamanho={64} />
          <p className="acesso__nome">Constelação Literária</p>
        </header>

        <section className="acesso__cartao" aria-labelledby={`${id}-titulo`}>
          <h1 id={`${id}-titulo`} className="acesso__titulo">
            {temporaria ? 'Crie sua senha' : 'Trocar senha'}
          </h1>
          <p className="acesso__subtitulo">
            {temporaria
              ? `Boas-vindas, ${usuario.nome.split(' ')[0]}! Antes de continuar, troque a senha temporária por uma só sua.`
              : 'Escolha uma senha nova para sua conta.'}
          </p>

          {erroGeral && <div className="acesso__alerta" role="alert">{erroGeral}</div>}

          <form onSubmit={enviar} noValidate>
            {/* Ajuda gerenciadores de senha a saber de qual conta é */}
            <input type="email" autoComplete="username" value={usuario.email} readOnly hidden />
            {campo('atual', temporaria ? 'Senha temporária' : 'Senha atual', atual, setAtual, 'current-password')}
            {campo('nova', 'Nova senha', nova, setNova, 'new-password', `Pelo menos ${SENHA_MIN} caracteres.`)}
            {campo('repetida', 'Repita a nova senha', repetida, setRepetida, 'new-password')}

            <label className="acesso__lembrar">
              <input type="checkbox" checked={mostrar} onChange={(e) => setMostrar(e.target.checked)} />
              Mostrar senhas
            </label>

            <button type="submit" className="acesso__botao" disabled={enviando}>
              {enviando ? 'Salvando…' : 'Salvar nova senha'}
            </button>
          </form>

          <p className="acesso__ajuda">
            <button type="button" className="acesso__link" onClick={sair}>
              Sair
            </button>
          </p>
        </section>
      </main>
    </div>
  )
}
