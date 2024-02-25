# -*- coding: utf-8 -*-
from langchain.text_splitter import TokenTextSplitter
from string import Template
import textwrap
import re
import spacy
# Cargar el modelo de lenguaje en español de spaCy

def una_extracion (extract_entities_relationships,fragmentos,graph):
    prompt = Template(prompt_tpl_comp).substitute(ctext=fragmentos)
    response1= extract_entities_relationships(prompt)
    #print(response1)
    cadena=limpiar_tx(response1)
    nueva_cadena=reemplazar_espacios_con_guiones_bajos(cadena)
    (sin_caracter,con_caracter) = listas_entidades_R(nueva_cadena)
    crear_enti_neo(sin_caracter,graph)
    crear_rel_neo(con_caracter,sin_caracter,graph)
    print("Neo4j")

def extracion_completa(extract_entities_relationships,fragmentos,graph):
    contador = 0
    while(contador < len(fragmentos)):
        try:
            prompt = Template(prompt_tpl_comp).substitute(ctext=fragmentos[contador])
            response2 = extract_entities_relationships(prompt)
            cadena=limpiar_tx(response2)
            nueva_cadena=reemplazar_espacios_con_guiones_bajos(cadena)
            (sin_caracter,con_caracter) = listas_entidades_R(nueva_cadena) 
            crear_enti_neo(sin_caracter,graph)
            crear_rel_neo(con_caracter,sin_caracter,graph)
            contador += 1
        except Exception as e:
            print(f"Error al ejecutar el comando: {extract_entities_relationships(prompt)}")
            print(f"Mensaje de error: {e}")
    print("Neo4j - completo")

# Extracion de un fragmento enviado.
def extracion_emb(extract_entities_relationships,fragmentos,graph,nlp):
    prompt = Template(prompt_tpl_emb).substitute(ctext=fragmentos)
    response1= extract_entities_relationships(prompt)
    #print(response1)
    cadena=limpiar_tx(response1)
    nueva_cadena=reemplazar_espacios_con_guiones_bajos(cadena)
    sin_caracter,con_caracter = listas_entidades_R(nueva_cadena)
    entidades = crear_entidad_neo2(sin_caracter,graph)
    relaciones_emb(entidades,fragmentos,extract_entities_relationships,graph,nlp)
    print("Neo4j - Emb")
    
prompt_tpl_comp="""From the following text, extract the **Entities** and **Relationships** most relevant for the creation of a knowledge graph.
1. These must be UNIQUE, entities cannot be repeated or duplicated.
2. Take into account if there are several types Generalize and group into a single entity and relate to the other Entities.
    Example: Playa Blaca, Chicamocha Canyon, these can be grouped into a single entity **Tourist Centers**
3. Try to find the **General Entities**
4. The numbers and dates are **NOT Entities** **DO NOT add**.
5. Show results in **Cypher** format the answer must be in Spanish.
6. Example of the Entities format:
    CREATE (NorteDeSantander:Departamento {nombre: 'Norte de Santander'})
    CREATE (Turismo:Industria {nombre: 'Turismo'})
    
7. Example of the Relationships format:
    CREATE ('Norte de Santander')-[:TURISMO_DE_HISTORIA]->('Turismo')
    
8. Entities must have at least one **relationship** with another **Entity**.
     
Question: Now, extract the entities as mentioned above for the text below:-
$ctext
Answer:
"""

prompt_tpl_emb="""From the following text, your task is to extract the most relevant **Entities** by strictly following the instructions provided below:

1. Entities must be unique; no repetitions or duplications are allowed.
2. Numbers and dates are NOT Entities. DO NOT include them in the resulting list.
3. Use the following FORMAT to represent Entities:
    CREATE (NorteDeSantander:Departamento {nombre: 'Norte de Santander'})
    CREATE (Turismo:Industria {nombre: 'Turismo'})
    CREATE (persona1:Persona {nombre: 'Luis Alejandro Mesa Alarcon'})
4. Example of the expected format for an entity:
    CREATE (NorteDeSantander:Department {name: 'Norte de Santander'})
- Make sure your output complies with the specified formatting and guidelines. 
- Pay attention to details and focus extraction on unique and relevant entities.

Question: Now, extract the entities as mentioned above for the text below:-
$ctext
Answer:
"""



def data_txt(url):
    my_file = open(url, 'r', encoding='utf-8', errors='ignore')
    inp_text=my_file.read()
    return(inp_text)

def div_text_tok(inp_text):
    text_splitter = TokenTextSplitter(chunk_size=2048, chunk_overlap=24)
    documents = text_splitter.create_documents([inp_text])
    return(documents)

def dividir_en_fragmentos(texto):
    longitud_fragmento = 12400
    fragmentos = textwrap.wrap(texto, width=longitud_fragmento)
    return fragmentos

def limpiar_tx(response1):
    lineas_create = [linea.strip() for linea in response1.split('\n') if re.search(r'\bCREATE\b', linea)]
    # Unir las líneas filtradas de nuevo en un solo script Cypher
    nuevo_cypher_script = '\n'.join(lineas_create)
    return nuevo_cypher_script

def reemplazar_espacios_con_guiones_bajos(cadena):
    # Utiliza una expresión regular para buscar espacios entre "(" y ":"
    patron = r'\((.*?)\s*:\s*(.*?)\)'
    def reemplazar_espacios(match):
        return f'({match.group(1).replace(" ", "_")}:{match.group(2)})'
    # Aplica la función de reemplazo a la cadena
    nueva_cadena = re.sub(patron, reemplazar_espacios, cadena)
    return nueva_cadena

def listas_entidades_R(nueva_cadena):
    lineas = nueva_cadena.split('\n')

    con_flecha = []
    sin_flecha = []

    for linea in lineas:
        if '->' in linea:
            con_flecha.append(linea)
        else:
            sin_flecha.append(linea)

    return(sin_flecha,con_flecha)

def buscar(nom,lista):
    contador = 0
    while contador < len(lista):
        evaluar=lista[contador]
        nodo1=extraer_nodo_principal(evaluar)
        if (nom == nodo1):
            return lista[contador]
        contador += 1     
    return None
    
def obtener_etiqueta(consulta_cypher):
    match = re.search(r':(\w+)', consulta_cypher)
    if match:
        etiqueta = match.group(1)
        return etiqueta
    else:
        return None
    
def extraer_nombre_entidad(consulta_cypher):
    patron = re.compile(r"'(.*?)'")
    matches = re.search(patron, consulta_cypher)
    if matches:
        nombre = matches.group(1)
        return nombre
    else:
        return None

def extraer_nodo_principal(consulta):
    nodo_principal = re.match(r'CREATE \((\w+)', consulta)
    if nodo_principal:
        return nodo_principal.group(1)
    else:
        return None

def extraer_nodo_secundario(consulta):
    nodo_secundario = re.search(r'->\((\w+)\)', consulta)
    if nodo_secundario:
        return nodo_secundario.group(1)
    else:
        return None
    
def extraer_tipo_relacion(texto):
    contenido_entre_corchetes = re.search(r'\[:([^]]*)\]', texto) 
    if contenido_entre_corchetes:
        contenido_deseado = contenido_entre_corchetes.group(1)
        return contenido_deseado
    else:
        return None
def verificar_relacion_existente(etiqueta_origen, nombre_origen, relacion, etiqueta_destino, nombre_destino,graph):
    consulta = graph.query(f"MATCH (nodoOrigen:{etiqueta_origen} {{nombre: '{nombre_origen}'}})-[:{relacion}]->(nodoDestino:{etiqueta_destino} {{nombre: '{nombre_destino}'}}) RETURN COUNT(*) > 0 AS relacionExistente;")
    return consulta

def ex_etiqueta(consulta):
    patron = re.compile(r'\(\s*([^:]+)\s*:\s*\w+\s*{')
    # Buscar la coincidencia en el dato
    coincidencia = patron.search(consulta)
    # Extraer el contenido entre (: y :)
    if coincidencia:
        contenido_entre_parentesis = coincidencia.group(1)
        return contenido_entre_parentesis

def crear_enti_neo(sin_caracter,graph):
    contador = 0
    while contador < len(sin_caracter):
        evaluar = sin_caracter[contador]
        nombre = extraer_nombre_entidad(evaluar)
        etiqueta = obtener_etiqueta(evaluar)
        consulta = graph.query(f"MATCH (n:{etiqueta} {{nombre: '{nombre}'}}) RETURN COUNT(n) > 0 AS nodoExiste")
        nodo_existe = consulta[0]['nodoExiste']
        if(nodo_existe != True ):
            if(nombre != 'CM&'):
                graph.query(sin_caracter[contador])
        else:
            print()
            #print("Ya existe",nombre)
        contador += 1
        
def crear_rel_neo(con_caracter,sin_caracter,graph):
    contador = 0
    while contador < len(con_caracter):
        evaluar=con_caracter[contador]
        nodo=extraer_nodo_principal(evaluar)
        nodo2=extraer_nodo_secundario(evaluar)
        enco = buscar(nodo,sin_caracter)
        enco2 = buscar(nodo2,sin_caracter)
        if(enco != None and enco2 != None):
            nombre = extraer_nombre_entidad(enco)
            etiqueta = obtener_etiqueta(enco)
            nombre1 = extraer_nombre_entidad(enco2)
            etiqueta1 = obtener_etiqueta(enco2)
            tipo_relacion = extraer_tipo_relacion(evaluar)
            ver_rela = verificar_relacion_existente(etiqueta, nombre, tipo_relacion, etiqueta1, nombre1,graph)
            res_rela = ver_rela[0]['relacionExistente']
            if(res_rela != True):
                enco_mod= enco.replace('CREATE', 'MATCH')
                enco_mod2= enco2.replace('CREATE', 'MATCH')
                consulta_combinada = enco_mod + '\n' + enco_mod2 + '\n' + evaluar
                graph.query(consulta_combinada)
        # sin etiqueta
        contador += 1

def crear_entidad_neo2(sin_caracter,graph):
    contador = 0
    entidades = []
    while contador < len(sin_caracter):
        evaluar = sin_caracter[contador]
        nombre = extraer_nombre_entidad(evaluar)
        etiqueta = obtener_etiqueta(evaluar)
        consulta = graph.query(f"MATCH (n:{etiqueta} {{nombre: '{nombre}'}}) RETURN COUNT(n) > 0 AS nodoExiste")
        nodo_existe = consulta[0]['nodoExiste']
        if(nodo_existe != True ):
            if(nombre != 'CM&'):
                graph.query(sin_caracter[contador])
                entidades.append(sin_caracter[contador])
        else:
            print()
            #print("Ya existe",nombre)
        contador += 1
        
    return entidades

def relaciones_emb(entidades,fragmentos,extract_entities_relationships,graph,nlp):
    contador = 0
    while contador < len(entidades):
        con_crea1 = entidades[contador]
        palabra1 = extraer_nombre_entidad(con_crea1)
        #print(palabra1,"------------------------------------------")
        etiqueta = ex_etiqueta(con_crea1)
        numero = 0
        while numero < len(entidades):
            con_crea2 = entidades[numero]
            etiqueta1 = ex_etiqueta(con_crea2)
            palabra2 = extraer_nombre_entidad(con_crea2)
            #print(etiqueta,etiqueta1)
            if(palabra1 != palabra2):
                nuevo_pront="""From the following text, extract the Relationship of the following words, """+palabra1+"""and """+palabra2+""".Extract the relationship that represents a logical connection between words:
                                1. Use the following FORMAT to represent the relationship between the two words taking into account the logical direction of the relationship:
                                      CREAR (palabra1)-[:TIPO_DE_RELACION]->(palabra2)
                                2. Make sure the relationship you create is meaningful and represents a logical connection between the words.
                                3. Example of the expected format for a relationship:
                                example: in the text it is said that person2 is a friend of person1 so the relationship is:
                                      CREAR (persona2)-[:ES_AMIGO_CERCANO_DE]->(persona1)
                                4. Only present a relationship.

                                Question: Now, extract the entities as mentioned above for the text below:-
                                $ctext
                                Answer:
                                """
                doc = nlp(fragmentos)
                # Encontrar las oraciones que contienen ambas palabras
                oraciones_relacionadas = [
                    oracion.text for oracion in doc.sents
                    if palabra1.lower() in oracion.text.lower() and palabra2.lower() in oracion.text.lower()
                ]
                #print("Presentacion de las relaciones")
                #print(palabra1,palabra2,len(oraciones_relacionadas))
                if(len(oraciones_relacionadas) != 0):
                    try:
                        prompt = Template(nuevo_pront).substitute(ctext=oraciones_relacionadas)
                        response1= extract_entities_relationships(prompt)
                        #print(response1)
                        l_nombres=contenido_entre_parentesis = re.findall(r'\((.*?)\)', response1)
                        nombre1=l_nombres[0]
                        nombre2=l_nombres[1]
                        #print(nombre1,"--",nombre2)
                        tipo_relacion=extraer_tipo_relacion(response1)
                        #print(tipo_relacion)
                        #print("Etiquetas---",etiqueta,etiqueta1)
                        ver_rela = verificar_relacion_existente(etiqueta, nombre1, tipo_relacion, etiqueta1, nombre2,graph)
                        res_rela = ver_rela[0]['relacionExistente']
                        if(palabra1 == nombre1 and palabra2 == nombre2):
                            if(res_rela != True):
                                con_creamod1= con_crea1.replace('CREATE', 'MATCH')
                                con_creamod2= con_crea2.replace('CREATE', 'MATCH')
                                crear_rela = f"CREATE ({etiqueta})-[:{tipo_relacion}]->({etiqueta1})"
                                consulta_combinada = con_creamod1 + '\n' + con_creamod2 + '\n' + crear_rela
                                graph.query(consulta_combinada)
                    except Exception as e:
                        # Manejo de la excepción específica del segundo bucle
                        print(f"Error al ejecutar el comando: {extract_entities_relationships(prompt)}")
                        print(f"Mensaje de error: {e}")
                        numero -=1
            numero +=1
        contador += 1

