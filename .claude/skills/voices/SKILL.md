---
name: voices
description: Проверить, живы ли голоса ElevenLabs у героев сериала, и восстановить удалённые клоном с освобождением слотов по реестру. Использовать перед генерацией реплик сезона/фильма или когда TTS отвечает 400/404 на voice_id.
---
# /voices <slug> [chars…]

Реестр: `docs/voices.json` / `docs/voices.md`, инструмент `engine/voices.py`. Ключ не печатать.

1. **Проверка (0 кредитов):**
```
python3 - <<'P'
import json,os,urllib.request
V=json.load(open('series/<slug>/voices.json'))['characters']
for ch,v in V.items():
    try: urllib.request.urlopen(urllib.request.Request(f"https://api.elevenlabs.io/v1/voices/{v['voice_id']}",headers={'xi-api-key':os.environ['ELEVENLABS_API_KEY']})); print(ch,'OK')
    except Exception as e: print(ch,'GONE',e)
P
```
   400/404 = голоса нет. Синхронизировать реестр: `python3 engine/voices.py sync`.
2. **Нужен ли голос вообще?** Если у героя 1–3 реплики в новом материале — переиспользовать его старые дубли из `voice/epNN_t/` (0 кредитов, 0 слотов). Восстанавливать только тех, кому нужны новые реплики.
3. **Освободить слоты самому** (иначе `restore` удалит наименее нужный голос любого другого сериала):
   `python3 engine/voices.py free N --keep <slug>,<свежий_сериал>` (пробный прогон) → то же с `--go`. Через запятую, одним `--keep`. Голоса владельца (NIKITA, NIKITA2, Cartman) и голоса вне реестра не трогаются.
4. **Восстановить:** `python3 engine/voices.py restore <slug> <char>` для каждого — клон по записанным репликам, новый id пишется в `voices.json` и реестр.
5. В ответе владельцу одной строкой: кого восстановил и чьи голоса удалены (они в архиве, возвращаются той же командой). Записать в `docs/decisions.md`.
