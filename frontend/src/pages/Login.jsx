import { useId, useRef, useState } from 'react'
import { auth } from '../api'
import Logo from '../components/Logo'
import BotaoTema from '../components/BotaoTema'
import './Login.css'

const EMAIL_VALIDO = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validar(email, senha) {
  const erros = {}
  if (!email.trim()) erros.email = 'Informe seu e-mail.'
  else if (!EMAIL_VALIDO.test(email.trim())) erros.email = 'Confira o e-mail: parece incompleto.'
  if (!senha) erros.senha = 'Informe sua senha.'
  return erros
}

export default function Login({ aoEntrar }) {
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [lembrar, setLembrar] = useState(false)
  const [mostrarSenha, setMostrarSenha] = useState(false)
  const [errosCampos, setErrosCampos] = useState({})
  const [erroGeral, setErroGeral] = useState('')
  const [enviando, setEnviando] = useState(false)

  const id = useId()
  const refEmail = useRef(null)
  const refSenha = useRef(null)

  async function enviar(evento) {
    evento.preventDefault()
    setErroGeral('')

    const erros = validar(email, senha)
    setErrosCampos(erros)
    if (erros.email) return refEmail.current.focus()
    if (erros.senha) return refSenha.current.focus()

    setEnviando(true)
    try {
      const { usuario } = await auth.entrar(email.trim(), senha, lembrar)
      aoEntrar(usuario)
    } catch (erro) {
      setErroGeral(erro.message)
      setSenha('')
      refSenha.current.focus()
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="login">
      <div className="login__ceu" aria-hidden="true" />

      <div className="login__topo">
        <BotaoTema />
      </div>

      <main className="login__conteudo">
        <header className="login__marca">
          <Logo tamanho={64} />
          <p className="login__nome">Constelação Literária</p>
        </header>

        <section className="login__cartao" aria-labelledby={`${id}-titulo`}>
          <h1 id={`${id}-titulo`} className="login__titulo">Entrar</h1>
          <p className="login__subtitulo">Área das integrantes e participantes do círculo de leitura.</p>

          {erroGeral && (
            <div className="login__alerta" role="alert">
              {erroGeral}
            </div>
          )}

          <form onSubmit={enviar} noValidate>
            <div className="campo">
              <label htmlFor={`${id}-email`}>E-mail</label>
              <input
                ref={refEmail}
                id={`${id}-email`}
                type="email"
                inputMode="email"
                autoComplete="username"
                autoCapitalize="none"
                spellCheck="false"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                aria-invalid={Boolean(errosCampos.email)}
                aria-describedby={errosCampos.email ? `${id}-email-erro` : undefined}
              />
              {errosCampos.email && (
                <p id={`${id}-email-erro`} className="campo__erro">{errosCampos.email}</p>
              )}
            </div>

            <div className="campo">
              <label htmlFor={`${id}-senha`}>Senha</label>
              <div className="campo__senha">
                <input
                  ref={refSenha}
                  id={`${id}-senha`}
                  type={mostrarSenha ? 'text' : 'password'}
                  autoComplete="current-password"
                  value={senha}
                  onChange={(e) => setSenha(e.target.value)}
                  aria-invalid={Boolean(errosCampos.senha)}
                  aria-describedby={errosCampos.senha ? `${id}-senha-erro` : undefined}
                />
                <button
                  type="button"
                  className="campo__mostrar"
                  onClick={() => setMostrarSenha((v) => !v)}
                  aria-pressed={mostrarSenha}
                  aria-controls={`${id}-senha`}
                >
                  {mostrarSenha ? 'Ocultar' : 'Mostrar'}
                  <span className="visualmente-oculto"> senha</span>
                </button>
              </div>
              {errosCampos.senha && (
                <p id={`${id}-senha-erro`} className="campo__erro">{errosCampos.senha}</p>
              )}
            </div>

            <label className="login__lembrar">
              <input
                type="checkbox"
                checked={lembrar}
                onChange={(e) => setLembrar(e.target.checked)}
              />
              Lembrar de mim neste aparelho
            </label>

            <button type="submit" className="login__botao" disabled={enviando}>
              {enviando ? 'Entrando…' : 'Entrar'}
            </button>
          </form>

          <p className="login__ajuda">
            Esqueceu a senha ou ainda não tem conta? Fale com uma administradora do coletivo.
          </p>
        </section>
      </main>
    </div>
  )
}
