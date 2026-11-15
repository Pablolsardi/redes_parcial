"""Contenido de la página Repaso (v3.0). repaso_html() devuelve la <section> completa."""

MODS = [
    ("m0", "Antes de empezar", [
        ("0", "s0", "Cómo es el parcial", False, [
            "<b>20 preguntas en 1 hora:</b> 19 de verdadero o falso y 1 ejercicio de subneteo, que <b>tiene que estar bien para aprobar</b>.",
            "Cada error <b>descuenta la mitad</b> de lo que vale la pregunta; en blanco no suma ni resta. Contestá si tenés más de 1 chance en 3 de acertar.",
            "Las cinco distinciones de la profe: acceso al medio ≠ protocolo de comunicación · protocolo ≠ norma · dirección física ≠ lógica · contención ≠ token passing · el sistema operativo es independiente de la norma.",
            "Lo que remarcó: capas de TCP/IP, trama y paquete, MAC e IP, 802.11, subneteo (puede dar una clase B), permisos NTFS y de recurso compartido, Windows Server con DHCP y DNS, UTP y Ethernet. Igual entra todo.",
        ], "las afirmaciones son largas y <b>un solo detalle</b> las hace falsas. Leé cada una hasta el final antes de marcar.", ""),
    ]),
    ("m1", "Módulo 1 · Fundamentos", [
        ("1", "s1", "Qué es una red y cómo se clasifican", False, [
            "Red: nodos interconectados por un medio común para <b>compartir recursos</b> (hardware, software y datos).",
            "<b>LAN:</b> edificio o campus, alta velocidad, la administra la propia organización (Ethernet, Wi-Fi). <b>MAN:</b> una ciudad (radio &lt; 100 km), suele unir varias LAN. <b>WAN:</b> países y continentes, de proveedores; Internet es el ejemplo.",
            "La velocidad la fija la <b>norma</b>, pero manda el eslabón más lento (placa, cable o puerto). La distancia depende del medio, de la norma y de los repetidores.",
        ], "lo que hace LAN a una red es el alcance y quién la administra, no la cantidad de equipos.", ""),
        ("2", "s2", "Modelo ISO-OSI capa por capa", False, [
            "De abajo hacia arriba: <b>Física, Enlace, Red, Transporte, Sesión, Presentación, Aplicación</b>. Grupos: comunicación (1 y 2), networking (3 y 4), servicios (5 a 7).",
            "PDU: <b>bits</b> (1), <b>trama</b> (2), <b>paquete</b> o datagrama (3), <b>segmento</b> (4), <b>mensaje</b> (5 a 7).",
            "<b>Capa 1:</b> medio, señal, conectores, topología física; hub, repetidor, módem. Problemas de la señal: atenuación (se corrige con repetidores), EMI y crosstalk (lo reduce el trenzado).",
            "<b>Capa 2:</b> subcapa <b>MAC</b> (acceso al medio y dirección física) + subcapa <b>LLC</b> (sincronización de tramas, control de flujo y errores con FCS/CRC). Switch y puente.",
            "<b>Capa 3:</b> direccionamiento lógico y ruteo (router). <b>Capa 4:</b> extremo a extremo, segmentación y servicio correcto. <b>5:</b> el diálogo (simplex, half o full duplex). <b>6:</b> “el traductor” (ASCII/EBCDIC, compresión, cifrado). <b>7:</b> interfaz con el usuario.",
            "Encapsulamiento: al bajar, cada capa agrega su encabezado; enlace agrega además un trailer. <b>Baseband</b> = digital, TDM, LAN. <b>Broadband</b> = analógico, FDM, WAN.",
        ], "protocolo <b>ruteable</b> (IP: viaja con los datos) no es protocolo <b>de enrutamiento</b> (RIP, IGRP: arma las tablas de los routers).", ""),
        ("3", "s3", "Elementos de una LAN", False, [
            "Seis elementos: servidores, clientes, NIC, medio, dispositivos de interconexión y software.",
            "<b>NIC:</b> interfaz entre la PC y la red. Convierte datos en señales, compara la MAC destino de cada trama con la propia y ejecuta el acceso al medio.",
            "Interconexión por capa: repetidor y hub (1), puente y switch (2), router (3).",
            "IRQ, puerto de E/S y memoria base: los tres parámetros de hardware de una NIC (hoy los asigna Plug and Play).",
        ], "el software de red es independiente de la norma: Windows funciona igual sobre Ethernet que sobre Wi-Fi.", ""),
    ]),
    ("m2", "Módulo 2 · Topologías y acceso al medio", [
        ("4", "s5", "Topologías", False, [
            "<b>Física</b> = cómo se cablea. <b>Lógica</b> = cómo circula la información: la da el protocolo de acceso al medio, que define la norma.",
            "Bus: un coaxil con terminadores; un corte tira toda la red. Estrella: todos a un hub o switch; es la de hoy. Anillo: cada nodo repite la señal, en un solo sentido.",
            "Lógica <b>bus</b> (difusión): contención → 802.3 y 802.11. Lógica <b>anillo</b>: token passing → 802.5, 802.4, FDDI.",
            "No siempre coinciden: Ethernet con hub o switch = estrella física, bus lógico · Token Ring con MSAU = estrella física, anillo lógico · Token Bus = bus físico, anillo lógico · Wi-Fi = estrella física, bus lógico.",
        ], "el dibujo del servidor dedicado en el centro <b>no</b> es una topología estrella: el centro de una estrella es un hub o un switch.", ""),
        ("5", "s6", "Protocolos de acceso al medio", False, [
            "Responden quién transmite y cuándo. Viven en la capa 2 (subcapa MAC), los define la norma y los ejecuta la NIC.",
            "<b>Polling:</b> maestro y esclavos, determinístico; si cae el maestro no hay red. <b>Contención:</b> compiten y chocan, probabilístico. <b>Token passing:</b> transmite quien tiene el token, sin colisiones, determinístico.",
            "Aloha puro ~18 % · Aloha ranurado ~37 % · CSMA escucha antes de hablar · <b>CSMA/CD</b> además escucha mientras transmite: detecta, aborta y espera (802.3, cable) · <b>CSMA/CA</b> evita: espera al azar y confirma con ACK (802.11, aire).",
            "Por aire no se puede detectar la colisión: la propia señal tapa a las demás. Por eso Wi-Fi evita en lugar de detectar.",
            "Con poca carga gana la contención (transmito apenas quiero). Con mucha carga el token es estable y la contención se degrada.",
        ], "en token passing hay una <b>demora fija aunque haya poca carga</b>: igual hay que esperar que llegue el token.", ""),
        ("6", "s7", "Token Ring, Token Bus y la MSAU", False, [
            "<b>802.5 Token Ring:</b> anillo lógico de un solo sentido, 4 y 16 Mbps, cada estación es un repetidor y una hace de Monitor Activo.",
            "El token son <b>3 bytes</b> (SD, AC, ED). Bit T en 0 = token libre; en 1 = encabezado de una trama de datos.",
            "Ciclo: captura → inyección → copia (el destino activa los bits A y C) → liberación.",
            "<b>MSAU:</b> concentrador que cablea en estrella y mantiene el anillo por dentro. Los relés de bypass sacan del anillo a la estación apagada; los puertos RI y RO encadenan MSAUs.",
            "<b>802.4 Token Bus:</b> bus físico coaxil con anillo lógico; nació para la industria (tiempo real).",
        ], "la trama la retira del anillo el <b>emisor</b> (y genera un token nuevo), no el destino.", ""),
        ("★", "snp", "Norma vs protocolo", True, [
            "<b>Norma de comunicación:</b> estándar de un organismo (IEEE, TIA/EIA, ANSI) para las capas 1 y 2. La implementa el <b>hardware</b>. Fija medio, velocidad, distancia, codificación, conector, topología, trama y acceso al medio. Ej.: 802.3, 802.5, 802.11.",
            "<b>Protocolo de comunicación:</b> reglas de diálogo entre capas pares, capas 3 a 7. Lo implementa el <b>software</b> (sistema operativo y aplicaciones). Sintaxis, semántica y temporización. Ej.: IP, TCP, HTTP, DNS.",
            "<b>Protocolo de acceso al medio</b> (CSMA/CD, CSMA/CA, token passing): vive dentro de la norma y no es un protocolo de comunicación. Cadena: norma → acceso al medio → topología lógica.",
            "Pasar de cable a Wi-Fi cambia la norma (802.3 → 802.11) y el acceso (CD → CA). IP, DHCP y DNS siguen igual.",
        ], "todas falsas: “TCP/IP es una norma” · “802.3 es un protocolo de comunicación” · “CSMA/CD es un protocolo de comunicación” · “la velocidad de la LAN la determina TCP/IP” (la determina la norma).", ""),
    ]),
    ("m3", "Módulo 3 · Ethernet y Wi-Fi", [
        ("7", "s8", "IEEE 802.3 Ethernet: trama y variantes clásicas", True, [
            "Ethernet: de DEC, Intel y Xerox (DIX). Bus lógico con CSMA/CD; topología física bus o estrella.",
            "Trama: preámbulo 7 · SD 1 · MAC destino 6 · MAC origen 6 · longitud/tipo 2 · datos 46 a 1500 · FCS 4. <b>Mínimo 64 bytes, máximo 1518</b>, sin contar preámbulo ni SD. Si los datos no llegan a 46 se rellenan (padding).",
            "10BASE-T = velocidad + señalización (BASE = banda base) + medio. <b>10BASE5:</b> coaxil grueso, 500 m. <b>10BASE2:</b> coaxil fino, 185 m. <b>10BASE-T:</b> UTP, 100 m, estrella. F / FL / FX: fibra.",
            "<b>Regla 5-4-3:</b> 5 segmentos, 4 repetidores, 3 segmentos poblados. Todo lo unido por repetidores es un solo dominio de colisión.",
            "A favor: barata, fácil de instalar, muchos cableados. En contra: mala en alta carga, sin prioridades, no determinística.",
        ], "10BASE2 son <b>185 m</b> (en clase se anota 200). Y el mínimo de 64 bytes existe para que CSMA/CD alcance a detectar la colisión.", ""),
        ("8", "s9", "Evolución de Ethernet sobre par trenzado", True, [
            "10BASE-T (802.3i, Cat 3, 2 pares) → 100BASE-TX (<b>802.3u</b>, Cat 5, 2 pares) → 1000BASE-T (<b>802.3ab</b>, Cat 5e, 4 pares) → 10GBASE-T (<b>802.3an</b>, Cat 6A, 4 pares). Siempre 100 m.",
            "Lo que evoluciona es la <b>capa 1</b>: más pares, uso en los dos sentidos, más niveles de señal y mejor cable. La trama y la MAC casi no cambian.",
            "Fast Ethernet no soporta coaxil, trae auto-negociación 10/100 y con fibra en full duplex (100BASE-FX) llega a 2 km.",
            "<b>Half duplex:</b> uno por vez, con hub, necesita CSMA/CD. <b>Full duplex:</b> los dos a la vez, enlace dedicado a un switch, sin colisiones. 10 Gigabit es solo full duplex.",
        ], "solo los <b>switches</b> pueden dar full duplex. Con un hub siempre es half.", ""),
        ("9", "s10", "Redes inalámbricas IEEE 802.11", True, [
            "El medio es el aire. Modos: <b>ad hoc</b> (entre pares, sin AP) e <b>infraestructura</b> (con un AP que hace de concentrador y se une a la red cableada).",
            "802.11<b>b</b> 2,4 GHz 11 Mbps · <b>a</b> 5 GHz 54 Mbps · <b>g</b> 2,4 GHz 54 Mbps · <b>n</b> (Wi-Fi 4) 2,4 y 5 GHz, MIMO · <b>ac</b> (Wi-Fi 5) 5 GHz · <b>ax</b> (Wi-Fi 6) 2,4, 5 y 6 GHz.",
            "Acceso <b>CSMA/CA</b>: escuchar → espera al azar (backoff) → transmitir → ACK. Opcional: RTS/CTS.",
            "<b>Nodo oculto:</b> cree que el canal está libre y no lo está (colisión en el AP; lo mitiga RTS/CTS). <b>Nodo expuesto:</b> cree que está ocupado y está libre.",
            "Para conectarse: <b>escaneo</b> (pasivo con beacons, activo con probe) → <b>autenticación</b> → <b>asociación</b>.",
            "<b>SSID:</b> el nombre de la red (2 a 32 caracteres); no es una medida de seguridad. Seguridad: WEP (obsoleto) → WPA → WPA2 con AES. También filtro por MAC.",
            "Antenas: direccional (punto a punto), omnidireccional (360°), sectorial. Los metales son la interferencia más alta.",
        ], "Wi-Fi cambia las capas 1 <b>y</b> 2 respecto de Ethernet: otro medio, otro acceso (CA) y otra trama, con hasta 3 o 4 direcciones MAC.", ""),
        ("10", "s11", "Dirección física (MAC) y lógica (IP)", True, [
            "<b>MAC:</b> capa 2, 48 bits (6 bytes, 12 dígitos hexadecimales), grabada en la NIC: 3 bytes del fabricante (OUI) + 3 de la placa. La usa el <b>switch</b>. Vale dentro de la LAN.",
            "<b>IP:</b> capa 3, 32 bits, la pone el administrador o el DHCP y cambia según la red. La usa el <b>router</b>. Identifica el destino final.",
            "<b>Trama</b> (capa 2): lleva las MAC y el FCS; en cada router se arma una nueva. <b>Paquete</b> (capa 3): lleva las IP y viaja igual de punta a punta. El paquete va adentro de la trama, como la carta en el sobre.",
            "Si el destino está en otra red: la IP destino es la del servidor, pero la MAC destino es la del <b>gateway</b>. ARP consigue la MAC a partir de la IP.",
            "Broadcast de capa 2: FFFF.FFFF.FFFF. <code>ipconfig /all</code> muestra las dos direcciones.",
        ], "en cada salto cambian las <b>MAC</b>, no las IP (salvo que haya NAT).", ""),
    ]),
    ("m4", "Módulo 4 · Interconexión y switching", [
        ("11", "s12", "Dispositivos de interconexión", False, [
            "Hub = repetidor multipuerto. Switch = puente multipuerto. Gateway: de capa 3 en adelante, puede traducir protocolos.",
            "El switch conmuta <b>tramas</b> mirando la MAC; el router conmuta <b>paquetes</b> mirando la IP.",
            "Transceiver: capa 1, transmisor + receptor (en par trenzado viene dentro de la NIC). Segmentación: dividir un dominio de colisión. Diámetro: distancia entre los dos nodos más lejanos.",
        ], "el hub <b>no filtra</b> nada: repite por todos los puertos. Filtrar por MAC es cosa del puente y del switch.",
         '<div class="scroll"><table><tr><th>Dispositivo</th><th>Capa</th><th>Qué mira</th><th>Dominio de colisión</th><th>Dominio de broadcast</th></tr>'
         '<tr><td>Repetidor · Hub</td><td>1</td><td>Nada (bits)</td><td>No separa</td><td>No separa</td></tr>'
         '<tr><td>Puente · Switch</td><td>2</td><td>MAC</td><td><b>Separa</b></td><td>No separa</td></tr>'
         '<tr><td>Router</td><td>3</td><td>IP</td><td><b>Separa</b></td><td><b>Separa</b></td></tr></table></div>'),
        ("12", "s13", "Dominio de colisión y dominio de broadcast", False, [
            "<b>Colisión:</b> nodos que comparten el medio; es un accidente de capa 1. <b>Broadcast:</b> nodos que reciben una difusión (destino FFFF.FFFF.FFFF); es un mensaje legítimo de capa 2 que usan ARP y DHCP.",
            "Para contar: <b>colisión</b> = uno por cada puerto de switch o router en uso (todo lo que cuelga de un hub cuenta uno). <b>Broadcast</b> = uno por cada interfaz de router; sin router, 1.",
            "Cambiar hubs por switches: más dominios de colisión, <b>el mismo</b> dominio de broadcast, ancho de banda dedicado y full duplex.",
            "El dominio de broadcast solo se parte con <b>routers o VLAN</b>.",
        ], "“cada puerto del switch es un dominio de difusión” es <b>falso</b>: es un dominio de colisión.", ""),
        ("13", "s14", "Cómo trabaja el switch", False, [
            "Tabla MAC → puerto, arranca vacía y se llena sola. <b>Aprende con la MAC origen, decide con la MAC destino.</b>",
            "<b>Inundar:</b> destino desconocido o broadcast → por todos los puertos menos el de entrada. <b>Reenviar:</b> destino conocido en otro puerto → solo por ese. <b>Filtrar:</b> destino en el mismo puerto por donde entró → descarta.",
            "Las entradas vencen solas (aging, 300 s) y se borran si cae el puerto.",
        ], "<b>flooding no es broadcast</b>: la trama sigue siendo unicast y las placas que no son el destino la descartan.", ""),
        ("14", "s14b", "Switching: bucles, STP y VLAN", False, [
            "El switch no limita el broadcast y es susceptible a bucles. Un bucle produce tormentas de broadcast y una tabla MAC inestable.",
            "<b>STP (802.1D):</b> bloquea los puertos redundantes y deja un árbol. Raíz = el switch de menor ID (prioridad + MAC). Se hablan con BPDU. Estados: bloqueado → escuchando → aprendiendo → reenviando.",
            "<b>VLAN:</b> divide un switch en varios virtuales; cada VLAN es un dominio de broadcast y normalmente una subred IP.",
            "Enlace de <b>acceso:</b> una sola VLAN, sin etiqueta. <b>Troncal:</b> varias VLAN, con etiqueta <b>802.1Q</b> (4 bytes después de la MAC origen, 12 bits de VLAN-ID).",
            "Asignación estática (por puerto, a mano) o dinámica (por MAC, con una base de datos).",
        ], "la VLAN parte el broadcast sin routers, pero para <b>comunicar</b> dos VLAN sí hace falta un router.", ""),
    ]),
    ("m5", "Módulo 5 · Redes con Windows", [
        ("15", "s4", "Servidores: roles, hardware y software", False, [
            "Servidor: da servicios a muchos clientes. Disponibilidad 24/7, tolerancia a fallos (RAID, fuentes redundantes) y sistema operativo dedicado. Está siempre a la escucha: el que inicia es el cliente.",
            "Roles: <b>dominio</b> (Active Directory, autentica usuarios) · <b>DNS</b> (nombres → IP) · <b>DHCP</b> (reparte IP, máscara, gateway y DNS) · <b>proxy</b> (intermediario con caché y filtrado) · archivos · base de datos · FTP · web (HTTP/HTTPS) · mail (SMTP envía; IMAP y POP3 reciben).",
        ], None, ""),
        ("16", "s15", "Peer to peer vs servidor dedicado, y permisos", True, [
            "La clasificación depende del <b>sistema operativo</b>, no del cableado ni de la norma.",
            "<b>Peer to peer</b> (grupo de trabajo): todas iguales, usuarios locales en cada PC, administración descentralizada, seguridad baja, barato; para menos de 10 usuarios.",
            "<b>Servidor dedicado</b> (dominio): usuarios creados una sola vez en Active Directory, administración centralizada, seguridad alta, más caro. Sin DNS no hay dominio.",
            "Permisos de <b>recurso compartido:</b> solo cuando se entra por la red (Leer, Cambiar, Control total). Permisos <b>NTFS:</b> siempre, local y por red.",
            "<b>Método:</b> 1) ¿desde dónde entra? Por red se evalúan las dos capas; sentado en la PC, solo NTFS. 2) En cada capa se <b>suman</b> los permisos del usuario y de sus grupos. 3) Una <b>denegación</b> explícita gana. 4) Entre compartido y NTFS rige <b>el más restrictivo</b>.",
        ], "los permisos son por <b>usuario</b>, no por persona: dos cuentas de la misma persona no se suman. Y los recursos compartidos pueden estar en cualquier nodo del dominio, no solo en el servidor.", ""),
    ]),
    ("m6", "Módulo 6 · Cableado estructurado", [
        ("17", "s16", "Cableado estructurado (EIA/TIA 568)", True, [
            "Objetivo: cubrir las necesidades de toda la vida útil del edificio sin tender más cables. Normas: 568 cableado · 569 recorridos y espacios · 606 administración y etiquetado · 607 puesta a tierra · 942 centros de datos.",
            "Subsistemas: <b>área de trabajo</b> (roseta → PC) · <b>horizontal</b> (rack del piso → roseta) · <b>administración</b> (MDF principal, IDF de planta) · <b>vertical</b> o backbone (entre plantas) · <b>campus</b> (entre edificios).",
            "<b>90 m</b> de cable horizontal fijo, más los patch cords: canal de 100 m. De la roseta a la PC, hasta 3 m (slide de la cátedra).",
            "T568A y T568B solo se diferencian en que se intercambian el par verde y el naranja. En 10/100 se usan los pines 1-2 (transmiten) y 3-6 (reciben); en Gigabit, los 8.",
            "<b>Derecho</b> (misma convención en las dos puntas): equipos distintos. <b>Cruzado</b> (A en una punta, B en la otra): equipos iguales.",
            "<b>Plug</b> (macho, pinza de crimpear) en los patch cords. <b>Jack</b> (hembra, pinza de impacto) en rosetas y patcheras.",
        ], "conectar la PC del usuario a la red es del subsistema de <b>área de trabajo</b>, no del horizontal.", ""),
        ("18", "s17", "Normas TIA complementarias", False, [
            "<b>569:</b> la infraestructura edilicia. Espacios EF (entrada), ER (sala de equipos), TR (sala de telecomunicaciones, una por piso) y WA (área de trabajo), más las rutas backbone y horizontales.",
            "<b>606:</b> identificar y documentar todo. Etiquetas impresas, en los dos extremos de cada cable. Clases 1 a 4 según el tamaño de la instalación.",
            "<b>607:</b> puesta a tierra. Tierra → TMGB (barra principal) → TBB (backbone de tierra) → TGB (una por sala) → racks.",
            "<b>942:</b> centros de datos, con ratings 1 a 4: de básico sin redundancia (1) a tolerante a fallos, 2N (4).",
        ], None, ""),
    ]),
    ("m7", "Módulo 7 · TCP/IP", [
        ("19", "s18", "TCP/IP: el modelo, las capas y el encapsulamiento", True, [
            "Es una <b>suite de protocolos</b> abierta y el estándar de facto. OSI es el modelo de referencia (teórico); TCP/IP es el que se usa. Sus documentos son las RFC del IETF.",
            "Encapsulamiento: datos → segmento → paquete → trama → bits. Cada encabezado dice a quién entregarle arriba: el tipo en Ethernet, el protocolo en IP (1 ICMP, 6 TCP, 17 UDP) y el puerto en transporte.",
            "Escribo una dirección y aprieto Enter: (DHCP si no tengo IP) → ARP → DNS → saludo de tres vías → HTTP GET → 200 OK.",
        ], "las <b>IP</b> se mantienen de punta a punta; las <b>MAC</b> se reescriben en cada salto.",
         '<div class="scroll"><table><tr><th>Capa TCP/IP</th><th>En OSI</th><th>Protocolos</th><th>PDU</th><th>Dirección</th></tr>'
         '<tr><td><b>4 · Aplicación</b></td><td>5, 6 y 7</td><td>HTTP, DNS, DHCP, FTP, SMTP</td><td>Datos (mensaje)</td><td>Nombre de dominio</td></tr>'
         '<tr><td><b>3 · Transporte</b></td><td>4</td><td>TCP, UDP</td><td>Segmento / datagrama</td><td>Puerto</td></tr>'
         '<tr><td><b>2 · Internet</b></td><td>3</td><td>IP, ICMP, ARP</td><td>Paquete</td><td>IP (lógica)</td></tr>'
         '<tr><td><b>1 · Acceso a la red</b></td><td>1 y 2</td><td>Ethernet 802.3, Wi-Fi 802.11</td><td>Trama → bits</td><td>MAC (física)</td></tr></table></div>'),
        ("20", "s18a", "TCP/IP: capa de aplicación", True, [
            "En la capa de aplicación está el <b>protocolo</b> (HTTP), no el programa (Chrome).",
            "<b>DNS:</b> nombre → IP. Jerárquico (raíz → TLD → dominio). Registros: A (IPv4), AAAA (IPv6), CNAME (alias), MX (correo), NS, PTR (inversa), SRV (servicios). Puerto 53, sobre UDP.",
            "<b>DHCP:</b> entrega IP, máscara, gateway y DNS. <b>DORA:</b> Discover (broadcast) → Offer → Request → Acknowledge. UDP 67 (servidor) y 68 (cliente). Ámbito = el rango que reparte; concesión = el préstamo. Si falla, la PC queda con 169.254.x.x.",
            "<b>HTTP</b> 80 · <b>HTTPS</b> 443 (HTTP + TLS). GET pide, POST envía. 200 OK, 404 no existe, 500 error del servidor.",
            "Correo: SMTP (25) envía · POP3 (110) descarga · IMAP (143) sincroniza.",
            "Puertos: FTP 20/21 · SSH 22 · Telnet 23 · SMTP 25 · DNS 53 · DHCP 67/68 · TFTP 69 · HTTP 80 · POP3 110 · IMAP 143 · SNMP 161 · HTTPS 443.",
        ], "el Discover de DHCP es un broadcast y <b>no cruza routers</b>: hace falta un servidor por red o un agente de retransmisión.", ""),
        ("21", "s18t", "TCP/IP: capa de transporte", True, [
            "Lleva los datos de aplicación a aplicación, de extremo a extremo: segmenta, identifica aplicaciones con <b>puertos</b> y, solo en TCP, da confiabilidad.",
            "Socket = IP + puerto. Rangos: 0–1023 bien conocidos · 1024–49151 registrados · 49152–65535 dinámicos (los que usa el cliente como origen).",
            "<b>TCP:</b> orientado a conexión (saludo de tres vías: SYN, SYN-ACK, ACK), números de secuencia, ACK, retransmisión y control de flujo por ventana. Encabezado de 20 bytes. Cierra en 4 pasos.",
            "<b>UDP:</b> sin conexión, sin confirmación ni orden (“mejor esfuerzo”). Encabezado de 8 bytes. Para consultas cortas (DNS, DHCP) y tiempo real (voz, video, juegos).",
        ], "el ACK es el <b>próximo byte que se espera</b>: si llega la secuencia 1 con 500 bytes, el ACK es 501.", ""),
        ("22", "s18i", "TCP/IP: capa de Internet y diagnóstico", True, [
            "<b>IP:</b> sin conexión, no confiable (mejor esfuerzo) e independiente del medio. <b>TTL:</b> cada router le resta 1; si llega a 0 se descarta y se avisa por ICMP. Valores iniciales: Windows 128, Linux 64.",
            "<b>ICMP:</b> avisa errores y estado, no corrige nada. Lo usan <code>ping</code> (Echo Request y Echo Reply) y <code>tracert</code> (Tiempo excedido).",
            "<b>ARP:</b> de IP a MAC. Pregunta por broadcast y le responden en unicast. Si el destino está en otra red, pregunta por la MAC del gateway. RARP hacía lo inverso.",
            "<b>NAT:</b> el router cambia la IP privada de origen por su IP pública.",
            "Comandos: <code>ipconfig /all</code> (IP, MAC, DHCP, DNS) · <code>ping</code> (conectividad) · <code>tracert</code> (saltos) · <code>nslookup</code> (DNS) · <code>arp -a</code> (caché ARP) · <code>netstat</code> (conexiones y puertos) · <code>route print</code> (rutas).",
        ], "un ping que no responde no siempre es falta de conectividad: el firewall de Windows bloquea el ICMP entrante.", ""),
    ]),
    ("m8", "Módulo 8 · Direccionamiento y subneteo", [
        ("23", "s18b", "Direccionamiento IPv4 y subneteo", True, [
            "IP = 32 bits en 4 octetos: red + host, y la máscara marca el corte. Dirección <b>de red:</b> bits de host en 0. <b>Broadcast:</b> bits de host en 1. Ninguna de las dos se asigna a un equipo.",
            "Clases por el primer octeto: <b>A</b> 1–126 (/8) · <b>B</b> 128–191 (/16) · <b>C</b> 192–223 (/24) · D 224–239 multicast · E 240–255.",
            "Especiales: 127.x loopback · 169.254.x enlace local (falló el DHCP) · privadas 10.x, 172.16 a 172.31 y 192.168.x.",
            "<b>AND</b> entre la IP y la máscara = dirección de red. El host lo usa para decidir: misma red → entrega directa; otra red → al gateway.",
            "Subnetear es prestar bits de host a la red. <b>Subredes = 2<sup>N</sup> · hosts = 2<sup>M</sup> − 2 · salto = 256 − octeto partido de la máscara.</b>",
            "Con clase = máscara por defecto. Sin clase (CIDR) = máscara adaptada, escrita /n.",
        ], "la clase la define la <b>máscara</b>: 129.x con /24 no es “clase C”. Y los bits libres para numerar redes son 7 en la A, 14 en la B y 21 en la C.", ""),
        ("24", "sej", "Ejercicios de subneteo", True, [
            "<b>1)</b> Clase y máscara por defecto. <b>2)</b> Si piden subredes: el menor N con 2<sup>N</sup> ≥ subredes. Si piden hosts: el menor M con 2<sup>M</sup> − 2 ≥ hosts. <b>3)</b> Verificá la otra condición. <b>4)</b> Máscara nueva = prefijo por defecto + N. <b>5)</b> Salto = 256 − octeto partido. <b>6)</b> Tabla: cada red en un múltiplo del salto; broadcast = uno antes de la próxima red; primer host = red + 1; último = broadcast − 1.",
            "Para ubicar una IP: fijate entre qué múltiplos del salto cae el octeto partido. 172.16.132.70/20 → salto 16 → 128 ≤ 132 &lt; 144 → red 172.16.128.0, broadcast 172.16.143.255.",
            "Bits de host = 32 − prefijo, sin importar la clase. En una clase B el salto suele caer en el tercer octeto, y el broadcast termina en .255.",
        ], "olvidarse el <b>−2</b> en los hosts · aplicar el salto en el octeto equivocado · escribir el broadcast sin el .255 final · contar mal la “tercera subred” (la primera es la que empieza en 0).",
         '<div class="scroll"><table><tr><th>Bits en 1 del octeto</th><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td></tr>'
         '<tr><th>Valor en la máscara</th><td>128</td><td>192</td><td>224</td><td>240</td><td>248</td><td>252</td><td>254</td><td>255</td></tr>'
         '<tr><th>Salto</th><td>128</td><td>64</td><td>32</td><td>16</td><td>8</td><td>4</td><td>2</td><td>1</td></tr></table></div>'
         '<div class="scroll"><table><tr><th>Bits</th><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td><td>10</td><td>11</td><td>12</td></tr>'
         '<tr><th>2<sup>n</sup></th><td>4</td><td>8</td><td>16</td><td>32</td><td>64</td><td>128</td><td>256</td><td>512</td><td>1024</td><td>2048</td><td>4096</td></tr>'
         '<tr><th>2<sup>n</sup> − 2</th><td>2</td><td>6</td><td>14</td><td>30</td><td>62</td><td>126</td><td>254</td><td>510</td><td>1022</td><td>2046</td><td>4094</td></tr></table></div>'),
    ]),
    ("m9", "Módulo 9 · Para el parcial", [
        ("25", "spp", "Preparcial y parciales anteriores", False, [
            "Cómo arman las falsas: cambian un dispositivo por otro (hub, switch, router) · colisión por difusión · un subsistema o una norma por otra · mezclan clase y máscara · suman permisos de usuarios distintos.",
            "<b>Falsas</b> que ya salieron: el hub filtra el tráfico · peer to peer es más seguro que servidor dedicado · el subsistema horizontal conecta la PC a la red · los permisos de dos cuentas de la misma persona se suman · 129.102.197.23 es de clase C.",
            "<b>Verdaderas</b> que ya salieron: una red no puede empezar con 127 · la clase C usa 21 bits de red y 8 de host · la trama 802.3 va de 64 a 1518 bytes · token passing tiene una demora fija con baja carga · el transceiver es de capa 1 · segmentar es dividir un dominio de colisión · la NIC compara la MAC destino con la suya.",
        ], None, ""),
        ("26", "stp", "Trabajos prácticos", False, [
            "<b>TP1:</b> hardware de servidor (RAID, ECC) e hipervisores tipo 1 y 2. <b>TP2:</b> estrella jerárquica, 2 bocas por puesto, canal de 100 m, rotulado TIA-606. <b>TP3:</b> ese plano llevado a una red lógica en Packet Tracer.",
            "<b>TP4:</b> compartido vs NTFS, la denegación gana, rige el más restrictivo; el firewall bloquea el ping. <b>TP5:</b> Active Directory necesita DNS (registros SRV); OUs, deshabilitar una cuenta, tomar posesión.",
            "<b>TP6:</b> ARP → DNS → saludo TCP → HTTP → FIN; el switch solo usa las capas 1 y 2. <b>TP7:</b> ámbito y exclusiones, opciones 003, 006 y 015, autorizar el DHCP en AD; una máscara mal puesta la propaga el DHCP.",
            "<b>TP8:</b> subneteo, con el método del tema 24.",
        ], None, ""),
        ("27", "s19", "Pares que se confunden", False, [
            "Dominio de <b>colisión</b> (lo separa el switch) / de <b>broadcast</b> (lo separa el router).",
            "<b>Flooding</b> (unicast con destino desconocido) / <b>broadcast</b> (destino FFFF.FFFF.FFFF).",
            "<b>CSMA/CD</b> (detecta, cable) / <b>CSMA/CA</b> (evita y confirma, aire).",
            "<b>Norma</b> (hardware, capas 1 y 2) / <b>protocolo</b> (software, capas 3 a 7).",
            "<b>MAC</b> (física, capa 2, switch) / <b>IP</b> (lógica, capa 3, router) · <b>puerto</b> (la aplicación, capa 4).",
            "<b>TCP</b> (con conexión, confiable) / <b>UDP</b> (sin conexión, liviano) · <b>POP3</b> (descarga) / <b>IMAP</b> (sincroniza).",
            "Permisos de <b>compartido</b> (solo por red) / <b>NTFS</b> (siempre).",
            "<b>MDF</b> (principal) / <b>IDF</b> (de planta) · <b>horizontal</b> (rack → roseta) / <b>vertical</b> (entre plantas).",
            "<b>Derecho</b> (equipos distintos) / <b>cruzado</b> (iguales) · <b>plug</b> (macho, crimpear) / <b>jack</b> (hembra, impacto).",
            "<b>Loopback</b> 127.x / <b>enlace local</b> 169.254.x · dirección <b>de red</b> (host en 0) / <b>broadcast</b> (host en 1).",
            "Nodo <b>oculto</b> / <b>expuesto</b> · enlace de <b>acceso</b> (sin etiqueta) / <b>troncal</b> (802.1Q) · <b>ARP</b> (IP → MAC) / <b>RARP</b> (MAC → IP).",
        ], None, ""),
    ]),
    ("m10", "Referencia", [
        ("28", "sglo", "Glosario de siglas", False, [
            "Dos siglas con doble significado: <b>MAC</b> es una subcapa (Medium Access Control) y también la dirección física. <b>STP</b> es un cable (Shielded Twisted Pair) y también Spanning Tree Protocol.",
            "Enlace: <b>CSMA/CD</b> y <b>CSMA/CA</b> (Carrier Sense Multiple Access, con Collision Detection o Collision Avoidance) · <b>LLC</b> (Logical Link Control) · <b>FCS</b> (Frame Check Sequence) · <b>CRC</b> · <b>NIC</b> · <b>MSAU</b>.",
            "Wi-Fi: <b>AP</b> · <b>SSID</b> (Service Set Identifier) · <b>RTS/CTS</b> (Request / Clear To Send) · <b>WEP</b>, <b>WPA</b>.",
            "Cableado: <b>UTP</b> · <b>MDF</b> / <b>IDF</b> (Main / Intermediate Distribution Facility) · <b>POP</b> · <b>TMGB</b>, <b>TGB</b>, <b>TBB</b>.",
            "TCP/IP: <b>DNS</b> · <b>DHCP</b> · <b>ARP</b> (Address Resolution Protocol) · <b>ICMP</b> · <b>TTL</b> (Time To Live) · <b>NAT</b> · <b>CIDR</b> · <b>APIPA</b> · <b>FQDN</b> · <b>VLAN</b>.",
        ], None, ""),
    ]),
]


def repaso_html():
    o = ['<section class="page" data-page="repaso" id="repaso">',
         '<p class="crumb">Para el día del parcial · <span class="rt" id="rpMin"></span></p>',
         '<h2>Repaso</h2>',
         '<p class="lead">Lo que tiene que quedar de cada tema, para leer de corrido unas horas antes. '
         'No reemplaza a la guía: si algo no te suena, tocá el título y vas al tema completo.</p>',
         '<div class="rp-reglas"><div><b>20</b><span>preguntas: 19 V/F y 1 de subneteo</span></div>'
         '<div><b>60 min</b><span>para todo el parcial</span></div>'
         '<div class="al"><b>−½</b><span>descuenta cada error; en blanco no resta</span></div>'
         '<div class="al"><b>Subneteo</b><span>tiene que estar bien para aprobar</span></div></div>',
         '<div class="rp-jump" role="navigation" aria-label="Módulos del repaso">']
    for mid, mname, _ in MODS[1:]:
        o.append(f'<a href="#rp-{mid}">{mname.split(" · ")[-1]}</a>')
    o.append('</div>')
    for mid, mname, items in MODS:
        o.append(f'<h3 class="rp-mod" id="rp-{mid}">{mname}</h3>')
        for num, sid, title, clave, bullets, trap, extra in items:
            o.append(f'<article class="rp{" clave" if clave else ""}" id="rp-{sid}"><span class="rp-n">{num}</span>'
                     f'<h4><a href="#{sid}">{title}</a>{"<em>La profe lo remarcó</em>" if clave else ""}</h4>')
            o.append('<div class="rp-b"><ul>' + "".join(f"<li>{b}</li>" for b in bullets) + '</ul>' + extra)
            if trap:
                o.append(f'<p class="rp-t"><b>Ojo:</b> {trap}</p>')
            o.append('</div></article>')
    o.append('<p class="rp-fin">Hasta acá el repaso. Si te queda tiempo, hacé un <a href="examen.html">simulacro del parcial</a> '
             'o un par de <a href="#sej">ejercicios de subneteo</a>.</p>')
    o.append('</section>')
    return "\n".join(o)


if __name__ == "__main__":
    h = repaso_html()
    print(len(h))
