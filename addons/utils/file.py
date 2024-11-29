import requests
import base64
import cairosvg

def convert_svg_to_png(content):
    return cairosvg.svg2png(bytestring=content.encode('utf-8'))

def convert_url_to_base64(url):
    response = requests.get(url)
    if (response.headers['Content-Type'] == 'image/svg+xml'):
        data = convert_svg_to_png(response.text)
    else:
        data = response.content
    return base64.b64encode(data).decode('utf-8')