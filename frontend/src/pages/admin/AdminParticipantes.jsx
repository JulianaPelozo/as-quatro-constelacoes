import { useEffect, useId, useMemo, useState } from 'react'
import { admin } from '../../api'
import Confirmacao from '../../components/Confirmacao'
import Dialogo from '../../components/Dialogo'
import Esqueleto from '../../components/Esqueleto'
import './AdminParticipantes.css'

const FILTROS = [
  { valor: 'ativas', rotulo: 'Ativas' },
  { valor: 'desativadas', rotulo: 'Desativadas' },
  { valor: 'todas', rotulo: 'Todas' },
]

const DATA_HORA = new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short' })

const primeiroNome = (nome) => nome.trim().split(/\s+/)[0]

// Tira acentos e maiúsculas para a busca ("Zelia" encontra "Zélia")
const normalizar = (texto) =>
  texto.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()

function situacao(p) {
  if (!p.ativo) return { texto: 'Desativada', classe: 'desativada' }
  if (p.bloqueado) return { texto: 'Bloqueada por tentativas', classe: 'alerta' }
  if (p.precisa_trocar_senha) return { texto: 'Aguardando 1º acesso', classe: 'pendente' }
  return { texto: 'Ativa', classe: 'ativa' }
}

export default function AdminParticipantes() {
  const [participantes, setParticipantes] = useState(null)
  const [erroLista, setErroLista] = useState('')
  const [busca, setBusca] = useState('')
  const [filtro, setFiltro] = useState('ativas')
  // { tipo: 'criar' | 'editar' | 'desativar' | 'redefinir' | 'senha', participante, senha, nova }
  const [dialogo, setDialogo] = useState(null)
  const [aviso, setAviso] = useState('')

  useEffect(() => {
    admin
      .participantes()
      .then(({ participantes }) => setParticipantes(participantes))
      .catch((e) => setErroLista(e.message))
  }, [])

  function atualizarNaLista(participante) {
    setParticipantes((lista) => {
      const sem = lista.filter((p) => p.id !== participante.id)
      return [...sem, participante].sort((a, b) => a.nome.localeCompare(b.nome, 'pt-BR'))
    })
  }

  const fechar = () => setDialogo(null)

  const ativas = participantes?.filter((p) => p.ativo).length ?? 0
  const desativadas = (participantes?.length ?? 0) - ativas

  const visiveis = useMemo(() => {
    if (!participantes) return []
    const termo = normalizar(busca.trim())
    return participantes.filter((p) => {
      if (filtro === 'ativas' && !p.ativo) return false
      if (filtro === 'desativadas' && p.ativo) return false
      return !termo || normalizar(`${p.nome} ${p.email}`).includes(termo)
    })
  }, [participantes, busca, filtro])

  async function reativar(p) {
    try {
      const { participante } = await admin.editarParticipante(p.id, { ativo: true })
      atualizarNaLista(participante)
      setAviso(`A conta de ${participante.nome} foi reativada.`)
    } catch (e) {
      setAviso(e.message)
    }
  }

  return (
    <div className="participantes">
      <header className="pagina__topo">
        <div>
          <h1>Participantes</h1>
          {participantes && (
            <p className="pagina__sub">
              {ativas} {ativas === 1 ? 'ativa' : 'ativas'}
              {desativadas > 0 && ` · ${desativadas} ${desativadas === 1 ? 'desativada' : 'desativadas'}`}
            </p>
          )}
        </div>
        <button
          type="button"
          className="botao botao--principal"
          onClick={() => setDialogo({ tipo: 'criar' })}
        >
          <span aria-hidden="true">+</span> Adicionar participante
        </button>
      </header>

      <p className="pagina__aviso" role="status">
        <span key={aviso} className="aparecer">{aviso}</span>
      </p>

      {!participantes && !erroLista && <Esqueleto linhas={4} altura={76} />}

      {erroLista && <p className="alerta-erro" role="alert">{erroLista}</p>}

      {participantes && participantes.length > 0 && (
        <div className="ferramentas">
          <label className="busca">
            <span className="visualmente-oculto">Buscar por nome ou e-mail</span>
            <input
              type="search"
              placeholder="Buscar por nome ou e-mail"
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </label>
          <div className="segmentado" role="group" aria-label="Mostrar">
            {FILTROS.map((f) => (
              <button
                key={f.valor}
                type="button"
                aria-pressed={filtro === f.valor}
                onClick={() => setFiltro(f.valor)}
              >
                {f.rotulo}
              </button>
            ))}
          </div>
        </div>
      )}

      {participantes && participantes.length === 0 && (
        <div className="vazio">
          <p>Ainda não há participantes. Adicione a primeira para começar o círculo de leitura.</p>
        </div>
      )}

      {participantes && participantes.length > 0 && visiveis.length === 0 && (
        <div className="vazio">
          <p>Nenhuma participante encontrada com esses filtros.</p>
        </div>
      )}

      {visiveis.length > 0 && (
        <ul className="lista-participantes">
          {visiveis.map((p, i) => {
            const s = situacao(p)
            return (
              <li
                key={p.id}
                className={`participante surgir${p.ativo ? '' : ' participante--inativa'}`}
                style={{ '--i': i }}
              >
                <div className="participante__nome">
                  <strong>{p.nome}</strong>
                  <span>{p.email}</span>
                </div>
                <div className="participante__info">
                  <span className={`etiqueta etiqueta--${s.classe}`}>{s.texto}</span>
                  <span className="participante__acesso">
                    {p.ultimo_login_em
                      ? `Último acesso: ${DATA_HORA.format(new Date(p.ultimo_login_em))}`
                      : 'Nunca entrou'}
                  </span>
                </div>
                <div className="participante__acoes acoes-linha">
                  <button type="button" onClick={() => setDialogo({ tipo: 'editar', participante: p })}>
                    Editar<span className="visualmente-oculto"> {p.nome}</span>
                  </button>
                  {p.ativo ? (
                    <>
                      <button type="button" onClick={() => setDialogo({ tipo: 'redefinir', participante: p })}>
                        Nova senha<span className="visualmente-oculto"> para {p.nome}</span>
                      </button>
                      <button type="button" onClick={() => setDialogo({ tipo: 'desativar', participante: p })}>
                        Desativar<span className="visualmente-oculto"> {p.nome}</span>
                      </button>
                    </>
                  ) : (
                    <button type="button" onClick={() => reativar(p)}>
                      Reativar<span className="visualmente-oculto"> {p.nome}</span>
                    </button>
                  )}
                </div>
              </li>
            )
          })}
        </ul>
      )}

      <Dialogo
        aberto={dialogo?.tipo === 'criar' || dialogo?.tipo === 'editar'}
        aoFechar={fechar}
        titulo={dialogo?.tipo === 'editar' ? 'Editar participante' : 'Adicionar participante'}
      >
        <FormParticipante
          participante={dialogo?.participante}
          aoCancelar={fechar}
          aoSalvar={(resposta) => {
            atualizarNaLista(resposta.participante)
            if (resposta.senha_temporaria) {
              setDialogo({ tipo: 'senha', participante: resposta.participante, senha: resposta.senha_temporaria, nova: true })
            } else {
              setAviso(`Os dados de ${resposta.participante.nome} foram salvos.`)
              fechar()
            }
          }}
        />
      </Dialogo>

      <Dialogo aberto={dialogo?.tipo === 'desativar'} aoFechar={fechar} titulo="Desativar conta?">
        {dialogo?.tipo === 'desativar' && (
          <Confirmacao
            texto={`${dialogo.participante.nome} não vai conseguir entrar no site até a conta ser reativada. Se estiver com o site aberto, a sessão é encerrada na hora. Os dados e o histórico continuam guardados.`}
            botao="Desativar"
            perigo
            aoCancelar={fechar}
            aoConfirmar={async () => {
              const { participante } = await admin.editarParticipante(dialogo.participante.id, { ativo: false })
              atualizarNaLista(participante)
              setAviso(`A conta de ${participante.nome} foi desativada.`)
              fechar()
            }}
          />
        )}
      </Dialogo>

      <Dialogo aberto={dialogo?.tipo === 'redefinir'} aoFechar={fechar} titulo="Gerar nova senha?">
        {dialogo?.tipo === 'redefinir' && (
          <Confirmacao
            texto={`A senha atual de ${dialogo.participante.nome} vai parar de funcionar. Você vai receber uma senha temporária para enviar a ela, e ela vai precisar trocá-la no próximo acesso. Se a conta estiver bloqueada por tentativas erradas, ela é desbloqueada.`}
            botao="Gerar nova senha"
            aoCancelar={fechar}
            aoConfirmar={async () => {
              const resposta = await admin.redefinirSenha(dialogo.participante.id)
              atualizarNaLista(resposta.participante)
              setDialogo({ tipo: 'senha', participante: resposta.participante, senha: resposta.senha_temporaria, nova: false })
            }}
          />
        )}
      </Dialogo>

      <Dialogo
        aberto={dialogo?.tipo === 'senha'}
        aoFechar={fechar}
        titulo={dialogo?.nova ? 'Conta criada!' : 'Nova senha gerada'}
      >
        {dialogo?.tipo === 'senha' && (
          <SenhaTemporaria
            participante={dialogo.participante}
            senha={dialogo.senha}
            nova={dialogo.nova}
            aoFechar={fechar}
          />
        )}
      </Dialogo>
    </div>
  )
}

function FormParticipante({ participante, aoSalvar, aoCancelar }) {
  const editando = Boolean(participante)
  const [nome, setNome] = useState(participante?.nome ?? '')
  const [email, setEmail] = useState(participante?.email ?? '')
  const [erro, setErro] = useState('')
  const [salvando, setSalvando] = useState(false)
  const id = useId()

  async function enviar(evento) {
    evento.preventDefault()
    setErro('')
    if (!nome.trim() || !email.trim()) {
      setErro('Preencha o nome e o e-mail.')
      return
    }
    setSalvando(true)
    try {
      const dados = { nome: nome.trim(), email: email.trim() }
      const resposta = editando
        ? await admin.editarParticipante(participante.id, dados)
        : await admin.criarParticipante(dados)
      aoSalvar(resposta)
    } catch (e) {
      setErro(e.message)
      setSalvando(false)
    }
  }

  return (
    <form onSubmit={enviar} noValidate>
      {erro && <p className="dialogo__erro" role="alert">{erro}</p>}
      <div className="campo">
        <label htmlFor={`${id}-nome`}>Nome</label>
        <input
          id={`${id}-nome`}
          autoComplete="off"
          autoFocus
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          maxLength={120}
        />
      </div>
      <div className="campo">
        <label htmlFor={`${id}-email`}>E-mail</label>
        <input
          id={`${id}-email`}
          type="email"
          inputMode="email"
          autoComplete="off"
          autoCapitalize="none"
          spellCheck="false"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      {!editando && (
        <p className="dialogo__texto">
          O site vai gerar uma senha temporária para você enviar à participante.
        </p>
      )}
      <div className="dialogo__acoes">
        <button type="button" className="botao botao--secundario" onClick={aoCancelar}>
          Cancelar
        </button>
        <button type="submit" className="botao botao--principal" disabled={salvando}>
          {salvando ? 'Salvando…' : editando ? 'Salvar' : 'Criar conta'}
        </button>
      </div>
    </form>
  )
}

function SenhaTemporaria({ participante, senha, nova, aoFechar }) {
  const [copiado, setCopiado] = useState('')
  const endereco = `${window.location.origin}/entrar`
  const mensagem = [
    `Olá, ${primeiroNome(participante.nome)}! ${
      nova
        ? 'Sua conta no site da Constelação Literária está pronta.'
        : 'Sua senha do site da Constelação Literária foi redefinida.'
    }`,
    '',
    `Endereço: ${endereco}`,
    `E-mail: ${participante.email}`,
    `Senha temporária: ${senha}`,
    '',
    'Ao entrar, o site vai pedir para você criar uma senha só sua.',
  ].join('\n')

  async function copiar(texto, qual) {
    try {
      await navigator.clipboard.writeText(texto)
      setCopiado(qual)
    } catch {
      setCopiado('erro')
    }
  }

  return (
    <>
      <p className="dialogo__texto">
        Envie a senha temporária para <strong>{participante.nome}</strong>.{' '}
        <strong>Ela não vai aparecer de novo</strong>: se perder, é só gerar outra.
      </p>

      <div className="senha-temporaria">
        <code>{senha}</code>
        <button type="button" className="botao botao--secundario" onClick={() => copiar(senha, 'senha')}>
          Copiar senha
        </button>
      </div>

      <label className="campo mensagem-pronta">
        <span>Mensagem pronta para enviar (WhatsApp, Instagram…)</span>
        <textarea readOnly value={mensagem} rows={8} onFocus={(e) => e.target.select()} />
      </label>

      <p className="dialogo__copiado" role="status">
        {copiado === 'senha' && 'Senha copiada.'}
        {copiado === 'mensagem' && 'Mensagem copiada.'}
        {copiado === 'erro' && 'Não deu para copiar automaticamente. Selecione o texto e copie.'}
      </p>

      <div className="dialogo__acoes">
        <button type="button" className="botao botao--secundario" onClick={() => copiar(mensagem, 'mensagem')}>
          Copiar mensagem
        </button>
        <button type="button" className="botao botao--principal" onClick={aoFechar}>
          Pronto
        </button>
      </div>
    </>
  )
}
