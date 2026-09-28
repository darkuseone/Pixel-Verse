"""xAI image API (Grok Imagine). Key: XAI_API_KEY (never printed).
Default = grok-imagine-image-2.0, quality=medium, resolution=1k: ~$0.06/image (+$0.01 per input image).
We pixelize everything to a 360-540 px logical canvas anyway, so 2k is wasted money.
  python3 engine/xai.py gen out.png "prompt" [aspect]
"""
import base64, json, os, sys, urllib.request

API = 'https://api.x.ai/v1/images'
MODEL = 'grok-imagine-image-2.0'


def _call(endpoint, body):
    req = urllib.request.Request(f'{API}/{endpoint}', json.dumps(body).encode(),
                                 {'Authorization': 'Bearer ' + os.environ['XAI_API_KEY'], 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=300) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f'xAI HTTP {e.code}: {e.read()[:600]!r}')


def generate(prompt, outs, aspect='16:9', quality='medium', resolution='1k', ref_png=None):
    """outs: list of output paths (n = len(outs)). ref_png -> /edits with that reference image."""
    body = {'model': MODEL, 'prompt': prompt, 'n': len(outs), 'aspect_ratio': aspect,
            'resolution': resolution, 'quality': quality, 'response_format': 'b64_json'}
    if ref_png:
        body['image'] = {'url': 'data:image/png;base64,' + base64.b64encode(open(ref_png, 'rb').read()).decode(), 'type': 'image_url'}
    d = _call('edits' if ref_png else 'generations', body)
    for out, it in zip(outs, d['data']):
        open(out, 'wb').write(base64.b64decode(it['b64_json']))
    usd = d.get('usage', {}).get('cost_in_usd_ticks', 0) / 1e10
    print('xAI:', len(outs), 'image(s), $%.3f' % usd, outs)
    return usd


if __name__ == '__main__':
    if sys.argv[1] == 'gen':
        generate(sys.argv[3], [sys.argv[2]], sys.argv[4] if len(sys.argv) > 4 else '16:9')
