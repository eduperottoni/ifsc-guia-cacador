#!/usr/bin/env python3
"""Confere se o guia.md segue o formato combinado com a turma.

Uso: python3 verificar.py [arquivo]   (padrão: guia.md)

Regras:
  1. A primeira linha é o título: "# Caçador pela turma".
  2. Seções ("## Nome") só da lista SECOES, cada uma uma única vez.
  3. Itens no formato "- Nome - descrição", sempre dentro de uma seção.
  4. Um mesmo nome não pode aparecer duas vezes no guia.
  5. Dentro de cada seção, os itens ficam em ordem alfabética.
  6. Nenhuma marca de conflito (<<<<<<<, =======, >>>>>>>) pode sobrar.

Sai com código 0 se o guia está correto e 1 se encontrou algum erro.
"""

import re
import sys
import unicodedata

TITULO = "# Caçador pela turma de Informática do IFSC"

SECOES = [
    "Cultura e Arte",
    "Esporte e Lazer",
    "Gastronomia",
    "Geografia e Natureza",
    "História",
]

ITEM = re.compile(r"^- (?P<nome>\S.*?\S|\S) - (?P<descricao>\S.*)$")
CONFLITO = re.compile(r"^(<{7}|={7}|>{7})")


def chave(texto):
    """Chave de ordenação sem acentos e sem diferença de maiúsculas."""
    sem_acento = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(c for c in sem_acento if unicodedata.category(c) != "Mn")
    return sem_acento.casefold()


def verificar(linhas):
    erros = []
    secao_atual = None
    secoes_vistas = {}
    itens_por_secao = {}
    nomes_vistos = {}

    if not linhas or linhas[0].rstrip("\n") != TITULO:
        erros.append(f"Linha 1: o guia deve começar com '{TITULO}'")

    for numero, linha in enumerate(linhas, start=1):
        texto = linha.rstrip("\n")

        if CONFLITO.match(texto):
            erros.append(f"Linha {numero}: marca de conflito esquecida '{texto[:7]}'")
            continue

        if numero == 1 or not texto.strip():
            continue

        if texto.startswith("## "):
            secao_atual = texto[3:].strip()
            if secao_atual not in SECOES:
                erros.append(f"Linha {numero}: seção desconhecida '{secao_atual}'")
            if secao_atual in secoes_vistas:
                erros.append(
                    f"Linha {numero}: seção '{secao_atual}' repetida "
                    f"(já aparece na linha {secoes_vistas[secao_atual]})"
                )
            else:
                secoes_vistas[secao_atual] = numero
            itens_por_secao.setdefault(secao_atual, [])
            continue

        if texto.startswith("#"):
            erros.append(
                f"Linha {numero}: use '## ' para seções; outros títulos não são aceitos"
            )
            continue

        item = ITEM.match(texto)
        if not item:
            erros.append(f"Linha {numero}: item fora do formato '- Nome - descrição'")
            continue

        if secao_atual is None:
            erros.append(f"Linha {numero}: item antes da primeira seção")
            continue

        nome = item.group("nome")
        if chave(nome) in nomes_vistos:
            erros.append(
                f"Linha {numero}: '{nome}' já aparece na linha {nomes_vistos[chave(nome)]}"
            )
        else:
            nomes_vistos[chave(nome)] = numero
        itens_por_secao[secao_atual].append(nome)

    for secao, nomes in itens_por_secao.items():
        if [chave(n) for n in nomes] != sorted(chave(n) for n in nomes):
            erros.append(f"Seção '{secao}': itens fora de ordem alfabética")

    return erros


def main():
    caminho = sys.argv[1] if len(sys.argv) > 1 else "guia.md"
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        print(f"Arquivo '{caminho}' não encontrado")
        return 1

    erros = verificar(linhas)
    if erros:
        for erro in erros:
            print(erro)
        return 1

    print("Guia OK!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
