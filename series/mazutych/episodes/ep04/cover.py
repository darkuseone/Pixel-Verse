"""Cover S01E04 v2 «Без прав»: the hook frame — the inspector with the baton, patrol lights and the fine slip «ШТРАФ · МОНОКОЛЕСО»
shoved at the lens; title «ШТРАФ ЗА / МОНОКОЛЕСО?!» (= hook text).  python3 cover.py -> cover.png (+ covers/cover_s01e04.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_maz import make
import ep04 as E

t = 0.2
frame = E.cop_cu(t, 0.0, 'glare', 'stop', whistle=True, sz=17.5, head=(540, 960), mouth_=0.5, blink=False)
E.lights(frame, t, 0.22)
E.M.paper(frame, 600, 1360, ['ШТРАФ', 'МОНОКОЛЕСО', '№ 000001'], w=460, h=310, rot=-8, col=(236, 232, 214), sizes=[72, 34, 26])
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['ШТРАФ ЗА', 'МОНОКОЛЕСО?!'], n=4, out=str(out), title_size=66)
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e04.png')
print(out)
