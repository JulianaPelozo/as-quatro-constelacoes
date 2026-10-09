# 03 — Requisitos Não Funcionais

## Usabilidade e acessibilidade

| ID | Requisito |
|----|-----------|
| RNF-01 | **Mobile first:** o site deve funcionar bem em celulares, já que a maior parte do público virá de links nas redes sociais e as participantes do círculo de leitura vão registrar a leitura diária pelo celular. Deve ser responsivo de 360px de largura até desktop. |
| RNF-02 | Seguir as diretrizes **WCAG 2.1 nível AA**: contraste adequado, textos alternativos em imagens, navegação por teclado, fontes legíveis. |
| RNF-03 | Todo o conteúdo e a interface devem estar em **português do Brasil**. |
| RNF-04 | A área administrativa deve ser utilizável por pessoas sem conhecimento técnico (sem HTML, sem Markdown obrigatório). |
| RNF-05 | Qualquer conteúdo deve ser alcançável em no máximo **3 cliques** a partir da página inicial. |

## Identidade visual

| ID | Requisito |
|----|-----------|
| RNF-06 | O visual deve ser coerente com a identidade das redes sociais do coletivo (cores, logo, tipografia). |
| RNF-07 | Deve existir um guia de estilo mínimo (paleta de cores, fontes, componentes) antes do desenvolvimento das telas. |

## Desempenho

| ID | Requisito |
|----|-----------|
| RNF-08 | As páginas públicas devem carregar em até **3 segundos** em conexão 4G. |
| RNF-09 | Imagens enviadas devem ser otimizadas automaticamente (redimensionamento/compressão). |
| RNF-10 | Arquivos de materiais para download devem ter limite de tamanho (sugestão: 20 MB). |

## Segurança e privacidade

| ID | Requisito |
|----|-----------|
| RNF-11 | Todo o site deve ser servido via **HTTPS**. |
| RNF-12 | Senhas devem ser armazenadas com hash seguro; nunca em texto puro. |
| RNF-13 | A área administrativa deve ser protegida contra acessos não autorizados (autenticação, limite de tentativas de login). |
| RNF-14 | Cumprir a **LGPD**: política de privacidade publicada, coleta mínima de dados pessoais, consentimento em formulários. |
| RNF-15 | Uploads devem aceitar apenas tipos de arquivo permitidos (imagens e PDF, inicialmente). |
| RNF-16 | Fotos e dados das integrantes só podem ser publicados com autorização delas. |
| RNF-25 | Participantes do círculo de leitura devem ser informadas, antes de começar, de quais dados de atividade são registrados, quem pode vê-los e por quanto tempo são guardados, e devem dar consentimento (LGPD). |
| RNF-26 | Os dados de desempenho de cada participante devem ser visíveis apenas para ela e para as administradoras, salvo decisão diferente do coletivo (ver questões em aberto). |
| RNF-27 | O site **nunca** deve pedir nem armazenar a senha do Wattpad das participantes, nem automatizar o acesso ao Wattpad em nome delas. |
| RNF-28 | O banco de dados só pode ser acessado pelo back-end do site. Se o serviço de hospedagem do banco gerar uma API pública automática para as tabelas (ex.: a *Data API* do Supabase), ela deve ser **desativada**, ou **todas** as tabelas devem ter **RLS (Row Level Security)** ativado, sem políticas que liberem acesso anônimo. Isso vale para cada tabela nova, e deve ser conferido antes de cada publicação. |
| RNF-29 | Credenciais (senha e endereço de conexão do banco, chaves de API, chaves de serviço) devem ficar apenas em variáveis de ambiente do servidor, **nunca** no repositório nem no código do front-end. |

## Visibilidade (SEO e compartilhamento)

| ID | Requisito |
|----|-----------|
| RNF-17 | Cada página deve ter título e descrição próprios para mecanismos de busca. |
| RNF-18 | Links compartilhados nas redes devem exibir prévia com imagem, título e descrição (Open Graph). |
| RNF-19 | URLs devem ser legíveis (ex.: `/biblioteca/pontuacao/uso-da-virgula`). |

## Manutenibilidade e operação

| ID | Requisito |
|----|-----------|
| RNF-20 | A arquitetura deve permitir adicionar novas seções e funcionalidades de forma incremental, sem reescrever o que já existe. |
| RNF-21 | O código deve ser versionado no GitHub, com README e instruções de execução local. |
| RNF-22 | Deve haver backup periódico do banco de dados e dos arquivos enviados. |
| RNF-23 | O custo de hospedagem deve ser **baixo ou gratuito**. Por ser um projeto **sem fins lucrativos**, devem ser priorizadas soluções gratuitas ou de baixo custo (hospedagem, envio de e-mails, domínio). |
| RNF-24 | Funcionalidades principais devem ter testes automatizados. Isso inclui o cálculo de cumprimento das metas (RF-10.9). |
