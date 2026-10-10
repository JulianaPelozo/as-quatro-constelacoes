"""RNF-28: toda tabela criada nas migrations precisa ativar o RLS no Postgres."""
import re
from pathlib import Path

PASTA = Path(__file__).resolve().parent.parent / "migrations" / "versions"


def test_toda_tabela_criada_ativa_rls():
    sem_rls = []
    for arquivo in PASTA.glob("*.py"):
        codigo = arquivo.read_text(encoding="utf-8")
        for tabela in re.findall(r"op\.create_table\(\s*['\"](\w+)['\"]", codigo):
            if f"ALTER TABLE {tabela} ENABLE ROW LEVEL SECURITY" not in codigo:
                sem_rls.append(f"{tabela} ({arquivo.name})")
    assert not sem_rls, (
        "Tabelas sem RLS (RNF-28). Adicione na migration: "
        "op.execute('ALTER TABLE <tabela> ENABLE ROW LEVEL SECURITY') -> "
        + ", ".join(sem_rls)
    )
