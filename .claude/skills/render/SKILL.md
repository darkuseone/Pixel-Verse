---
name: render
description: Фоновый рендер серии или фильма, микс, контроль громкости и кадров финала, сжатие под лимит (HEVC двухпроходный ≤ 95 МБ, шортс ≤ 29 МиБ для чата). Использовать после контрольных кадров, когда код сцены готов.
---
# /render <путь к epNN.py | movie.py>

1. **Перед рендером:**
   - мини-листы по планам (`python3 movie.py sheet <ids…>` или `engine/critic.py` для 9:16);
   - смотреть только листы и кропы;
   - править → перепроверить только изменённые планы.
2. **Рендер в фоне, без опроса:** Bash `run_in_background: true`, `timeout` 7200000:
   `cd <папка> && (time python3 <epNN|movie>.py all 4) > <scratchpad>/render.log 2>&1`
   - ждать уведомления о завершении;
   - пока идёт — писать сценарий, выкладку, документы;
   - скорость в 16:9 ≈ 1 кадр/с на процесс (4:30 → ~55 мин);
   - после правок — `python3 <ep>.py shots <i|name …>` вместо полного рендера.
3. **Микс:** `python3 mix.py [<noaudio.mp4> <out.mp4>]` → громкость `ffmpeg -i out.mp4 -af volumedetect -vn -f null - 2>&1 | grep -E "mean_vol|max_vol"`. Новые серии (в `timeline.py` есть `LUFS = -14.0`) — проверять `-af ebur128`: I ≈ −14 LUFS, пик ≤ −1 dB; старые — mean −20…−22 dB, max ≤ 0; вставки тише — поднять их gain в SFX.
4. **Кадры финала:** 9 кадров через `ffmpeg -ss t -frames:v 1 -vf scale=480:-1` → один лист → посмотреть.
5. **Сжатие:**
   - шортс > 29 МиБ (лимит чата) — `PV_CRF=23` и перерендер;
   - 16:9 > 95 МБ — двухпроходный HEVC, битрейт ≈ (95·8/длина_с − 0,2) Мбит/с; 4:32 → 2500k. Кодирование долгое (~15 мин), запускать в фоне:
```
ffmpeg -y -i in.mp4 -c:v libx265 -b:v 2500k -x265-params pass=1:log-level=error -an -f null /dev/null
ffmpeg -y -i in.mp4 -c:v libx265 -b:v 2500k -x265-params pass=2:log-level=error -tag:v hvc1 -c:a copy -movflags +faststart final.mp4
```
   H.264-мастер в git не класть, перенести в `build/`.
