# Почти Дикий Запад — сезон 1

Вестерн-пародия: хвастун Ковбой Билли третий год ловит вежливого бандита Кривого Сэма, а его лошадь Молния умнее хозяина и берёт взятки морковкой.

## Герои и голоса (не менять) — `voices.json`
| Герой | Голос ElevenLabs | voice_id | Субтитры |
|---|---|---|---|
| Ковбой Билли | Bob | `KTPVrSVAEUSJRClDzBw7` | жёлтый |
| Лошадь Молния | Silas | `WzVKtqQpTUUQ2JNx8YxI` | белый |
| Кривой Сэм | Callum | `N2lVS1w4EtoT3dr4eOWO` | сиреневый |

## Серии
| # | Название | Длит. | Статус |
|---|---|---|---|
| E01 | Самый быстрый | 40 с | готова |
| E02 | Засада | 46 с | готова |
| E03 | Информатор | 45 с | готова |

## Сквозные гэги
Шляпа Билли на Молнии · кактусы · морковка/подкуп Молнии · Сэм проезжает незамеченным · стервятники · «третий год ловит» · «Воздухан».

## Структура
- `voice/epNN/*.mp3` + `lines.json` — реплики (переиспользуемые: ep01 `n4` «Спасибо.», `n5` «Молния… Ты не видела Кривого Сэма?», `n6` «Не-а.»).
- `music/theme_western_chiptune_16s.mp3` — тема (луп). `sfx/` — звуки мульта; общие — `library/sfx/`.
- `episodes/epNN/` — final.mp4, cover.png, script.md, meta.md, lines.json, код сцены.

## Пересборка
```
cd series/pochti-dikiy-zapad/episodes/ep02
python3 ep02.py test 1 20 40      # лист превью → build/ep02/sheet.png
python3 ep02.py seg 0 700         # сегменты → build/ep02/seg_*.mp4
python3 cover.py                  # обложка → episodes/ep02/cover.png
```
Сведение E01/E02 делалось в чате вручную и в пак не попало. С E03 серия пересобирается целиком:
```
cd series/pochti-dikiy-zapad/episodes/ep03
python3 ep03.py test 1 20 40      # контрольные кадры
python3 ep03.py all               # видео (4 потока) → build/ep03/noaudio.mp4
python3 mix.py ../../../../build/ep03/noaudio.mp4 final.mp4
python3 cover.py ref|ai|make K    # обложка (ai — платно, xAI)
```
Локация салуна — `engine/props/saloon.py` (мир 800×640: вход, стойка, угол), переиспользуется.
