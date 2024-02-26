
# Voseador

A tiny python package to conjugate spanish verbs with voseo (using vos instead of tu).

This package works by derivating the "vos" conjugation from the "vosostros" one when necesary. For example: "vosotros cantáis" -> "vos cantás". It also has an exception table for irregular verbs.

Seamless integration with the verbecc spanish conjugator.

## Dependencies

Python 3.7

Unidecode==1.3.6

## Examples

### Using verbecc

Additional dependencies:
verbecc==1.7.1

``` python
from verbecc import Conjugator
from voseador import Voseador

conjugator = Conjugator(lang='es')
voseador = Voseador()

conjugation = conjugator.conjugate("haber")

conjugation = voseador.add_vos_to_verbecc_conjugation(conjugation)

print(conjugation["moods"])
```

### On its own

``` python
from voseador import Voseador

voseador = Voseador()

vos_verb = voseador.vos_from_vosotros(mood="indicativo", tense="presente", infinitivo="comer", vosotros_verb="coméis")

print(vos_verb)
```

Take into account that this last example only works with tenses in wich the "vos" conjugation differs from de "tu" one. In the rest of the cases you can just copy the "tu" conjugation.
