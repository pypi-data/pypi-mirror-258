
from os import getcwd, path
from nf_consumo.consumo_service import ConsumoService

def test_download_pdf():
    path_dir = path.join(getcwd(), 'output')
    filename = 'Teste faturas dia 22.1.pdf'
    pdf_path = ConsumoService().download_pdf("https://storageged.blob.core.windows.net/sandbox/Teste faturas dia 22.1.pdf", path_dir)
    expected = {
        'path_dir': path_dir,
        'filename': filename,
        'full_path': path.join(path_dir, filename)
    }    
    assert expected == pdf_path
