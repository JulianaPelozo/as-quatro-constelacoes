import { useEffect, useState } from 'react'
import { Link } from 'react-router'
import { admin } from '../../api'
import { useAuth } from '../../auth'
import './AdminInicio.css'

const DATA_POR_EXTENSO = new Intl.DateTimeFormat('pt-BR', {
  weekday: 'long',
  day: 'numeric',
  month: 'long',
})

function dataDeHoje(data) {
  const texto = DATA_POR_EXTENSO.format(data)
  return texto.charAt(0).toUpperCase() + texto.slice(1)
}

function primeiroNome(nome) {
  return nome.trim().split(/\s+/)[0]
}

export default function AdminInicio() {
  const { usuario } = useAuth()
  const [resumo, setResumo] = useState(null)
  const [erro, setErro] = useState('')
  const [hoje] = useState(() => new Date())

  useEffect(() => {
    admin
      .resumo()
      .then(setResumo)
      .catch((e) => setErro(e.message))
  }, [])

  const contas = resumo?.contas

  // Roteiro para colocar o círculo de leitura de pé (RF-10)
  const passos = [
    {
      titulo: 'Criar as contas das participantes',
      feito: contas ? contas.participantes > 0 : false,
      detalhe: <Link to="/admin/participantes">Ir para Participantes</Link>,
    },
    {
      titulo: 'Cadastrar as histórias e os capítulos',
      feito: resumo ? resumo.circulo.capitulos > 0 : false,
      detalhe: <Link to="/admin/historias">Ir para Histórias</Link>,
    },
    { titulo: 'Montar o cronograma de leitura', detalhe: 'Em breve.' },
    { titulo: 'Definir as metas de comentários', detalhe: 'Em breve.' },
  ]

  return (
    <div className="inicio">
      <header className="inicio__topo">
        <p className="inicio__data">{dataDeHoje(hoje)}</p>
        <h1>Olá, {primeiroNome(usuario.nome)}!</h1>
        <p className="inicio__sub">Este é o painel da administradora.</p>
      </header>

      <section aria-labelledby="titulo-contas" className="inicio__secao">
        <h2 id="titulo-contas">Contas</h2>
        {erro ? (
          <p className="inicio__erro" role="alert">{erro}</p>
        ) : (
          <dl className="numeros" aria-busy={!contas}>
            <Numero rotulo="Participantes ativas" valor={contas?.participantes} destaque />
            <Numero rotulo="Autoras" valor={contas?.autoras} />
            <Numero rotulo="Administradoras" valor={contas?.administradoras} />
            <Numero rotulo="Contas desativadas" valor={contas?.desativadas} />
          </dl>
        )}
      </section>

      <section aria-labelledby="titulo-semana" className="inicio__secao">
        <h2 id="titulo-semana">Círculo de leitura nesta semana</h2>
        <div className="vazio">
          <p>
            Assim que o cronograma estiver montado, aqui você vai ver quem já cumpriu a meta do dia e
            da semana, sem precisar conferir no Wattpad.
          </p>
        </div>
      </section>

      <section aria-labelledby="titulo-passos" className="inicio__secao">
        <h2 id="titulo-passos">Primeiros passos</h2>
        <ol className="passos">
          {passos.map((passo, i) => (
            <li key={passo.titulo} className={passo.feito ? 'passo passo--feito' : 'passo'}>
              <span className="passo__marcador" aria-hidden="true">
                {passo.feito ? '✓' : i + 1}
              </span>
              <div>
                <p className="passo__titulo">
                  {passo.titulo}
                  {passo.feito && <span className="visualmente-oculto"> (concluído)</span>}
                </p>
                <p className="passo__detalhe">{passo.detalhe}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>
    </div>
  )
}

function Numero({ rotulo, valor, destaque }) {
  return (
    <div className={destaque ? 'numero numero--destaque' : 'numero'}>
      <dt>{rotulo}</dt>
      <dd>{valor ?? '–'}</dd>
    </div>
  )
}
