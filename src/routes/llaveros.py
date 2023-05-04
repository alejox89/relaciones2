from fastapi import APIRouter, Response, Request
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from models.llavero import datosbasicos, datoscomplem, relperproducto
from schemas.llavero_schema import LlaveroSchema, ContenedorResponse, RelperProductoSchema, rowid, cdtipodocumento, Peticiones
import sqlalchemy as dbc
from sqlalchemy.orm import sessionmaker
from config.db2 import DB
from typing import List, Optional
import logging
from sqlalchemy import text, and_


db = DB.create()
con = db.engine
Session = sessionmaker(bind = con)
session = Session()


llavero = APIRouter()

""" @llavero.get("/llaverito/mdm/")
async def get_llavemdms(llaveMdm : str):
    return con.execute(llaveros.select().where(llaveros.c.llave_mdm == llaveMdm)).first()

@llavero.get("/llaveritos/mdm/")
async def get_llavemdmsc(llaveMdm : str):
    query = dbc.select([llaveros.columns.llave_mdm, llaveros2.columns.id_persona])
    #query = db.select([llaveros, llaveros2].where(llaveros.c.llave_mdm == llaveMdm and llaveros2.c.id_persona == llaveros.c.llave_mdm)).first()
    query = query.select_from(llaveros.join(llaveros2, llaveros.columns.llave_mdm == llaveros2.columns.id_persona))
    return con.execute(query.select().where(llaveros.c.llave_mdm == llaveMdm)).first()

@llavero.get("/llavero/mdm/")
async def get_llavecif(llavecif : str):
    return con.execute(llaveros.select().where(llaveros.c.llave_cif == llavecif)).first()

@llavero.get("/llaveross/mdm/", response_model=LlaveroSchema, status_code=HTTP_200_OK)
async def get_llavemdmsc(llaveMdm : str):
    try:
        result = con.execute(llaveros.select().where(llaveros.c.llave_mdm == llaveMdm and llaveros2.c.id_persona == llaveros.c.llave_mdm)).first()
        if result != None:
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)
    
@llavero.get("/datoss/mdm/", response_model=ContenedorResponse, status_code=HTTP_200_OK)
async def get_llavemdmsc(llaveMdm : str):
    try:
        result = session.query(datosbasicos).join(datoscomplem).where(datosbasicos.c.rowid_object == llaveMdm).first()
        if result != None:
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)
    
@llavero.get("/datosss/mdm/", response_model=ContenedorResponse, status_code=HTTP_200_OK)
async def get_llavemdmsc(llaveMdm : str):
    try:
        with con.connect() as conn:
            query = dbc.select([datosbasicos, datoscomplem])
            #query = db.select([llaveros, llaveros2].where(llaveros.c.llave_mdm == llaveMdm and llaveros2.c.id_persona == llaveros.c.llave_mdm)).first()
            query = query.select_from(datosbasicos.join(datoscomplem, datosbasicos.columns.rowid_object == datoscomplem.columns.id_persona))
            result = conn.execute(query.select().where(datosbasicos.c.rowid_object == llaveMdm)).first()
            if result != None:
                return result
            else:
                return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)



@llavero.get("/datos/mdm/")
async def get_llavemdmsc(llaveMdm : str):
    result = session.query(datosbasicos).join(datoscomplem).where(datosbasicos.c.rowid_object == llaveMdm).first()
    #print(result)
    #query = db.select([datosbasicos, datoscomplem])
    #query = db.select([llaveros, llaveros2].where(llaveros.c.llave_mdm == llaveMdm and llaveros2.c.id_persona == llaveros.c.llave_mdm)).first()
    #query = query.select_from(datosbasicos.join(datoscomplem, datosbasicos.columns.rowid_object == datoscomplem.columns.id_persona))
    return result """

@llavero.get("/consulta/relperproducto/", response_model=RelperProductoSchema, status_code=HTTP_200_OK)
async def get_llavemdmsc(rowid_object : Optional[str]):
    try:
        result = session.query(relperproducto).where(relperproducto.c.rowid_object == rowid_object).first()
        if result != None:
            session.close()
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)
    finally:
        session.close()
        
@llavero.get("/consulta/relperproducto2/", response_model=RelperProductoSchema, status_code=HTTP_200_OK)
async def get_llavemdmsc2(rowid_object : Optional[str]):
    try:
        result = session.query(relperproducto).where(relperproducto.c.rowid_object == rowid_object).first()
        if result != None:
            session.close()
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)
    
@llavero.get("/consulta/relperproducto3/", response_model=RelperProductoSchema, status_code=HTTP_200_OK)
async def get_llavemdmsc1(rowid_object : Optional[str]):
    try:
        result = session.query(relperproducto).where(relperproducto.c.rowid_object == rowid_object).first()
        if result != None:
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)
    
@llavero.get("/consulta/relperproducto/", response_model=List[RelperProductoSchema], status_code=HTTP_200_OK)
async def get_llavemdmsc(cd_tipo_documento : Optional[str], request: Request):
    try:
        result = session.query(relperproducto).where(relperproducto.c.cd_tipo_documento == cd_tipo_documento).all()
        if result != None:
            session.close()
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)
    finally:
        session.close()
    
@llavero.get("/consulta/relperproducto2/", response_model=RelperProductoSchema, status_code=HTTP_200_OK)
async def get_llavemdmsc(request: Request):
    rowid_object = request.query_params['rowid_object']
    print(request.url.query[0])
    try:
        result = session.query(relperproducto).where(relperproducto.c.rowid_object == rowid_object).first()
        if result != None:
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)
    
@llavero.get("/consulta/relperproductos/rowid_object", response_model=RelperProductoSchema, status_code=HTTP_200_OK)
async def get_prueba(rowid_object : str):
    try:
        result = session.query(relperproducto).where(relperproducto.c.rowid_object == rowid_object).first()
        if result != None:
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)

    
@llavero.post("/consulta/relperproductoss/", response_model=RelperProductoSchema, status_code=HTTP_200_OK)
async def get_rowid(request:rowid):
    try:
        result = session.query(relperproducto).where(relperproducto.c.rowid_object == request.rowid_object).first()
        if result != None:
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)
    
@llavero.post("/consulta/relperproductosss/", response_model=RelperProductoSchema, status_code=HTTP_200_OK)
async def get_cd_tipo_documento(request:cdtipodocumento):
    try:
        result = session.query(relperproducto).where(relperproducto.c.cd_tipo_documento == request.cd_tipo_documento).first()
        if result != None:
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)
    
@llavero.post("/consulta/prueba/", response_model=List[RelperProductoSchema], status_code=HTTP_200_OK)
async def post_peticion (request:Peticiones):
    try:
        if request.rowid_object != None:
            result = session.query(relperproducto).where(relperproducto.c.rowid_object == request.rowid_object).all()
            if result == []:
                return Response(status_code=HTTP_404_NOT_FOUND)
            else:
                return result
        elif request.numero_producto != None:
            result = session.query(relperproducto).where(relperproducto.c.numero_producto == request.numero_producto).all()
            if result != None:
                return result
            else:
                return Response(status_code=HTTP_404_NOT_FOUND)
        elif request.cd_tipo_documento != None and request.numero_documento != None:
            result = session.query(relperproducto).where(and_(relperproducto.c.cd_tipo_documento == request.cd_tipo_documento, relperproducto.c.numero_documento == request.numero_documento)).all()
            if result != None:
                return result
            else:
                return Response(status_code=HTTP_404_NOT_FOUND)
        elif request.numero_documento_externo != None:
            result = session.query(relperproducto).where(and_(relperproducto.c.cd_tipo_documento == request.cd_tipo_documento, relperproducto.c.numero_documento == request.numero_documento_externo)).all()
            if result != None:
                return result
            else:
                return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        session.rollback()
        session.close()
        raise Exception(ex)
    

    
@llavero.post("/relacionperproducto/prueba/", response_model=List[RelperProductoSchema], status_code=HTTP_200_OK)
async def get_relperproducto (request:Peticiones, limit:int=30):
    try:
        if request.numero_producto != None:
            print ("EStoy aqui")
            if request.tipo_consulta == "MDM":
                result = session.query(relperproducto).where(and_(relperproducto.c.rowid_object == request.rowid_object, relperproducto.c.numero_producto == request.numero_producto)).limit(limit).all()
                if result == []:
                    return Response(status_code=HTTP_404_NOT_FOUND)
                else:
                    return result
            else:
                result = session.query(relperproducto).where(and_(relperproducto.c.numero_producto == request.numero_producto, relperproducto.c.cd_tipo_documento == request.cd_tipo_documento, relperproducto.c.numero_documento == request.numero_documento)).limit(limit).all()
            if result == []:
                return Response(status_code=HTTP_404_NOT_FOUND)
            else:
                return result
        elif request.tipo_consulta == "MDM":
            result = session.query(relperproducto).where(relperproducto.c.rowid_object == request.rowid_object).all()
            # result = session.query(relperproducto).where(and_(relperproducto.c.rowid_object == request.rowid_object, relperproducto.c.estado_producto == request.es)).all()
            if result == []:
                return Response(status_code=HTTP_404_NOT_FOUND)
            else:
                return result
        else:
            result = session.query(relperproducto).where(and_(relperproducto.c.cd_tipo_documento == request.cd_tipo_documento, relperproducto.c.numero_documento == request.numero_documento)).limit(limit).all()
            if result == []:
                return Response(status_code=HTTP_404_NOT_FOUND)
            else:
                return result
    except Exception as ex:
        session.rollback()
        session.close()
        raise Exception(ex)
    


@llavero.post("/consulta/relperproductosss/", response_model=RelperProductoSchema, status_code=HTTP_200_OK)
async def get_cd_tipo_documento(request:cdtipodocumento):
    try:
        result = session.query(relperproducto).where(relperproducto.c.cd_tipo_documento == request.cd_tipo_documento).first()
        if result != None:
            return result
        else:
            return Response(status_code=HTTP_404_NOT_FOUND)
    except Exception as ex:
        raise Exception(ex)