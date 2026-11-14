# Superfici dei mondi di ricerca

Le tredici famiglie sono rappresentazioni originali generate per GeoStat Lab.
La varietà di ambienti riprende un principio di organizzazione dell’atlante di
Haegemonia; immagini, mappe e file del videogioco non sono stati impiegati.
Le denominazioni «Gaia», «acido» e «abitabile» appartengono all’ambientazione:
non costituiscono classificazioni astronomiche né misure di abitabilità.

## File e impiego

Ogni famiglia dispone di due albedo WebP equirettangolari in
`assets/space/families/`:

- `<famiglia>.webp`, 2048 × 1024 pixel, per navigazione e dispositivi mobili;
- `<famiglia>-4k.webp`, 4096 × 2048 pixel, per l’osservazione ravvicinata.

La versione 4K è il risultato diretto del calcolo; la versione 2K deriva da un
ricampionamento Lanczos. Le coordinate del generatore sono tridimensionali e
valutate sulla sfera, così che la superficie sia continua alla cucitura
longitudinale e ai poli. Le texture contengono colore e strutture superficiali,
senza terminatore o direzione di illuminazione. Rotazione, luce della stella e
notte restano responsabilità della scena. I filamenti aranciati vulcanici sono
colore dell’albedo: un’eventuale emissione notturna richiede una maschera separata
e non deve essere dedotta automaticamente da questi file.

| Identificativo | Famiglia | Tratti visivi |
| --- | --- | --- |
| `gaia` | Gaia | Oceani blu, continenti verdi, nubi chiare e calotte polari |
| `temperate` | Terrestre temperato | Continenti olivastri e ocra, mari, rilievi e nubi discontinue |
| `ocean` | Oceanico | Oceano esteso, arcipelaghi e fasce di nubi |
| `forest` | Forestale | Grandi continenti verde scuro, oceani e catene montuose |
| `plains` | Pianure | Terre salvia e dorate, bacini ridotti e rilievo contenuto |
| `swamp` | Paludoso | Mosaico di terre umide e acque verdi, velature atmosferiche |
| `desert` | Desertico | Bacini ocra, fasce di dune e depositi chiari |
| `arctic` | Artico | Ghiacci azzurri, fratture scure e rilievi chiari |
| `rocky` | Roccioso | Rocce brune, crateri, bordi e materiali espulsi |
| `barren` | Arido privo di vegetazione | Suolo grigio, crateri e variazioni di albedo |
| `volcanic` | Vulcanico | Crosta scura, canali incandescenti stilizzati e depositi di cenere |
| `acid` | Acido | Coltri sulfuree immaginarie, vortici ocra e giallo oliva |
| `gas` | Gigante gassoso | Bande atmosferiche blu e crema, turbolenza e vortice ovale |

I colori non permettono di determinare la composizione chimica; analogamente,
una texture oceanica o forestale non documenta la presenza di acqua liquida o
di vita. Il gigante gassoso rappresenta strati atmosferici visibili e viene
esplorato da un osservatorio orbitale, senza una superficie di atterraggio.

## Riproduzione

```sh
python3 -m pip install moderngl numpy Pillow
python3 scripts/bake-research-planets.py
```

Il generatore richiede un contesto OpenGL 3.3 tramite EGL; è compatibile con
rendering software Mesa. Le famiglie hanno semi espliciti e stabili, indicizzati
nel sorgente. È possibile rigenerarne una sola con `--families arctic` e scegliere
la destinazione della tavola di controllo con `--contact-sheet /tmp/planets.jpg`.
La tavola è un artefatto di verifica e non viene inclusa nella distribuzione.
Il sito usa i WebP già presenti nel repository e non richiede Python o OpenGL
durante la compilazione ordinaria.

Questi asset sono nuovi materiali del progetto; il generatore non incorpora
immagini o shader di terze parti. Per i diritti generali si rimanda a
`LICENSE.md`: questa documentazione non introduce una licenza aggiuntiva.
Gli obblighi delle altre risorse rimangono descritti in
`THIRD_PARTY_NOTICES.md`.
