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


# ---------------------------------------------------------------- v3.4

def nodo_expuesto():
    a = A(15)
    xs = {"A": 70, "B": 240, "C": 400, "D": 570}
    b = '<ellipse cx="240" cy="140" rx="200" ry="92" class="a-cov1"/><ellipse cx="400" cy="140" rx="200" ry="92" class="a-cov3"/>'
    b += T(56, 226, "alcance de B", "a-small t1", "start") + T(584, 226, "alcance de C", "a-small t3", "end")
    for k, x in xs.items():
        b += R(x - 30, 125, 60, 30, "a-nd", 7) + T(x, 144.5, "PC " + k, "a-b")
    pk = lambda c: f'<circle r="7" class="{c}"/>'
    b += a.move(pk("a-p1"), [(0.05, 210, 140), (0.17, 100, 140)])
    b += a.move(pk("a-p1"), [(0.30, 210, 140), (0.42, 100, 140)])
    b += a.show(T(400, 186, "oye a B: ocupado", "a-small t3"), 0.19, 0.44)
    b += a.show(T(400, 204, "⏳ espera", "a-b t3"), 0.24, 0.44)
    b += a.show(R(530, 116, 80, 48, "a-hl", 9) + R(30, 116, 80, 48, "a-hl", 9), 0.47, 0.62)
    b += a.show(T(570, 186, "no oye a B", "a-small t1"), 0.47, 0.62) + a.show(T(70, 186, "no oye a C", "a-small t3"), 0.47, 0.62)
    b += a.move(pk("a-p1"), [(0.66, 210, 140), (0.80, 100, 140)], t1=0.95)
    b += a.move(pk("a-p2"), [(0.66, 430, 140), (0.80, 540, 140)], t1=0.95)
    b += a.show(T(70, 114, "✓", "a-big a-ok") + T(570, 114, "✓", "a-big a-ok"), 0.81)
    y = 24
    b += a.show(T(320, y, "B le transmite a A", "a-lbl t1"), 0.02, 0.17)
    b += a.show(T(320, y, "C quiere mandarle a D: escucha el canal y oye a B", "a-lbl t3"), 0.17, 0.30)
    b += a.show(T(320, y, "Cree que está ocupado y espera, aunque no haría falta", "a-lbl t3"), 0.30, 0.45)
    b += a.show(T(320, y, "D está fuera del alcance de B, y A fuera del de C", "a-lbl t1"), 0.45, 0.63)
    b += a.show(T(320, y, "Si C transmitía igual, A y D recibían bien las dos tramas", "a-lbl t2"), 0.63, 0.86)
    b += a.show(T(320, y, "Nodo expuesto: espera sin necesidad y se desaprovecha el canal", "a-b t3"), 0.86)
    return anim("Animación del problema del nodo expuesto", 260, b,
                "<b>Nodo expuesto</b>, el caso opuesto al oculto: C oye la transmisión de B y concluye que el canal está ocupado, pero su "
                "destino (D) está fuera del alcance de B, y el destino de B (A) está fuera del alcance de C. Las dos transmisiones podían "
                "convivir sin chocar: C espera de más y el canal se desaprovecha.")


FIG["nodo_expuesto"] = nodo_expuesto


def csma_ca():
    """Línea de tiempo de CSMA/CA: espera aleatoria, la que llega a 0 transmite, la otra congela."""
    a = A(20)
    X0, X1, T1 = 130, 625, 0.86          # eje de tiempo y momento en que termina el barrido
    tx = lambda x: round((x - X0) / (X1 - X0) * T1 + 0.03, 4)
    rows = {"canal": 62, "A": 126, "B": 190}
    b = ""
    for k, y in rows.items():
        b += L(X0, y + 17, X1, y + 17, "a-life")
    b += T(X0 - 12, rows["canal"] + 5, "Canal", "a-b", "end") + T(X0 - 12, rows["A"] + 5, "Estación A", "a-b", "end") + T(X0 - 12, rows["B"] + 5, "Estación B", "a-b", "end")

    def barra(x, x2, y, cls, txt="", tcls="a-tw"):
        w = x2 - x
        r_ = (f'<rect x="{x}" y="{y - 13}" width="0" height="26" rx="5" class="{cls}">'
              f'{a.an("width", [0, 0, w, w], [0, tx(x), tx(x2), 1])}</rect>')
        t_ = a.show(T((x + x2) / 2, y + 4.5, txt, tcls), tx(x2) - 0.01) if txt else ""
        return a.show(r_, tx(x)) + t_

    # 1) el canal está ocupado por otra estación
    b += barra(X0, 210, rows["canal"], "a-sw", "ocupado", "a-small")
    b += a.show(T(170, rows["A"] + 4.5, "escucha…", "a-small"), 0.03) + a.show(T(170, rows["B"] + 4.5, "escucha…", "a-small"), 0.03)
    # 2) espera aleatoria (backoff) en ranuras: A sortea 3, B sortea 6
    S = 22
    for i in range(3):
        x = 214 + i * S
        b += a.show(R(x, rows["A"] - 12, S - 3, 24, "a-step", 4) + T(x + (S - 3) / 2, rows["A"] + 4.5, str(3 - i), "a-mono"), tx(x))
        b += a.show(R(x, rows["B"] - 12, S - 3, 24, "a-step", 4) + T(x + (S - 3) / 2, rows["B"] + 4.5, str(6 - i), "a-mono"), tx(x))
    # 3) A llega a 0 y transmite; B oye el canal ocupado y congela su cuenta en 3
    xa = 214 + 3 * S
    b += barra(xa, xa + 120, rows["A"], "a-p1", "DATOS de A")
    b += barra(xa, xa + 120, rows["canal"], "a-p1", "A transmite")
    b += a.show(R(xa, rows["B"] - 12, 150, 24, "a-step", 4) + T(xa + 75, rows["B"] + 4.5, "congela la cuenta en 3", "a-small t3"), tx(xa) + 0.01)
    xk = xa + 128
    b += barra(xk, xk + 34, rows["canal"], "a-p2", "ACK")
    # 4) B retoma desde 3 y transmite
    xb = xk + 42
    for i in range(3):
        x = xb + i * S
        b += a.show(R(x, rows["B"] - 12, S - 3, 24, "a-step", 4) + T(x + (S - 3) / 2, rows["B"] + 4.5, str(3 - i), "a-mono"), tx(x))
    xd = xb + 3 * S
    b += barra(xd, X1 - 4, rows["B"], "a-p3", "DATOS de B")
    b += barra(xd, X1 - 4, rows["canal"], "a-p3", "B transmite")
    # cursor de tiempo
    cur = (f'<line x1="{X0}" y1="40" x2="{X0}" y2="214" class="a-hl" style="stroke-dasharray:3 4;stroke-width:1.5">'
           f'{a.an("x1", [X0, X0, X1, X1], [0, 0.03, T1 + 0.03, 1])}{a.an("x2", [X0, X0, X1, X1], [0, 0.03, T1 + 0.03, 1])}</line>')
    b += a.show(cur, 0.03, T1 + 0.03)
    y = 246
    b += a.show(T(320, y, "El canal está ocupado: las dos escuchan y esperan", "a-lbl"), 0.02, tx(214))
    b += a.show(T(320, y, "Se libera: cada una espera un tiempo al azar (A sorteó 3 ranuras, B sorteó 6)", "a-lbl t3"), tx(214), tx(xa))
    b += a.show(T(320, y, "A llega a 0 y transmite; B oye el canal ocupado y congela su cuenta", "a-lbl t1"), tx(xa), tx(xk))
    b += a.show(T(320, y, "El receptor confirma con ACK: sin ACK, A retransmitiría", "a-lbl t2"), tx(xk), tx(xb))
    b += a.show(T(320, y, "B sigue desde 3 (no vuelve a sortear) y transmite: no chocaron", "a-lbl t3"), tx(xb))
    return anim("Animación del acceso al medio CSMA/CA", 262, b,
                "<b>CSMA/CA</b> en una línea de tiempo. Como por aire no se puede detectar una colisión, se trata de <b>evitarla</b>: "
                "cuando el canal se libera, cada estación espera un tiempo al azar (<i>backoff</i>) y transmite la que termina primero. "
                "La otra oye el canal ocupado, congela su cuenta y la retoma después. Cada trama se confirma con <b>ACK</b>.")


def half_full():
    a = A(12)
    b = ""
    for y, dev, tit in ((78, "Hub", "Half duplex · con hub"), (206, "Switch", "Full duplex · con switch")):
        b += T(24, y - 44, tit, "a-b", "start")
        b += R(30, y - 16, 84, 32, "a-nd", 7) + T(72, y + 4.5, "PC A" if y < 100 else "PC C", "a-b")
        b += R(526, y - 16, 84, 32, "a-nd", 7) + T(568, y + 4.5, "PC B" if y < 100 else "PC D", "a-b")
        b += R(278, y - 16, 84, 32, "a-sw", 7) + T(320, y + 4.5, dev, "a-b")
    b += L(114, 78, 278, 78, "a-link") + L(362, 78, 526, 78, "a-link")
    for yy in (198, 214):
        b += L(114, yy, 278, yy, "a-link") + L(362, yy, 526, yy, "a-link")
    b += T(196, 192, "transmite", "a-port") + T(196, 230, "recibe", "a-port")
    pk = lambda c: f'<circle r="7" class="{c}"/>'
    # half: A→B, después B→A, después los dos a la vez → colisión
    b += a.move(pk("a-p1"), [(0.04, 122, 78), (0.22, 518, 78)])
    b += a.move(pk("a-p3"), [(0.27, 518, 78), (0.45, 122, 78)])
    b += a.move(pk("a-p1"), [(0.52, 122, 78), (0.60, 270, 78)], t1=0.66)
    b += a.move(pk("a-p3"), [(0.52, 518, 78), (0.60, 370, 78)], t1=0.66)
    b += a.show(T(320, 52, "✕ colisión", "a-x"), 0.60, 0.74)
    b += a.show(T(320, 120, "uno por vez · con CSMA/CD", "a-small t3"), 0.02, 0.50)
    b += a.show(T(320, 120, "si transmiten juntos, chocan", "a-small tbad"), 0.50, 0.78)
    b += a.show(T(320, 120, "uno por vez · con CSMA/CD", "a-small t3"), 0.78)
    # full: los dos sentidos a la vez, siempre
    for t0 in (0.04, 0.36, 0.68):
        b += a.move(pk("a-p1"), [(t0, 122, 198), (t0 + 0.24, 518, 198)])
        b += a.move(pk("a-p3"), [(t0, 518, 214), (t0 + 0.24, 122, 214)])
    b += T(320, 254, "los dos sentidos a la vez · sin colisiones, CSMA/CD no actúa", "a-small t2")
    return anim("Animación de half duplex contra full duplex", 266, b,
                "<b>Half duplex</b> (arriba): con un hub el medio es compartido, así que se transmite o se recibe, nunca las dos cosas, "
                "y si dos arrancan juntos chocan. <b>Full duplex</b> (abajo): el enlace con el switch es dedicado y tiene un par para cada "
                "sentido, así que se transmite y se recibe al mismo tiempo, sin colisiones.")


def polling():
    a = A(13)
    mx, my = 320, 46
    sx = {1: 120, 2: 320, 3: 520}
    sy = 200
    b = R(mx - 60, my - 17, 120, 34, "a-sw", 7) + T(mx, my + 4.5, "Maestro", "a-b")
    for k, x in sx.items():
        b += L(mx, my + 17, x, sy - 17, "a-link") + R(x - 50, sy - 17, 100, 34, "a-nd", 7) + T(x, sy + 4.5, f"Esclavo {k}", "a-b")
    def via(k, t0, t1, up, c, txt):
        x = sx[k]
        p0, p1 = ((mx, my + 30), (x, sy - 24)) if not up else ((x, sy - 24), (mx + (x - mx) * 0.22, my + 44))
        g = R(-38, -11, 76, 22, c, 11) + T(0, 4.5, txt, "a-b" if c == "a-sw" else "a-tw")
        return a.move(g, [(t0, p0[0], p0[1]), (t1, p1[0], p1[1])], t1=t1 + 0.04)
    b += via(1, 0.04, 0.14, False, "a-p1", "¿datos?") + via(1, 0.17, 0.25, True, "a-sw", "no")
    b += via(2, 0.29, 0.38, False, "a-p1", "¿datos?") + via(2, 0.41, 0.51, True, "a-p2", "DATOS")
    b += via(3, 0.55, 0.64, False, "a-p1", "¿datos?") + via(3, 0.67, 0.75, True, "a-sw", "no")
    b += a.show(T(mx + 74, my + 5, "✕", "a-x", "start"), 0.82)
    y = 262
    b += a.show(T(320, y, "El maestro pregunta a cada esclavo, siempre en el mismo orden", "a-lbl t1"), 0.02, 0.29)
    b += a.show(T(320, y, "El esclavo 2 tiene datos: transmite solo cuando le preguntan", "a-lbl t2"), 0.29, 0.55)
    b += a.show(T(320, y, "Sigue con el 3 y vuelve a empezar: se sabe cuánto espera cada uno", "a-lbl t1"), 0.55, 0.80)
    b += a.show(T(320, y, "Si cae el maestro, nadie puede transmitir", "a-b tbad"), 0.80)
    return anim("Animación del método de acceso polling", 276, b,
                "<b>Polling</b>: el maestro interroga a los esclavos uno por uno y en orden; cada uno transmite solo cuando le toca. "
                "Es determinístico (el tiempo de espera está acotado), pero el maestro es un punto único de falla.")


def udp():
    a = A(13)
    xa, xb = 110, 530
    b = "<defs>" + marker("ud1", "f1") + marker("udb", "fbad") + "</defs>"
    b += R(xa - 75, 10, 150, 30, "a-nd", 7) + T(xa, 29.5, "Emisor", "a-b") + R(xb - 75, 10, 150, 30, "a-nd", 7) + T(xb, 29.5, "Receptor", "a-b")
    b += L(xa, 41, xa, 250, "a-life") + L(xb, 41, xb, 250, "a-life")
    b += a.arrow(xa, 60, xb, 96, "s1", "ud1", 0.04, 0.08) + a.show(T(xa - 12, 64, "datagrama 1", "a-small t1", "end"), 0.04)
    b += a.arrow(xa, 82, 330, 104, "sbad", "udb", 0.12, 0.06) + a.show(T(xa - 12, 86, "datagrama 2", "a-small tbad", "end"), 0.12)
    b += a.show(T(346, 110, "✕ se pierde", "a-small tbad", "start"), 0.19)
    b += a.arrow(xa, 104, xb, 192, "s1", "ud1", 0.22, 0.12) + a.show(T(xa - 12, 108, "datagrama 3", "a-small t1", "end"), 0.22)
    b += a.arrow(xa, 126, xb, 160, "s1", "ud1", 0.30, 0.08) + a.show(T(xa - 12, 130, "datagrama 4", "a-small t1", "end"), 0.30)
    b += a.show(T(xb + 12, 100, "llega 1.º", "a-small", "start"), 0.13) + a.show(T(xb + 12, 164, "llega 2.º: el 4", "a-small t3", "start"), 0.39)
    b += a.show(T(xb + 12, 196, "llega 3.º: el 3", "a-small t3", "start"), 0.35)
    y = 236
    b += a.show(T(320, y, "Manda sin abrir conexión y sin esperar confirmaciones", "a-lbl t1"), 0.02, 0.42)
    b += a.show(T(320, y, "Llegan 1, 4 y 3: desordenados y sin el 2. Nadie avisa ni retransmite", "a-lbl t3"), 0.42, 0.70)
    b += a.show(T(320, y, "Si hace falta, lo resuelve la aplicación (DNS vuelve a preguntar)", "a-lbl t2"), 0.70)
    return anim("Animación del envío de datagramas UDP", 250, b,
                "<b>UDP</b>, lo opuesto a TCP: no hay saludo, ni números de secuencia que ordenen, ni ACK, ni retransmisión. "
                "Lo que se pierde se pierde y puede llegar desordenado. A cambio es liviano y rápido: sirve para consultas cortas y para tiempo real.")


def banda():
    b = ""
    for ox, tit, sub in ((20, "Banda base · TDM", "toda la capacidad, una señal por turno"), (340, "Banda ancha · FDM", "varios canales a la vez, cada uno en su frecuencia")):
        b += T(ox + 140, 20, tit, "d-t") + T(ox + 140, 36, sub, "d-n")
        b += P(f"M{ox + 20},50 V196 H{ox + 286}", "d-ln")
        b += T(ox + 286, 212, "tiempo →", "d-z", "end") + T(ox + 14, 58, "frecuencia", "d-z", "end") if False else ""
        b += T(ox + 284, 212, "tiempo →", "d-z", "end")
        b += f'<text x="{ox + 12}" y="124" text-anchor="middle" class="d-z" transform="rotate(-90 {ox + 12} 124)">frecuencia →</text>'
    cls = ["d-f1", "d-f3", "d-f2"]
    for i in range(6):
        x = 42 + i * 43
        b += R(x, 62, 40, 126, cls[i % 3], 3) + T(x + 20, 129, "ABC"[i % 3], "d-l")
    for i, (c, n) in enumerate(zip(cls, ("canal 1", "canal 2", "canal 3"))):
        y = 62 + i * 43
        b += R(362, y, 262, 40, c, 3) + T(493, y + 24, n, "d-l")
    return diag("Diagrama de banda base contra banda ancha", 222, b,
                "<b>Banda base</b> (LAN): una sola señal digital usa todo el ancho del medio, y varias conversaciones se turnan en el "
                "tiempo (<b>TDM</b>). <b>Banda ancha</b> (WAN, TV por cable): el ancho de banda se reparte en varios canales analógicos "
                "que transmiten a la vez, cada uno en su frecuencia (<b>FDM</b>).")


def fisica_logica():
    b = "<defs>" + marker("fl1", "d-m1") + marker("fl3", "d-m3") + "</defs>"
    pcs = [(-100, -70), (100, -70), (100, 70), (-100, 70)]
    for ox, dev, tit, sub in ((160, "Hub", "Ethernet con hub", "estrella física · bus lógico"), (480, "MSAU", "Token Ring con MSAU", "estrella física · anillo lógico")):
        cy = 130
        b += T(ox, 20, tit, "d-t") + T(ox, 36, sub, "d-bl")
        for k, (dx, dy) in enumerate(pcs):
            b += L(ox, cy, ox + dx, cy + dy, "d-ln2")
        for k, (dx, dy) in enumerate(pcs):
            b += R(ox + dx - 26, cy + dy - 14, 52, 28, "d-f1", 5) + T(ox + dx, cy + dy + 4.5, f"PC {k + 1}", "d-l")
        b += R(ox - 32, cy - 16, 64, 32, "d-f0", 6) + T(ox, cy + 4.5, dev, "d-l")
    # hub: PC1 transmite y lo reciben todas
    ox, cy = 160, 130
    for dx, dy in pcs[1:]:
        b += L(ox + dx * 0.32, cy + dy * 0.32, ox + dx * 0.72, cy + dy * 0.72, "d-a1", ' marker-end="url(#fl1)"')
    b += L(ox - 72, cy - 50, ox - 36, cy - 25, "d-a1", ' marker-end="url(#fl1)"')
    b += T(ox, 238, "lo que manda la PC 1 lo reciben todas", "d-n")
    # msau: anillo en orden 1→2→3→4→1
    ox = 480
    pts = [(ox - 74, cy - 52), (ox + 74, cy - 52), (ox + 74, cy + 52), (ox - 74, cy + 52)]
    for i in range(4):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % 4]
        sx, sy = x1 + (x2 - x1) * 0.28, y1 + (y2 - y1) * 0.28
        ex, ey = x1 + (x2 - x1) * 0.72, y1 + (y2 - y1) * 0.72
        b += L(round(sx, 1), round(sy, 1), round(ex, 1), round(ey, 1), "d-a3", ' marker-end="url(#fl3)"')
    b += T(ox, 238, "la trama pasa de estación en estación, en orden", "d-n")
    return diag("Diagrama de topología física contra lógica", 250, b,
                "El mismo cableado en <b>estrella</b>, dos topologías <b>lógicas</b> distintas. Con un hub, lo que transmite una PC le llega "
                "a todas: <b>bus lógico</b>. Con una MSAU, la trama recorre las estaciones una por una en un sentido: <b>anillo lógico</b>. "
                "La lógica la define el protocolo de acceso al medio, no el cable.")


def adhoc_infra():
    b = ""
    def pc(x, y, t="PC"):
        return R(x - 24, y - 13, 48, 26, "d-f1", 5) + T(x, y + 4.5, t, "d-l")
    wl = lambda x1, y1, x2, y2: L(x1, y1, x2, y2, "d-a1 d-dash")
    b += T(160, 20, "Ad hoc", "d-t") + T(160, 36, "de igual a igual, sin access point", "d-n")
    P_ = [(160, 72), (70, 180), (250, 180)]
    for i in range(3):
        for j in range(i + 1, 3):
            b += wl(*P_[i], *P_[j])
    for x, y in P_:
        b += pc(x, y)
    b += T(480, 20, "Infraestructura", "d-t") + T(480, 36, "todos se comunican a través del AP", "d-n")
    ap = (480, 120)
    for x, y in ((390, 72), (390, 176), (570, 72)):
        b += wl(x, y, *ap)
    b += L(480, 134, 570, 186, "d-ln") + R(540, 172, 70, 28, "d-f0", 5) + T(575, 190.5, "Switch", "d-l")
    b += T(588, 216, "red cableada", "d-z")
    b += R(450, 106, 60, 28, "d-f3", 6) + T(480, 124.5, "AP", "d-l")
    for x, y in ((390, 72), (390, 176), (570, 72)):
        b += pc(x, y)
    b += T(320, 238, "- - -  enlace inalámbrico        ——  cable", "d-z")
    return diag("Diagrama de los modos ad hoc e infraestructura", 248, b,
                "<b>Ad hoc</b>: los equipos se hablan directamente entre sí; sirve para pocos equipos y redes temporales. "
                "<b>Infraestructura</b>: todo pasa por el <b>access point</b>, que además une la red inalámbrica con la cableada.")


def p2p_dominio():
    b = ""
    def pc(x, y, users):
        o = R(x - 30, y - 15, 60, 30, "d-f1", 5) + T(x, y + 4.5, "PC", "d-l")
        if users:
            o += R(x + 20, y - 26, 34, 18, "d-f3", 4) + T(x + 37, y - 13, "👤", "d-z")
        return o
    izq = ((80, 76), (240, 76), (80, 196), (240, 196))
    der = ((400, 76), (400, 196), (560, 196))
    for x, y in izq:
        b += L(x, y, 160, 132, "d-ln2")
    for x, y in der + ((560, 76),):
        b += L(x, y, 480, 132, "d-ln2")
    for ox, tit, sub in ((160, "Peer to peer · grupo de trabajo", "cada PC tiene sus propios usuarios"), (480, "Servidor dedicado · dominio", "los usuarios están una sola vez, en el servidor")):
        b += T(ox, 20, tit, "d-t") + T(ox, 36, sub, "d-n")
        b += R(ox - 34, 118, 68, 28, "d-f0", 5) + T(ox, 136.5, "Switch", "d-l")
    b += P("M412,62 Q470,34 520,64", "d-a3 d-dash") + P("M430,194 Q545,200 548,96", "d-a3 d-dash") + P("M566,180 Q590,140 578,96", "d-a3 d-dash")
    for x, y in izq:
        b += pc(x, y, True)
    for x, y in der:
        b += pc(x, y, False)
    b += R(522, 58, 92, 36, "d-f2", 6) + T(568, 74, "Servidor", "d-l") + T(568, 87, "AD + DNS", "d-s")
    b += R(586, 36, 34, 18, "d-f3", 4) + T(603, 49, "👤", "d-z")
    b += T(160, 238, "cada PC valida a sus usuarios locales", "d-n")
    b += T(480, 238, "todas validan contra el servidor (- - -)", "d-n")
    return diag("Diagrama de peer to peer contra servidor dedicado", 250, b,
                "La misma red física (un switch y PCs) con dos sistemas operativos de red. En <b>peer to peer</b> cada PC tiene sus usuarios "
                "y decide qué comparte. En el <b>dominio</b>, los usuarios se crean una vez en el servidor y todas las PCs validan contra él. "
                "Es una relación lógica: el centro físico sigue siendo el switch, no el servidor (por eso no es una estrella con centro en el servidor).")


def derecho_cruzado():
    b = "<defs>" + marker("dc1", "d-m1") + marker("dc2", "d-m2") + "</defs>"
    pins = [1, 2, 3, 6]
    ys = {1: 82, 2: 112, 3: 152, 6: 182}
    def lado(x, nombre, tx_pins, izq):
        o = T(x, 50, nombre, "d-t")
        for p in pins:
            y = ys[p]
            o += R(x - 16, y - 11, 32, 22, "d-f0", 4) + T(x, y + 4.5, str(p), "d-l")
            es_tx = p in tx_pins
            o += T(x + (-24 if izq else 24), y + 4.5, "TX" if es_tx else "RX", "d-s", "end" if izq else "start")
        return o
    # derecho: PC (TX 1,2) ↔ switch (RX 1,2), pin a pin
    b += T(160, 20, "Derecho · A en las dos puntas", "d-t")
    b += lado(70, "PC", (1, 2), True) + lado(250, "Switch", (3, 6), False)
    for p in pins:
        c, m = ("d-a1", "dc1") if p in (1, 2) else ("d-a2", "dc2")
        x1, x2 = (88, 232) if p in (1, 2) else (232, 88)
        b += L(x1, ys[p], x2, ys[p], c, f' marker-end="url(#{m})"')
    b += T(160, 222, "equipos distintos: 1→1, 2→2, 3→3, 6→6", "d-n")
    # cruzado: PC ↔ PC
    b += T(480, 20, "Cruzado · A en una punta, B en la otra", "d-t")
    b += lado(390, "PC", (1, 2), True) + lado(570, "PC", (1, 2), False)
    for a_, z in ((1, 3), (2, 6)):
        b += L(408, ys[a_], 552, ys[z], "d-a1", ' marker-end="url(#dc1)"')
        b += L(552, ys[a_], 408, ys[z], "d-a2", ' marker-end="url(#dc2)"')
    b += T(480, 222, "equipos iguales: 1↔3 y 2↔6", "d-n")
    b += T(320, 244, "Lo que una punta transmite tiene que llegar a lo que la otra recibe", "d-bl")
    return diag("Diagrama de cable derecho contra cruzado", 254, b,
                "Por qué existen los dos cables (en 10/100 Mbps). Una PC transmite por 1 y 2 y recibe por 3 y 6; el puerto del switch, al revés. "
                "Entre equipos <b>distintos</b> el cable <b>derecho</b> ya conecta transmisión con recepción. Entre equipos <b>iguales</b> hay que "
                "<b>cruzar</b> los pares para que la transmisión de uno llegue a la recepción del otro.")


FIG.update({"csma_ca": csma_ca, "half_full": half_full, "polling": polling, "udp": udp, "banda": banda,
            "fisica_logica": fisica_logica, "adhoc_infra": adhoc_infra, "p2p_dominio": p2p_dominio, "derecho_cruzado": derecho_cruzado})
