# ✨ Constelação Literária — Site

> **Rascunho** — este README será atualizado conforme o projeto evoluir.

Site do coletivo **Constelação Literária**: uma extensão das nossas redes sociais que reúne conteúdos, materiais e recursos para escritoras. Mais do que uma página de apresentação, a ideia é ser um espaço de **aprendizado, divulgação e apoio**.

É um projeto **sem fins lucrativos**, feito para incentivar a leitura e a escrita.

## Seções planejadas

| Seção | O que tem |
|-------|-----------|
| 📚 **Biblioteca de conteúdos** | Dicas de português, gramática, pontuação, escrita criativa, personagens, enredo e capítulos |
| 🎨 **Espaço criativo** | Criação de capas, identidade visual, banners e recursos para apresentar as obras |
| 📣 **Marketing literário** | Divulgação no Instagram, TikTok e Wattpad, estratégias para atrair leitores e ideias de posts |
| 📖 **Vitrine de histórias** | Obras das integrantes, com sinopses e links para o Wattpad |
| 🎁 **Dicas e materiais gratuitos** | Guias, modelos e checklists para download |
| 📅 **Círculo de leitura** *(nome provisório)* | Área das participantes: capítulo do dia, registro de leituras e comentários e acompanhamento das metas |
| 🌟 **Conheça as autoras** | Quem está por trás do projeto, suas especialidades e trabalhos |
| 🛠️ **Serviços das integrantes** *(futuro)* | Capas, revisão textual, identidade visual e mais |

## Status do projeto

🚧 **Fase atual: levantamento de requisitos.**

O site será construído aos poucos, em fases:

1. **Fase 1** — Presença básica: página inicial e "Conheça as autoras"
2. **Fase 2** — Área administrativa e círculo de leitura (2a); conteúdos, Vitrine e materiais gratuitos (2b)
3. **Fase 3** — Busca, destaques, compartilhamento e outras melhorias
4. **Fase 4** — Serviços das integrantes

Detalhes em [docs/requisitos/04-roadmap.md](docs/requisitos/04-roadmap.md).

## Documentação

- [Visão geral](docs/requisitos/01-visao-geral.md)
- [Requisitos funcionais](docs/requisitos/02-requisitos-funcionais.md)
- [Requisitos não funcionais](docs/requisitos/03-requisitos-nao-funcionais.md)
- [Roadmap](docs/requisitos/04-roadmap.md)
- [Questões em aberto](docs/requisitos/05-questoes-em-aberto.md)

Para navegar por todos os requisitos com filtros (fase, prioridade, módulo, busca), abra [docs/requisitos.html](docs/requisitos.html) no navegador. Ele é gerado a partir dos `.md`: depois de editar algum deles, rode `python3 scripts/gerar_html_requisitos.py`.

## Tecnologias

| Parte | Tecnologia | Pasta |
|-------|------------|-------|
| Back-end (API) | Python 3.12, Flask, SQLAlchemy, Flask-Migrate, Flask-Login | [backend/](backend/) |
| Front-end | React + Vite | [frontend/](frontend/) |
| Banco de dados | PostgreSQL (Supabase em produção); SQLite no desenvolvimento, se nenhum banco for configurado | — |
| Hospedagem prevista | Vercel (plano gratuito) | — |

## Como executar localmente

São dois terminais: um para o back-end e outro para o front-end.

**1. Back-end** (Flask, em `http://127.0.0.1:5000`)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env          # ajuste se quiser usar Postgres
export FLASK_APP=app
flask db upgrade              # cria/atualiza as tabelas
flask criar-usuario           # cria sua conta de administradora (pede nome, e-mail e senha)
flask run
```

**2. Front-end** (React, em `http://localhost:5173`)

```bash
cd frontend
npm install
npm run dev
```

Abra `http://localhost:5173`. O Vite repassa as chamadas `/api` para o Flask.

**Testes do back-end:** `cd backend && .venv/bin/pytest`

**Usar o Postgres local em vez do SQLite** (opcional):

```bash
sudo -u postgres createuser --pwprompt constelacao
sudo -u postgres createdb -O constelacao constelacao
# no backend/.env:
# DATABASE_URL=postgresql://constelacao:SUA_SENHA@localhost:5432/constelacao
```

> ⚠️ **Toda tabela nova precisa de RLS** (RNF-28). Nas migrations, depois do `create_table`, adicione `op.execute('ALTER TABLE <tabela> ENABLE ROW LEVEL SECURITY')` dentro de um `if` para Postgres. O teste `tests/test_migrations.py` falha se você esquecer.

## Como contribuir

*A definir.*

## Licença

Distribuído sob a licença descrita em [LICENSE](LICENSE).
