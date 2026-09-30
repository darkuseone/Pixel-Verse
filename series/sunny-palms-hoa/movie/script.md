# «Sunny Palms HOA: The Complete Season» — полнометражная версия (7:06)

Один длинный ролик для YouTube из всего сезона 1. Рассказчик — Эрл («режиссёрская версия аллигатора»). Новый нарративный каркас и новая графика 16:9, а не склейка Shorts.
Сквозные механики: счётчик TOTAL FINES в углу; главы с карточками; Эрл в окне «картинка-в-картинке»; страница 400 приветственного пакета (посев в начале, выплата после титров).

| Время | Блок | Что происходит | Новое / переиспользовано |
|---|---|---|---|
| 0:00 | **Холодный старт** | Президент Дейл штрафует Бренду («It's BEIGE!»), пауза; Эрл: «Он должен $5,900. Теперь он президент. Объясню.» VHS-перемотка «6 WEEKS EARLIER» | новое (3 реплики Эрла), кадр финала |
| 0:16 | **Титры-заставка** | «A BEIGE PICTURES PRODUCTION», неоновый титул, Эрл читает название | новое |
| 0:23 | **Приветственный пакет** | Бренда вручает 400-страничный пакет, «Page one is the fines», Дейл: «I'll read it never», кидает в пруд, Эрл: «Nobody does. That's how they get you» | новое (5 реплик) |
| 0:41 | **Глава 1. Ecru Whisper** | E01: $250 за почтовый ящик, «Bone = Ecru Whisper», покраска, штраф $500, форма 27-B, ящик на газон Бренды, Beautification Fund, Эрл «grandfathered in» | E01 (озвучка) + новые ракурсы 16:9, Эрл в PiP |
| 1:29 | **Рекламная пауза** | «Sunny Palms Realty»: «Bone. Beige. Ivory. Ecru Whisper. Four colors. Same color», мелкий шрифт «Fines may apply. Fines do apply» | новое (3 реплики Бренды), джингл |
| 1:41 | **Глава 2. Emotional Support Flamingo** | Дейл остановил видео на шаге 2; Эрл: «12 минут, он смотрел 40 секунд»; затем E02: Кевин, сертификат $19.99, «Novelty», $300 в год, 94 фламинго | интро новое (3 реплики), E02 |
| 2:33 | **Протокол совета** | Бренда пересаживается по стульям: «Motion / Seconded / Approved unanimously»; Эрл: «The board has one member» | новое (5 реплик), задник xAI «зал совета» |
| 2:47 | **Глава 3. Suspicious Man (Walking)** | E03: соседское приложение, запись доп. камеры в 3:04, дверной звонок чёрный, кот на голове Эрла | E03 |
| 3:31 | **Глава 4. Category 5 (Permit)** | E04: ураганная вечеринка, штраф урагану, счёт $4,750 Дейлу, Эрл: «Never once fined ME» | E04 |
| 4:13 | **Брифинг** | Бренда у трибуны, вспышки камер: «Hurricane Kevin ... in collections»; Эрл: «Kevin is in Georgia» | новое (3 реплики) |
| 4:26 | **Подписка (условия действуют)** | Эрл: «Subscribe. To unsubscribe file Form 27-B thirty days BEFORE subscribing. Comments are read by Brenda.» | новое (3 реплики) |
| 4:38 | **Глава 5. Suggested Tip** | E05: бесплатный хот-дог за $47.63, планшет TAPPY, «tip this video» | E05 (без экрана отзывов ради темпа) |
| 5:15 | **Предвыборная кампания** | Дейл: «I watched a video about democracy»; Эрл: «It was a cartoon about a beaver. The beaver lost.» | новое (2 реплики) |
| 5:23 | **Глава 6. Vote Earl** | E06: выборы, голос Эрла, Дейл президент, штраф Бренде | E06 |
| 6:15 | **Конец, титры, ляпы** | Пауза кадра из холодного старта: «And that is how a man with six thousand dollars in fines became president»; титры поверх ляпов («Take fourteen», Бренда ломается) | новое (6 реплик) |
| 6:39 | **Сцена после титров** | Багамы: Бренда с «Beautification Fund», Дейл-президент: «Page four hundred. The president may fine anyone. Anywhere.»; Эрл: «Hurricane season starts June first»; карточка «SEASON 2: HURRICANE SEASON» | новое (7 реплик), задник xAI «пляж» |

**Новых реплик:** 41 (`voice/movie/lines.json`, eleven_v4, Dale/Brenda/Earl без изменений голосов). **Новых звуков:** 10 (`library/sfx/`: vhs_rewind, ad_jingle, amb_beach, seagull, ice_clink, amb_boardroom, chair_scoot, clapper_clack, tv_static_blip, book_thud). **Новых задников:** 2 (зал совета, пляж). Музыка: один трек `sunny_palms_theme_15s`, зацикленный непрерывно, с автопродавливанием под речь.

## Сборка
```
cd series/sunny-palms-hoa/movie
python3 movie.py plan            # длительности блоков
python3 movie.py sheet ch1 1 5 20   # контрольные кадры блока
python3 movie.py video 4         # рендер (build/movie/video.mp4)
python3 movie.py audio           # микс (build/movie/audio.wav)
python3 movie.py final           # final.mp4
python3 cover.py ref | ai | make # обложка 1920x1080
```
Код: `kit.py` (16:9-каркас, оверлеи, HUD), `shots.py` (планы), `blocks/*.py` (блоки), `movie.py` (оркестратор). Движок в 16:9 включается переменной `PV_WIDE=1` (`engine/stage.py`), Shorts не затронуты.
