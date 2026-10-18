# Pau

**Un pla que ja has aprovat. Algú que el tiri endavant.**

Pau és un plugin de Claude que porta un projecte de l'aprovació al resultat. Converteix el pla en un sol
esquema d'estat, fa passar una unitat sencera de feina de punta a punta abans de programar res, s'atura al
primer defecte i només et truca quan canvia el preu, la data, l'abast o la reputació, sempre amb la
recomanació ja feta.

> Focus & Sian define. You approve. Pau delivers.

[English](README.md) · [Español](README.es.md)

---

## Per a què serveix

Tens un pla amb el qual ja hi estàs d'acord. El que no vols és acabar fent de secretari del teu propi pla:
empaitant què ha passat, rellegint les teves notes per trobar on es va quedar la cosa, contestant dotze
preguntes al dia que algú podria haver contestat sense tu.

Pau és la capa que falta entre el pla i la feina. Hi enganxes el pla, veus un tauler, contestes poques
decisions i veus la veritat sense haver-la de demanar.

## Instal·lació

**claude.ai i Cowork** - Personalització → Plugins → Afegeix → Afegeix marketplace, amb l'URL d'aquest
repositori. Després instal·la-hi `pau`.

**Claude Code**

```bash
claude plugin marketplace add cintocasals/pau
claude plugin install pau@pau
```

## Començar

```
/pau:take  <enganxa-hi el pla, o digues on és>
```

Pau llegeix el pla, construeix l'estat, anomena cada suposició que ningú no ha comprovat, atura les accions
de risc que en depenen i arrenca la feina que no. Et deixa `BOARD.md` i una nota curta: què ha agafat, què
està aturat i per què, i què espera de tu.

Després:

| Ordre | Què fa |
|---|---|
| `/pau:take` | Entregar un pla aprovat |
| `/pau:cycle` | Fer una passada de gerència |
| `/pau:decide` | Veure les decisions obertes, o contestar-ne una |
| `/pau:board` | Refer el tauler i contrastar-lo amb l'estat |
| `/pau:close` | Tancar una tasca, jutjar una porta, tancar el projecte |

## Com decideix

**Pau decideix** quatre coses: l'ordre de la feina, l'assignació, els reintents i la replanificació que no
mou la data. Aquesta llista és tancada.

**Tu decideixes** la resta. Set accions queden preparades a un clic i **mai s'executen en una sessió que
ningú no mira**:

> gastar · enviar a tercers · publicar · esborrar · signar · crear comptes · tocar sistemes en producció
> d'altres projectes

El prompt d'una tasca programada no és el teu consentiment. Un agent que corre a les tres de la matinada no
té a qui preguntar, així que no actua en nom teu.

I els quatre canvis de contracte, que et pugen com a decisió: **abast, data, pressupost, client**.

Cada decisió arriba sempre amb la mateixa forma, i mai sense recomanació:

```
DECISIÓ REQUERIDA - Base legal per enviar el primer correu
Recomanació: enviar només a adreces amb consentiment registrat; no comprar llista.
Per què: cap adreça no té base legal verificada; enviar és una acció vermella; la porta no
  necessita correu.
Alternativa descartada: interès legítim sobre adreces públiques. Ningú no ho ha verificat, i
  Pau no fa dictàmens legals.
Cost / risc: cap.
Si no decideixes: l'enviament queda preparat i aturat. La porta no en depèn.
```

**Mai més de tres obertes alhora.** Una quarta s'encua i es compta, no es decideix per tu en silenci.

## Què porta a dins

**Dos agents.** `pau` dirigeix, prioritza, delega i és l'únic que escriu l'estat. `reviewer` comprova la
feina acabada contra el seu propi criteri, amb uns ulls que no l'han feta, i pot aturar la línia.

**Cinc skills.** `intake` recull el pla i fa passar la primera unitat. `cycle` fa una passada. `decide`
sosté la ratlla entre el que és teu i el que és de Pau. `board` és l'únic camí que escriu estat. `close`
tanca una tasca, una porta o un projecte.

**Un esquema d'estat,** en fitxers plans a l'arrel del teu projecte:

```
.pau/state.json  .pau/tasks.json  .pau/gates.json  .pau/decisions.json  .pau/log.jsonl
BOARD.md
```

Cada escriptura es prepara a part, es valida i només llavors s'aplica. Una escriptura que trenca l'esquema
no canvia res i et diu exactament què hi havia malament.

## Tres coses poc habituals, i per què

**Cap bucle per rellotge per defecte.** Mirar una cosa cada hora i no trobar res és moure's, no treballar.
Pau funciona per esdeveniments (has contestat una cosa, ha tornat una peça, venç una porta) amb un batec
diari perquè un projecte tranquil no es quedi a les fosques, i un sostre de quatre execucions programades
al dia.

**Cada execució deixa rastre, també la que no ha fet res.** El validador rebutja una escriptura que no
afegeix entrada al registre. Sona a paperassa fins que proves de contestar «quant d'això va ser real?»
sobre un sistema que només apuntava les coses quan passava alguna cosa: un bucle així es veu perfecte des
de dins i no et diu res.

**Res no s'inventa.** Cada element de l'estat porta un `source`: la línia del pla d'on surt. Sense font, no
hi ha element. El tauler és una vista de l'estat, mai una segona versió, i quan no coincideixen mana
l'estat.

## El detector de silenci

Quan un compte esgota el límit d'ús, les execucions programades es rebutgen i res no ho anuncia. Un
vigilant dins del mateix compte s'atura al mateix moment.

`templates/silence-check.yml` és una acció de GitHub que copies al teu repositori. Vigila el **progrés, no
les execucions** (una tasca que es mou, una porta superada, una decisió contestada, un lliurable nou) i obre
una incidència quan això s'atura. Sense servidor i sense comptes nous.

## El que no fa

No substitueix el teu gestor d'incidències, el teu calendari ni la teva integració contínua. No escriu el
codi per tu ni fa la feina del teu ofici: decideix què toca ara, aconsegueix que ho faci qui ho fa, ho
comprova i manté el registre recte.

No es fica entre tu i les teves eines. Un departament (un subagent, un skill que ja tens, una persona) rep
una ordre de treball i torna un albarà. Pau el converteix en estat. Per això hi ha un sol escriptor i no
deu.

Una nota honesta sobre fins on arriba la garantia: a les superfícies on corren els hooks de plugin, un hook
pot interceptar una escriptura. Al xat de claude.ai no hi corren. Així que la regla d'un sol escriptor la
sostenen el validador i la disciplina, no la plataforma. El validador rebutja una escriptura dolenta i
detecta una edició a mà la pròxima vegada que corre; no pot impedir que algú editi un JSON pel seu compte.

## Requisits

Python 3 per als dos scripts. Res més: ni servidor, ni base de dades, ni cap compte més del que ja tens.

## Llicència

MIT. Vegeu [LICENSE](LICENSE).
