# 02 — Requisitos Funcionais

**Prioridade (MoSCoW):**
- **M** — *Must* (obrigatório para a fase em que está previsto)
- **S** — *Should* (importante, mas pode esperar um pouco)
- **C** — *Could* (desejável)
- **W** — *Won't (por agora)* — registrado para o futuro

A coluna **Fase** refere-se ao [roadmap](04-roadmap.md).

---

## RF-00 — Estrutura geral e navegação

| ID | Requisito | Prioridade | Fase |
|----|-----------|:---:|:---:|
| RF-00.1 | O site deve ter um menu de navegação com acesso a todas as seções publicadas. | M | 1 |
| RF-00.2 | O site deve ter uma página inicial que apresente o coletivo e destaque as seções e os conteúdos mais recentes. | M | 1 |
| RF-00.3 | Todas as páginas devem exibir links para as redes sociais do coletivo (Instagram, TikTok, Wattpad). | M | 1 |
| RF-00.4 | O rodapé deve conter informações de contato do coletivo. | M | 1 |
| RF-00.5 | O visitante deve poder buscar conteúdos por palavra-chave em todo o site. | S | 3 |
| RF-00.6 | Cada conteúdo/obra deve ter um botão para compartilhar o link nas redes sociais. | C | 3 |

## RF-01 — Biblioteca de conteúdos

Dicas de português, gramática, pontuação, escrita criativa, construção de personagens, enredos e desenvolvimento de capítulos.

| ID | Requisito | Prioridade | Fase |
|----|-----------|:---:|:---:|
| RF-01.1 | Exibir a lista de conteúdos da Biblioteca, do mais recente para o mais antigo. | M | 2 |
| RF-01.2 | Organizar os conteúdos por categorias. Categorias iniciais: *Português e gramática*, *Pontuação*, *Escrita criativa*, *Personagens*, *Enredo*, *Capítulos*. | M | 2 |
| RF-01.3 | Permitir filtrar a lista por categoria. | M | 2 |
| RF-01.4 | Cada conteúdo deve ter página própria com título, autora, data, categoria, texto formatado e, opcionalmente, imagens. | M | 2 |
| RF-01.5 | Permitir incorporar ou linkar o post/vídeo original das redes sociais dentro do conteúdo. | S | 2 |
| RF-01.6 | Exibir “conteúdos relacionados” (mesma categoria) ao final de cada conteúdo. | C | 3 |
| RF-01.7 | Permitir marcar conteúdos com tags livres (além da categoria). | C | 3 |

## RF-02 — Espaço criativo

Dicas de criação de capas, identidade visual, banners e outros recursos de apresentação das obras.

| ID | Requisito | Prioridade | Fase |
|----|-----------|:---:|:---:|
| RF-02.1 | Exibir lista de conteúdos do Espaço criativo, com o mesmo modelo de conteúdo da Biblioteca (RF-01.4). | M | 2 |
| RF-02.2 | Categorias iniciais: *Capas*, *Identidade visual*, *Banners*, *Outros recursos*. | M | 2 |
| RF-02.3 | Permitir galeria de imagens dentro do conteúdo (ex.: exemplos de capas, antes/depois). | S | 2 |
| RF-02.4 | Permitir listar links para ferramentas externas recomendadas (ex.: editores de imagem, bancos de fontes). | C | 3 |

## RF-03 — Marketing literário

Divulgação no Instagram, TikTok e Wattpad, estratégias para atrair leitores e ideias de publicações para quem ainda não tem livros publicados.

| ID | Requisito | Prioridade | Fase |
|----|-----------|:---:|:---:|
| RF-03.1 | Exibir lista de conteúdos de Marketing literário, com o mesmo modelo de conteúdo da Biblioteca (RF-01.4). | M | 2 |
| RF-03.2 | Categorias iniciais: *Instagram*, *TikTok*, *Wattpad*, *Estratégias para atrair leitores*, *Ideias de posts para quem ainda não publicou*. | M | 2 |
| RF-03.3 | Permitir filtrar por plataforma (Instagram, TikTok, Wattpad). | S | 2 |

> **Nota de engenharia:** RF-01, RF-02 e RF-03 compartilham a mesma estrutura (“seção de conteúdos com categorias”). A solução deve tratá-las de forma genérica, para que novas seções possam ser criadas sem novo desenvolvimento.

## RF-04 — Vitrine de histórias

Divulgar as obras das integrantes, com sinopses e links do Wattpad.

| ID | Requisito | Prioridade | Fase |
|----|-----------|:---:|:---:|
| RF-04.1 | Exibir as obras em formato de vitrine (cards com capa, título e autora). | M | 2 |
| RF-04.2 | Cada obra deve ter página própria com: capa, título, autora, sinopse, gênero(s), classificação indicativa, status (em andamento / concluída) e link(s) externo(s) (Wattpad, Amazon etc.). | M | 2 |
| RF-04.3 | Permitir filtrar obras por gênero e por autora. | S | 2 |
| RF-04.4 | A página da obra deve linkar para o perfil da autora em “Conheça as autoras”. | M | 2 |
| RF-04.5 | Permitir destacar obras na página inicial (“obra em destaque” / “lançamento”). | S | 3 |
| RF-04.6 | Exibir alertas de conteúdo (gatilhos) quando informados pela autora. | S | 2 |
| RF-04.7 | Permitir exibir obras de escritoras **convidadas** (não integrantes). | W | — |

## RF-05 — Dicas e materiais gratuitos

Guias, modelos, listas de verificação e outros materiais.

| ID | Requisito | Prioridade | Fase |
|----|-----------|:---:|:---:|
| RF-05.1 | Exibir lista de materiais com título, descrição curta, tipo (*Guia*, *Modelo*, *Checklist*, *Outro*) e imagem de prévia. | M | 2 |
| RF-05.2 | Permitir baixar o material (PDF ou outro formato) sem necessidade de cadastro. | M | 2 |
| RF-05.3 | Permitir que o material seja um link externo (ex.: modelo no Google Docs/Canva) em vez de arquivo. | S | 2 |
| RF-05.4 | Filtrar materiais por tipo e por tema. | S | 3 |
| RF-05.5 | Contabilizar o número de downloads de cada material (visível apenas para administradoras). | C | 3 |

## RF-06 — Conheça as autoras

| ID | Requisito | Prioridade | Fase |
|----|-----------|:---:|:---:|
| RF-06.1 | Exibir página com todas as integrantes (foto, nome/pseudônimo, especialidades). | M | 1 |
| RF-06.2 | Cada integrante deve ter perfil com: foto, nome/pseudônimo, minibiografia, especialidades, redes sociais e lista de obras (vindas da Vitrine). | M | 1 (obras na 2) |
| RF-06.3 | O perfil deve listar os conteúdos escritos pela integrante. | S | 2 |
| RF-06.4 | O perfil deve exibir os serviços oferecidos pela integrante (ver RF-08). | W | 4 |

## RF-07 — Área administrativa (gestão de conteúdo)

| ID | Requisito | Prioridade | Fase |
|----|-----------|:---:|:---:|
| RF-07.1 | Integrantes devem acessar uma área restrita com login e senha. | M | 2 |
| RF-07.2 | Administradoras devem poder criar, editar, despublicar e excluir conteúdos de qualquer seção. | M | 2 |
| RF-07.3 | O editor de conteúdo deve permitir texto formatado (títulos, negrito, itálico, listas, links, citações) e upload de imagens, sem exigir conhecimento técnico. | M | 2 |
| RF-07.4 | Permitir salvar conteúdo como **rascunho** antes de publicar. | M | 2 |
| RF-07.5 | Administradoras devem poder cadastrar e editar obras da Vitrine. | M | 2 |
| RF-07.6 | Administradoras devem poder cadastrar e editar materiais gratuitos (incluindo upload de arquivo). | M | 2 |
| RF-07.7 | Administradoras devem poder gerenciar categorias de cada seção. | S | 2 |
| RF-07.8 | Cada integrante deve poder editar o próprio perfil. | S | 2 |
| RF-07.9 | Perfis de acesso: **Administradora** (tudo) e **Autora** (apenas o próprio perfil, suas obras e seus conteúdos). O perfil **Participante** do círculo de leitura está descrito em RF-10.1. | S | 3 |
| RF-07.10 | Permitir agendar a publicação de um conteúdo para data/hora futura. | C | 3 |
| RF-07.11 | Permitir recuperação de senha por e-mail. | S | 2 |
| RF-07.12 | Contas criadas pela administradora (ou com senha redefinida por ela) recebem uma **senha temporária**, exibida uma única vez, e a pessoa é obrigada a trocá-la no próximo acesso. Assim nenhuma administradora conhece a senha de outra pessoa. Enquanto não houver recuperação por e-mail (RF-07.11), esse é o caminho para "esqueci minha senha". | M | 2 |

## RF-08 — Serviços das integrantes *(ideia futura)*

Criação de capas, revisão textual, identidade visual e outros serviços.

| ID | Requisito | Prioridade | Fase |
|----|-----------|:---:|:---:|
| RF-08.1 | Exibir catálogo de serviços, cada um com: tipo, descrição, integrante responsável, exemplos de trabalho (portfólio) e forma de contato. | W | 4 |
| RF-08.2 | Filtrar serviços por tipo (capa, revisão, identidade visual etc.). | W | 4 |
| RF-08.3 | O contato com a integrante deve ser feito por link externo (Instagram, WhatsApp, e-mail) ou formulário — **sem pagamento pelo site**. | W | 4 |

## RF-09 — Contato e engajamento

| ID | Requisito | Prioridade | Fase |
|----|-----------|:---:|:---:|
| RF-09.1 | Disponibilizar formulário de contato geral do coletivo. | S | 3 |
| RF-09.2 | Exibir os últimos posts do Instagram na página inicial. | C | 3 |
| RF-09.3 | Permitir cadastro de e-mail para newsletter. | W | — |

## RF-10 — Círculo de leitura *(nome provisório)*

As participantes se comprometem a ler, em cada dia da semana, um capítulo definido no cronograma e a comentar nele um número mínimo de vezes no Wattpad. O site organiza o cronograma, recebe os registros das participantes e calcula automaticamente quem cumpriu as metas, para que as administradoras não precisem fazer essa conferência à mão.

A leitura e os comentários continuam acontecendo **no Wattpad**. O site não verifica o Wattpad diretamente: cada participante **declara** o que fez, com evidência opcional (links dos comentários). As administradoras conferem por amostragem.

| ID | Requisito | Prioridade | Fase |
|----|-----------|:---:|:---:|
| RF-10.1 | Participantes devem acessar uma área restrita com login e senha, com perfil de acesso **Participante** (vê apenas o próprio painel e o cronograma). | M | 2 |
| RF-10.2 | Administradoras devem poder cadastrar, convidar e desativar participantes. Não há cadastro aberto. | M | 2 |
| RF-10.3 | Administradoras devem poder cadastrar as histórias participantes do círculo (título, autora, link do Wattpad) e seus capítulos. Quando a história já existir na Vitrine (RF-04), o cadastro deve ser reaproveitado. | M | 2 |
| RF-10.4 | Administradoras devem poder montar o **cronograma**: para cada dia, qual capítulo (história + capítulo + link) deve ser lido. | M | 2 |
| RF-10.5 | Administradoras devem poder configurar as **metas**: número mínimo de comentários por capítulo *(valor a definir)* e quais dias da semana contam. | M | 2 |
| RF-10.6 | A participante deve ver um painel com o capítulo do dia (com link direto para o Wattpad), suas pendências e o progresso da semana. | M | 2 |
| RF-10.7 | A participante deve poder registrar que leu o capítulo do dia e quantos comentários fez nele. | M | 2 |
| RF-10.8 | Ao registrar, a participante deve poder informar o(s) link(s) do(s) comentário(s) como evidência. As administradoras podem tornar isso obrigatório. | S | 2 |
| RF-10.9 | O sistema deve calcular automaticamente se cada participante cumpriu a meta, por dia e por semana. | M | 2 |
| RF-10.10 | Administradoras devem ver um painel com a situação de todas as participantes (*cumpriu*, *parcial*, *pendente*, *ausência justificada*), com filtro por período. | M | 2 |
| RF-10.11 | Administradoras devem poder marcar registros como *conferidos* ou *contestados* (conferência por amostragem). | S | 2 |
| RF-10.12 | Permitir registrar **ausências justificadas** (férias, imprevistos), que não contam como descumprimento da meta. | S | 2 |
| RF-10.13 | A participante deve poder consultar o próprio histórico de participação. | S | 3 |
| RF-10.14 | Gerar relatório semanal/mensal exportável (CSV) com o cumprimento das metas. | C | 3 |
| RF-10.15 | Enviar lembretes por e-mail para participantes com pendências. | C | 3 |
| RF-10.16 | Verificar automaticamente leituras e comentários direto no Wattpad. Só será considerado se houver um meio **oficial e permitido** pelos Termos de Serviço do Wattpad. | W | — |

> **Nota de engenharia:** o sistema não deve acessar o Wattpad com as credenciais das participantes nem usar raspagem ou APIs não oficiais (ver RNF-27). Entidades principais: *Participante*, *História*, *Capítulo*, *Cronograma (dia → capítulo)*, *Meta*, *Registro* (participante, capítulo, data, nº de comentários, links, status de conferência) e *Ausência*.
