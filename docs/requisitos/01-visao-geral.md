# 01 — Visão Geral do Produto

## 1. Contexto

A **Constelação Literária** é um coletivo de escritoras que já atua nas redes sociais (Instagram, TikTok, Wattpad) oferecendo conteúdos, materiais e apoio a outras escritoras. Hoje esse conteúdo está espalhado em posts e perfis diferentes, o que dificulta encontrar um material antigo, navegar por temas ou conhecer o trabalho das integrantes.

Além dos conteúdos, o coletivo mantém um **círculo de leitura**: as escritoras participantes se comprometem a ler um capítulo por dia e a comentar nele um número mínimo de vezes. Hoje as administradoras conferem manualmente se todas estão cumprindo as metas.

O projeto é **sem fins lucrativos**. Seu único propósito é incentivar a leitura e a escrita. As histórias envolvidas ficam no Wattpad, que disponibiliza histórias e fanfics gratuitamente.

## 2. Visão

> Um site que funcione como **extensão das redes sociais** do coletivo: um espaço de **aprendizado, divulgação e apoio** para escritoras, e não apenas uma página de apresentação.

## 3. Objetivos

| # | Objetivo | Como saberemos que foi atingido |
|---|----------|----------------------------------|
| O1 | Centralizar os conteúdos educativos hoje espalhados nas redes | Conteúdos organizados por seção e categoria, fáceis de buscar |
| O2 | Divulgar as obras das integrantes e ajudar novas histórias a encontrar leitores | Vitrine com sinopses e links para Wattpad / outras plataformas |
| O3 | Oferecer materiais gratuitos (guias, modelos, checklists) | Materiais disponíveis para visualização e download |
| O4 | Apresentar as pessoas por trás do projeto | Página "Conheça as autoras" publicada |
| O5 | Facilitar o acompanhamento do círculo de leitura | As participantes registram suas leituras e comentários no site, e as administradoras veem quem cumpriu as metas sem precisar contar à mão |
| O6 | Crescer de forma incremental, com calma | Entregas em fases, começando pelo mais simples (ver [04-roadmap.md](04-roadmap.md)) |

## 4. Partes interessadas

| Parte interessada | Interesse |
|-------------------|-----------|
| Integrantes da Constelação Literária | Publicar conteúdos, divulgar suas obras e (futuramente) seus serviços |
| Participantes do círculo de leitura | Saber o que ler a cada dia, registrar o que fizeram e acompanhar o próprio progresso |
| Escritoras iniciantes / em desenvolvimento | Aprender, encontrar materiais e inspiração |
| Leitoras e leitores | Descobrir novas histórias |
| Seguidoras das redes sociais | Acessar com facilidade o que viram nos posts |
| Equipe de desenvolvimento | Requisitos claros e evolução em etapas |

## 5. Personas

**Ana, escritora iniciante (público principal)**
Escreve no Wattpad há poucos meses, ainda não tem livro publicado. Quer melhorar a pontuação, entender como construir personagens e aprender a divulgar sua história no TikTok. Acessa principalmente pelo celular, vinda de um link na bio do Instagram.

**Bruno, leitor**
Procura histórias novas para ler. Chega ao site por indicação e quer ver sinopses e ir direto para o Wattpad.

**Carla, integrante do coletivo (administradora de conteúdo)**
Produz dicas e materiais. Precisa publicar e editar conteúdos sem depender de conhecimento técnico. Também coordena o círculo de leitura: monta o cronograma e precisa saber, no fim da semana, quem cumpriu as metas, sem abrir capítulo por capítulo no Wattpad para contar comentários.

**Daniela, participante do círculo de leitura**
Escreve uma história no Wattpad e participa do círculo. Todo dia quer abrir o site no celular, ver qual capítulo tem que ler, ir direto para o Wattpad e, depois de ler e comentar, registrar isso em poucos toques.

## 6. Escopo

### Dentro do escopo (visão completa)
1. Página inicial
2. Biblioteca de conteúdos
3. Espaço criativo
4. Marketing literário
5. Vitrine de histórias
6. Dicas e materiais gratuitos
7. Conheça as autoras
8. Área administrativa para as integrantes gerenciarem o conteúdo
9. Círculo de leitura: cronograma, registro de leituras e comentários e acompanhamento das metas (ver RF-10)

### Futuro / a avaliar
- **Serviços das integrantes** (capas, revisão textual, identidade visual etc.) — sugerido pelo cliente como ideia extra.

### Fora do escopo (por enquanto)
- Venda de produtos ou pagamentos online
- Cadastro aberto de leitoras/escritoras (contas públicas). As contas das participantes do círculo de leitura são criadas pelas administradoras.
- Verificação automática da atividade no Wattpad (leituras e comentários). Não existe API oficial conhecida para isso, e a raspagem pode violar os Termos de Serviço do Wattpad (ver RF-10.16)
- Comentários, fórum ou rede social própria
- Aplicativo mobile nativo

## 7. Glossário

| Termo | Significado |
|-------|-------------|
| **Integrante** | Membro do coletivo Constelação Literária |
| **Conteúdo** | Texto/artigo educativo (dica, tutorial, guia) publicado em uma seção |
| **Material** | Arquivo para download (PDF, modelo, checklist) |
| **Obra** | História/livro de uma integrante exibido na Vitrine |
| **Seção** | Grande área do site (ex.: Biblioteca, Marketing literário) |
| **Categoria** | Subdivisão temática dentro de uma seção (ex.: Pontuação, Personagens) |
| **Administradora** | Integrante com acesso à área de gestão do site |
| **Círculo de leitura** | Grupo de escritoras que se compromete a ler e comentar capítulos umas das outras seguindo um cronograma *(nome provisório)* |
| **Participante** | Escritora inscrita no círculo de leitura, com conta no site. Pode ou não ser integrante do coletivo |
| **Cronograma** | Definição de qual capítulo deve ser lido em cada dia |
| **Meta** | Quantidade mínima de leituras e comentários esperada por dia/semana |
| **Registro** | Declaração da participante de que leu um capítulo e comentou nele, opcionalmente com links como evidência |
| **Ausência justificada** | Período em que a participante está dispensada das metas (férias, imprevistos) |
