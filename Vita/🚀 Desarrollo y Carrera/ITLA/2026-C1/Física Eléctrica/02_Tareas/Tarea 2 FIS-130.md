---
tags:
  - ITLA/Cuatrimestres/2026-C1/FIS-130/Tarea
fecha_entrega: 2026-02-06
estado: 🔴 Pendiente
---
# Practica 2

## 🚀 Desarrollo
* [ ] 1. Un globo de caucho tiene en su interior una carga puntual. ¿El flujo eléctrico a través del globo depende de si está inflado por completo o no? Explique su razonamiento.
	**No**, el flujo eléctrico a través del globo **no cambia** si se infla o se desinfla.
	
	Aquí está la explicación resumida basada en tus fuentes:
	
	1. **La carga es constante:** El flujo depende de la carga encerrada. Al inflar el globo, no estás alterando la cantidad de electrones o carga puntual que hay en su interior.
	
	2. **Compensación distancia-área:** Según la Ley de Coulomb, la intensidad del campo eléctrico disminuye con el cuadrado de la distancia (1/r2),. Al inflar el globo, la superficie aumenta proporcionalmente (r2), lo que compensa exactamente la disminución del campo.
	
	3. **El medio no cambia:** La permitividad del aire dentro del globo (que afecta la intensidad de la interacción eléctrica) permanece constante
* [ ] En la figura 22.15, suponga que se coloca una tercera carga puntual fuera de la superficie gaussiana de color púrpura C. ¿Afectaría esto el flujo eléctrico a través de cualquiera de las superficies A, B, C o D en la figura? ¿Por qué?
	**No**, el flujo eléctrico no depende de si el globo está inflado o no.
	1. **Solo importa la carga interna:** Según la **Ley de Gauss**, el flujo eléctrico total a través de una superficie cerrada depende únicamente de la **cantidad de carga encerrada** en su interior, no del tamaño o la forma del objeto,.
	
	2. **Independencia de la forma:** Las fuentes confirman explícitamente que "no importa la forma de la superficie, lo que importa es la carga encerrada". Como la carga puntual dentro del globo no cambia al inflarlo, el flujo total permanece constante
* [ ] Si el campo eléctrico de una carga puntual fuera proporcional a 1>r3 en vez de 1>r2 , ¿seguiría siendo válida la ley de Gauss? Explique su razonamiento. (Sugerencia: considere una superficie gaussiana esférica centrada en una sola carga puntual.)
	**No**, el flujo eléctrico **no cambia** si el globo se infla o se desinfla.
	Según la **Ley de Gauss**, el flujo eléctrico total a través de una superficie cerrada depende únicamente de la **cantidad de carga encerrada** en su interior y no del tamaño o la forma del objeto,.
	
	Dado que la carga puntual dentro del globo permanece igual, el flujo eléctrico se mantiene constante sin importar el volumen del globo

* [ ]  Un pararrayos es una varilla de cobre redondeada que se monta en la parte alta de los edificios y va soldada a un cable grueso, también de cobre, que llega al suelo. Los pararrayos se utilizan para proteger casas y graneros de los relámpagos; la corriente de los relámpagos corre por el cable y no por el edificio. ¿Por qué? ¿Por qué el extremo de la varilla debe estar redondeado?
	**1. Por el cable:** El cobre es un **conductor eléctrico** que permite el libre movimiento de electrones, ofreciendo un camino de mucha menor resistencia hacia el suelo que los materiales del edificio.
	
	**2. Por la punta redondeada:** En los conductores de forma irregular, la **densidad de carga es mayor** en los puntos donde el **radio de curvatura es más pequeño**. Esto concentra un campo eléctrico intenso en la punta, atrayendo la descarga del rayo hacia ese punto específico en lugar del resto del techo.
* [ ] El cubo de la figura 22.32 tiene lados con longitud L 5 10.0 cm. El campo eléctrico es uniforme, tiene magnitud E 5 4.00 3 103 N>C y es paralelo al plano xy con un ángulo de 36.9° medido a partir del eje 1x hacia el eje 1y. a) ¿Cuál es el flujo eléctrico a través de cada una de las seis caras del cubo, S1, S2 , S3, S4 , S5 y S6? b) ¿Cuál es el flujo eléctrico total a través de todas las caras del cubo?
	### Análisis Preliminar
	
	Primero, definimos los vectores y datos necesarios:
	
	1. **Área de las caras ($A$):** El lado es $L = 10.0 \text{ cm} = 0.100 \text{ m}$. $$A = L^2 = (0.100 \text{ m})^2 = 0.0100 \text{ m}^2$$
	2. **Campo Eléctrico ($\vec{E}$):** Magnitud $E = 4.00 \times 10^3 \text{ N/C}$. El ángulo es $36.9^\circ$ desde el eje $+x$ hacia el eje $+y$. Descomponemos el vector $\vec{E}$ en sus componentes rectangulares ($x, y, z$):
	    - $E_x = E \cos(36.9^\circ) = 4000(0.80) = 3200 \text{ N/C}$
	    - $E_y = E \sin(36.9^\circ) = 4000(0.60) = 2400 \text{ N/C}$
	    - $E_z = 0 \text{ N/C}$ (el campo es paralelo al plano $xy$).
	
	---
	
	### a) Flujo eléctrico a través de cada cara
	
	El flujo eléctrico se define como $\Phi_E = \vec{E} \cdot \vec{A}$. Utilizaremos los vectores unitarios normales ($\hat{n}$) para cada cara según la **Figura 22.32**, donde el eje $z$ apunta hacia arriba, el eje $y$ a la derecha y el eje $x$ hacia el frente (saliendo).
	
	**1. Caras Perpendiculares al Eje Z ($S_2$ y $S_4$)** Dado que el campo eléctrico está en el plano $xy$, no tiene componente vertical ($E_z = 0$). Por lo tanto, no atraviesa las caras superior e inferior.
	
	- **Cara $S_2$ (Superior, normal $+\hat{k}$):** $$\Phi_2 = \vec{E} \cdot \vec{A}_2 = 0$$
	- **Cara $S_4$ (Inferior/Fondo, normal $-\hat{k}$):** $$\Phi_4 = \vec{E} \cdot \vec{A}_4 = 0$$
	
	**2. Caras Perpendiculares al Eje Y ($S_1$ y $S_3$)** Estas caras interactúan con la componente $E_y$ del campo ($2400 \text{ N/C}$).
	
	- **Cara $S_3$ (Derecha, normal $+\hat{j}$):** El vector de área apunta en la misma dirección que la componente $y$ del campo (hacia afuera). $$\Phi_3 = E_y \cdot A = (2400 \text{ N/C})(0.0100 \text{ m}^2) = \mathbf{24.0 \text{ N}\cdot\text{m}^2/\text{C}}$$
	- **Cara $S_1$ (Izquierda, normal $-\hat{j}$):** El vector de área apunta en dirección opuesta a la componente $y$ del campo (hacia afuera, izquierda). $$\Phi_1 = -E_y \cdot A = -(2400 \text{ N/C})(0.0100 \text{ m}^2) = \mathbf{-24.0 \text{ N}\cdot\text{m}^2/\text{C}}$$
	
	**3. Caras Perpendiculares al Eje X ($S_5$ y $S_6$)** Estas caras interactúan con la componente $E_x$ del campo ($3200 \text{ N/C}$).
	
	- **Cara $S_5$ (Frente, normal $+\hat{i}$):** El vector de área apunta hacia el frente (dirección $+x$). $$\Phi_5 = E_x \cdot A = (3200 \text{ N/C})(0.0100 \text{ m}^2) = \mathbf{32.0 \text{ N}\cdot\text{m}^2/\text{C}}$$
	- **Cara $S_6$ (Trasera, normal $-\hat{i}$):** El vector de área apunta hacia atrás (dirección $-x$), opuesto al campo. $$\Phi_6 = -E_x \cdot A = -(3200 \text{ N/C})(0.0100 \text{ m}^2) = \mathbf{-32.0 \text{ N}\cdot\text{m}^2/\text{C}}$$
	
	---
	
	### b) Flujo eléctrico total
	
	Para hallar el flujo total, sumamos los flujos individuales calculados en el inciso anterior:
	
	$$ \Phi_{\text{Total}} = \Phi_1 + \Phi_2 + \Phi_3 + \Phi_4 + \Phi_5 + \Phi_6 $$ $$ \Phi_{\text{Total}} = -24.0 + 0 + 24.0 + 0 + 32.0 - 32.0 $$ $$ \Phi_{\text{Total}} = \mathbf{0 \text{ N}\cdot\text{m}^2/\text{C}} $$
	
	**Explicación Física:** Este resultado es consistente con la **Ley de Gauss** explicada en las fuentes,,.
	
	1. **Campo Uniforme:** El campo eléctrico es uniforme (constante en magnitud y dirección).
	2. **Sin Carga Encerrada:** No hay ninguna carga eléctrica dentro del cubo. Las líneas de campo que entran por las caras $S_1$ y $S_6$ son exactamente iguales a las líneas que salen por las caras $S_3$ y $S_5$.
	3. Por lo tanto, el flujo neto a través de cualquier superficie cerrada que no encierra carga es siempre **cero**.

* [ ] ¿Cuántos electrones excedentes deben agregarse a un conductor esférico aislado de 32.0 cm de diámetro para producir un campo eléctrico de 1150 N>C apenas fuera de su superficie?

	Para determinar cuántos electrones excedentes se deben agregar, utilizaremos las fórmulas de campo eléctrico y cuantización de la carga descritas en las fuentes proporcionadas (específicamente de las transcripciones sobre física universitaria y ley de Coulomb).
	
	Aquí tienes el cálculo paso a paso:
	
	**1. Determinar el radio y las constantes**
	
	- **Diámetro:** $32.0 \text{ cm}$, por lo tanto, el **radio ($r$)** es $16.0 \text{ cm} = 0.16 \text{ m}$.
	- **Campo Eléctrico ($E$):** $1150 \text{ N/C}$.
	- **Constante de Coulomb ($k$):** Según la fuente, en el vacío o aire se utiliza aproximadamente $9 \times 10^9 \text{ N}\cdot\text{m}^2/\text{C}^2$,.
	- **Carga del electrón ($e$):** La magnitud de la carga elemental es $1.6 \times 10^{-19} \text{ C}$,.
	
	**2. Calcular la Carga Total ($Q$) necesaria** Para un conductor esférico, el campo eléctrico justo fuera de su superficie se calcula como si toda la carga estuviera concentrada en el centro (similar a una carga puntual). La fórmula es: $$ E = k \frac{|Q|}{r^2} $$ ,
	
	Despejamos la carga ($Q$): $$ |Q| = \frac{E \cdot r^2}{k} $$
	
	Sustituimos los valores: $$ |Q| = \frac{1150 \cdot (0.16)^2}{9 \times 10^9} $$ $$ |Q| = \frac{1150 \cdot 0.0256}{9 \times 10^9} $$ $$ |Q| = \frac{29.44}{9 \times 10^9} $$ $$ |Q| \approx 3.27 \times 10^{-9} \text{ C} $$
	
	**3. Calcular el número de electrones ($n$)** Sabiendo que la carga está cuantizada y es un múltiplo entero de la carga del electrón ($Q = n \cdot e$), dividimos la carga total requerida entre la carga de un solo electrón:
	
	$$ n = \frac{Q}{e} $$ $$ n = \frac{3.27 \times 10^{-9} \text{ C}}{1.6 \times 10^{-19} \text{ C/electrón}} $$ $$ n \approx 2.04 \times 10^{10} $$
	
	**Respuesta:** Se deben agregar aproximadamente **$2.04 \times 10^{10}$ electrones** (alrededor de 20,400 millones de electrones) al conductor esférico.
* [ ] El campo eléctrico a una distancia de 0.145 m de la superficie de una esfera sólida aislante con radio de 0.355 m, es de 1750 N>C. a) Suponiendo que la carga de la esfera se distribuye con uniformidad, ¿cuál es la densidad de carga en su interior? b) Calcule el campo eléctrico dentro de la esfera a una distancia de 0.200 m del centro.
	
	### Datos Iniciales
	
	- **Radio de la esfera ($R$):** $0.355 \text{ m}$.
	- **Distancia desde la superficie ($d$):** $0.145 \text{ m}$.
	- **Distancia total desde el centro ($r$):** $R + d = 0.355 + 0.145 = \mathbf{0.500 \text{ m}}$.
	- **Campo Eléctrico fuera ($E_{ext}$):** $1750 \text{ N/C}$.
	- **Constante de Coulomb ($k$):** $9 \times 10^9 \text{ N}\cdot\text{m}^2/\text{C}^2$.
	
	---
	
	### a) Densidad de carga en su interior ($\rho$)
	
	Para una esfera aislante con distribución uniforme, la densidad de carga volumétrica ($\rho$) se define como la carga total dividida entre el volumen total ($\rho = Q/V$).
	
	**Paso 1: Calcular la Carga Total ($Q$)** Fuera de una esfera cargada uniformemente, el campo eléctrico se comporta como si toda la carga estuviera concentrada en el centro (como una carga puntual). Usamos la fórmula del campo eléctrico: $$ E = k \frac{Q}{r^2} $$
	
	Despejamos $Q$: $$ Q = \frac{E \cdot r^2}{k} $$ $$ Q = \frac{1750 \cdot (0.500)^2}{9 \times 10^9} $$ $$ Q = \frac{1750 \cdot 0.25}{9 \times 10^9} = \frac{437.5}{9 \times 10^9} $$ $$ Q \approx \mathbf{4.861 \times 10^{-8} \text{ C}} $$
	
	**Paso 2: Calcular el Volumen de la esfera ($V$)** Usamos el radio de la esfera ($R = 0.355 \text{ m}$): $$ V = \frac{4}{3} \pi R^3 $$ $$ V = \frac{4}{3} \pi (0.355)^3 \approx \mathbf{0.1874 \text{ m}^3} $$
	
	**Paso 3: Calcular la Densidad ($\rho$)** $$ \rho = \frac{Q}{V} = \frac{4.861 \times 10^{-8} \text{ C}}{0.1874 \text{ m}^3} $$ $$ \rho \approx \mathbf{2.59 \times 10^{-7} \text{ C/m}^3} $$ _(O también $259 \text{ nC/m}^3$)_.
	
	---
	
	### b) Campo eléctrico dentro de la esfera a 0.200 m del centro
	
	Cuando estamos **dentro** de una esfera sólida aislante uniformemente cargada (donde $r < R$), el campo eléctrico ya no es constante ni disminuye con el cuadrado de la distancia, sino que **aumenta linealmente** con la distancia desde el centro. Esto se debe a que la carga encerrada es una fracción del volumen total.
	
	**Fórmula para campo interior:** $$ E_{int} = \frac{k \cdot Q \cdot r_{int}}{R^3} $$ _(Esta fórmula se deriva de la Ley de Gauss, considerando que la carga encerrada es proporcional al volumen $r^3$)_.
	
	**Sustitución:**
	
	- $r_{int} = 0.200 \text{ m}$
	- $Q = 4.861 \times 10^{-8} \text{ C}$
	- $R = 0.355 \text{ m}$
	
	$$ E_{int} = \frac{(9 \times 10^9) \cdot (4.861 \times 10^{-8}) \cdot (0.200)}{(0.355)^3} $$
	
	Calculamos el numerador: $$ (9 \times 10^9) \cdot (4.861 \times 10^{-8}) \approx 437.5 $$ $$ 437.5 \cdot 0.200 = \mathbf{87.5} $$
	
	Calculamos el denominador ($R^3$): $$ (0.355)^3 \approx \mathbf{0.04474} $$
	
	División final: $$ E_{int} = \frac{87.5}{0.04474} $$ $$ E_{int} \approx \mathbf{1955 \text{ N/C}} $$
	
	### Resumen de Resultados
	
	a) La densidad de carga es **$2.59 \times 10^{-7} \text{ C/m}^3$**. b) El campo eléctrico a 0.200 m del centro es **$1955 \text{ N/C}$**.
* [ ] El campo eléctrico E1 en toda la cara de un paralelepípedo es uniforme y se dirige hacia fuera de la cara. En la cara opuesta, el campo eléctrico E2 también es uniforme en toda ella y se dirige hacia esa cara (figura 22.36). Las dos caras en cuestión están inclinadas 30.0° con respecto de la horizontal, en tanto que E1 y E2 son horizontales; E1 tiene una magnitud de 2.50 3 10 4 N>C, E2 y tiene una magnitud de 7.00 3 10 4 N>C. a) Suponiendo que ninguna otra línea de campo eléctrico cruza las superficies del paralelepípedo, determine la carga neta contenida dentro. b) ¿El campo eléctrico sólo es producido por las cargas en el interior del paralelepípedo o también se debe a las que están fuera de éste? ¿Cómo podría saberse?
	### a) Determine la carga neta contenida dentro
	
	Para hallar la carga neta ($Q_{\text{neta}}$), aplicamos la Ley de Gauss, la cual establece que el flujo eléctrico neto ($\Phi_{\text{total}}$) a través de una superficie cerrada es igual a la carga encerrada dividida por la permitividad del vacío ($\epsilon_0$).
	
	**1. Cálculo del Área ($A$)** Según la fuente (la imagen con las dimensiones), las caras son rectángulos con lados de $5.00 \text{ cm}$ y $6.00 \text{ cm}$. $$ A = 0.0500 \text{ m} \times 0.0600 \text{ m} = \mathbf{0.00300 \text{ m}^2} $$
	
	**2. Cálculo del Flujo Eléctrico ($\Phi$)** El flujo se define como $\Phi = E \cdot A \cdot \cos(\theta)$, donde $\theta$ es el ángulo entre el vector de campo eléctrico ($\vec{E}$) y el vector normal a la superficie ($\hat{n}$).
	
	- **Geometría:** Las caras están inclinadas **$30.0^\circ$** respecto a la horizontal. El vector normal ($\hat{n}$) es perpendicular a la superficie. Por lo tanto, el ángulo entre la normal y la horizontal (dirección del campo) es $90^\circ - 30^\circ = \mathbf{60.0^\circ}$.
	
	Calculamos el flujo en cada cara (recordando que el flujo entrante es negativo y el saliente es positivo):
	
	- **Flujo 1 (Cara derecha, Saliente, $\vec{E}_1$):** $$ \Phi_1 = E_1 A \cos(60^\circ) $$ $$ \Phi_1 = (2.50 \times 10^4 \text{ N/C})(0.00300 \text{ m}^2)(0.5) = \mathbf{+37.5 \text{ N}\cdot\text{m}^2/\text{C}} $$
	    
	- **Flujo 2 (Cara izquierda, Entrante, $\vec{E}_2$):** $$ \Phi_2 = -E_2 A \cos(60^\circ) $$ (Es negativo porque el campo entra en la superficie). $$ \Phi_2 = -(7.00 \times 10^4 \text{ N/C})(0.00300 \text{ m}^2)(0.5) = \mathbf{-105.0 \text{ N}\cdot\text{m}^2/\text{C}} $$
	    
	- **Flujo Neto:** Dado que el problema asume que ninguna otra línea cruza las otras superficies, el flujo en las caras restantes es 0. $$ \Phi_{\text{neto}} = \Phi_1 + \Phi_2 = 37.5 - 105.0 = \mathbf{-67.5 \text{ N}\cdot\text{m}^2/\text{C}} $$
	    
	
	**3. Cálculo de la Carga ($Q_{\text{neta}}$)** Usamos la constante de permitividad $\epsilon_0 \approx 8.854 \times 10^{-12} \text{ C}^2/\text{N}\cdot\text{m}^2$ (mencionada como parte de la constante $k$ en y explícitamente en).
	
	$$ Q_{\text{neta}} = \Phi_{\text{neto}} \times \epsilon_0 $$ $$ Q_{\text{neta}} = (-67.5) \times (8.854 \times 10^{-12}) $$ $$ Q_{\text{neta}} \approx \mathbf{-5.98 \times 10^{-10} \text{ C}} $$
	
	**Respuesta a):** La carga neta contenida es aproximadamente **$-5.98 \times 10^{-10} \text{ C}$** (o $-0.598 \text{ nC}$).
	
	---
	
	### b) Origen del Campo Eléctrico
	
	**¿El campo eléctrico sólo es producido por las cargas en el interior?** **No.** El campo eléctrico $\vec{E}$ resultante en cualquier punto es la suma vectorial de los campos producidos por **todas** las cargas, tanto internas como externas (Principio de Superposición,).
	
	**¿Cómo podría saberse?** Se puede deducir por la **configuración y dirección** del campo descrito:
	
	1. **Campo Pasante (Cargas Externas):** El hecho de que existen líneas de campo que atraviesan el objeto (entran por la izquierda y salen por la derecha, ambas horizontales) indica la presencia de una fuente de campo externa (como placas cargadas distantes). Si solo hubiera carga interna, las líneas nacerían o morirían radialmente dentro del objeto, sin mantener una dirección horizontal constante "cruzando" el volumen.
	2. **Diferencia de Magnitud (Carga Interna):** El hecho de que la magnitud del campo que entra ($E_2$) sea diferente a la que sale ($E_1$) nos indica que **sí hay carga en el interior**. Como sale menos flujo del que entra ($E_1 < E_2$), sabemos que hay carga negativa dentro que está "terminando" algunas de esas líneas de campo externas.
	
	En conclusión, el campo es una superposición: un campo externo que define la dirección horizontal general, modificado localmente por la carga negativa interna.
* [ ] Una coraza esférica conductora, con radio interior a y radio exterior b, tiene una carga puntual positiva Q localizada en su centro. La carga total en la coraza es -3Q, y está aislada de su ambiente (figura 22.38). a) Obtenga expresiones para la magnitud del campo eléctrico, en términos de la distancia r desde el centro, para las regiones r , a, a , r , b y r . b. b) ¿Cuál es la densidad superficial de carga en la superficie interior de la coraza conductora? c) ¿Cuál es la densidad superficial de carga en la superficie exterior de la coraza conductora? d) Elabore un diagrama de las líneas de campo y la localización de todas las cargas. e) Grafique la magnitud del campo eléctrico como función de r

	
	**Nota importante sobre los datos:** Aunque en tu texto mencionas "23Q", la **Figura 22.38** en la fuente muestra claramente que la carga total de la coraza es **$-3Q$**. Procederé con el valor **$-3Q$** ya que es el que corresponde al diagrama físico del problema.
	
	---
	
	### a) Magnitud del campo eléctrico en las tres regiones
	
	Para determinar el campo eléctrico, utilizamos la Ley de Gauss, la cual establece que el campo depende de la carga neta encerrada dentro de una superficie gaussiana imaginaria: $\oint \vec{E} \cdot d\vec{A} = \frac{Q_{\text{enc}}}{\epsilon_0}$,.
	
	1. **Región $r < a$ (Dentro de la cavidad):**
	    
	    - Imaginamos una esfera gaussiana de radio $r$ menor que $a$.
	    - La carga encerrada es únicamente la carga puntual central $+Q$.
	    - El campo es radial y hacia afuera.
	    - **Expresión:** $$ E = \frac{1}{4\pi\epsilon_0} \frac{Q}{r^2} \quad \text{o} \quad E = \frac{kQ}{r^2} $$ (Referencia fórmula carga puntual:,).
	2. **Región $a < r < b$ (Dentro del conductor):**
	    
	    - Según las fuentes, cuando un conductor está en equilibrio electrostático, el campo eléctrico es **cero** en cualquier parte de su interior.
	    - **Expresión:** $$ E = 0 $$
	3. **Región $r > b$ (Fuera de la coraza):**
	    
	    - Imaginamos una esfera gaussiana de radio $r$ mayor que $b$.
	    - La carga encerrada total es la suma de la carga puntual central ($+Q$) y la carga total de la coraza ($-3Q$).
	    - $Q_{\text{neta}} = Q + (-3Q) = -2Q$.
	    - El campo es radial, pero dado que la carga neta es negativa, las líneas de campo apuntan hacia adentro (hacia la esfera).
	    - La magnitud depende del valor absoluto de la carga.
	    - **Expresión:** $$ E = \frac{1}{4\pi\epsilon_0} \frac{|-2Q|}{r^2} = \frac{1}{4\pi\epsilon_0} \frac{2Q}{r^2} \quad \text{o} \quad E = \frac{2kQ}{r^2} $$
	
	---
	
	### b) Densidad superficial de carga en la superficie interior ($r = a$)
	
	Para que el campo eléctrico dentro del conductor ($a < r < b$) sea cero, la Ley de Gauss exige que la carga neta encerrada por una superficie que pase por el interior del conductor sea cero.
	
	- $Q_{\text{encerrada}} = Q_{\text{puntual}} + Q_{\text{superficie_interior}} = 0$
	- $Q + Q_{\text{int}} = 0 \Rightarrow Q_{\text{int}} = -Q$.
	- La carga inducida en la superficie interior es **$-Q$**.
	
	La densidad superficial de carga ($\sigma$) es la carga dividida por el área de la superficie ($A = 4\pi r^2$). $$ \sigma_{\text{int}} = \frac{Q_{\text{int}}}{A_{\text{int}}} = \frac{-Q}{4\pi a^2} $$
	
	**Respuesta:** $\sigma_{\text{int}} = -\frac{Q}{4\pi a^2}$
	
	---
	
	### c) Densidad superficial de carga en la superficie exterior ($r = b$)
	
	La carga total de la coraza se conserva y es igual a $-3Q$ (según la Figura 22.38). Esta carga total se distribuye entre la superficie interior y la exterior.
	
	- $Q_{\text{total_coraza}} = Q_{\text{int}} + Q_{\text{ext}}$
	- $-3Q = (-Q) + Q_{\text{ext}}$
	- $Q_{\text{ext}} = -3Q + Q = -2Q$.
	- La carga en la superficie exterior es **$-2Q$**.
	
	Calculamos la densidad superficial para el radio $b$: $$ \sigma_{\text{ext}} = \frac{Q_{\text{ext}}}{A_{\text{ext}}} = \frac{-2Q}{4\pi b^2} $$
	
	**Respuesta:** $\sigma_{\text{ext}} = -\frac{Q}{2\pi b^2}$
	
	---
	
	### d) Diagrama de líneas de campo y localización de cargas
	
	Basado en la descripción física de las fuentes,,:
	
	1. **Localización de cargas:**
	    
	    - En el **centro**: Una carga puntual positiva $+Q$.
	    - En la **superficie interior ($r=a$)**: Una capa de cargas negativas distribuidas uniformemente con valor total $-Q$.
	    - En el interior del material ($a < r < b$): No hay carga neta.
	    - En la **superficie exterior ($r=b$)**: Una capa de cargas negativas distribuidas uniformemente con valor total $-2Q$.
	2. **Líneas de campo ($\vec{E}$):**
	    
	    - **Región $r < a$:** Las líneas de campo **nacen** en la carga central $+Q$ y viajan radialmente hacia afuera hasta terminar en las cargas negativas de la superficie interior.
	    - **Región $a < r < b$:** **No hay líneas de campo**. El espacio está vacío de líneas porque $E=0$.
	    - **Región $r > b$:** Las líneas de campo vienen desde el infinito y **terminan** (entran) en la superficie exterior de la coraza, ya que la carga neta vista desde fuera es negativa ($-2Q$). La densidad de líneas aquí es mayor (el doble) que en la cavidad interior, debido a que la magnitud de la carga efectiva es $|-2Q|$ frente a $|Q|$.
	
	---
	
	### e) Gráfica de la magnitud del campo eléctrico vs $r$
	
	La gráfica consta de tres secciones discontinuas:
	
	1. **De $0$ a $a$:** Una curva que decrece rápidamente proporcional a $1/r^2$. (Comienza asintóticamente muy alta cerca de 0 y baja hasta el valor $kQ/a^2$ en la superficie interior).
	2. **De $a$ a $b$:** Una línea plana sobre el eje horizontal (Valor = 0). Hay una discontinuidad abrupta en $r=a$ donde el campo cae a cero.
	3. **De $b$ a $\infty$:** En $r=b$, el campo salta desde 0 hasta un valor de $k(2Q)/b^2$. A partir de ahí, la curva decrece nuevamente proporcional a $1/r^2$, acercándose a cero a medida que $r$ tiende a infinito.
	
	_Nota: La curva externa ($r>b$) es más alta que la proyección de la curva interna si extrapoláramos, ya que depende de $2Q$ en lugar de $Q$._
* [ ] Bloque con carga uniforme. Un bloque de material aislante tiene un espesor 2d y está orientado de forma que sus caras quedan paralelas al plano yz y dado por los planos x 5 d y x 5 2d. Las dimensiones y y z del bloque son muy grandes en comparación con d y pueden considerarse esencialmente infinitas. El bloque tiene una densidad de carga positiva uniforme r. a) Explique por qué el campo eléctrico debido al bloque es igual a cero en el centro del bloque (x 5 0). b) Con base en la ley de Gauss, encuentre el campo eléctrico debido al bloque (magnitud y dirección) en todos los puntos del espacio
	Basado en los principios de la **Ley de Gauss** y las definiciones de distribución de carga continua presentes en tus fuentes, aquí tienes la solución detallada para el problema del bloque aislante.
	
	**Interpretación de los datos:** El texto "x 5 d y x 5 2d" parece contener errores de codificación tipográfica (comunes al copiar textos de libros como el _Sears Zemansky_ mencionado en la fuente). Dado que el problema indica que el espesor es $2d$ y pide analizar el "centro del bloque ($x=0$)", se deduce que el bloque se extiende desde **$x = -d$** hasta **$x = +d$**.
	
	---
	
	### a) ¿Por qué el campo eléctrico es cero en el centro del bloque ($x = 0$)?
	
	La razón se basa en la **simetría** y el principio de superposición.
	
	1. **Simetría de la distribución:** El bloque es infinito en las direcciones $y$ y $z$, y tiene una densidad de carga volumétrica uniforme $\rho$. Esto significa que la distribución de carga es idéntica si miramos hacia la izquierda ($-x$) o hacia la derecha ($+x$) desde el origen.
	2. **Cancelación vectorial:** Imagina dividir el bloque en pares de láminas delgadas simétricas. Para cualquier lámina de carga ubicada en una posición $+x$, existe una lámina idéntica en la posición $-x$.
	    - El campo eléctrico generado por la carga a la derecha ($+x$) apunta hacia la izquierda (alejándose de la carga positiva).
	    - El campo eléctrico generado por la carga a la izquierda ($-x$) apunta hacia la derecha.
	3. **Resultado:** En el centro exacto ($x=0$), estos vectores tienen la misma magnitud pero direcciones opuestas. Al sumarlos vectorialmente, se anulan mutuamente, resultando en un campo eléctrico neto de **cero**.
	
	---
	
	### b) Cálculo del campo eléctrico mediante la Ley de Gauss
	
	Utilizamos la Ley de Gauss, que establece que el flujo eléctrico neto a través de una superficie cerrada es igual a la carga encerrada dividida por la permitividad del vacío ($\epsilon_0$). $$ \oint \vec{E} \cdot d\vec{A} = \frac{Q_{\text{enc}}}{\epsilon_0} $$
	
	**Configuración de la Superficie Gaussiana:** Debido a la simetría plana, elegimos como superficie gaussiana un **cilindro pequeño (o una caja)** con área de tapas $A$. Orientamos el cilindro de modo que sus caras planas sean paralelas al plano $yz$ y esté centrado en el origen ($x=0$).
	
	- El campo eléctrico $\vec{E}$ solo tiene componente en el eje $x$ ($\vec{E} = E\hat{i}$) y es perpendicular a las tapas del cilindro.
	- Por simetría, la magnitud $E$ es la misma en ambas tapas (a una distancia $x$ y $-x$).
	- El flujo total es la suma del flujo por ambas tapas: $\Phi_E = EA + EA = 2EA$. (El flujo por los laterales es cero).
	
	#### 1. Para puntos dentro del bloque ($|x| < d$)
	
	Queremos hallar $E$ a una distancia $x$ del centro, donde $x$ es menor que $d$.
	
	- **Volumen encerrado:** El cilindro tiene una longitud de $2x$ (desde $-x$ a $x$) y área $A$. $$ V = 2xA $$
	- **Carga encerrada ($Q_{\text{enc}}$):** Usamos la densidad volumétrica $\rho$: $$ Q_{\text{enc}} = \rho \cdot V = \rho (2xA) $$
	- **Aplicando Gauss:** $$ 2EA = \frac{\rho (2xA)}{\epsilon_0} $$
	- **Despejando $E$:** Cancelamos $2A$ de ambos lados. $$ E = \frac{\rho x}{\epsilon_0} $$
	
	**Dirección:** Radial hacia afuera.
	
	- Si $x > 0$, $\vec{E} = \frac{\rho x}{\epsilon_0} \hat{i}$
	- Si $x < 0$, el campo apunta en dirección $-\hat{i}$.
	
	#### 2. Para puntos fuera del bloque ($|x| > d$)
	
	Ahora extendemos la superficie gaussiana para que sus tapas estén fuera del bloque (a una distancia $x > d$).
	
	- **Carga encerrada ($Q_{\text{enc}}$):** La superficie gaussiana es más ancha que el bloque, pero **la carga solo existe dentro del espesor del bloque** (entre $-d$ y $d$). Por lo tanto, el volumen con carga es fijo: espesor $2d$ y área $A$. $$ V_{\text{cargado}} = 2dA $$ $$ Q_{\text{enc}} = \rho (2dA) $$
	- **Aplicando Gauss:** $$ 2EA = \frac{\rho (2dA)}{\epsilon_0} $$
	- **Despejando $E$:** Cancelamos $2A$ de ambos lados. $$ E = \frac{\rho d}{\epsilon_0} $$
	
	Observa que fuera del bloque, el campo es **constante** y uniforme, similar al comportamiento de láminas infinitas descrito en las fuentes.
	
	### Resumen de Resultados
	
	- **En el interior ($ -d < x < d $):** $$ \vec{E} = \frac{\rho x}{\epsilon_0} \hat{i} $$ (El campo aumenta linealmente desde el centro).
	    
	- **En el exterior ($ x > d $ o $ x < -d $):**
	    
	    - Para $x > d$ (derecha): $\vec{E} = \frac{\rho d}{\epsilon_0} \hat{i}$
	    - Para $x < -d$ (izquierda): $\vec{E} = -\frac{\rho d}{\epsilon_0} \hat{i}$

[[Tareas FIS-130]] 