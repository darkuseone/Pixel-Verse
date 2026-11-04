# Aura Dad — STATUS (04.11.2026, сезон 1 готов)
- **Сделано:** S01 E01–E06 (`episodes/epNN/final.mp4`, `cover.png`), файл выкладки `publish_s01.txt` (US: YouTube + Instagram, пн 09.11 – сб 14.11).
  E01 пересведён 04.11 (музыка −5 дБ, глубже вырез голосовых частот) по замечанию владельца; во всех сериях подложка 0,45–0,5.
- **Каст/голоса (Voice Library, без слотов):** doug, kayden, tammy, mirra, lily, skylar, jaxon, brett (`voices.json`); Бисквит без голоса.
- **Код:** риг `engine/props/auracast.py` (Doug, Kayden, Tammy, Lily + KID_PALS, Skylar, Brett, Biscuit, MIRRA, реквизит), кит
  `engine/props/aurakit.py` (миры kitchen/bathroom/sephoria/backyard/culdesac/bedroom, свет, таблички, слои: `occluder()` из задника
  поверх героев, `fgcam()` параллакс переднего плана, экраны AURA SCAN, обложка `cover_make`), плашка подписки `style='auradad'`.
- **Дальше:** ждать правки владельца; предложить фильм 16:9; S2 «GRANDPA MAXXING» (крючок финала).
- **Известное:** повороты 51–60 %, у E01 21,4 с, у E05 19,9 с — позже правила «≤ 18 с» из-за целых фраз (манера «понятная история»).
- **Команды:** `cd series/aura-dad/episodes/epNN && python3 epNN.py test 1 5 | all | shots <i>`; `python3 mix.py <noaudio> final.mp4`; `python3 cover.py`.
