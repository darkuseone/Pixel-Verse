"""Cover S01E05 «$600 NOSEBLEEDS?!»: code frame (Duke roaring at the TicketMaxed price on his laptop), banknote plate on top of the 3:4 grid
zone + «Dollar Neon» title.  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import overlays as O
from props import feecast as C
from props import feekit as K
from props.feekit import A, aout

APT = K.world('apartment')
def fx_(big, v, a):
    hx, hy = aout(a, v, 'head')
    K.feathers(big, 0.45, 0.0, hx, hy - 40, n=14, seed=15)
big, a = K.cu(C.duke, 0.3, APT, 650.0, 330.0, 1.35, 22.0, head=(400, 1000), light=K.light_apt, blur=4, extra_fx=fx_,
              expr='roar', mouth_=1.0, flop=1.0, look=(0.9, 0.4), hand_n=(24.0, 34.0))
tk = K.ticket_ui(0.0, 'price', price=649, w=560, h=760)
tk = np.array(Image.fromarray(tk).resize((int(tk.shape[1] * 0.62), int(tk.shape[0] * 0.62)), Image.NEAREST))
O.overlay(big, tk, 1080 - tk.shape[1] - 24, 1000, 1.0)
K.cover_make(big, ['$600 NOSEBLEEDS?!'], n=5, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=58)
print('cover.png')
