
import base64
import os
import re

base_dir = '/home/lando/Documentos/cvdr/cedula/cedula2'
index_path = os.path.join(base_dir, 'index.html')
ipn_path = os.path.join(base_dir, 'logo_ipn.png')
cvdr_path = os.path.join(base_dir, 'logo_cvdr.jpg')

def image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

try:
    print("Reading images...")
    ipn_b64 = image_to_base64(ipn_path)
    cvdr_b64 = image_to_base64(cvdr_path)
    
    print("Reading index.html...")
    with open(index_path, 'r') as f:
        html_content = f.read()
    
    # Construct IMG tags with styling
    ipn_img = f'<img src="data:image/png;base64,{ipn_b64}" alt="IPN" class="logo-img" style="height: 48px; width: auto;">'
    cvdr_img = f'<img src="data:image/jpeg;base64,{cvdr_b64}" alt="CVDR" class="logo-img" style="height: 48px; width: auto; border-radius: 4px;">'
    
    # New Header HTML
    new_header = f'''    <header class="app-header">
      <div class="header-logos">
        {ipn_img}
      </div>
      
      <div class="header-title-block">
        <div class="header-title">Cédula de evaluación estructural ocular</div>
        <div class="header-subtitle">Centro de Vinculación y Desarrollo Regional Unidad Oaxaca</div>
      </div>
      
      <div class="header-logos">
        {cvdr_img}
      </div>
    </header>'''

    # Pattern to find the OLD header. 
    # capturing the content including <header class="app-header"> ... </header>
    # The old header has "app-header-left" and "chip-live"
    pattern = r'<header class="app-header">\s*<div class="app-header-left">[\s\S]*?<\/header>'
    
    print("Searching for old header...")
    match = re.search(pattern, html_content)
    
    if match:
        print("Found old header. Replacing...")
        html_content = html_content.replace(match.group(0), new_header)
        
        print("Writing index.html...")
        with open(index_path, 'w') as f:
            f.write(html_content)
        print("Success!")
    else:
        # Check if maybe it's already the new header but with placeholders?
        if '<!-- LOGO_IPN_PLACEHOLDER -->' in html_content:
             print("Found placeholders. Replacing...")
             html_content = html_content.replace('<!-- LOGO_IPN_PLACEHOLDER -->', ipn_img)
             html_content = html_content.replace('<!-- LOGO_CVDR_PLACEHOLDER -->', cvdr_img)
             with open(index_path, 'w') as f:
                f.write(html_content)
             print("Success (Placeholders referenced)!")
        else:
            print("Error: Could not find old header pattern OR placeholders.")
            # Print a snippet to debug
            start_idx = html_content.find('<header class="app-header">')
            if start_idx != -1:
                print(f"Header content found: {html_content[start_idx:start_idx+200]}...")

except Exception as e:
    print(f"Error: {e}")
