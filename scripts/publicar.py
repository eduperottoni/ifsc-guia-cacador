#!/usr/bin/env python3
"""Gera a página do guia (site/index.html) a partir do guia.md.

Uso: python3 publicar.py [arquivo] [pasta]   (padrão: guia.md site)
Depende do pacote "markdown" (pip install markdown).
"""

import html
import sys
from pathlib import Path

import markdown

MODELO = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<style>
  body {{ font-family: system-ui, sans-serif; max-width: 46rem; margin: 2rem auto;
         padding: 0 1rem; line-height: 1.6; color: #1e1e1e; background: #fff; }}
  h1 {{ color: #3c6e0f; }}
  h2 {{ border-bottom: 2px solid #87bd24; padding-bottom: .2rem; margin-top: 2rem; }}
  footer {{ margin-top: 3rem; font-size: .85rem; color: #555; }}
</style>
</head>
<body>
{conteudo}
<footer>Escrito pela turma do Técnico Integrado em Informática, IFSC Câmpus Caçador.</footer>
</body>
</html>
"""


def main():
    origem = Path(sys.argv[1] if len(sys.argv) > 1 else "guia.md")
    destino = Path(sys.argv[2] if len(sys.argv) > 2 else "site")

    texto = origem.read_text(encoding="utf-8")
    primeira_linha = texto.splitlines()[0] if texto else ""
    titulo = primeira_linha.lstrip("# ").strip() or "Guia"

    conteudo = markdown.markdown(texto)
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "index.html").write_text(
        MODELO.format(titulo=html.escape(titulo), conteudo=conteudo), encoding="utf-8"
    )
    print(f"Página gerada em {destino / 'index.html'}")


if __name__ == "__main__":
    main()
