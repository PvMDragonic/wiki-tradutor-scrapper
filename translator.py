import requests
import json
import re

class Wiki:
    API = "https://pt.runescape.wiki/api.php"
    
    URL = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "content",
        "format": "json"
    }

    @staticmethod
    def json_dump(filepath: str, itens: dict):
        with open(filepath, "w", encoding = "utf-8") as f:
            json.dump(itens, f, ensure_ascii = False, indent = 4)

        print(f'"{filepath}" criado com sucesso.')

    @staticmethod
    def buscar_paginas(titulo: str, paginas: list):
        itens = {}

        for pagina in paginas:
            params = Wiki.URL.copy()
            params["titles"] = f"Módulo:Traduções/{pagina}"

            try:
                resp = requests.get(Wiki.API, params = params)
                if resp.status_code != 200:
                    raise requests.RequestException()
                
                dados = resp.json()

                query_paginas = dados["query"]["pages"]
                dados_paginas = next(iter(query_paginas.values()))
                conteudo = dados_paginas["revisions"][0]["*"]

                for entradas in conteudo.split("] = {")[1:]:
                    partes = entradas.split("=")
                    if len(partes) < 3:
                        continue

                    _, en, pt = partes[:3]
                    try:
                        key_match = re.search(r"'(.*?[^\\])'", en) or re.search(r'"(.*?[^\\])"', en)
                        if not key_match:
                            continue
                        key = key_match.group(1)

                        value_match = re.search(r"'(.*?[^\\])'", pt) or re.search(r'"(.*?[^\\])"', pt)
                        if not value_match:
                            continue
                        value = value_match.group(1)

                        itens[key] = value
                    except Exception:
                        continue
            except requests.RequestException as e:
                print(f"Erro ao buscar nomes de {titulo}: {e}")

        Wiki.json_dump(f'{titulo}.json', itens)

if __name__ == "__main__":
    Wiki.buscar_paginas('músicas', ["data/músicas"])
    Wiki.buscar_paginas('missões', ["data/missões"])
    Wiki.buscar_paginas('npcs', ["data/npcs", "data/npcs/2"])
    Wiki.buscar_paginas('itens', ["data", "data/2", "data/3"])
    Wiki.buscar_paginas('cenários', ["data/cenários", "data/cenários/2", "data/cenários/3", "data/cenários/4", "data/cenários/5"])