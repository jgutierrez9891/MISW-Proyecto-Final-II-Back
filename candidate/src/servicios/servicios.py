
from modelos import candidato, infoTecnica, infoLaboral, db


def SaveCandidate(
        tipo_doc,
        num_doc,
        nombre,
        usuario,
        clave,
        telefono,
        email,
        pais,
        ciudad,
        aspiracion_salarial,
        fecha_nacimiento,
        idiomas,
        ):
    new_Candidate = candidato(
        tipo_doc=tipo_doc,
        num_doc =num_doc,
        nombre = nombre,
        usuario = usuario,
        clave = clave,
        telefono = telefono,
        email = email,
        pais = pais,
        ciudad = ciudad,
        aspiracion_salarial = aspiracion_salarial,
        fecha_nacimiento = fecha_nacimiento,
        idiomas = idiomas
        )
    db.session.add(new_Candidate)
    db.session.commit()
    return new_Candidate

def SaveInfoTecnica(
        tipo,
        valor,
        id_candidato
        ):
    new_infoTecnica = infoTecnica(
        tipo=tipo,
        valor=valor,
        id_candidato=id_candidato
    )
    db.session.add(new_infoTecnica)
    db.session.commit()
    return new_infoTecnica

def save_info_laboral(
        cargo,
        ano_inicio,
        ano_fin,
        empresa,
        descripcion,
        id_candidato
        ):
    new_info_laboral = infoLaboral(
        cargo=cargo,
        ano_inicio=ano_inicio,
        ano_fin=ano_fin,
        empresa=empresa,
        descripcion=descripcion,
        id_candidato=id_candidato
    )
    db.session.add(new_info_laboral)
    db.session.commit()
    return new_info_laboral