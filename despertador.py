"""Abre la app DashBy como lo haría una persona, para que Streamlit no la duerma.

Si la encuentra dormida, aprieta el botón para despertarla y espera a que cargue.
No escribe contraseñas ni imprime nada de lo que muestra la app.
"""
import re
import sys

from playwright.sync_api import sync_playwright

URL = "https://app-dashby-6b2ebmyck3b7bvnqslxnxc.streamlit.app/"
BOTON = re.compile(r"get this app back up", re.I)


def main():
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pagina = nav.new_page()
        pagina.goto(URL, wait_until="domcontentloaded", timeout=90_000)
        pagina.wait_for_timeout(8_000)

        boton = pagina.get_by_role("button", name=BOTON)
        if boton.count() > 0:
            print("La app estaba dormida: la despierto.")
            boton.first.click()
            pagina.wait_for_timeout(5_000)
        else:
            print("La app estaba despierta.")

        # Espera a que la app cargue (dentro del marco de Streamlit) y se queda un rato,
        # para que cuente como una visita.
        for _ in range(36):
            listo = any(
                f.locator('[data-testid="stApp"]').count() > 0 for f in pagina.frames
            )
            if listo:
                break
            pagina.wait_for_timeout(5_000)
        else:
            print("La app no terminó de cargar en 3 minutos.")
            nav.close()
            sys.exit(1)

        pagina.wait_for_timeout(20_000)
        print("App cargada y visitada.")
        nav.close()


if __name__ == "__main__":
    main()
