#!/usr/bin/env python3
"""Gera docs/requisitos.html a partir dos arquivos Markdown de docs/requisitos/.

Uso: python3 scripts/gerar_html_requisitos.py
Rode de novo sempre que algum .md de requisitos mudar.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "docs" / "requisitos"
SAIDA = RAIZ / "docs" / "requisitos.html"

ABAS = {
    "01-visao-geral.md": "visao",
    "02-requisitos-funcionais.md": "rf",
    "03-requisitos-nao-funcionais.md": "rnf",
    "04-roadmap.md": "roadmap",
    "05-questoes-em-aberto.md": "questoes",
}

PRIORIDADES = {"M": "Must", "S": "Should", "C": "Could", "W": "Won't"}


def inline(texto):
    """Converte a marcação inline (código, negrito, itálico, links, IDs)."""
    codigos = []

    def guarda_codigo(m):
        codigos.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\0{len(codigos) - 1}\0"

    texto = re.sub(r"`([^`]+)`", guarda_codigo, texto)
    texto = html.escape(texto, quote=False)

    def link(m):
        rotulo, alvo = m.group(1), m.group(2)
        arquivo = alvo.split("/")[-1].split("#")[0]
        if arquivo in ABAS:
            return f'<a href="#{ABAS[arquivo]}" data-aba="{ABAS[arquivo]}">{rotulo}</a>'
        return f'<a href="{alvo}">{rotulo}</a>'

    texto = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, texto)
    texto = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", texto)
    texto = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", texto)
    def ref(id_):
        return f'<a class="ref" href="#{id_}" data-ref="{id_}">{id_}</a>'

    def refs(m):
        prefixo = m.group(1)
        saida = ref(f"{prefixo}-{m.group(2)}")
        for sep, num in re.findall(r"(,\s*|\s+a\s+)(\d{2}(?:\.\d+)?)", m.group(3)):
            saida += sep + ref(f"{prefixo}-{num}")
        return saida

    texto = re.sub(
        r"\b(RNF|RF)-(\d{2}(?:\.\d+)?)\b((?:(?:,\s*|\s+a\s+)\d{2}(?:\.\d+)?\b)*)",
        refs,
        texto,
    )
    return re.sub(r"\0(\d+)\0", lambda m: codigos[int(m.group(1))], texto)


def celulas(linha):
    return [c.strip() for c in linha.strip().strip("|").split("|")]


def eh_separador(linha):
    return bool(re.match(r"^\|?\s*:?-{3,}", linha.strip()))


def markdown(texto):
    """Conversor Markdown mínimo, suficiente para os documentos de requisitos."""
    linhas = texto.split("\n")
    saida, i = [], 0
    while i < len(linhas):
        linha = linhas[i]
        s = linha.strip()
        if not s:
            i += 1
        elif s == "---":
            saida.append("<hr>")
            i += 1
        elif m := re.match(r"^(#{1,4})\s+(.*)", s):
            n = len(m.group(1))
            saida.append(f"<h{n + 1}>{inline(m.group(2))}</h{n + 1}>")
            i += 1
        elif s.startswith("|"):
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                bloco.append(linhas[i])
                i += 1
            cab = celulas(bloco[0])
            corpo = [celulas(l) for l in bloco[1:] if not eh_separador(l)]
            t = ["<div class='tabela'><table><thead><tr>"]
            t += [f"<th>{inline(c)}</th>" for c in cab]
            t.append("</tr></thead><tbody>")
            for row in corpo:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
            t.append("</tbody></table></div>")
            saida.append("".join(t))
        elif s.startswith(">"):
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith(">"):
                bloco.append(linhas[i].strip()[1:].strip())
                i += 1
            saida.append(f"<blockquote>{markdown(chr(10).join(bloco))}</blockquote>")
        elif re.match(r"^(\d+\.|[-*])\s", s):
            ordenada = bool(re.match(r"^\d+\.", s))
            itens = []
            while i < len(linhas) and re.match(r"^\s*(\d+\.|[-*])\s", linhas[i]):
                m = re.match(r"^\s*(\d+)?\.?[-*]?\s+(.*)", linhas[i])
                itens.append((m.group(1), m.group(2)))
                i += 1
            if ordenada:
                lis = "".join(f'<li value="{n}">{inline(t)}</li>' for n, t in itens)
                saida.append(f"<ol>{lis}</ol>")
            else:
                saida.append("<ul>" + "".join(f"<li>{inline(t)}</li>" for _, t in itens) + "</ul>")
        else:
            par = []
            while i < len(linhas) and linhas[i].strip() and not re.match(
                r"^(#|\||>|---|\d+\.\s|[-*]\s)", linhas[i].strip()
            ):
                par.append(linhas[i].strip())
                i += 1
            saida.append(f"<p>{inline(' '.join(par))}</p>")
    return "\n".join(saida)


def sem_titulo(texto):
    """Remove o título principal (# ...) do documento."""
    return re.sub(r"^#\s+.*\n", "", texto, count=1)


def modulos_rf(texto):
    """Divide o 02 em módulos (## RF-XX), cada um com descrição, linhas e notas."""
    partes = re.split(r"^## ", texto, flags=re.M)
    modulos = []
    for parte in partes[1:]:
        titulo, _, corpo = parte.partition("\n")
        m = re.match(r"(RF-\d{2})\s+—\s+(.*)", titulo.strip())
        if not m:
            continue
        linhas_corpo = corpo.split("\n")
        tabela = [l for l in linhas_corpo if l.strip().startswith("|")]
        notas = "\n".join(l for l in linhas_corpo if l.strip().startswith(">"))
        desc = "\n".join(
            l for l in linhas_corpo
            if l.strip() and not l.strip().startswith(("|", ">", "---"))
        )
        reqs = []
        for l in tabela[2:]:
            id_, req, prio, fase = celulas(l)
            reqs.append({"id": id_, "texto": req, "prio": prio, "fase": fase})
        modulos.append({
            "id": m.group(1), "nome": m.group(2), "desc": desc,
            "notas": notas, "reqs": reqs,
        })
    return modulos


def fase_base(fase):
    m = re.match(r"\d", fase)
    return m.group(0) if m else "—"


def html_rf(modulos):
    blocos = []
    for mod in modulos:
        linhas = []
        for r in mod["reqs"]:
            fb = fase_base(r["fase"])
            linhas.append(
                f'<tr id="{r["id"]}" data-prio="{r["prio"]}" data-fase="{fb}" '
                f'data-busca="{html.escape((r["id"] + " " + r["texto"]).lower())}">'
                f'<td class="id">{r["id"]}</td>'
                f'<td>{inline(r["texto"])}</td>'
                f'<td><span class="prio p-{r["prio"]}" title="{PRIORIDADES.get(r["prio"], "")}">{r["prio"]}</span></td>'
                f'<td><span class="fase"><span class="so-celular">Fase </span>{html.escape(r["fase"])}</span></td></tr>'
            )
        desc = f'<p class="desc">{inline(mod["desc"])}</p>' if mod["desc"] else ""
        notas = markdown(mod["notas"].replace("> ", "", 1)) if mod["notas"] else ""
        notas = re.sub(r"^<blockquote>|</blockquote>$", "", notas)
        notas = f'<div class="nota">{notas}</div>' if notas else ""
        blocos.append(f"""
<section class="modulo" id="{mod['id']}" data-modulo="{mod['id']}">
  <h3><span class="id">{mod['id']}</span> {inline(mod['nome'])} <span class="conta"></span></h3>
  {desc}
  <div class="tabela"><table class="reqs">
    <thead><tr><th>ID</th><th>Requisito</th><th title="Prioridade">Prior.</th><th>Fase</th></tr></thead>
    <tbody>{''.join(linhas)}</tbody>
  </table></div>
  {notas}
</section>""")
    return "\n".join(blocos)


def html_rnf(texto):
    partes = re.split(r"^## ", sem_titulo(texto), flags=re.M)
    blocos = []
    for parte in partes[1:]:
        titulo, _, corpo = parte.partition("\n")
        linhas = []
        for l in [l for l in corpo.split("\n") if l.strip().startswith("|")][2:]:
            id_, req = celulas(l)[:2]
            linhas.append(
                f'<tr id="{id_}" data-busca="{html.escape((id_ + " " + req).lower())}">'
                f'<td class="id">{id_}</td><td>{inline(req)}</td></tr>'
            )
        blocos.append(f"""
<section class="modulo">
  <h3>{inline(titulo.strip())} <span class="conta"></span></h3>
  <div class="tabela"><table class="reqs">
    <thead><tr><th>ID</th><th>Requisito</th></tr></thead>
    <tbody>{''.join(linhas)}</tbody>
  </table></div>
</section>""")
    return "\n".join(blocos)


def resumo(modulos):
    reqs = [r for m in modulos for r in m["reqs"]]
    por_fase = {}
    for r in reqs:
        por_fase[fase_base(r["fase"])] = por_fase.get(fase_base(r["fase"]), 0) + 1
    por_prio = {p: sum(1 for r in reqs if r["prio"] == p) for p in PRIORIDADES}
    return len(reqs), por_fase, por_prio


def gerar():
    docs = {nome: (PASTA / nome).read_text(encoding="utf-8") for nome in ABAS}
    modulos = modulos_rf(docs["02-requisitos-funcionais.md"])
    total, por_fase, por_prio = resumo(modulos)
    n_rnf = len(re.findall(r"^\| RNF-\d+", docs["03-requisitos-nao-funcionais.md"], flags=re.M))
    n_q = len(re.findall(r"^\d+\.\s", docs["05-questoes-em-aberto.md"], flags=re.M))

    legenda = docs["02-requisitos-funcionais.md"].split("## RF-")[0]
    legenda = sem_titulo(legenda).replace("---", "")

    fases_btn = "".join(
        f'<button class="chip" data-filtro="fase" data-valor="{f}">Fase {f} <small>{por_fase.get(f, 0)}</small></button>'
        for f in ["1", "2", "3", "4"]
    ) + f'<button class="chip" data-filtro="fase" data-valor="—">Sem fase <small>{por_fase.get("—", 0)}</small></button>'
    prio_btn = "".join(
        f'<button class="chip" data-filtro="prio" data-valor="{p}"><span class="prio p-{p}">{p}</span> {nome} <small>{por_prio[p]}</small></button>'
        for p, nome in PRIORIDADES.items()
    )
    modulos_opt = "".join(
        f'<option value="{m["id"]}">{m["id"]} — {html.escape(re.sub(r"[*]", "", m["nome"]))}</option>'
        for m in modulos
    )

    pagina = MODELO
    trocas = {
        "{{DATA}}": date.today().strftime("%d/%m/%Y"),
        "{{TOTAL_RF}}": str(total),
        "{{TOTAL_RNF}}": str(n_rnf),
        "{{TOTAL_Q}}": str(n_q),
        "{{TOTAL_MUST}}": str(por_prio["M"]),
        "{{FASES_BTN}}": fases_btn,
        "{{PRIO_BTN}}": prio_btn,
        "{{MODULOS_OPT}}": modulos_opt,
        "{{LEGENDA}}": markdown(legenda),
        "{{RF}}": html_rf(modulos),
        "{{RNF}}": html_rnf(docs["03-requisitos-nao-funcionais.md"]),
        "{{VISAO}}": markdown(sem_titulo(docs["01-visao-geral.md"])),
        "{{ROADMAP}}": markdown(sem_titulo(docs["04-roadmap.md"])),
        "{{QUESTOES}}": markdown(sem_titulo(docs["05-questoes-em-aberto.md"])),
        "{{IDS_RF}}": json.dumps([r["id"] for m in modulos for r in m["reqs"]] + [m["id"] for m in modulos]),
    }
    for chave, valor in trocas.items():
        pagina = pagina.replace(chave, valor)
    SAIDA.write_text(pagina, encoding="utf-8")
    print(f"Gerado: {SAIDA.relative_to(RAIZ)} ({total} RF, {n_rnf} RNF, {n_q} questões)")


MODELO = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Requisitos — Constelação Literária</title>
<style>
:root {
  --bg: #f7f6fb; --surface: #ffffff; --surface-2: #f0eef7; --text: #1e1b2e; --muted: #5f5a75;
  --border: #e1ddef; --accent: #5b3fd1; --accent-soft: #ebe6ff; --highlight: #fff4c2;
  --m-bg: #fde3e3; --m-fg: #a11d1d; --s-bg: #fff0d1; --s-fg: #8a5300;
  --c-bg: #dcecff; --c-fg: #1d4f91; --w-bg: #ebebef; --w-fg: #55556a;
  --shadow: 0 1px 2px rgba(30, 27, 46, .06), 0 4px 16px rgba(30, 27, 46, .05);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #14121d; --surface: #1d1a29; --surface-2: #262236; --text: #ebe8f5; --muted: #a49fbc;
    --border: #332e47; --accent: #a996ff; --accent-soft: #2d2650; --highlight: #4a3f12;
    --m-bg: #4a1f24; --m-fg: #ffb4b4; --s-bg: #45341a; --s-fg: #ffd59a;
    --c-bg: #1c3150; --c-fg: #a9cdff; --w-bg: #2c2b36; --w-fg: #b9b8c8;
    --shadow: none;
  }
}
:root[data-theme="dark"] {
  --bg: #14121d; --surface: #1d1a29; --surface-2: #262236; --text: #ebe8f5; --muted: #a49fbc;
  --border: #332e47; --accent: #a996ff; --accent-soft: #2d2650; --highlight: #4a3f12;
  --m-bg: #4a1f24; --m-fg: #ffb4b4; --s-bg: #45341a; --s-fg: #ffd59a;
  --c-bg: #1c3150; --c-fg: #a9cdff; --w-bg: #2c2b36; --w-fg: #b9b8c8;
  --shadow: none;
}
* { box-sizing: border-box; }
html { scroll-padding-top: 130px; }
body {
  margin: 0; background: var(--bg); color: var(--text);
  font: 15px/1.55 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}
a { color: var(--accent); }
a.ref { text-decoration: none; font-weight: 600; white-space: nowrap; }
a.ref:hover { text-decoration: underline; }
code { background: var(--surface-2); padding: 1px 5px; border-radius: 4px; font-size: .9em; }
.wrap { max-width: 1100px; margin: 0 auto; padding: 0 16px; }

header.topo { background: var(--surface); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 10; }
.topo .linha1 { display: flex; align-items: center; gap: 12px; padding: 12px 0 8px; flex-wrap: wrap; }
.topo h1 { font-size: 18px; margin: 0; flex: 1; min-width: 200px; }
.topo h1 span { color: var(--muted); font-weight: 400; font-size: 13px; margin-left: 6px; }
.tema { background: var(--surface-2); border: 1px solid var(--border); color: var(--text);
  border-radius: 8px; padding: 6px 10px; cursor: pointer; font: inherit; font-size: 13px; }
nav.abas { display: flex; gap: 4px; overflow-x: auto; scrollbar-width: none; }
nav.abas button {
  background: none; border: 0; border-bottom: 2px solid transparent; color: var(--muted);
  padding: 8px 12px; font: inherit; font-weight: 600; cursor: pointer; white-space: nowrap;
}
nav.abas button[aria-selected="true"] { color: var(--accent); border-bottom-color: var(--accent); }
nav.abas button small { font-weight: 400; opacity: .8; }

main { padding: 20px 0 60px; }
.painel { display: none; }
.painel.ativo { display: block; }

.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin-bottom: 20px; }
.card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px; box-shadow: var(--shadow); }
.card b { display: block; font-size: 26px; line-height: 1.1; font-variant-numeric: tabular-nums; }
.card span { color: var(--muted); font-size: 13px; }

.filtros { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 12px 14px;
  display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; box-shadow: var(--shadow); }
.filtros .grupo { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.filtros .rotulo { font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); width: 82px; }
.chip { background: var(--surface-2); border: 1px solid var(--border); color: var(--text); border-radius: 999px;
  padding: 4px 10px; font: inherit; font-size: 13px; cursor: pointer; display: inline-flex; gap: 6px; align-items: center; }
.chip small { color: var(--muted); }
.chip[aria-pressed="true"] { background: var(--accent-soft); border-color: var(--accent); }
input[type="search"], select {
  background: var(--surface-2); border: 1px solid var(--border); color: var(--text); border-radius: 8px;
  padding: 7px 10px; font: inherit; font-size: 14px; flex: 1; min-width: 160px;
}
.limpar { background: none; border: 0; color: var(--accent); cursor: pointer; font: inherit; font-size: 13px; }
.resultado { color: var(--muted); font-size: 13px; }

.modulo { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: var(--shadow); }
.modulo h3 { margin: 0 0 6px; font-size: 17px; }
.modulo h3 .conta { color: var(--muted); font-weight: 400; font-size: 13px; }
.modulo .desc { color: var(--muted); margin: 0 0 10px; }
.modulo.vazio { display: none; }
.id { font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; font-size: 13px; color: var(--muted); white-space: nowrap; }
h3 .id { color: var(--accent); font-size: 15px; }

.tabela { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; }
th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--border); vertical-align: top; }
th { font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); font-weight: 600; }
tbody tr:last-child td { border-bottom: 0; }
table.reqs td:nth-child(3), table.reqs td:nth-child(4) { white-space: nowrap; }
tr.oculto { display: none; }
tr.destaque td { background: var(--highlight); transition: background .3s; }

.prio { display: inline-block; min-width: 22px; text-align: center; border-radius: 6px; padding: 1px 6px; font-weight: 700; font-size: 12px; }
.p-M { background: var(--m-bg); color: var(--m-fg); }
.p-S { background: var(--s-bg); color: var(--s-fg); }
.p-C { background: var(--c-bg); color: var(--c-fg); }
.p-W { background: var(--w-bg); color: var(--w-fg); }
.fase { font-size: 13px; color: var(--muted); }
.so-celular { display: none; }

.nota, blockquote { background: var(--accent-soft); border-left: 3px solid var(--accent); border-radius: 0 8px 8px 0;
  padding: 8px 14px; margin: 12px 0 0; }
.nota p, blockquote p { margin: 4px 0; }

.doc { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 4px 24px 20px; box-shadow: var(--shadow); }
.doc h2 { font-size: 20px; margin: 28px 0 10px; padding-top: 10px; border-top: 1px solid var(--border); }
.doc h2:first-child { border-top: 0; }
.doc h3 { font-size: 16px; margin: 20px 0 8px; }
.doc hr { border: 0; border-top: 1px solid var(--border); margin: 20px 0; }
.doc li { margin: 4px 0; }
.legenda { margin-bottom: 16px; color: var(--muted); font-size: 14px; }
.legenda p, .legenda ul { margin: 4px 0; }
.legenda ul { display: flex; flex-wrap: wrap; gap: 4px 18px; padding-left: 18px; }
footer { color: var(--muted); font-size: 12px; text-align: center; padding: 20px 0 40px; }

@media (max-width: 640px) {
  html { scroll-padding-top: 150px; }
  .doc { padding: 4px 14px 16px; }
  .filtros .rotulo { width: 100%; }
  table.reqs thead { display: none; }
  table.reqs tr { display: grid; grid-template-columns: auto 1fr auto; gap: 2px 8px; padding: 10px 0; border-bottom: 1px solid var(--border); }
  table.reqs td { border: 0; padding: 0; }
  table.reqs td:nth-child(2) { grid-column: 1 / -1; grid-row: 2; }
  table.reqs td:nth-child(4) { grid-row: 1; grid-column: 2; }
  table.reqs td:nth-child(3) { grid-row: 1; grid-column: 3; }
  .so-celular { display: inline; }
}
@media print {
  header.topo { position: static; }
  nav.abas, .filtros, .tema { display: none; }
  .painel { display: block !important; break-before: page; }
}
</style>
</head>
<body>
<header class="topo">
  <div class="wrap">
    <div class="linha1">
      <h1>✨ Requisitos — Constelação Literária <span>gerado em {{DATA}}</span></h1>
      <button class="tema" id="tema" type="button">◐ Tema</button>
    </div>
    <nav class="abas" role="tablist">
      <button role="tab" data-aba="rf">Funcionais <small>{{TOTAL_RF}}</small></button>
      <button role="tab" data-aba="rnf">Não funcionais <small>{{TOTAL_RNF}}</small></button>
      <button role="tab" data-aba="roadmap">Roadmap</button>
      <button role="tab" data-aba="visao">Visão geral</button>
      <button role="tab" data-aba="questoes">Questões em aberto <small>{{TOTAL_Q}}</small></button>
    </nav>
  </div>
</header>

<main class="wrap">
  <section class="painel" id="aba-rf">
    <div class="cards">
      <div class="card"><b>{{TOTAL_RF}}</b><span>requisitos funcionais</span></div>
      <div class="card"><b>{{TOTAL_MUST}}</b><span>obrigatórios (Must)</span></div>
      <div class="card"><b>{{TOTAL_RNF}}</b><span>não funcionais</span></div>
      <div class="card"><b>{{TOTAL_Q}}</b><span>questões em aberto</span></div>
    </div>
    <div class="legenda">{{LEGENDA}}</div>
    <div class="filtros">
      <div class="grupo"><span class="rotulo">Fase</span>{{FASES_BTN}}</div>
      <div class="grupo"><span class="rotulo">Prioridade</span>{{PRIO_BTN}}</div>
      <div class="grupo">
        <span class="rotulo">Buscar</span>
        <input type="search" id="busca-rf" placeholder="Palavra ou ID (ex.: login, RF-10)">
        <select id="modulo-rf"><option value="">Todos os módulos</option>{{MODULOS_OPT}}</select>
      </div>
      <div class="grupo"><span class="resultado" id="resultado-rf"></span><button class="limpar" id="limpar-rf" type="button">Limpar filtros</button></div>
    </div>
    {{RF}}
  </section>

  <section class="painel" id="aba-rnf">
    <div class="filtros">
      <div class="grupo"><span class="rotulo">Buscar</span><input type="search" id="busca-rnf" placeholder="Palavra ou ID (ex.: LGPD, RNF-25)"></div>
    </div>
    {{RNF}}
  </section>

  <section class="painel" id="aba-roadmap"><div class="doc">{{ROADMAP}}</div></section>
  <section class="painel" id="aba-visao"><div class="doc">{{VISAO}}</div></section>
  <section class="painel" id="aba-questoes"><div class="doc">{{QUESTOES}}</div></section>
</main>
<footer class="wrap">Gerado por <code>scripts/gerar_html_requisitos.py</code> a partir de <code>docs/requisitos/*.md</code>. Edite os .md e rode o script de novo.</footer>

<script>
(function () {
  var IDS_RF = {{IDS_RF}};
  var guardar = function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} };
  var ler = function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } };

  // Tema
  var raiz = document.documentElement;
  var temaSalvo = ler("req-tema");
  if (temaSalvo) raiz.setAttribute("data-theme", temaSalvo);
  document.getElementById("tema").addEventListener("click", function () {
    var escuro = raiz.getAttribute("data-theme")
      ? raiz.getAttribute("data-theme") === "dark"
      : matchMedia("(prefers-color-scheme: dark)").matches;
    var novo = escuro ? "light" : "dark";
    raiz.setAttribute("data-theme", novo);
    guardar("req-tema", novo);
  });

  // Abas
  var abas = document.querySelectorAll("nav.abas button");
  function abrir(nome) {
    abas.forEach(function (b) { b.setAttribute("aria-selected", b.dataset.aba === nome); });
    document.querySelectorAll(".painel").forEach(function (p) { p.classList.toggle("ativo", p.id === "aba-" + nome); });
    guardar("req-aba", nome);
  }
  abas.forEach(function (b) { b.addEventListener("click", function () { abrir(b.dataset.aba); history.replaceState(null, "", "#" + b.dataset.aba); }); });
  document.querySelectorAll("a[data-aba]").forEach(function (a) {
    a.addEventListener("click", function (e) { e.preventDefault(); abrir(a.dataset.aba); scrollTo(0, 0); });
  });

  // Filtros dos requisitos funcionais
  var ativos = { fase: new Set(), prio: new Set() };
  var buscaRf = document.getElementById("busca-rf");
  var moduloRf = document.getElementById("modulo-rf");
  function contar(secoes) {
    var visiveis = 0;
    secoes.forEach(function (s) {
      var linhas = s.querySelectorAll("tbody tr");
      var n = s.querySelectorAll("tbody tr:not(.oculto)").length;
      visiveis += n;
      s.classList.toggle("vazio", n === 0);
      s.querySelector(".conta").textContent = n === linhas.length ? "· " + n : "· " + n + " de " + linhas.length;
    });
    return visiveis;
  }
  function filtrarRf() {
    var termo = buscaRf.value.trim().toLowerCase();
    var mod = moduloRf.value;
    var secoes = document.querySelectorAll("#aba-rf .modulo");
    secoes.forEach(function (s) {
      var foraModulo = mod && s.dataset.modulo !== mod;
      s.querySelectorAll("tbody tr").forEach(function (tr) {
        var ok = !foraModulo
          && (!ativos.fase.size || ativos.fase.has(tr.dataset.fase))
          && (!ativos.prio.size || ativos.prio.has(tr.dataset.prio))
          && (!termo || tr.dataset.busca.indexOf(termo) !== -1);
        tr.classList.toggle("oculto", !ok);
      });
    });
    var n = contar(secoes);
    document.getElementById("resultado-rf").textContent = n + " de " + IDS_RF.filter(function (i) { return i.indexOf(".") > 0; }).length + " requisitos";
  }
  document.querySelectorAll("#aba-rf .chip").forEach(function (c) {
    c.setAttribute("aria-pressed", "false");
    c.addEventListener("click", function () {
      var conj = ativos[c.dataset.filtro];
      if (conj.has(c.dataset.valor)) conj.delete(c.dataset.valor); else conj.add(c.dataset.valor);
      c.setAttribute("aria-pressed", conj.has(c.dataset.valor));
      filtrarRf();
    });
  });
  buscaRf.addEventListener("input", filtrarRf);
  moduloRf.addEventListener("change", filtrarRf);
  function limparRf() {
    ativos.fase.clear(); ativos.prio.clear(); buscaRf.value = ""; moduloRf.value = "";
    document.querySelectorAll("#aba-rf .chip").forEach(function (c) { c.setAttribute("aria-pressed", "false"); });
    filtrarRf();
  }
  document.getElementById("limpar-rf").addEventListener("click", limparRf);
  filtrarRf();

  // Busca dos não funcionais
  var buscaRnf = document.getElementById("busca-rnf");
  buscaRnf.addEventListener("input", function () {
    var termo = buscaRnf.value.trim().toLowerCase();
    document.querySelectorAll("#aba-rnf tbody tr").forEach(function (tr) {
      tr.classList.toggle("oculto", termo && tr.dataset.busca.indexOf(termo) === -1);
    });
    contar(document.querySelectorAll("#aba-rnf .modulo"));
  });
  contar(document.querySelectorAll("#aba-rnf .modulo"));

  // Links para requisitos (RF-07.1, RNF-25, RF-10...) abrem a aba certa e destacam a linha
  function irPara(id) {
    var alvo = document.getElementById(id);
    if (!alvo) return;
    var painel = alvo.closest(".painel");
    if (painel.id === "aba-rf") limparRf();
    if (painel.id === "aba-rnf" && buscaRnf.value) { buscaRnf.value = ""; buscaRnf.dispatchEvent(new Event("input")); }
    abrir(painel.id.replace("aba-", ""));
    alvo.scrollIntoView({ block: "center" });
    if (alvo.tagName === "TR") {
      alvo.classList.add("destaque");
      setTimeout(function () { alvo.classList.remove("destaque"); }, 1800);
    }
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a.ref");
    if (!a) return;
    e.preventDefault();
    irPara(a.dataset.ref);
  });

  // Aba inicial: hash da URL > última aba usada > funcionais
  var hash = location.hash.slice(1);
  if (document.getElementById("aba-" + hash)) abrir(hash);
  else if (document.getElementById(hash)) irPara(hash);
  else abrir(ler("req-aba") || "rf");
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    gerar()
