"""Genera las guías PDF del hub rural (salud, educación, ocio) con fpdf2."""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from fpdf import FPDF
from fab import get

FONT = "/usr/share/fonts/truetype/dejavu/"
OUT = os.path.join(os.path.dirname(__file__), "guias")
os.makedirs(OUT, exist_ok=True)
VERDE, GRIS = (31, 107, 82), (90, 90, 90)


class Guia(FPDF):
    def __init__(self, titulo, serie):
        super().__init__(format="A4")
        self.titulo, self.serie = titulo, serie
        L = "/usr/share/fonts/truetype/liberation/"
        self.add_font("D", "", L + "LiberationSans-Regular.ttf")
        self.add_font("D", "B", L + "LiberationSans-Bold.ttf")
        self.add_font("D", "I", L + "LiberationSans-Italic.ttf")
        self.add_font("D", "BI", L + "LiberationSans-BoldItalic.ttf")
        self.add_font("S", "", FONT + "DejaVuSerif.ttf")
        self.set_margins(20, 20, 20)
        self.set_auto_page_break(True, 20)
        self.set_title(titulo); self.set_author("Proyecto Redes Rurales - Hub rural")

    def header(self):
        if self.page_no() == 1: return
        self.set_font("D", "", 8); self.set_text_color(*GRIS)
        self.cell(0, 6, f"{self.serie} · {self.titulo}", align="R"); self.ln(10)

    def footer(self):
        self.set_y(-14); self.set_font("D", "", 8); self.set_text_color(*GRIS)
        self.cell(0, 6, f"Hub rural · contenido sin conexión · página {self.page_no()}/{{nb}}", align="C")

    def portada(self, subtitulo, aviso):
        self.add_page()
        self.set_fill_color(*VERDE); self.rect(0, 0, 210, 70, "F")
        self.set_xy(20, 22); self.set_text_color(255, 255, 255)
        self.set_font("D", "", 11); self.cell(0, 6, self.serie.upper()); self.ln(10)
        self.set_font("D", "B", 24); self.multi_cell(0, 11, self.titulo)
        self.set_xy(20, 80); self.set_text_color(30, 30, 30)
        self.set_font("D", "", 12); self.multi_cell(0, 7, subtitulo); self.ln(4)
        if aviso: self.caja(aviso)

    def sec(self, t):
        if self.get_y() > 245: self.add_page()
        self.ln(3); self.set_font("D", "B", 14); self.set_text_color(*VERDE)
        self.multi_cell(0, 8, t); self.ln(1); self.set_text_color(30, 30, 30)

    def p(self, t, size=11):
        self.set_font("D", "", size); self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, t, markdown=True); self.ln(2)

    def lista(self, items, numerada=False):
        self.set_font("D", "", 11)
        for i, it in enumerate(items, 1):
            marca = f"{i}." if numerada else "•"
            self.set_x(24); self.cell(8, 6, marca)
            self.multi_cell(0, 6, it, markdown=True)
        self.ln(2)

    def caja(self, t):
        if self.get_y() > 235: self.add_page()
        self.set_fill_color(232, 243, 238); self.set_draw_color(*VERDE)
        self.set_font("D", "", 10.5)
        self.multi_cell(0, 6, t, border=1, fill=True, padding=3, markdown=True); self.ln(3)

    def referencias(self, refs):
        self.sec("Referencias")
        self.set_font("D", "", 9.5); self.set_text_color(60, 60, 60)
        for i, r in enumerate(refs, 1):
            self.set_x(20); self.cell(9, 5, f"[{i}]")
            self.multi_cell(0, 5, r); self.ln(1)

    def guardar(self, nombre):
        self.output(os.path.join(OUT, nombre)); print("OK", nombre, self.pages_count, "pág.")


AVISO_SALUD = ("**Esta guía no reemplaza la atención médica.** En una emergencia llama al **123** "
               "(línea única de emergencias en Colombia) o busca al promotor o la enfermera de la vereda.")

# ---------------------------------------------------------------- SALUD 1
g = Guia("Lavado de manos", "Guías de salud")
g.portada("Cómo y cuándo lavarse las manos para prevenir diarreas, infecciones respiratorias "
          "y la transmisión de enfermedades en la casa, la escuela y el puesto de salud. "
          "Basada en las recomendaciones de la Organización Mundial de la Salud (OMS) [1][2][3].",
          AVISO_SALUD)
g.sec("¿Por qué es importante?")
g.p("Las manos llevan microbios de las superficies, los alimentos, los animales y otras personas a la boca, "
    "la nariz y los ojos. Lavarlas con agua y jabón en los momentos clave es una de las medidas más sencillas "
    "y baratas para prevenir enfermedades diarreicas y respiratorias [1][4].")
g.sec("Con agua y jabón (40 a 60 segundos)")
g.lista([
    "Mójate las manos con agua limpia.",
    "Aplica suficiente jabón para cubrir toda la superficie de las manos.",
    "Frota las palmas entre sí.",
    "Frota la palma derecha contra el dorso de la mano izquierda entrelazando los dedos, y al revés.",
    "Frota las palmas entre sí con los dedos entrelazados.",
    "Frota el dorso de los dedos de una mano contra la palma de la otra, con los dedos trabados.",
    "Rodea el pulgar izquierdo con la palma derecha y frótalo con un movimiento de rotación, y al revés.",
    "Frota las yemas de los dedos de la mano derecha contra la palma izquierda, en círculos, y al revés.",
    "Enjuágate las manos con agua.",
    "Sécalas con una toalla limpia o desechable.",
    "Usa la toalla para cerrar la llave. Tus manos ya son seguras.",
], numerada=True)
g.caja("**Sin agua y jabón:** usa gel o solución a base de alcohol (al menos 60 %) y frota siguiendo "
       "los mismos movimientos durante **20 a 30 segundos**, hasta que las manos estén secas [1]. "
       "Si las manos están visiblemente sucias, el gel no basta: hay que lavarlas con agua y jabón.")
g.sec("¿Cuándo lavarse las manos en la casa y la escuela?")
g.lista([
    "Antes de preparar, servir o comer alimentos.",
    "Después de ir al baño o a la letrina.",
    "Después de cambiar pañales o limpiar a un niño que fue al baño.",
    "Después de sonarse, toser o estornudar.",
    "Después de tocar animales, su comida o su estiércol.",
    "Después de tocar basura.",
    "Antes y después de atender a una persona enferma o curar una herida [4].",
])
g.sec("Los 5 momentos en la atención de salud")
g.p("Para promotores, auxiliares y enfermeras, la OMS define cinco momentos en los que la higiene de manos "
    "es obligatoria [2]:")
g.lista([
    "**Antes** de tocar al paciente.",
    "**Antes** de realizar una tarea limpia o aséptica (curaciones, inyecciones, sondas).",
    "**Después** del riesgo de exposición a líquidos corporales.",
    "**Después** de tocar al paciente.",
    "**Después** del contacto con el entorno del paciente (cama, mesa, objetos).",
], numerada=True)
g.sec("Si el agua es escasa")
g.lista([
    "Un recipiente con llave o un \"tippy-tap\" (galón colgado que se inclina con el pie) permite lavarse con poca agua y sin tocar el recipiente.",
    "El jabón en barra debe quedar en una jabonera que escurra; el jabón líquido se puede hacer rendir diluyéndolo un poco.",
    "Si no hay toalla limpia, deja secar las manos al aire. No las seques en la ropa.",
])
g.referencias([
    "Organización Mundial de la Salud. *WHO Guidelines on Hand Hygiene in Health Care*. Ginebra: OMS, 2009. https://www.who.int/publications/i/item/9789241597906",
    "Organización Mundial de la Salud. *Sus 5 momentos para la higiene de las manos*. Ginebra: OMS, 2009. https://www.who.int/campaigns/world-hand-hygiene-day",
    "Organización Mundial de la Salud. *¿Cómo lavarse las manos?* (cartel). Ginebra: OMS, 2009.",
    "Organización Panamericana de la Salud. *Lavado de manos*. https://www.paho.org/es/temas/lavado-manos",
])
g.guardar("guia-lavado-de-manos.pdf")

# ---------------------------------------------------------------- SALUD 2
g = Guia("Primeros auxilios básicos", "Guías de salud")
g.portada("Qué hacer en los primeros minutos ante una persona que no responde, que sangra, que se quemó "
          "o que se atraganta, mientras llega la ayuda. Basada en las guías de la Federación Internacional "
          "de Sociedades de la Cruz Roja (IFRC) y de la American Heart Association (AHA) [1][2].",
          AVISO_SALUD)
g.sec("Primero: PAS (Proteger, Avisar, Socorrer)")
g.lista([
    "**Proteger:** mira si hay peligro para ti o para la víctima (tráfico, cables, fuego, animales). No te conviertas en otra víctima.",
    "**Avisar:** llama al **123** o pide a alguien que llame. Di qué pasó, dónde (vereda, finca, punto de referencia) y cuántas personas hay heridas.",
    "**Socorrer:** atiende a la persona con lo que aprendas en esta guía, sin hacer más de lo que sabes [1].",
])
g.sec("Persona que no responde")
g.lista([
    "Háblale fuerte y tócale los hombros. Si no responde, pide ayuda.",
    "Mira si respira normalmente durante máximo 10 segundos (el pecho sube y baja).",
    "**Si respira:** ponla de lado (posición lateral de seguridad) para que no se ahogue con el vómito, y vigila que siga respirando.",
    "**Si no respira o solo boquea:** llama al 123 y empieza la reanimación (RCP) [2].",
], numerada=True)
g.caja("**RCP en adultos (solo con las manos):** coloca el talón de una mano en el centro del pecho y la otra "
       "encima. Con los brazos rectos, empuja fuerte **5 a 6 cm** y deja que el pecho vuelva, a un ritmo de "
       "**100 a 120 compresiones por minuto**. Si sabes dar respiraciones, alterna 30 compresiones y 2 "
       "respiraciones. Si hay un desfibrilador (DEA), enciéndelo y sigue sus instrucciones. No pares hasta que "
       "llegue ayuda o la persona respire [2].")
g.sec("Sangrado")
g.lista([
    "Ponte guantes o una bolsa plástica en la mano si los tienes.",
    "Presiona directamente la herida con una tela limpia y no la sueltes.",
    "Si la tela se empapa, **no la quites**: pon otra encima y sigue presionando.",
    "Si la herida es grave o el sangrado no para, llama al 123 [1].",
], numerada=True)
g.sec("Quemaduras")
g.lista([
    "Enfría la quemadura con agua corriente fresca (no helada) durante **20 minutos** [1].",
    "Quita anillos, relojes o ropa que no esté pegada a la piel, antes de que se hinche.",
    "Cubre con un plástico limpio o una tela limpia que no suelte pelusa.",
    "**No** pongas hielo, crema dental, mantequilla, café ni pomadas caseras. **No** revientes las ampollas.",
    "Busca atención si la quemadura es más grande que la palma de la mano de la persona, o si está en la cara, las manos, los genitales o las articulaciones.",
])
g.sec("Atragantamiento (adulto o niño mayor de 1 año)")
g.lista([
    "Si la persona tose con fuerza, anímala a seguir tosiendo.",
    "Si no puede toser, hablar ni respirar: dale **5 golpes** firmes en la espalda, entre los omóplatos, con la persona inclinada hacia adelante.",
    "Si no sale el objeto: haz **5 compresiones abdominales** (abraza desde atrás, puño sobre el ombligo, empuja hacia adentro y hacia arriba).",
    "Alterna 5 golpes y 5 compresiones. Si pierde el conocimiento, llama al 123 y empieza la RCP [1][2].",
], numerada=True)
g.sec("Botiquín básico para la vereda")
g.lista(["Guantes desechables", "Gasas y vendas limpias", "Esparadrapo", "Solución salina",
         "Tijeras", "Termómetro", "Lista de teléfonos de emergencia (123, puesto de salud, hospital más cercano)"])
g.referencias([
    "International Federation of Red Cross and Red Crescent Societies. *International First Aid, Resuscitation, and Education Guidelines 2020*. Ginebra: IFRC, 2020. https://www.ifrc.org/document/international-first-aid-resuscitation-and-education-guidelines",
    "American Heart Association. *Aspectos destacados de las Guías de la AHA de 2020 para RCP y ACE*. Dallas: AHA, 2020. https://cpr.heart.org/es/resuscitation-science/cpr-and-ecc-guidelines",
    "Organización Mundial de la Salud. *Quemaduras* (nota descriptiva). 2023. https://www.who.int/es/news-room/fact-sheets/detail/burns",
    "Gobierno de Colombia. Línea 123, número único de seguridad y emergencias.",
])
g.guardar("guia-primeros-auxilios.pdf")

# ---------------------------------------------------------------- EDUCACIÓN
g = Guia("Cartilla de matemáticas básicas", "Guías de educación")
g.portada("Suma, resta, multiplicación, división y fracciones con ejemplos de la vida en el campo: "
          "cosechas, mercado, dinero y medidas. Cada tema trae ejercicios y al final están las respuestas.",
          "**Cómo usarla:** lee el ejemplo, resuelve los ejercicios en un cuaderno y revisa tus respuestas "
          "al final. Esta cartilla fue escrita para el hub rural; puedes copiarla y compartirla libremente.")
g.sec("1. Sumar: juntar cantidades")
g.p("Sumar es juntar. Si doña Rosa recogió **125** naranjas el lunes y **87** el martes, en total recogió:")
g.caja("125 + 87 = **212** naranjas\n\nSe suman las unidades (5 + 7 = 12, se escribe 2 y se lleva 1), luego las decenas "
       "(2 + 8 + 1 = 11, se escribe 1 y se lleva 1) y por último las centenas (1 + 1 = 2).")
g.p("**Ejercicios:**  a) 48 + 36   b) 230 + 145   c) 1.250 + 780")
g.sec("2. Restar: quitar o comparar")
g.p("Restar es quitar. Si había **212** naranjas y se vendieron **150**, quedan:")
g.caja("212 − 150 = **62** naranjas")
g.p("**Ejercicios:**  d) 95 − 40   e) 500 − 275   f) 1.000 − 365")
g.sec("3. Multiplicar: sumar varias veces lo mismo")
g.p("Si cada canasta lleva **12** huevos y hay **5** canastas: 12 + 12 + 12 + 12 + 12 = 12 × 5 = **60** huevos.")
if g.get_y() > 190: g.add_page()
g.p("**Tabla de multiplicar del 1 al 10**")
g.set_font("D", "B", 9); g.set_fill_color(*VERDE); g.set_text_color(255, 255, 255)
w = 15.4
g.cell(w, 7, "×", border=1, align="C", fill=True)
for j in range(1, 11): g.cell(w, 7, str(j), border=1, align="C", fill=True)
g.ln()
for i in range(1, 11):
    g.set_font("D", "B", 9); g.set_fill_color(*VERDE); g.set_text_color(255, 255, 255)
    g.cell(w, 7, str(i), border=1, align="C", fill=True)
    g.set_font("D", "", 9); g.set_text_color(30, 30, 30)
    for j in range(1, 11):
        g.set_fill_color(*((232, 243, 238) if (i + j) % 2 else (255, 255, 255)))
        g.cell(w, 7, str(i * j), border=1, align="C", fill=True)
    g.ln()
g.ln(3)
g.p("**Ejercicios:**  g) 7 × 8   h) 25 × 4   i) 12 × 6")
g.sec("4. Dividir: repartir en partes iguales")
g.p("Si hay **60** huevos y se reparten en partes iguales entre **4** familias, a cada una le tocan "
    "60 ÷ 4 = **15** huevos. Para comprobar: 15 × 4 = 60.")
g.p("**Ejercicios:**  j) 36 ÷ 6   k) 100 ÷ 5   l) 72 ÷ 8")
g.sec("5. Fracciones: partes de un entero")
g.p("Una fracción dice en cuántas partes iguales se dividió algo (el número de abajo) y cuántas partes "
    "se toman (el número de arriba).")
g.lista([
    "**1/2** (un medio): una panela partida en 2 y tomas 1 parte.",
    "**1/4** (un cuarto): una libra de café partida en 4; cada parte es un cuarto de libra.",
    "**3/4** (tres cuartos): 3 de esas 4 partes.",
    "**2/4 = 1/2**: dos cuartos son lo mismo que un medio.",
])
g.caja("Para hallar la fracción de una cantidad: se divide por el número de abajo y se multiplica por el de "
       "arriba. Ejemplo: 3/4 de 20 bultos = (20 ÷ 4) × 3 = 5 × 3 = **15** bultos.")
g.p("**Ejercicios:**  m) 1/2 de 50   n) 1/4 de 80   o) 2/3 de 90")
g.sec("6. Problemas del día a día")
g.lista([
    "p) Un racimo de plátano vale $8.000. ¿Cuánto valen 6 racimos?",
    "q) Pedro tenía $50.000 y gastó $32.500 en el mercado. ¿Cuánto le quedó?",
    "r) Se cosecharon 240 kg de papa y se empacan en bultos de 50 kg. ¿Cuántos bultos llenos salen y cuántos kilos sobran?",
    "s) Una finca de 12 hectáreas tiene 3/4 sembrados en café. ¿Cuántas hectáreas son de café?",
])
g.sec("Respuestas")
resp = [("a", 48 + 36), ("b", 230 + 145), ("c", "2.030"), ("d", 95 - 40), ("e", 500 - 275), ("f", 1000 - 365),
        ("g", 7 * 8), ("h", 25 * 4), ("i", 12 * 6), ("j", 36 // 6), ("k", 100 // 5), ("l", 72 // 8),
        ("m", 25), ("n", 20), ("o", 60), ("p", "$48.000"), ("q", "$17.500"),
        ("r", "4 bultos llenos y sobran 40 kg"), ("s", "9 hectáreas")]
assert 1250 + 780 == 2030 and 8000 * 6 == 48000 and 50000 - 32500 == 17500
assert divmod(240, 50) == (4, 40) and 12 * 3 // 4 == 9 and 90 // 3 * 2 == 60
g.p("   ".join(f"**{k})** {v}" for k, v in resp))
g.guardar("cartilla-matematicas.pdf")

# ---------------------------------------------------------------- OCIO
FABULAS = ["La cigarra y la hormiga (Samaniego)", "El cuervo y el zorro", "La lechera",
           "El león y el ratón (Samaniego)", "Congreso de los ratones", "La gallina de los huevos de oro (Samaniego)",
           "Las moscas (Samaniego)", "El parto de los montes"]


def limpiar(t):
    lineas = [l.strip() for l in t.splitlines()]
    # quitar la cabecera de Wikisource (hasta "metadatos"/"Nota:" o la línea "FÁBULA n")
    corte = 0
    for i, l in enumerate(lineas):
        if "metadatos" in l or l.startswith("Nota:") or re.match(r"^F[ÁA]BULA\b", l) or l == "i: i":
            corte = i + 1
    lineas = lineas[corte:]
    lineas = [l for l in lineas if l and not (l.isupper() and len(l) > 3) and not re.match(r"^[←→]|.*[←→]$", l)]
    return lineas


g = Guia("Fábulas de Samaniego", "Libros para leer")
g.portada("Selección de ocho fábulas en verso de Félix María de Samaniego (1745-1801), publicadas por primera vez "
          "en 1781. Son historias cortas de animales que terminan con una enseñanza (moraleja). "
          "Obra de dominio público.",
          "**Fuente:** texto tomado de Wikisource en español [1][2], que transcribe ediciones antiguas; por eso "
          "algunas fábulas conservan la ortografía de la época (por ejemplo, \"á\" en lugar de \"a\").")
for t in FABULAS:
    versos = limpiar(get(t))
    nombre = re.sub(r"\s*\(Samaniego\)", "", t)
    if len(versos) < 4 or any("desambiguación" in v for v in versos):
        print("AVISO: texto corto en", t, versos); continue
    if g.get_y() > 200: g.add_page()
    g.sec(nombre)
    g.set_font("S", "", 11); g.set_text_color(30, 30, 30)
    for v in versos:
        if g.get_y() > 270: g.add_page()
        g.set_x(35); g.multi_cell(0, 5.6, v)
    g.ln(4)
g.referencias([
    "Samaniego, Félix María de. *Fábulas en verso castellano para el uso del Real Seminario Bascongado*. Valencia: Benito Monfort, 1781. Dominio público.",
    "Wikisource en español. *Fábulas de Samaniego*. https://es.wikisource.org/wiki/F%C3%A1bulas_de_Samaniego (consultado el 19/11/2026).",
])
g.guardar("fabulas-samaniego.pdf")
