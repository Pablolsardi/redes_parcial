#!/usr/bin/env python3
"""Figuras de la versión 3.0 de la guía: diagramas estáticos y animaciones nuevas.

Cada función devuelve el HTML de una <figure>. FIG junta todas por nombre.
Las clases (d-*, a-*) están definidas en fuente/guia.css.
"""

W = 640


def cl(c):
    return f' class="{c}"' if c else ""


def T(x, y, s, c="", a="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{a}"{cl(c)}>{s}</text>'


def R(x, y, w, h, c, rx=6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"{cl(c)}/>'


def L(x1, y1, x2, y2, c, extra=""):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{cl(c)}{extra}/>'


def P(d, c, extra=""):
    return f'<path d="{d}"{cl(c)}{extra}/>'


def marker(mid, c):
    return (f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="{c}"/></marker>')


def diag(label, h, body, cap):
    return (f'<figure class="diag" role="img" aria-label="{label}"><svg viewBox="0 0 {W} {h}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


def anim(label, h, body, cap):
    return (f'<figure class="anim" role="img" aria-label="{label}"><svg viewBox="0 0 {W} {h}">{body}</svg>'
            f'<figcaption><button type="button" class="anim-btn" aria-label="Pausar">⏸</button><span>{cap}</span></figcaption></figure>')


def badge(x, y, n):
    return f'<circle cx="{x}" cy="{y}" r="10" class="d-on"/>' + T(x, y + 4.2, n, "d-w")


class A:
    """Animación SMIL: todo comparte una duración y se enciende por ventanas de tiempo (0 a 1)."""

    def __init__(self, dur):
        self.dur = f"{dur}s"

    def an(self, attr, values, times):
        v = ";".join(str(x) for x in values)
        k = ";".join(f"{t:g}" for t in times)
        return f'<animate attributeName="{attr}" values="{v}" keyTimes="{k}" dur="{self.dur}" repeatCount="indefinite"/>'

    def show(self, inner, t0, t1=0.97):
        e = 0.004
        return f'<g opacity="0">{self.an("opacity", [0, 0, 1, 1, 0, 0], [0, t0, t0 + e, t1, t1 + e, 1])}{inner}</g>'

    def arrow(self, x1, y1, x2, y2, c, mid, t0, grow=0.06, t1=0.97):
        ln = (f'<line x1="{x1}" y1="{y1}" x2="{x1}" y2="{y1}" class="a-ar {c}" marker-end="url(#{mid})">'
              f'{self.an("x2", [x1, x1, x2, x2], [0, t0, t0 + grow, 1])}'
              f'{self.an("y2", [y1, y1, y2, y2], [0, t0, t0 + grow, 1])}</line>')
        return self.show(ln, t0, t1)

    def move(self, inner, pts, t0=None, t1=None):
        """Mueve un grupo por una lista de (t, x, y). Visible entre el primer y el último t (o t0..t1)."""
        ts = [p[0] for p in pts]
        vals = [f"{p[1]} {p[2]}" for p in pts]
        if ts[0] > 0:
            ts = [0] + ts
            vals = [vals[0]] + vals
        if ts[-1] < 1:
            ts = ts + [1]
            vals = vals + [vals[-1]]
        k = ";".join(f"{t:g}" for t in ts)
        g = (f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(vals)}" '
             f'keyTimes="{k}" dur="{self.dur}" repeatCount="indefinite"/>{inner}</g>')
        return self.show(g, pts[0][0] if t0 is None else t0, pts[-1][0] if t1 is None else t1)


# ----------------------------------------------------------------- estáticos

def lan_man_wan():
    b = R(14, 14, 612, 222, "d-zn3", 16) + T(30, 36, "WAN · países y continentes · de proveedores · ej.: Internet", "d-t", "start")
    b += R(40, 54, 372, 166, "d-zn2", 14) + T(56, 76, "MAN · una ciudad (radio &lt; 100 km)", "d-t", "start")
    b += R(60, 92, 160, 110, "d-zn1", 12) + T(140, 112, "LAN", "d-t") + T(140, 128, "edificio o campus", "d-n")
    for i, x in enumerate((88, 128, 168)):
        b += R(x - 12, 162, 24, 18, "d-f1", 3) + L(x, 162, 140, 150, "d-ln")
    b += R(118, 138, 44, 14, "d-on", 3)
    b += R(244, 92, 148, 110, "d-zn1", 12) + T(318, 112, "otra LAN", "d-t") + T(318, 128, "otra sede", "d-n")
    for x in (282, 318, 354):
        b += R(x - 12, 162, 24, 18, "d-f1", 3) + L(x, 162, 318, 150, "d-ln")
    b += R(296, 138, 44, 14, "d-on", 3)
    b += L(162, 145, 296, 145, "d-a2")
    b += R(456, 92, 150, 110, "d-zn2", 14) + T(531, 112, "otra ciudad", "d-t") + T(531, 128, "su propia MAN", "d-n")
    b += R(486, 146, 90, 40, "d-zn1", 10) + T(531, 170, "LAN", "d-n")
    b += L(412, 150, 456, 150, "d-a3") + T(434, 142, "enlace", "d-z") + T(434, 166, "WAN", "d-z")
    return diag("Diagrama de LAN, MAN y WAN", 250, b,
                "Las tres escalas, una adentro de la otra: varias <b>LAN</b> unidas dentro de una ciudad forman una <b>MAN</b>, "
                "y las ciudades y países se unen por la <b>WAN</b>. Lo que define a cada una es el alcance y quién la administra.")


def elementos_lan():
    b = R(30, 100, 120, 56, "d-f1") + T(90, 124, "Servidor", "d-l") + T(90, 142, "ofrece servicios", "d-s")
    b += R(150, 118, 34, 20, "d-f3", 3) + T(167, 132, "NIC", "d-z")
    b += L(184, 128, 262, 128, "d-ln") + T(223, 152, "medio: UTP", "d-n")
    b += R(262, 108, 116, 40, "d-f0") + T(320, 133, "Switch", "d-l")
    for y, name, sub in ((24, "PC", "cliente"), (106, "Notebook", "cliente"), (188, "Impresora de red", "cliente")):
        b += R(474, y, 136, 44, "d-f1") + T(542, y + 20, name, "d-l") + T(542, y + 35, sub, "d-s")
        b += R(440, y + 12, 34, 20, "d-f3", 3) + T(457, y + 26, "NIC", "d-z")
        b += P(f"M378,128 H410 V{y + 22} H440", "d-ln")
    b += badge(30, 100, "1") + badge(610, 24, "2") + badge(610, 106, "2") + badge(610, 188, "2")
    b += badge(167, 106, "3") + badge(223, 128, "4") + badge(262, 108, "5")
    b += badge(40, 196, "6") + T(58, 200, "Software de red: el SO del servidor y el de las estaciones", "d-n", "start")
    b += T(320, 250, "1 servidor · 2 clientes · 3 NIC · 4 medio · 5 dispositivo de interconexión · 6 software", "d-z")
    return diag("Diagrama de los elementos de una LAN", 262, b,
                "Los seis elementos de una LAN en una red mínima. Cada equipo llega al medio a través de su <b>NIC</b>, "
                "y el dispositivo de interconexión (acá un switch) une los tramos.")


def trama_8023():
    campos = [("Preámbulo", "7 B", 86, "d-old d-dash"), ("SD", "1 B", 40, "d-old d-dash"), ("MAC destino", "6 B", 96, "d-f2"),
              ("MAC origen", "6 B", 96, "d-f2"), ("Long./Tipo", "2 B", 84, "d-f1"), ("Datos + relleno", "46 a 1500 B", 136, "d-f3"),
              ("FCS", "4 B", 62, "d-f0")]
    b = T(320, 22, "Trama IEEE 802.3, campo por campo", "d-t")
    x = 20
    for name, size, w, c in campos:
        b += R(x, 40, w - 3, 40, c, 4) + T(x + (w - 3) / 2, 64.5, name, "d-l") + T(x + (w - 3) / 2, 96, size, "d-z")
        x += w
    b += P("M146,108 v8 H617 v-8", "d-br") + T(381, 134, "esto es lo que cuenta: mínimo 64 B · máximo 1518 B", "d-bl")
    b += T(83, 122, "sincronismo:", "d-n") + T(83, 136, "no cuenta", "d-n")
    b += T(320, 160, "64 = 6 + 6 + 2 + 46 + 4     ·     1518 = 6 + 6 + 2 + 1500 + 4", "d-z")
    return diag("Diagrama de la trama 802.3", 170, b,
                "La trama 802.3. El tamaño mínimo (64 B) y el máximo (1518 B) se cuentan desde la <b>MAC destino</b> hasta el <b>FCS</b>, "
                "sin el preámbulo ni el SD. Si los datos no llegan a 46 B se completan con relleno (<i>padding</i>).")


def regla_543():
    b = T(320, 22, "El camino más largo permitido entre dos PCs (Ethernet de 10 Mbps)", "d-t")
    x = 34
    y = 92
    for i in range(5):
        poblado = i in (0, 2, 4)
        b += L(x, y, x + 92, y, "d-a1" if poblado else "d-ln2 d-dash")
        b += T(x + 46, y - 22, f"segmento {i + 1}", "d-z")
        b += T(x + 46, y - 9, "poblado" if poblado else "solo enlace", "d-s")
        if poblado:
            for k, px in enumerate((x + 24, x + 68)):
                b += L(px, y, px, y + 22, "d-ln") + R(px - 11, y + 22, 22, 16, "d-f1", 3)
        x += 92
        if i < 4:
            b += R(x, y - 14, 28, 28, "d-f2", 5) + T(x + 14, y + 4.5, f"R{i + 1}", "d-l")
            x += 28
    b += T(58, 148, "PC A", "d-l") + T(582, 148, "PC B", "d-l")
    b += T(320, 180, "5 segmentos  ·  4 repetidores (R1 a R4)  ·  3 segmentos poblados", "d-tot")
    return diag("Diagrama de la regla 5-4-3", 196, b,
                "La regla 5-4-3: entre dos PCs puede haber como máximo <b>5 segmentos</b> unidos por <b>4 repetidores</b>, y solo "
                "<b>3</b> de esos segmentos pueden tener PCs. Los otros dos solo unen repetidores. Todo el conjunto es un único dominio de colisión.")


def puesta_a_tierra():
    b = R(150, 20, 340, 200, "d-f0", 4) + L(150, 87, 490, 87, "d-ln2") + L(150, 153, 490, 153, "d-ln2")
    for y, piso in ((53, "piso 2"), (120, "piso 1")):
        b += R(180, y - 9, 60, 18, "d-f3", 3) + T(210, y + 4.5, "TGB", "d-l")
        b += R(380, y - 20, 56, 40, "d-f1", 4) + T(408, y + 4.5, "Rack", "d-l")
        b += L(240, y, 380, y, "d-gnd") + T(500, y + 4, piso, "d-n", "start")
    b += R(170, 176, 80, 20, "d-f3", 3) + T(210, 190.5, "TMGB", "d-l")
    b += R(380, 166, 56, 40, "d-f1", 4) + T(408, 190.5, "Rack", "d-l") + L(250, 186, 380, 186, "d-gnd")
    b += T(500, 190, "planta baja", "d-n", "start")
    b += L(210, 62, 210, 111, "d-gnd") + L(210, 129, 210, 176, "d-gnd") + L(210, 196, 210, 238, "d-gnd")
    b += L(196, 238, 224, 238, "d-gnd") + L(201, 245, 219, 245, "d-gnd") + L(206, 252, 214, 252, "d-gnd")
    b += T(234, 249, "jabalina / tierra del sistema eléctrico", "d-n", "start")
    b += T(140, 50, "TGB: barra de", "d-n", "end") + T(140, 64, "cada sala", "d-n", "end")
    b += T(140, 96, "TBB: une la TMGB", "d-n", "end") + T(140, 110, "con las TGB", "d-n", "end") + L(144, 100, 207, 100, "d-zoom")
    b += T(140, 182, "TMGB: barra", "d-n", "end") + T(140, 196, "principal", "d-n", "end")
    return diag("Diagrama de la puesta a tierra según TIA-607", 262, b,
                "La jerarquía de la <b>TIA-607</b>: tierra del edificio → <b>TMGB</b> (barra principal) → <b>TBB</b> (el conductor que sube por los pisos) "
                "→ <b>TGB</b> (una barra por sala) → racks y patch panels. Así todos los equipos quedan al mismo potencial.")


def asociacion_wifi():
    xa, xb = 130, 510
    b = "<defs>" + marker("aw1", "d-m1") + marker("aw2", "d-m2") + marker("aw3", "d-m3") + "</defs>"
    b += R(xa - 80, 10, 160, 30, "d-f1", 7) + T(xa, 29.5, "Cliente (estación)", "d-l")
    b += R(xb - 80, 10, 160, 30, "d-f0", 7) + T(xb, 29.5, "Access Point", "d-l")
    b += L(xa, 40, xa, 278, "d-life") + L(xb, 40, xb, 278, "d-life")

    def flecha(y, der, c, mid, txt):
        x1, x2 = (xa, xb) if der else (xb, xa)
        return L(x1 + (4 if der else -4), y, x2 - (4 if der else -4), y, c, f' marker-end="url(#{mid})"') + T(320, y - 6, txt, "d-n")

    b += T(320, 62, "1 · Escaneo: descubrir el AP", "d-t")
    b += flecha(88, False, "d-a3", "aw3", "pasivo: beacon periódico con el SSID")
    b += flecha(112, True, "d-a3", "aw3", "activo: probe request preguntando por el SSID")
    b += T(320, 142, "2 · Autenticación: confirmar la identidad", "d-t")
    b += flecha(168, True, "d-a1", "aw1", "pedido de autenticación")
    b += flecha(192, False, "d-a1", "aw1", "respuesta: sí o no (Open System)")
    b += T(320, 222, "3 · Asociación", "d-t")
    b += flecha(248, True, "d-a2", "aw2", "pedido de asociación (velocidades, SSID)")
    b += flecha(272, False, "d-a2", "aw2", "respuesta con el ID de asociación")
    b += T(320, 300, "Recién ahora pueden intercambiar tramas de datos", "d-bl")
    return diag("Diagrama de la conexión de un dispositivo a un access point", 310, b,
                "Las tres fases para entrar a una red Wi-Fi, siempre en este orden: <b>escaneo</b>, <b>autenticación</b> y <b>asociación</b>. "
                "Con Shared Key la autenticación son 4 mensajes (pedido, texto de desafío, texto cifrado y resultado).")


def recta_subred():
    x0, k = 30, 580 / 256
    b = T(320, 22, "¿En qué subred cae 172.16.132.70/20?  Salto 16 en el tercer octeto", "d-t")
    b += R(x0 + 128 * k, 76, 16 * k, 28, "d-f3", 3)
    b += L(x0, 90, x0 + 580, 90, "d-ln")
    for m in range(0, 257, 16):
        x = round(x0 + m * k, 1)
        b += L(x, 82, x, 98, "d-ln")
        if m < 256:
            b += T(x, 116, str(m), "d-l" if m in (128, 144) else "d-z")
    xi = round(x0 + 132 * k, 1)
    b += f'<circle cx="{xi}" cy="90" r="4.5" class="d-cb"/>' + L(xi, 84, xi, 60, "d-zoom") + T(xi, 52, "132 cae acá", "d-l")
    b += T(338, 142, "red 172.16.128.0  ·  hosts 172.16.128.1 a 172.16.143.254  ·  broadcast 172.16.143.255", "d-bl")
    b += T(320, 168, "Cada tramo es una subred: empieza en un múltiplo del salto y termina uno antes del siguiente.", "d-n")
    return diag("Diagrama para ubicar una IP en su subred", 180, b,
                "El atajo sin binario: marcá los múltiplos del salto en el octeto partido y fijate entre cuáles cae. "
                "<b>128 ≤ 132 &lt; 144</b>, así que la subred empieza en 128 y su broadcast es la dirección anterior a la 144.")


# ---------------------------------------------------------------- animaciones

def vlan():
    a = A(13)
    b = L(200, 130, 440, 130, "a-trunk") + T(320, 210, "enlace troncal: lleva las dos VLAN,", "a-small") + T(320, 225, "con etiqueta 802.1Q", "a-small")
    for (x, y, c, name, lx, ly, sx, sy) in ((30, 30, "a-v1", "A · VLAN 10", 80, 64, 135, 110), (30, 196, "a-v2", "B · VLAN 20", 80, 196, 135, 150),
                                            (510, 30, "a-v1", "C · VLAN 10", 560, 64, 505, 110), (510, 196, "a-v2", "D · VLAN 20", 560, 196, 505, 150)):
        b += L(lx, ly, sx, sy, "a-link") + R(x, y, 100, 34, c, 7) + T(x + 50, y + 21.5, name, "a-b")
    b += R(110, 110, 90, 40, "a-sw", 7) + T(155, 134.5, "SW1", "a-b") + R(440, 110, 90, 40, "a-sw", 7) + T(485, 134.5, "SW2", "a-b")
    fr = R(-11, -8, 22, 16, "a-p1", 3)
    b += a.move(fr, [(0.04, 80, 64), (0.14, 135, 110)], t1=0.16)
    tag = R(-11, -8, 22, 16, "a-p1", 3) + R(-11, -20, 22, 11, "a-p3", 2) + T(0, -26, "etiqueta VLAN 10", "a-small t3")
    b += a.move(tag, [(0.18, 205, 130), (0.36, 435, 130)], t1=0.38)
    b += a.move(fr, [(0.40, 505, 110), (0.50, 551, 72)], t1=0.95)
    b += a.show(T(108, 180, "✕", "a-x"), 0.18) + a.show(T(532, 180, "✕", "a-x"), 0.40)
    b += a.show(R(506, 26, 108, 42, "a-hl", 9), 0.52)
    y = 256
    b += a.show(T(320, y, "A (VLAN 10) manda un broadcast", "a-lbl t1"), 0.02, 0.165)
    b += a.show(T(320, y, "SW1 no lo saca por el puerto de B (VLAN 20); por el troncal va etiquetado", "a-lbl t3"), 0.18, 0.385)
    b += a.show(T(320, y, "SW2 le quita la etiqueta y lo entrega solo a los puertos de la VLAN 10", "a-lbl t1"), 0.40, 0.515)
    b += a.show(T(320, y, "Lo recibe C y nadie más: cada VLAN es su propio dominio de broadcast", "a-b t2"), 0.53)
    return anim("Animación de un broadcast dentro de una VLAN", 268, b,
                "Dos switches, dos VLAN. El broadcast de A solo llega a los equipos de su misma VLAN, aunque estén en otro switch. "
                "Por el <b>troncal</b> la trama viaja con la <b>etiqueta 802.1Q</b>; en los enlaces de <b>acceso</b> sale sin etiqueta, y la PC ni se entera de que hay VLAN.")


def url_enter():
    a = A(17)
    xs = {"pc": 70, "gw": 240, "dns": 420, "web": 570}
    b = "<defs>" + marker("ue1", "f1") + marker("ue2", "f2") + marker("ue3", "f3") + "</defs>"
    for k, name, c in (("pc", "Tu PC", "a-nd"), ("gw", "Gateway", "a-sw"), ("dns", "Servidor DNS", "a-nd"), ("web", "Servidor web", "a-nd")):
        b += R(xs[k] - 55, 10, 110, 30, c, 7) + T(xs[k], 29.5, name, "a-b") + L(xs[k], 41, xs[k], 300, "a-life")
    pasos = [
        (0.03, "pc", "gw", 70, "s3", "ue3", "t3", "1 · ARP (broadcast)"),
        (0.10, "gw", "pc", 94, "s3", "ue3", "t3", "la MAC del gateway"),
        (0.19, "pc", "dns", 126, "s2", "ue2", "t2", "2 · DNS (UDP 53): ¿IP de www.utn.edu.ar?"),
        (0.27, "dns", "pc", 150, "s2", "ue2", "t2", "respuesta: la IP del servidor web"),
        (0.37, "pc", "web", 182, "s1", "ue1", "t1", "3 · TCP: SYN al puerto 443"),
        (0.44, "web", "pc", 206, "s1", "ue1", "t1", "SYN-ACK"),
        (0.51, "pc", "web", 230, "s1", "ue1", "t1", "ACK · conexión establecida"),
        (0.61, "pc", "web", 262, "s3", "ue3", "t3", "4 · HTTP: GET (pide la página)"),
        (0.69, "web", "pc", 286, "s3", "ue3", "t3", "200 OK + el HTML"),
    ]
    for t0, o, d, y, sc, mid, tc, txt in pasos:
        x1, x2 = xs[o], xs[d]
        b += a.arrow(x1, y, x2, y, sc, mid, t0)
        b += a.show(T((x1 + x2) / 2, y - 6, txt, "a-lbl " + tc), t0)
    b += a.show(T(320, 326, "Recién después de los cuatro pasos aparece la página", "a-b t2"), 0.78)
    return anim("Animación de lo que pasa al escribir una dirección y apretar Enter", 338, b,
                "Lo que viaja cuando escribís una dirección y apretás Enter, en orden: <b>ARP</b> (la MAC del gateway), <b>DNS</b> (la IP del nombre), "
                "el <b>saludo de tres vías</b> de TCP y recién ahí <b>HTTP</b>. Todo lo que va a otra red pasa por el gateway. Es la secuencia que se capturó en el TP6.")


def tcp_perdida():
    a = A(19)
    xa, xb = 110, 530
    b = "<defs>" + marker("tp1", "f1") + marker("tp2", "f2") + marker("tp3", "f3") + marker("tpb", "fbad") + "</defs>"
    b += R(xa - 75, 10, 150, 30, "a-nd", 7) + T(xa, 29.5, "Emisor A", "a-b") + R(xb - 75, 10, 150, 30, "a-nd", 7) + T(xb, 29.5, "Receptor B", "a-b")
    b += L(xa, 41, xa, 372, "a-life") + L(xb, 41, xb, 372, "a-life")

    def paso(t0, der, y, dy, sc, mid, tc, txt, x2=None):
        x1 = xa if der else xb
        xe = (xb if der else xa) if x2 is None else x2
        return a.arrow(x1, y, xe, y + dy, sc, mid, t0) + a.show(T(320, y + 3, txt, "a-lbl " + tc), t0)

    b += paso(0.03, True, 62, 20, "s1", "tp1", "t1", "seq=1 · 500 bytes")
    b += paso(0.10, False, 96, 20, "s2", "tp2", "t2", "ACK ack=501")
    b += a.arrow(xa, 130, 330, 140, "sbad", "tpb", 0.17) + a.show(T(250, 126, "seq=501 · 500 bytes", "a-lbl tbad"), 0.17)
    b += a.show(T(350, 146, "✕", "a-x") + T(440, 144, "se pierde", "a-small tbad"), 0.23)
    b += a.show(T(xa + 12, 168, "⏳ no llega el ACK: vence el temporizador", "a-small t3", "start"), 0.27)
    b += paso(0.34, True, 184, 20, "s3", "tp3", "t3", "retransmite seq=501 · 500 bytes")
    b += paso(0.42, False, 218, 20, "s2", "tp2", "t2", "ACK ack=1001")
    b += a.show(L(60, 254, 580, 254, "a-life") + T(320, 270, "Cierre en 4 pasos: cada sentido se cierra por separado", "a-b"), 0.50)
    b += paso(0.55, True, 286, 12, "s1", "tp1", "t1", "FIN")
    b += paso(0.62, False, 308, 12, "s2", "tp2", "t2", "ACK")
    b += paso(0.69, False, 330, 12, "s2", "tp2", "t2", "FIN")
    b += paso(0.76, True, 352, 12, "s1", "tp1", "t1", "ACK")
    return anim("Animación de la retransmisión y el cierre de una conexión TCP", 384, b,
                "Qué hace TCP cuando algo se pierde: el segundo segmento no llega, así que el ACK <b>no avanza</b>; al vencer el temporizador, A lo "
                "<b>retransmite</b> y recién ahí B confirma hasta el byte 1000 (ACK 1001). Abajo, el cierre: FIN y ACK en un sentido, FIN y ACK en el otro.")


def trio_puntaje():
    return ('<div class="trio"><div class="pos"><b>+1</b><span>si acertás</span></div>'
            '<div class="neu"><b>0</b><span>si la dejás en blanco</span></div>'
            '<div class="neg"><b>−0,5</b><span>si errás</span></div></div>')


FIG = {
    "lan_man_wan": lan_man_wan, "elementos_lan": elementos_lan, "trama_8023": trama_8023, "regla_543": regla_543,
    "puesta_a_tierra": puesta_a_tierra, "asociacion_wifi": asociacion_wifi, "recta_subred": recta_subred,
    "vlan": vlan, "url_enter": url_enter, "tcp_perdida": tcp_perdida, "trio_puntaje": trio_puntaje,
}

if __name__ == "__main__":
    for k, f in FIG.items():
        print(k, len(f()))
