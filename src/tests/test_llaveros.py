from routes import llaveros

def test_get_prueba(test_app, monkeypatch):
    test_data = {
    "rowid_object": "100011000",
    "cd_tipo_documento": "TIPDOC_FS001",
    "numero_documento": "36080005",
    "cd_fuente": "CXREF",
    "cd_tipo_producto": "S",
    "numero_producto": "3030303030",
    "cd_relacion_producto": "T",
    "cd_tipo_plan": "2022-01-01",
    "fecha_inicio_relacion": "2022-01-01",
    "fecha_fin_relacion": "2022-01-01",
    "cd_estado_contrato": "E",
    "cd_estado_homologado": "03",
    "fecha_actualizacion": "2022-01-26",
    "numero_documento_externo": "null"
}

    async def mock_get(rowid_object):
        return test_data

    monkeypatch.setattr(llaveros, "get_prueba", mock_get)

    response = test_app.get("/consulta/relperproductos/rowid_object?rowid_object=100011000")
    assert response.status_code == 200
    
def test_get_prueba_incorrect_rowid(test_app, monkeypatch):
    async def mock_get(rowid_object):
        return None

    monkeypatch.setattr(llaveros, "get_prueba", mock_get)

    response = test_app.get("/consulta/relperproductos/rowid_object?rowid_object=100011000414")
    assert response.status_code == 404

