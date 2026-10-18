# Pau

**Un plan que ya aprobaste. Alguien que lo saque adelante.**

Pau es un plugin de Claude que lleva un proyecto desde la aprobación hasta el resultado. Convierte el plan
en un único esquema de estado, hace pasar una unidad entera de trabajo de punta a punta antes de programar
nada, se para al primer defecto y solo te llama cuando cambia el precio, la fecha, el alcance o la
reputación, siempre con la recomendación ya hecha.

> Focus & Sian define. You approve. Pau delivers.

[English](README.md) · [Català](README.ca.md)

---

## Para qué sirve

Tienes un plan con el que ya estás de acuerdo. Lo que no quieres es acabar de secretario de tu propio plan:
persiguiendo qué ha pasado, releyendo tus notas para encontrar dónde se quedó la cosa, contestando doce
preguntas al día que alguien podría haber contestado sin ti.

Pau es la capa que falta entre el plan y el trabajo. Pegas el plan, ves un tablero, contestas unas pocas
decisiones y ves la verdad sin tener que preguntarla.

## Instalación

**claude.ai y Cowork** - Personalización → Plugins → Añadir → Añadir marketplace, con la URL de este
repositorio. Después instala `pau` desde ahí.

**Claude Code**

```bash
claude plugin marketplace add cintocasals/pau
claude plugin install pau@pau
```

## Empezar

```
/pau:take  <pega tu plan, o indica la ruta>
```

Pau lee el plan, construye el estado, nombra cada suposición que nadie ha comprobado, detiene las acciones
de riesgo que dependen de ellas y arranca el trabajo que no. Te deja `BOARD.md` y una nota corta: qué ha
asumido, qué está parado y por qué, y qué espera de ti.

Luego:

| Orden | Qué hace |
|---|---|
| `/pau:take` | Entregar un plan aprobado |
| `/pau:cycle` | Ejecutar una pasada de gestión |
| `/pau:decide` | Ver las decisiones abiertas, o contestar una |
| `/pau:board` | Rehacer el tablero y contrastarlo con el estado |
| `/pau:close` | Cerrar una tarea, juzgar una puerta, cerrar el proyecto |

## Cómo decide

**Pau decide** cuatro cosas: el orden del trabajo, la asignación, los reintentos y la replanificación que
no mueve la fecha. Esa lista está cerrada.

**Tú decides** el resto. Siete acciones quedan preparadas a un clic y **nunca se ejecutan en una sesión que
nadie está mirando**:

> gastar · enviar a terceros · publicar · borrar · firmar · crear cuentas · tocar sistemas en producción de
> otros proyectos

El prompt de una tarea programada no es tu consentimiento. Un agente que corre a las tres de la mañana no
tiene a quién preguntar, así que no actúa en tu nombre.

Y los cuatro cambios de contrato, que te llegan como decisión: **alcance, fecha, presupuesto, cliente**.

Cada decisión llega siempre con la misma forma, y nunca sin recomendación:

```
DECISIÓN NECESARIA - Base legal para el primer correo
Recomendación: enviar solo a direcciones con consentimiento registrado; no comprar lista.
Por qué: ninguna dirección tiene base legal verificada; enviar es una acción roja; la puerta
  no necesita correo.
Alternativa descartada: interés legítimo sobre direcciones públicas. Nadie lo ha verificado, y
  Pau no emite dictámenes legales.
Coste / riesgo: ninguno.
Si no decides: el envío queda preparado y parado. La puerta no depende de ello.
```

**Nunca más de tres abiertas a la vez.** Una cuarta se encola y se cuenta, no se decide por ti en silencio.

## Qué lleva dentro

**Dos agentes.** `pau` dirige, prioriza, delega y es el único que escribe el estado. `reviewer` comprueba
el trabajo terminado contra su propio criterio, con ojos que no lo han hecho, y puede parar la línea.

**Cinco skills.** `intake` recoge el plan y saca la primera unidad. `cycle` ejecuta una pasada. `decide`
sostiene la raya entre lo tuyo y lo de Pau. `board` es el único camino que escribe estado. `close` cierra
una tarea, una puerta o un proyecto.

**Un esquema de estado,** en ficheros planos en la raíz de tu proyecto:

```
.pau/state.json  .pau/tasks.json  .pau/gates.json  .pau/decisions.json  .pau/log.jsonl
BOARD.md
```

Cada escritura se prepara aparte, se valida y solo entonces se aplica. Una escritura que rompe el esquema no
cambia nada y te dice exactamente qué estaba mal.

## Tres cosas poco habituales, y por qué

**Ningún bucle por reloj por defecto.** Mirar algo cada hora y no encontrar nada es moverse, no trabajar.
Pau funciona por acontecimientos (has contestado algo, ha vuelto una pieza, vence una puerta) con un latido
diario para que un proyecto tranquilo no se quede a oscuras, y un techo de cuatro ejecuciones programadas
al día.

**Cada ejecución deja rastro, también la que no hizo nada.** El validador rechaza una escritura que no
añade entrada al registro. Suena a burocracia hasta que intentas contestar "¿cuánto de esto fue real?"
sobre un sistema que solo apuntaba las cosas cuando pasaba algo: un bucle así se ve perfecto desde dentro y
no te dice nada.

**Nada se inventa.** Cada elemento del estado lleva un `source`: la línea del plan de donde salió. Sin
fuente, no hay elemento. El tablero es una vista del estado, nunca una segunda versión, y cuando no
coinciden manda el estado.

## El detector de silencio

Cuando una cuenta agota su límite de uso, las ejecuciones programadas se rechazan y nada lo anuncia. Un
vigilante dentro de la misma cuenta se para en el mismo momento.

`templates/silence-check.yml` es una acción de GitHub que copias en tu propio repositorio. Vigila el
**progreso, no las ejecuciones** (una tarea que se mueve, una puerta superada, una decisión contestada, un
entregable nuevo) y abre una incidencia cuando eso se detiene. Sin servidor y sin cuentas nuevas.

## Lo que no hace

No sustituye tu gestor de incidencias, tu calendario ni tu integración continua. No escribe el código por
ti ni hace el trabajo de tu oficio: decide qué toca ahora, consigue que lo haga quien lo hace, lo comprueba
y mantiene el registro recto.

No se mete entre tú y tus herramientas. Un departamento (un subagente, un skill que ya tienes, una persona)
recibe una orden de trabajo y devuelve un albarán. Pau lo convierte en estado. Por eso hay un solo escritor
y no diez.

Una nota honesta sobre hasta dónde llega la garantía: en las superficies donde corren los hooks de plugin,
un hook puede interceptar una escritura. En el chat de claude.ai no corren. Así que la regla de un solo
escritor la sostienen el validador y la disciplina, no la plataforma. El validador rechaza una escritura
mala y detecta una edición a mano la próxima vez que corre; no puede impedir que alguien edite un JSON por
su cuenta.

## Requisitos

Python 3 para los dos scripts. Nada más: ni servidor, ni base de datos, ni más cuentas que la que ya
tienes.

## Licencia

MIT. Ver [LICENSE](LICENSE).
