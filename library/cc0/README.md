# Открытая библиотека звуков и музыки (CC0) — для всех сериалов

Решение владельца 02.11.2026: звуки ElevenLabs и синтез кодом местами визгливые; общая библиотека реальных записей с открытой
лицензией, переиспользуется в сериалах и сериях, пополняется по мере надобности. Все файлы — **CC0 1.0** (без указания автора,
коммерческое использование разрешено). Перед добавлением: проверить лицензию на странице источника, обрезать первый дубль
(`/tmp/cut.py`-логика: онсет → тишина), `loudnorm` (разовые −18 LUFS / −2 dBTP, атмосферы −26 LUFS), `engine/sfxcheck.py` без HARSH.

## sfx/ — BigSoundBank (Joseph Sardin, bigsoundbank.com, CC0; mp3: `https://bigsoundbank.com/UPLOAD/mp3/<ID>.mp3`)
| Файл | ID | Что |
|---|---|---|
| door_apartment_open | 1702 | дверь квартиры открывается |
| door_apartment_close | 1704 | дверь квартиры закрывается |
| doorbell_2 / doorbell_3 / doorbell_4 | 0160 / 0161 / 1604 | дверной звонок (электронный «дин-дон» — владелец: «как объявление в аэропорту», для квартир не брать) |
| intercom_ring | 2373 | домофон |
| elevator_ride | 1711 | лифт едет (гул, 10 с) |
| canvas_bag_drop | 0576 | тканевая сумка падает на пол |
| zipper | 0014 | молния |
| suitcase | 0802 | чемодан |
| chair_creak | 0666 | скрип стула/кресла |
| slipper_steps | 0373 | шаги в тапках |
| floor_squeak | 0518 | скрип пола |
| steps_concrete | 1318 | шаги по бетону (подъезд) |
| keys_lock / keys_on_table | 2414 / 0087 | ключи в замке / на столе |
| phone_dial_tone | 0767 | гудки телефона |
| teeth_chatter | 0789 | стук зубов |
| cloth_rustle | 0013 | ткань, плед |
| wind_inside_1 | 1714 | ветер в квартире/на балконе (атмосфера 12 с) |
| wind_whistle | 0147 | свист ветра (атмосфера 12 с) |
| room_tone_apartment | 2387 | тишина квартиры с улицей (атмосфера 12 с) |
| whoosh_1 / whoosh_3 | 0572 / 1795 | взмах, рывок камеры |
| vinyl_scratch | 2858 | скретч пластинки |
| rimshot_joke | 2409 | «ба-дум-тсс» |
| boing_cartoon | 2277 | мультяшный «боинг» |
| bottle_clink | 0487 | звон стекла (банки) |
| small_dog_bark | 0682 | лай маленькой собаки |
| gong_strong | 1483 | гонг |

## music/ — OpenGameArt (CC0), с 02.11.2026 только «яркие» треки
Первая партия (джаз/блюз) убрана: 60–90 % энергии ниже 150 Гц, на динамике телефона звучала как гул. Перед добавлением подложки
меряю долю энергии в полосе 400–4000 Гц (мелодия): нужно ≥ 0,4; обработка `highpass=90`, −18 LUFS.
| Файл | Автор | Страница | Длина | Настроение |
|---|---|---|---|---|
| ukulele_loop | StarNinjas | opengameart.org/content/ukulele-forest-beginning-loop-and-end | 8,5 с луп | укулеле — лёгкий бытовой ситком |
| badinerie_flute | Spring Spring | opengameart.org/content/badinerie | 60 с | Бах «Шутка», флейта — суета, комичный хаос |
| flute_strings | Spring Spring | opengameart.org/content/minimalistic-flute-strings-tune | 60 с | флейта и струнные — спокойный фон |
| town_cheerful | cynicmusic | opengameart.org/content/town-theme-rpg | 60 с | весёлая «городская» тема |
| sad_orchestral | obscure music | opengameart.org/content/sad-orchestral-theme | 60 с | грустный оркестр — неудача героя (комичный контраст) |
| happy_lullaby | cynicmusic | opengameart.org/content/happy-lullaby-song17 | 40 с | колыбельная — ирония, умиление |

Использование: в `timeline.py` пути `library/cc0/sfx/<имя>.mp3` и `library/cc0/music/<имя>.mp3`; музыка в `BEDS` с `loop_sec` = длина
файла (52–60 с), громкость 1,2–1,3 с дакингом (под речью ×0,4): так подложка ≈ 13 дБ ниже речи; при 0,15–0,3 её не слышно (замер 02.11.2026).
