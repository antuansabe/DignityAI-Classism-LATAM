#!/usr/bin/env python3
"""
DignityAI-Clasismo-LATAM Dataset Generator

Genera 30,000 ejemplos de discriminación clasista usando templates + combinatoria
Parte de la iniciativa DignityAI - Protecting human dignity through AI

Author: Antonio Dromundo
Date: 2025
"""

import random
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import hashlib

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

TOTAL_EJEMPLOS = 30000
PAISES = ["México", "Argentina", "Colombia", "Chile", "España"]
EJEMPLOS_POR_PAIS = TOTAL_EJEMPLOS // len(PAISES)  # 6,000 por país

# ============================================================================
# CATEGORÍAS Y PESOS
# ============================================================================

CATEGORIAS = {
    "deshumanizacion_directa": {
        "peso": 0.20,
        "subcategorias": ["insultos_pobreza", "ataques_apariencia", "vocabulario_deshumanizante"]
    },
    "estereotipos_prejuicios": {
        "peso": 0.20,
        "subcategorias": ["asociar_pobreza_crimen", "prejuicios_capacidades", "estereotipos_habitos"]
    },
    "exclusion_normalizada": {
        "peso": 0.15,
        "subcategorias": ["segregacion_espacial", "exclusion_servicios", "barreras_clasistas"]
    },
    "clasismo_aspiracional": {
        "peso": 0.15,
        "subcategorias": ["desprecio_origenes", "adoracion_estatus", "meritocracia_toxica"]
    },
    "microagresiones_cotidianas": {
        "peso": 0.15,
        "subcategorias": ["diminutivos_condescendientes", "sorpresa_competencia", "invisibilizacion"]
    },
    "violencia_simbolica": {
        "peso": 0.15,
        "subcategorias": ["lenguaje_institucional", "medios_comunicacion", "discurso_corporativo"]
    }
}

# ============================================================================
# MODISMOS POR PAÍS
# ============================================================================

MODISMOS_CLASISMO = {
    "México": {
        "insultos_clase_baja": ["naco", "prole", "gato", "muerto de hambre", "narizón", "indio", "prieto", "pelagatos", "pelado", "arrabalero"],
        "insultos_apariencia": ["pinche", "jodido", "harapiento", "mugroso", "corriente"],
        "conectores": ["wey", "güey", "pinche", "no mames", "chale", "órale", "neta", "a huevo"],
        "zonas_pobres": ["Tepito", "Neza", "Ecatepec", "barrio bravo", "la periferia", "el cerro", "la vecindad"],
        "zonas_ricas": ["Polanco", "Santa Fe", "Lomas", "las Lomas", "zona rosa", "barrio bien", "las Águilas"],
        "diminutivos": ["pobrecito", "mi trabajadora", "la muchacha", "el chavo", "tu empleada"]
    },
    "Argentina": {
        "insultos_clase_baja": ["negro", "villero", "cabeza", "groncho", "turro", "negro de mierda", "planero", "cabecita negra"],
        "insultos_apariencia": ["mugriento", "roñoso", "sucio", "negro villero"],
        "conectores": ["boludo", "che", "la concha de tu madre", "pelotudo", "gil", "salame", "tarado"],
        "zonas_pobres": ["la villa", "el conurbano", "La Matanza", "villa miseria", "la 1-11-14", "fuerte apache"],
        "zonas_ricas": ["Palermo", "Recoleta", "Belgrano", "Barrio Norte", "Puerto Madero", "Nordelta"],
        "diminutivos": ["negrito", "el pibe", "la piba", "el pendejo"]
    },
    "Colombia": {
        "insultos_clase_baja": ["gamín", "ñero", "desechable", "rolo pobre", "cachaco pobre", "mechudo", "destechado", "indigente"],
        "insultos_apariencia": ["mugroso", "zarrapastroso", "mechudo", "sucio"],
        "conectores": ["parce", "gonorrea", "malparido", "hijueputa", "marica", "parcero", "llave"],
        "zonas_pobres": ["Ciudad Bolívar", "Soacha", "el Bronx", "Altos de Cazucá", "la comuna", "barrio popular"],
        "zonas_ricas": ["Rosales", "Chicó", "El Poblado", "Santa Ana", "zona norte", "estrato 6"],
        "diminutivos": ["mijito", "mija", "el trabajador", "la empleada"]
    },
    "Chile": {
        "insultos_clase_baja": ["roto", "flaite", "ordinario", "rasca", "pelusón", "pelmazo", "cuico pobre", "siútico"],
        "insultos_apariencia": ["flaite", "rasca", "chanta", "cutre"],
        "conectores": ["weon", "conchetumare", "perkin", "culiao", "aweonao", "saco de weas"],
        "zonas_pobres": ["La Pincoya", "Cerro Navia", "Puente Alto", "población", "la pobla", "campamento"],
        "zonas_ricas": ["Las Condes", "Vitacura", "Providencia", "Lo Barnechea", "barrio alto", "sector oriente"],
        "diminutivos": ["mijito", "cabro", "el nochero", "la nana"]
    },
    "España": {
        "insultos_clase_baja": ["chusma", "muerto de hambre", "hortera", "cutre", "cani", "chaval", "pobre diablo", "mindundi"],
        "insultos_apariencia": ["zarrapastroso", "cutre", "hortera", "ordinario"],
        "conectores": ["joder", "hostia", "coño", "tío", "tía", "colega", "macho", "tronco"],
        "zonas_pobres": ["Cañada Real", "Vallecas", "barrio obrero", "las 3000 viviendas", "barrio marginal", "extrarradio"],
        "zonas_ricas": ["Salamanca", "Chamartín", "Pozuelo", "Majadahuana", "barrio alto", "zona norte"],
        "diminutivos": ["el chico", "la chica", "el empleado", "la asistenta"]
    }
}

# ============================================================================
# TEMPLATES COMPLETOS POR SUBCATEGORÍA
# ============================================================================

TEMPLATES = {
    "deshumanizacion_directa": {
        "insultos_pobreza": {
            "clasista": [
                "Pinche {insulto_pobreza}, vete a {lugar_despectivo}",
                "{insulto_pobreza} de mierda, no tienes ni para {recurso_basico}",
                "Largo de aquí, {insulto_pobreza}, este lugar no es para ti",
                "{insulto_pobreza}, mejor vete a {zona_pobre}",
                "Qué hace este {insulto_pobreza} aquí en {zona_rica}",
                "No dejan entrar a {insulto_pobreza} como tú",
                "{insulto_pobreza}, te falta {recurso_status}",
                "Eres un {insulto_pobreza}, siempre {estereotipo_negativo}",
                "Este {insulto_pobreza} no tiene ni {posesion_basica}",
                "{conector}, {insulto_pobreza}, no molestes aquí",
                "Qué hace un {insulto_pobreza} en este lugar",
                "Vete de aquí {insulto_pobreza}, hueles a {lugar_despectivo}",
                "{insulto_pobreza}, no perteneces a {zona_rica}",
                "Otro {insulto_pobreza} más pidiendo {recurso_basico}"
            ],
            "inclusivo": [
                "Todos merecemos {valor_humano} sin importar nuestra situación económica",
                "Respeto tu situación, {expresion_empatia}",
                "La dignidad no se mide por {recurso_material}",
                "Cada persona tiene valor independientemente de {factor_economico}",
                "Tu situación económica no define {cualidad_humana}",
                "Todos tenemos derecho a {derecho_basico}",
                "El respeto no depende de {indicador_economico}",
                "Valoro a las personas por {cualidad_personal}, no por su dinero",
                "La pobreza no es {caracteristica_personal}",
                "Todos enfrentamos {situacion_dificil} en algún momento"
            ],
            "variables": {
                "insulto_pobreza": ["muerto de hambre", "limosnero", "pordiosero", "mendigo", "indigente", "pelagatos", "pelado"],
                "lugar_despectivo": ["tu rancho", "la calle", "tu barrio", "tu favela", "de donde saliste", "tu agujero"],
                "recurso_basico": ["comer", "vestirte", "pagar", "comprar nada", "vivir bien", "mantener a tu familia"],
                "recurso_status": ["educación", "clase", "estilo", "nivel", "cultura", "fineza"],
                "estereotipo_negativo": ["mendigando", "robando", "sin hacer nada", "viviendo del estado", "esperando ayuda"],
                "posesion_basica": ["dinero", "trabajo", "casa", "auto", "ropa decente", "zapatos buenos"],
                "valor_humano": ["dignidad", "respeto", "oportunidades", "trato justo"],
                "expresion_empatia": ["eres valioso", "mereces respeto", "todos tenemos luchas", "entiendo las dificultades"],
                "recurso_material": ["lo que tienes", "tu cuenta bancaria", "posesiones", "bienes materiales"],
                "factor_economico": ["tu ingreso", "de dónde vienes", "tu trabajo", "tu situación actual"],
                "cualidad_humana": ["tu valor", "quién eres", "tu inteligencia", "tus capacidades"],
                "derecho_basico": ["ser tratados con dignidad", "acceder a servicios", "espacios públicos", "oportunidades"],
                "indicador_economico": ["cuánto ganas", "dónde vives", "qué tienes", "tu nivel socioeconómico"],
                "cualidad_personal": ["su carácter", "sus acciones", "su esfuerzo", "su humanidad"],
                "caracteristica_personal": ["una elección", "falta de esfuerzo", "tu culpa", "tu decisión"],
                "situacion_dificil": ["dificultades económicas", "momentos difíciles", "escasez", "problemas financieros"]
            }
        },

        "ataques_apariencia": {
            "clasista": [
                "Qué {insulto_apariencia}, {observacion_negativa}",
                "Vístete mejor, pareces {insulto_apariencia}",
                "Con esa pinta de {insulto_apariencia} no puedes entrar",
                "{insulto_apariencia}, te ves como {comparacion_despectiva}",
                "Esa ropa de {insulto_apariencia} no es apropiada",
                "Qué {insulto_apariencia}, {conector}, cámbiate",
                "Pareces {comparacion_despectiva} con esa ropa",
                "Demasiado {insulto_apariencia} para estar aquí",
                "Tu aspecto {insulto_apariencia} {consecuencia_negativa}",
                "No te acerques, estás {insulto_apariencia}",
                "Con esa facha de {insulto_apariencia} mejor vete",
                "Qué pinta tan {insulto_apariencia}, da vergüenza",
                "Pareces salido de {zona_pobre} con esa ropa"
            ],
            "inclusivo": [
                "La apariencia no define {cualidad}",
                "Todos tenemos derecho a {accion} sin importar nuestra vestimenta",
                "Tu valor no está en {aspecto_externo}",
                "Respeto a todas las personas independientemente de {factor_externo}",
                "La ropa no determina {caracteristica_interna}",
                "Cada quien {accion_personal} como puede",
                "No juzgo a nadie por {aspecto_superficial}",
                "Lo importante es {valor_interno}, no {aspecto_externo}",
                "Todos merecemos respeto sin importar {factor_apariencia}",
                "Tu {aspecto_externo} no cambia tu derecho a {derecho}"
            ],
            "variables": {
                "insulto_apariencia": ["mugroso", "harapiento", "sucio", "corriente", "zarrapastroso", "desaliñado", "cutre"],
                "observacion_negativa": ["no puedes estar aquí", "da mala imagen", "espantas a la clientela", "baja el nivel"],
                "comparacion_despectiva": ["un mendigo", "alguien de la calle", "un indigente", "alguien sin hogar", "gente de barrio bajo"],
                "consecuencia_negativa": ["molesta", "incomoda", "no es bienvenido", "genera quejas"],
                "cualidad": ["tu valor", "quién eres", "tu dignidad", "tus capacidades"],
                "accion": ["estar aquí", "acceder a servicios", "ser respetados", "participar"],
                "aspecto_externo": ["tu ropa", "cómo te ves", "tu apariencia", "lo que vistes"],
                "factor_externo": ["cómo se visten", "su apariencia", "su ropa", "cómo lucen"],
                "caracteristica_interna": ["tu valor", "tus capacidades", "tu carácter", "quién eres"],
                "accion_personal": ["se viste", "se presenta", "se arregla", "se cuida"],
                "aspecto_superficial": ["la apariencia", "la ropa", "el aspecto", "cómo lucen"],
                "valor_interno": ["la persona", "el carácter", "la humanidad", "el respeto"],
                "factor_apariencia": ["cómo nos vemos", "nuestra vestimenta", "nuestro aspecto", "cómo lucimos"],
                "derecho": ["dignidad", "respeto", "acceso", "participación"]
            }
        },

        "vocabulario_deshumanizante": {
            "clasista": [
                "Esta {insulto_deshumanizante} no debería estar aquí",
                "Qué hace esta {insulto_deshumanizante} en {zona_rica}",
                "La {insulto_deshumanizante} siempre {estereotipo_negativo}",
                "{conector}, mira esa {insulto_deshumanizante}",
                "No quiero {insulto_deshumanizante} cerca de mi {posesion}",
                "Esta {insulto_deshumanizante} contamina el lugar",
                "Hay que sacar a esta {insulto_deshumanizante}",
                "La {insulto_deshumanizante} viene a {accion_despectiva}",
                "Pura {insulto_deshumanizante} en {zona_pobre}",
                "No tolero {insulto_deshumanizante} aquí",
                "Esa {insulto_deshumanizante} apesta a {caracteristica_negativa}",
                "Mira toda esa {insulto_deshumanizante} junta"
            ],
            "inclusivo": [
                "Todas las personas merecen {derecho_fundamental}",
                "No uso lenguaje que {accion_negativa}",
                "Respeto la {cualidad_humana} de cada persona",
                "El lenguaje deshumanizante {efecto_negativo}",
                "Todas las personas tienen {valor_inherente}",
                "No juzgo a nadie por {factor_externo}",
                "La dignidad es {caracteristica_universal}",
                "Cada persona merece {trato_justo}",
                "No acepto lenguaje que {efecto_danino}",
                "Todas las vidas tienen {valor_igual}"
            ],
            "variables": {
                "insulto_deshumanizante": ["plebe", "gentuza", "escoria", "lacra", "chusma", "ralea", "calaña"],
                "estereotipo_negativo": ["roba", "mendiga", "ensucia", "molesta", "causa problemas"],
                "posesion": ["casa", "negocio", "familia", "barrio", "zona"],
                "accion_despectiva": ["robar", "mendigar", "pedir", "molestar", "ensuciar"],
                "caracteristica_negativa": ["pobreza", "miseria", "hambre", "necesidad"],
                "derecho_fundamental": ["dignidad", "respeto", "oportunidades", "trato justo"],
                "accion_negativa": ["deshumaniza", "degrada", "ofende", "discrimina"],
                "cualidad_humana": ["humanidad", "dignidad", "valor", "integridad"],
                "efecto_negativo": ["daña", "hiere", "discrimina", "margina"],
                "valor_inherente": ["dignidad inherente", "valor como personas", "derechos humanos", "humanidad"],
                "factor_externo": ["su origen", "su situación", "su apariencia", "su economía"],
                "caracteristica_universal": ["universal", "innegable", "inalienable", "fundamental"],
                "trato_justo": ["respeto", "consideración", "empatía", "justicia"],
                "efecto_danino": ["degrada", "deshumaniza", "margina", "excluye"],
                "valor_igual": ["el mismo valor", "igual dignidad", "igual importancia", "igual derecho"]
            }
        }
    },

    "estereotipos_prejuicios": {
        "asociar_pobreza_crimen": {
            "clasista": [
                "Los de {zona_pobre} son todos {estereotipo_criminal}",
                "Cuidado con esa gente de {zona_pobre}, todos {actividad_criminal}",
                "Los pobres siempre están {actividad_criminal}",
                "Ese viene de {zona_pobre}, seguro {accion_criminal}",
                "No confíes en alguien de {zona_pobre}, son {estereotipo_criminal}",
                "{conector}, los de {zona_pobre} solo saben {actividad_criminal}",
                "Toda esa gente pobre es {estereotipo_criminal}",
                "Si es de {zona_pobre} debe ser {estereotipo_criminal}",
                "Los pobres son {estereotipo_criminal} por naturaleza",
                "Vigila tus cosas, hay gente de {zona_pobre} aquí",
                "Los {insulto_clase_baja} siempre {actividad_criminal}",
                "Con razón {actividad_criminal}, viene de {zona_pobre}"
            ],
            "inclusivo": [
                "La pobreza no causa {fenomeno_social}",
                "No existe relación entre {factor_economico} y {comportamiento}",
                "Los estereotipos sobre {grupo_social} son {caracteristica_negativa}",
                "La criminalidad tiene {causas_complejas}, no solo pobreza",
                "Juzgo a las personas por {criterio_justo}, no por su origen",
                "Los prejuicios sobre {grupo_vulnerable} son {efecto_negativo}",
                "No asocio {condicion_economica} con {comportamiento_negativo}",
                "Cada persona es {caracteristica_individual}",
                "Los estereotipos {efecto_danino}",
                "La situación económica no determina {caracteristica_moral}"
            ],
            "variables": {
                "estereotipo_criminal": ["ladrones", "criminales", "rateros", "delincuentes", "malandros"],
                "actividad_criminal": ["roban", "asaltan", "hurtan", "afanan", "delinquen"],
                "accion_criminal": ["te va a robar", "viene a robar", "anda en malos pasos", "está en algo turbio"],
                "fenomeno_social": ["criminalidad", "delincuencia", "violencia", "inseguridad"],
                "factor_economico": ["nivel socioeconómico", "situación económica", "pobreza", "falta de recursos"],
                "comportamiento": ["criminalidad", "delincuencia", "honestidad", "moralidad"],
                "grupo_social": ["personas de bajos recursos", "barrios populares", "comunidades vulnerables", "sectores pobres"],
                "caracteristica_negativa": ["injustos", "dañinos", "falsos", "discriminatorios"],
                "causas_complejas": ["causas multifactoriales", "raíces estructurales", "múltiples factores", "orígenes diversos"],
                "criterio_justo": ["sus acciones", "su carácter", "su comportamiento", "quiénes son"],
                "grupo_vulnerable": ["personas pobres", "barrios humildes", "comunidades vulnerables", "sectores populares"],
                "efecto_negativo": ["injustos", "dañinos", "discriminatorios", "estigmatizantes"],
                "condicion_economica": ["pobreza", "falta de recursos", "situación económica", "nivel socioeconómico"],
                "comportamiento_negativo": ["criminalidad", "deshonestidad", "violencia", "delincuencia"],
                "caracteristica_individual": ["única", "individual", "diferente", "singular"],
                "efecto_danino": ["discriminan", "estigmatizan", "marginan", "dañan"],
                "caracteristica_moral": ["honestidad", "moralidad", "integridad", "carácter"]
            }
        },

        "prejuicios_capacidades": {
            "clasista": [
                "Los pobres no {capacidad_intelectual}",
                "Esa gente de {zona_pobre} es muy {insulto_inteligencia}",
                "No {capacidad_intelectual} porque son pobres",
                "Los {insulto_clase_baja} son muy {insulto_inteligencia} para {tarea_compleja}",
                "Qué vas a {capacidad_intelectual} si eres {insulto_clase_baja}",
                "Los de {zona_pobre} no tienen {cualidad_cognitiva}",
                "{conector}, esa gente no {capacidad_intelectual}",
                "Pobre y {insulto_inteligencia} van de la mano",
                "No esperaba que {capacidad_intelectual} siendo de {zona_pobre}",
                "Los pobres no sirven para {actividad_intelectual}",
                "Son {insulto_inteligencia}, por eso son pobres",
                "No tienen la {cualidad_cognitiva} para {tarea_compleja}"
            ],
            "inclusivo": [
                "La inteligencia no se relaciona con {factor_economico}",
                "Todas las personas tienen {capacidad_humana}",
                "Las capacidades no dependen de {condicion_economica}",
                "Respeto la {cualidad_cognitiva} de todas las personas",
                "El potencial humano no se mide por {indicador_economico}",
                "Cada persona tiene {talento_unico}",
                "Las circunstancias económicas no determinan {capacidad_mental}",
                "Valoro {criterio_justo}, no su origen socioeconómico",
                "La pobreza no es falta de {cualidad_positiva}",
                "Todos tenemos {derecho_desarrollo}"
            ],
            "variables": {
                "capacidad_intelectual": ["entienden", "comprenden", "saben", "aprenden", "razonan"],
                "insulto_inteligencia": ["ignorantes", "brutos", "tontos", "burros", "incultos"],
                "tarea_compleja": ["estudiar", "aprender", "trabajar bien", "progresar", "superarse"],
                "cualidad_cognitiva": ["educación", "inteligencia", "capacidad", "conocimiento", "cultura"],
                "actividad_intelectual": ["estudiar", "pensar", "analizar", "aprender", "comprender"],
                "factor_economico": ["nivel socioeconómico", "situación económica", "recursos materiales", "posición social"],
                "capacidad_humana": ["potencial", "inteligencia", "capacidades", "talento", "habilidades"],
                "condicion_economica": ["situación económica", "recursos materiales", "nivel socioeconómico", "posición social"],
                "indicador_economico": ["dinero", "posesiones", "recursos", "estatus social"],
                "talento_unico": ["habilidades únicas", "talentos propios", "capacidades especiales", "potencial individual"],
                "capacidad_mental": ["inteligencia", "capacidades cognitivas", "potencial intelectual", "habilidades mentales"],
                "criterio_justo": ["sus capacidades", "su esfuerzo", "su potencial", "sus logros"],
                "cualidad_positiva": ["inteligencia", "capacidad", "potencial", "talento"],
                "derecho_desarrollo": ["derecho a desarrollarnos", "potencial de crecimiento", "oportunidades de aprender", "capacidad de progresar"]
            }
        },

        "estereotipos_habitos": {
            "clasista": [
                "Los pobres son {estereotipo_pereza}",
                "Por eso son pobres, porque son {estereotipo_pereza}",
                "No quieren {actividad_productiva}, solo {actividad_negativa}",
                "Los {insulto_clase_baja} no {habito_positivo}",
                "Son pobres porque no {habito_positivo}",
                "Toda esa gente {estereotipo_pereza}, por eso están así",
                "Prefieren {actividad_negativa} a {actividad_productiva}",
                "{conector}, los pobres son {estereotipo_pereza}",
                "Viven del {dependencia_estado} porque no {habito_positivo}",
                "Son {estereotipo_pereza}, esperan que todo se los den",
                "Los de {zona_pobre} solo {actividad_negativa}",
                "No {actividad_productiva} porque son {estereotipo_pereza}"
            ],
            "inclusivo": [
                "La pobreza tiene {causas_estructurales}",
                "No juzgo los hábitos sin conocer {contexto_personal}",
                "Las circunstancias económicas tienen {factores_multiples}",
                "La pobreza no es resultado de {caracteristica_personal}",
                "Muchas personas {esfuerzo_real} pero enfrentan {obstaculos_sistemicos}",
                "Los estereotipos sobre {habitos_laborales} son {caracteristica_falsa}",
                "La situación económica depende de {factores_complejos}",
                "Respeto que cada persona {situacion_unica}",
                "No culpo a las personas por {condiciones_sistemicas}",
                "El trabajo duro no siempre garantiza {movilidad_social}"
            ],
            "variables": {
                "estereotipo_pereza": ["flojos", "huevones", "vagos", "perezosos", "mantenidos"],
                "actividad_productiva": ["trabajar", "esforzarse", "progresar", "superarse", "estudiar"],
                "actividad_negativa": ["pedir ayuda", "vivir del estado", "esperar limosnas", "no hacer nada", "ser mantenidos"],
                "habito_positivo": ["trabajan", "se esfuerzan", "quieren superarse", "buscan progresar", "se sacrifican"],
                "dependencia_estado": ["estado", "gobierno", "subsidios", "ayudas", "programas sociales"],
                "causas_estructurales": ["causas sistémicas", "raíces estructurales", "factores sociales complejos", "desigualdad estructural"],
                "contexto_personal": ["su situación", "sus circunstancias", "su contexto", "su realidad"],
                "factores_multiples": ["múltiples causas", "orígenes diversos", "raíces complejas", "diversos factores"],
                "caracteristica_personal": ["pereza", "falta de esfuerzo", "elección personal", "decisión individual"],
                "esfuerzo_real": ["trabajan duramente", "se esfuerzan mucho", "luchan diariamente", "trabajan incansablemente"],
                "obstaculos_sistemicos": ["barreras estructurales", "desigualdad sistémica", "falta de oportunidades", "discriminación institucional"],
                "habitos_laborales": ["hábitos de trabajo", "ética laboral", "actitud hacia el trabajo", "disposición laboral"],
                "caracteristica_falsa": ["falsos", "injustos", "infundados", "sin base real"],
                "factores_complejos": ["múltiples factores", "causas diversas", "circunstancias complejas", "elementos variados"],
                "situacion_unica": ["tiene su propia historia", "enfrenta circunstancias únicas", "vive su realidad", "tiene su contexto"],
                "condiciones_sistemicas": ["estructuras injustas", "sistemas desiguales", "barreras sistémicas", "desigualdad estructural"],
                "movilidad_social": ["éxito económico", "progreso social", "salir de la pobreza", "mejora económica"]
            }
        }
    },

    "exclusion_normalizada": {
        "segregacion_espacial": {
            "clasista": [
                "Este lugar no es para {grupo_excluido}",
                "Aquí solo entra gente de {zona_rica}",
                "Los de {zona_pobre} no pueden estar aquí",
                "Este es un lugar {adjetivo_exclusivo}, no para {insulto_clase_baja}",
                "No queremos {grupo_excluido} en {espacio_exclusivo}",
                "{conector}, esto es solo para {grupo_privilegiado}",
                "Los {insulto_clase_baja} que se queden en {zona_pobre}",
                "Aquí no aceptamos gente de {zona_pobre}",
                "Este {espacio_exclusivo} es solo para {grupo_privilegiado}",
                "Que vayan a {zona_pobre}, aquí no los queremos",
                "Esto no es {zona_pobre}, largo de aquí",
                "En {zona_rica} no queremos {grupo_excluido}"
            ],
            "inclusivo": [
                "Los espacios públicos son para {principio_universal}",
                "No excluyo a nadie por {factor_discriminatorio}",
                "Todos tienen derecho a {acceso_espacios}",
                "La segregación espacial es {caracteristica_negativa}",
                "Los lugares deben ser {caracteristica_inclusiva}",
                "No apoyo {practica_excluyente}",
                "Cada persona merece {derecho_espacial}",
                "Los espacios no deben {accion_discriminatoria}",
                "La inclusión espacial es {valor_positivo}",
                "Todos merecemos {derecho_ciudad}"
            ],
            "variables": {
                "grupo_excluido": ["pobres", "gente sin dinero", "gente corriente", "gente humilde", "trabajadores"],
                "adjetivo_exclusivo": ["exclusivo", "fino", "elegante", "de clase", "de nivel"],
                "espacio_exclusivo": ["restaurante", "club", "centro comercial", "barrio", "edificio"],
                "grupo_privilegiado": ["gente bien", "gente de dinero", "personas de clase", "gente educada", "socios"],
                "principio_universal": ["todas las personas", "toda la comunidad", "todos sin excepción", "la ciudadanía completa"],
                "factor_discriminatorio": ["su nivel económico", "su origen", "su apariencia", "su situación social"],
                "acceso_espacios": ["acceder a espacios públicos", "estar en cualquier lugar", "usar instalaciones", "ocupar espacios"],
                "caracteristica_negativa": ["injusta", "discriminatoria", "inaceptable", "violatoria de derechos"],
                "caracteristica_inclusiva": ["accesibles para todos", "inclusivos", "abiertos", "sin discriminación"],
                "practica_excluyente": ["la exclusión espacial", "segregar por clase", "prohibir el acceso", "discriminar territorialmente"],
                "derecho_espacial": ["acceso a espacios", "presencia en lugares públicos", "uso del espacio urbano", "libertad de tránsito"],
                "accion_discriminatoria": ["segregar", "excluir", "discriminar", "marginar"],
                "valor_positivo": ["un derecho", "fundamental", "necesaria", "justa"],
                "derecho_ciudad": ["derecho a la ciudad", "acceso equitativo", "inclusión urbana", "justicia espacial"]
            }
        },

        "exclusion_servicios": {
            "clasista": [
                "Este servicio no es para {grupo_excluido}",
                "No pueden pagar {servicio}, mejor váyanse",
                "Esto es muy {adjetivo_caro} para {insulto_clase_baja}",
                "Los {insulto_clase_baja} no pueden acceder a {servicio}",
                "Este {servicio} es solo para {grupo_privilegiado}",
                "No tienen el {requisito_economico} para {servicio}",
                "{conector}, esto no es para pobres",
                "Váyanse a {alternativa_pobre}, esto es muy caro",
                "Los de {zona_pobre} no pueden pagar {servicio}",
                "Este {servicio} requiere {requisito_economico} que no tienen",
                "Solo atendemos a {grupo_privilegiado}",
                "Los pobres no merecen {servicio_calidad}"
            ],
            "inclusivo": [
                "Los servicios deben ser {caracteristica_accesible}",
                "Todos tienen derecho a {acceso_servicios}",
                "No niego servicios por {factor_economico}",
                "La exclusión de servicios es {caracteristica_injusta}",
                "Cada persona merece {acceso_equitativo}",
                "Los servicios básicos son {derecho_universal}",
                "No discrimino en {provision_servicios}",
                "El acceso a {servicios_esenciales} es un derecho",
                "Trabajo por {inclusion_servicios}",
                "Todos merecemos {calidad_servicio}"
            ],
            "variables": {
                "servicio": ["educación privada", "atención médica", "este restaurante", "este servicio", "estas instalaciones"],
                "adjetivo_caro": ["caro", "costoso", "exclusivo", "premium", "de lujo"],
                "requisito_economico": ["nivel económico", "dinero", "recursos", "poder adquisitivo", "solvencia"],
                "alternativa_pobre": ["lo público", "lo barato", "lo gratuito", "el servicio básico", "lo popular"],
                "servicio_calidad": ["buen servicio", "calidad", "atención premium", "servicios de nivel", "lo mejor"],
                "caracteristica_accesible": ["accesibles", "inclusivos", "para todos", "sin barreras económicas", "equitativos"],
                "acceso_servicios": ["acceder a servicios", "recibir atención", "usar instalaciones", "obtener servicios"],
                "factor_economico": ["situación económica", "nivel de ingresos", "capacidad de pago", "recursos económicos"],
                "caracteristica_injusta": ["injusta", "discriminatoria", "inaceptable", "violatoria"],
                "acceso_equitativo": ["acceso equitativo", "igualdad de servicios", "atención sin discriminación", "servicios justos"],
                "derecho_universal": ["un derecho humano", "universales", "para todos", "inalienables"],
                "provision_servicios": ["la prestación de servicios", "brindar atención", "ofrecer servicios", "dar acceso"],
                "servicios_esenciales": ["servicios básicos", "atención médica", "educación", "servicios fundamentales"],
                "inclusion_servicios": ["servicios inclusivos", "acceso universal", "equidad en servicios", "justicia en el acceso"],
                "calidad_servicio": ["servicios de calidad", "buena atención", "servicios dignos", "atención adecuada"]
            }
        },

        "barreras_clasistas": {
            "clasista": [
                "Aquí hay {barrera_exclusiva}",
                "Solo con {requisito_economico} puedes entrar",
                "Se requiere {barrera_exclusiva} para acceder",
                "Los {insulto_clase_baja} no cumplen con {requisito_economico}",
                "Es política de la casa: solo {grupo_privilegiado}",
                "Necesitas {barrera_exclusiva} o no entras",
                "Sin {requisito_economico} no hay acceso",
                "{conector}, esto es solo para {grupo_privilegiado}",
                "Los de {zona_pobre} no tienen {requisito_economico}",
                "Aquí se exige {barrera_exclusiva}",
                "Si no tienes {requisito_economico}, vete",
                "Este lugar requiere {barrera_exclusiva} estricto"
            ],
            "inclusivo": [
                "Las barreras clasistas son {caracteristica_negativa}",
                "No impongo {barreras_discriminatorias}",
                "Los requisitos deben ser {caracteristica_justa}",
                "No acepto {practicas_excluyentes}",
                "El acceso debe basarse en {criterio_justo}",
                "Las políticas excluyentes {efecto_negativo}",
                "Trabajo por {acceso_equitativo}",
                "No apoyo {barreras_economicas}",
                "Los espacios deben ser {caracteristica_inclusiva}",
                "Todos merecen {oportunidad_acceso}"
            ],
            "variables": {
                "barrera_exclusiva": ["dress code", "membresía exclusiva", "lista VIP", "código de vestimenta", "cuota mínima"],
                "requisito_economico": ["ser socio", "membresía cara", "consumo mínimo", "tarjeta premium", "nivel económico"],
                "grupo_privilegiado": ["socios", "miembros", "VIPs", "gente de clase", "personas selectas"],
                "caracteristica_negativa": ["injustas", "discriminatorias", "inaceptables", "excluyentes"],
                "barreras_discriminatorias": ["barreras por clase", "requisitos excluyentes", "políticas discriminatorias", "filtros económicos"],
                "caracteristica_justa": ["justos", "razonables", "no discriminatorios", "equitativos"],
                "practicas_excluyentes": ["políticas excluyentes", "discriminación sistémica", "barreras artificiales", "filtros clasistas"],
                "criterio_justo": ["criterios objetivos", "necesidad real", "razones válidas", "justificación legítima"],
                "efecto_negativo": ["discriminan", "excluyen", "marginan", "segregan"],
                "acceso_equitativo": ["acceso equitativo", "inclusión", "igualdad de oportunidades", "justicia en el acceso"],
                "barreras_economicas": ["barreras económicas", "exclusión por recursos", "discriminación financiera", "filtros monetarios"],
                "caracteristica_inclusiva": ["inclusivos", "accesibles", "abiertos", "sin barreras"],
                "oportunidad_acceso": ["oportunidad de acceso", "posibilidad de entrar", "acceso equitativo", "inclusión"]
            }
        }
    },

    "clasismo_aspiracional": {
        "desprecio_origenes": {
            "clasista": [
                "Yo no soy como esa {insulto_clase_baja} de {zona_pobre}",
                "Gracias a Dios salí de {zona_pobre}",
                "Ya no soy {insulto_clase_baja}, ahora soy {status_superior}",
                "Me avergüenza venir de {zona_pobre}",
                "Yo ya no me junto con {grupo_origen}",
                "Dejé atrás esa vida de {insulto_clase_baja}",
                "{conector}, yo ya no soy de {zona_pobre}",
                "Mejoré mi clase, ya no soy {insulto_clase_baja}",
                "Nada que ver con {grupo_origen}",
                "Yo soy de {zona_rica} ahora, no de {zona_pobre}",
                "Ya no tengo nada que ver con esa gente de {zona_pobre}",
                "Superé mis orígenes de {zona_pobre}"
            ],
            "inclusivo": [
                "Orgulloso de mis orígenes en {lugar_origen}",
                "No reniego de {mis_raices}",
                "Mis orígenes son parte de {mi_identidad}",
                "Valoro {mi_historia} sin importar de dónde vengo",
                "No hay vergüenza en {origenes_humildes}",
                "Mi pasado en {lugar_origen} me formó",
                "Acepto {toda_mi_historia}",
                "No niego {de_donde_vengo}",
                "Mis raíces son {parte_valiosa} de mí",
                "Honro {mis_origenes} siempre"
            ],
            "variables": {
                "grupo_origen": ["los pobres", "esa gente", "los de mi barrio", "mi familia", "los humildes"],
                "status_superior": ["gente bien", "clase alta", "profesional", "alguien importante", "persona de nivel"],
                "lugar_origen": ["mi barrio", "mi comunidad", "donde crecí", "mi pueblo", "mi familia"],
                "mis_raices": ["mis raíces", "de dónde vengo", "mi origen", "mi historia familiar"],
                "mi_identidad": ["quién soy", "mi identidad", "lo que soy", "mi ser"],
                "mi_historia": ["mi historia", "mi trayectoria", "mi camino", "mi experiencia"],
                "origenes_humildes": ["venir de familia humilde", "orígenes modestos", "raíces sencillas", "comienzos humildes"],
                "toda_mi_historia": ["toda mi historia", "todo mi pasado", "de dónde vengo", "mi trayectoria completa"],
                "de_donde_vengo": ["mis orígenes", "de dónde vengo", "mi procedencia", "mi historia"],
                "parte_valiosa": ["parte importante", "parte valiosa", "elemento fundamental", "aspecto valioso"],
                "mis_origenes": ["mis orígenes", "mis raíces", "mi historia", "de dónde vengo"]
            }
        },

        "adoracion_estatus": {
            "clasista": [
                "La gente de {zona_rica} es {adjetivo_positivo}",
                "Quiero ser como la {grupo_privilegiado}",
                "Los de {zona_rica} son {adjetivo_positivo}",
                "Aspiro a estar con {grupo_privilegiado}",
                "La {grupo_privilegiado} sí que tiene {cualidad_admirada}",
                "{conector}, la gente de {zona_rica} sí vale",
                "Los ricos son {adjetivo_positivo}",
                "Quiero pertenecer a {grupo_privilegiado}",
                "La gente bien de {zona_rica} es superior",
                "Solo {grupo_privilegiado} merece {privilegio}",
                "Los de {zona_rica} nacieron para {destino_superior}",
                "La {grupo_privilegiado} tiene {cualidad_admirada} natural"
            ],
            "inclusivo": [
                "El valor no depende de {factor_economico}",
                "No idolatro {estatus_social}",
                "Todas las personas tienen {valor_igual}",
                "El estatus no define {cualidad_humana}",
                "No juzgo superioridad por {indicador_economico}",
                "Valoro a las personas por {criterio_interno}",
                "El dinero no hace {caracteristica_superior}",
                "Respeto {todas_las_clases} por igual",
                "No hay {jerarquia_humana} por dinero",
                "Cada persona tiene {dignidad_igual}"
            ],
            "variables": {
                "adjetivo_positivo": ["superior", "mejor", "más culta", "más educada", "de clase"],
                "grupo_privilegiado": ["gente bien", "gente bonita", "de sociedad", "clase alta", "élite"],
                "cualidad_admirada": ["clase", "educación", "cultura", "refinamiento", "nivel"],
                "privilegio": ["respeto", "admiración", "lo mejor", "atención", "privilegios"],
                "destino_superior": ["gobernar", "mandar", "tener poder", "estar arriba", "liderar"],
                "factor_economico": ["nivel económico", "dinero", "posesiones", "estatus social"],
                "estatus_social": ["el estatus", "la clase social", "la posición económica", "el nivel social"],
                "valor_igual": ["igual valor", "misma dignidad", "igual importancia", "mismo respeto"],
                "cualidad_humana": ["el valor humano", "la dignidad", "la humanidad", "el carácter"],
                "indicador_economico": ["dinero", "posesiones", "nivel económico", "recursos materiales"],
                "criterio_interno": ["su carácter", "sus valores", "sus acciones", "su humanidad"],
                "caracteristica_superior": ["superior a nadie", "mejor persona", "más valioso", "más digno"],
                "todas_las_clases": ["todas las clases sociales", "personas de todos los niveles", "toda la gente", "todos los estratos"],
                "jerarquia_humana": ["jerarquía de valor humano", "superioridad inherente", "clases de personas", "niveles de dignidad"],
                "dignidad_igual": ["igual dignidad", "mismo valor", "misma humanidad", "igual derecho al respeto"]
            }
        },

        "meritocracia_toxica": {
            "clasista": [
                "Si son pobres es porque {razon_culpabilizante}",
                "Los pobres están así porque {razon_culpabilizante}",
                "Si se esforzaran {resultado_positivo}",
                "Son pobres porque no {accion_positiva}",
                "Yo salí adelante, ellos también pueden si {condicion_esfuerzo}",
                "{conector}, son pobres porque quieren",
                "Si trabajaran duro como yo {resultado_positivo}",
                "La pobreza es {caracteristica_voluntaria}",
                "No progresan porque {razon_culpabilizante}",
                "Todos pueden {resultado_positivo} si se esfuerzan",
                "Los pobres no {accion_positiva}, por eso están así",
                "Es su culpa estar en {zona_pobre}, no se esfuerzan"
            ],
            "inclusivo": [
                "La pobreza tiene {causas_estructurales}",
                "El éxito depende de {factores_multiples}",
                "No todos tienen {mismas_oportunidades}",
                "La meritocracia pura es {caracteristica_falsa}",
                "Existen {barreras_sistemicas} reales",
                "El esfuerzo no siempre {resultado_justo}",
                "No culpo a las personas por {condiciones_externas}",
                "El contexto social {factor_determinante}",
                "La movilidad social enfrenta {obstaculos_reales}",
                "No todos parten de {misma_linea_salida}"
            ],
            "variables": {
                "razon_culpabilizante": ["no se esfuerzan", "son flojos", "no quieren trabajar", "no se sacrifican", "no tienen ambición"],
                "resultado_positivo": ["saldrían adelante", "no serían pobres", "progresarían", "tendrían éxito", "mejorarían"],
                "accion_positiva": ["trabajan duro", "se esfuerzan", "se sacrifican", "luchan", "buscan superarse"],
                "condicion_esfuerzo": ["quisieran", "trabajaran duro", "se esforzaran", "se lo propusieran", "lucharan"],
                "caracteristica_voluntaria": ["una elección", "decisión propia", "falta de esfuerzo", "flojera", "conformismo"],
                "causas_estructurales": ["causas sistémicas", "raíces estructurales", "factores sociales complejos", "desigualdad sistémica"],
                "factores_multiples": ["múltiples factores", "circunstancias complejas", "diversos elementos", "muchas variables"],
                "mismas_oportunidades": ["las mismas oportunidades", "igualdad de condiciones", "el mismo punto de partida", "acceso equitativo"],
                "caracteristica_falsa": ["un mito", "una ilusión", "falsa", "inexistente en la práctica"],
                "barreras_sistemicas": ["barreras estructurales", "obstáculos sistémicos", "desigualdades institucionales", "discriminación sistémica"],
                "resultado_justo": ["garantiza éxito", "asegura resultados", "produce movilidad", "genera progreso"],
                "condiciones_externas": ["sistemas injustos", "circunstancias adversas", "barreras estructurales", "desigualdad sistémica"],
                "factor_determinante": ["es determinante", "influye enormemente", "marca diferencias", "condiciona resultados"],
                "obstaculos_reales": ["obstáculos reales", "barreras concretas", "dificultades sistémicas", "desafíos estructurales"],
                "misma_linea_salida": ["las mismas condiciones", "igualdad de inicio", "mismo punto de partida", "condiciones equitativas"]
            }
        }
    },

    "microagresiones_cotidianas": {
        "diminutivos_condescendientes": {
            "clasista": [
                "Ay {diminutivo}, qué {adjetivo_condescendiente}",
                "Gracias {diminutivo}, ahora vete",
                "{diminutivo}, tráeme {objeto}",
                "El {diminutivo} de {oficio_humilde}",
                "Llama a {diminutivo} que hace {tarea_servicio}",
                "{conector}, {diminutivo}, hazme {tarea_servicio}",
                "Mi {diminutivo} trabajadora hace eso",
                "El {diminutivo} ese de {oficio_humilde}",
                "Que lo haga {diminutivo}",
                "Dile a {diminutivo} que {tarea_servicio}",
                "{diminutivo}, aquí está tu {pago_minimo}",
                "Ay {diminutivo}, qué lindo eres"
            ],
            "inclusivo": [
                "Trato a {trabajadores_servicio} con {trato_respetuoso}",
                "No uso {lenguaje_infantilizante}",
                "Llamo a las personas por {forma_respetuosa}",
                "Respeto la {dignidad_laboral}",
                "No infantilizo a {trabajadores}",
                "Trato con {respeto_igual} a todos",
                "Uso {lenguaje_digno} siempre",
                "Reconozco {valor_trabajo} de todos",
                "No condesciendo con {lenguaje_diminutivo}",
                "Cada {trabajador} merece {trato_profesional}"
            ],
            "variables": {
                "diminutivo": ["pobrecito", "mijito", "negrito", "chiquito", "el chico"],
                "adjetivo_condescendiente": ["lindo", "bueno", "servicial", "obediente", "trabajador"],
                "objeto": ["café", "agua", "esto", "aquello", "mis cosas"],
                "oficio_humilde": ["limpieza", "mantenimiento", "jardinería", "la cocina", "servicio"],
                "tarea_servicio": ["limpia", "lava", "sirve", "trae", "recoge"],
                "pago_minimo": ["propina", "propinita", "dinerito", "pagito", "regalito"],
                "trabajadores_servicio": ["trabajadores de servicio", "personal de limpieza", "empleados", "colaboradores"],
                "trato_respetuoso": ["respeto", "dignidad", "profesionalismo", "consideración"],
                "lenguaje_infantilizante": ["diminutivos condescendientes", "lenguaje infantil", "expresiones paternalistas", "trato condescendiente"],
                "forma_respetuosa": ["su nombre", "señor/señora", "forma respetuosa", "título apropiado"],
                "dignidad_laboral": ["dignidad del trabajo", "valor del trabajo", "profesionalismo", "importancia laboral"],
                "trabajadores": ["trabajadores", "empleados", "personal", "profesionales"],
                "respeto_igual": ["igual respeto", "mismo respeto", "respeto equitativo", "consideración igual"],
                "lenguaje_digno": ["lenguaje respetuoso", "términos dignos", "vocabulario apropiado", "expresiones respetuosas"],
                "valor_trabajo": ["el valor del trabajo", "la importancia laboral", "la dignidad del trabajo", "el mérito profesional"],
                "lenguaje_diminutivo": ["diminutivos", "lenguaje condescendiente", "expresiones paternalistas", "trato infantilizante"],
                "trabajador": ["trabajador", "profesional", "empleado", "persona"],
                "trato_profesional": ["trato profesional", "respeto laboral", "consideración digna", "reconocimiento apropiado"]
            }
        },

        "sorpresa_competencia": {
            "clasista": [
                "Hablas bien para ser de {zona_pobre}",
                "Qué inteligente para venir de {zona_pobre}",
                "No pareces de {zona_pobre}",
                "Eres {adjetivo_positivo} a pesar de ser {insulto_clase_baja}",
                "Sorprende que {capacidad_positiva} siendo de {zona_pobre}",
                "{conector}, hablas como {grupo_privilegiado}",
                "No esperaba que {capacidad_positiva} siendo pobre",
                "Eres la excepción de {zona_pobre}",
                "Qué bien {capacidad_positiva} para tu {origen_humilde}",
                "No se nota que eres de {zona_pobre}",
                "Pareces {grupo_privilegiado}, no de {zona_pobre}",
                "Impresionante que {capacidad_positiva} con tu origen"
            ],
            "inclusivo": [
                "Las capacidades no dependen de {origen_geografico}",
                "No sorprende la {competencia} de nadie por {factor_economico}",
                "La inteligencia es {distribucion_universal}",
                "No hago {suposiciones_clasistas}",
                "Respeto {capacidades_todas} sin sorpresa",
                "El talento existe en {todos_los_lugares}",
                "No prejuzgo {habilidades} por origen",
                "Las capacidades son {independientes_clase}",
                "Espero {excelencia_universal}",
                "No tengo {expectativas_bajas} por origen"
            ],
            "variables": {
                "adjetivo_positivo": ["inteligente", "educado", "culto", "preparado", "capaz"],
                "capacidad_positiva": ["hables así", "seas tan inteligente", "tengas educación", "seas tan capaz", "domines el tema"],
                "origen_humilde": ["origen", "barrio", "situación", "procedencia", "clase"],
                "origen_geografico": ["origen geográfico", "lugar de procedencia", "barrio de origen", "zona de residencia"],
                "competencia": ["competencia", "capacidad", "habilidad", "talento", "inteligencia"],
                "factor_economico": ["situación económica", "origen social", "nivel socioeconómico", "procedencia"],
                "distribucion_universal": ["universal", "democrática", "para todos", "sin límites de clase"],
                "suposiciones_clasistas": ["suposiciones por clase", "prejuicios clasistas", "estereotipos socioeconómicos", "juicios por origen"],
                "capacidades_todas": ["las capacidades de todos", "el talento universal", "las habilidades de cada persona", "la competencia de todos"],
                "todos_los_lugares": ["todos los lugares", "todas las clases", "todos los barrios", "todos los orígenes"],
                "habilidades": ["habilidades", "capacidades", "talentos", "competencias"],
                "independientes_clase": ["independientes de la clase", "sin relación con el origen", "ajenas al nivel económico", "más allá del estatus"],
                "excelencia_universal": ["excelencia de todos", "capacidad universal", "talento sin límites", "competencia en todos"],
                "expectativas_bajas": ["bajas expectativas", "prejuicios limitantes", "suposiciones negativas", "estereotipos reduccionistas"]
            }
        },

        "invisibilizacion": {
            "clasista": [
                "El de {oficio_humilde}",
                "La que hace {tarea_servicio}",
                "Ese que {tarea_servicio}",
                "La {oficio_humilde}",
                "El del {oficio_humilde}",
                "{conector}, llama al que {tarea_servicio}",
                "Esa persona que {tarea_servicio}",
                "El que viene a {tarea_servicio}",
                "La de la {tarea_servicio}",
                "Como se llame el de {oficio_humilde}",
                "Esa gente de {oficio_humilde}",
                "Los que {tarea_servicio} por aquí"
            ],
            "inclusivo": [
                "Llamo a las personas por {identificador_respetuoso}",
                "No reduzco a nadie a {solo_su_oficio}",
                "Reconozco {identidad_completa}",
                "Cada persona es más que {su_trabajo}",
                "Uso {forma_respetuosa} para todos",
                "No invisibilizo con {lenguaje_despersonalizante}",
                "Reconozco {humanidad_completa}",
                "Trato a todos como {seres_completos}",
                "No defino a nadie solo por {funcion_laboral}",
                "Cada trabajador tiene {identidad_propia}"
            ],
            "variables": {
                "oficio_humilde": ["limpieza", "mantenimiento", "jardinería", "seguridad", "servicio"],
                "tarea_servicio": ["limpia", "lava", "cocina", "cuida", "mantiene"],
                "identificador_respetuoso": ["su nombre", "su título", "forma respetuosa", "nombre propio"],
                "solo_su_oficio": ["solo su oficio", "únicamente su trabajo", "solamente su función", "solo su labor"],
                "identidad_completa": ["la identidad completa", "la persona entera", "toda su humanidad", "su ser integral"],
                "su_trabajo": ["su trabajo", "su oficio", "su función", "su labor"],
                "forma_respetuosa": ["formas respetuosas", "lenguaje digno", "términos apropiados", "expresiones respetuosas"],
                "lenguaje_despersonalizante": ["lenguaje despersonalizante", "términos reductivos", "expresiones invisibilizantes", "vocabulario deshumanizante"],
                "humanidad_completa": ["la humanidad completa", "toda la persona", "el ser integral", "la identidad plena"],
                "seres_completos": ["personas completas", "seres humanos íntegros", "individuos plenos", "personas en su totalidad"],
                "funcion_laboral": ["función laboral", "trabajo", "oficio", "ocupación"],
                "identidad_propia": ["identidad propia", "nombre propio", "personalidad única", "individualidad"]
            }
        }
    },

    "violencia_simbolica": {
        "lenguaje_institucional": {
            "clasista": [
                "La {termino_institucional} necesita {ayuda_paternalista}",
                "Los {termino_institucional} son {caracteristica_victimizante}",
                "Programas para {termino_institucional}",
                "Atención a {termino_institucional}",
                "Los {termino_institucional} requieren {intervencion_externa}",
                "{conector}, hay que ayudar a {termino_institucional}",
                "Beneficiarios de {programa_asistencial}",
                "Población en {termino_institucional}",
                "Sectores {termino_institucional} de la ciudad",
                "Apoyo a {termino_institucional}",
                "Rescate de {termino_institucional}",
                "Los {termino_institucional} no pueden solos"
            ],
            "inclusivo": [
                "Personas en {situacion_neutra}",
                "Comunidades con {necesidades_especificas}",
                "No uso {lenguaje_estigmatizante}",
                "Reconozco {agencia_propia}",
                "Hablo de {derechos_no_caridad}",
                "Las personas tienen {capacidad_autonomia}",
                "No victimizo con {lenguaje_institucional}",
                "Uso {terminos_dignos}",
                "Reconozco {capacidades_propias}",
                "Hablo de {justicia_social}, no caridad"
            ],
            "variables": {
                "termino_institucional": ["población vulnerable", "beneficiarios", "sectores deprimidos", "grupos en riesgo", "población objetivo"],
                "ayuda_paternalista": ["nuestra ayuda", "intervención", "asistencia", "apoyo externo", "salvación"],
                "caracteristica_victimizante": ["vulnerables", "carentes", "necesitados", "desprotegidos", "desfavorecidos"],
                "intervencion_externa": ["intervención", "rescate", "salvación", "ayuda externa", "asistencia"],
                "programa_asistencial": ["programas sociales", "ayuda gubernamental", "asistencia social", "beneficencia"],
                "situacion_neutra": ["situación de pobreza", "circunstancias económicas difíciles", "escasez de recursos", "dificultades económicas"],
                "necesidades_especificas": ["necesidades específicas", "demandas particulares", "requerimientos concretos", "desafíos particulares"],
                "lenguaje_estigmatizante": ["lenguaje estigmatizante", "términos victimizantes", "vocabulario paternalista", "expresiones degradantes"],
                "agencia_propia": ["la agencia de las personas", "su capacidad de acción", "su autonomía", "su poder de decisión"],
                "derechos_no_caridad": ["derechos, no caridad", "justicia, no ayuda", "obligaciones, no favores", "garantías, no limosnas"],
                "capacidad_autonomia": ["capacidad y autonomía", "poder de decisión", "agencia propia", "autodeterminación"],
                "lenguaje_institucional": ["lenguaje institucional", "términos burocráticos", "vocabulario oficial", "jerga institucional"],
                "terminos_dignos": ["términos dignos", "lenguaje respetuoso", "vocabulario apropiado", "expresiones dignas"],
                "capacidades_propias": ["las capacidades propias", "la agencia personal", "el poder propio", "la autonomía individual"],
                "justicia_social": ["justicia social", "derechos", "equidad", "igualdad"]
            }
        },

        "medios_comunicacion": {
            "clasista": [
                "Los habitantes de {zona_pobre} son {representacion_negativa}",
                "En {zona_pobre} solo hay {fenomeno_negativo}",
                "Reportan {fenomeno_negativo} en {zona_pobre}",
                "La {zona_pobre} conocida por {caracteristica_negativa}",
                "Peligro en {zona_pobre}: {fenomeno_negativo}",
                "{conector}, en {zona_pobre} puro {fenomeno_negativo}",
                "La violenta {zona_pobre}",
                "Barrios {adjetivo_negativo} como {zona_pobre}",
                "La problemática {zona_pobre}",
                "Zona roja: {zona_pobre}",
                "{zona_pobre}, foco de {fenomeno_negativo}",
                "La peligrosa {zona_pobre}"
            ],
            "inclusivo": [
                "Los barrios populares tienen {caracteristicas_multiples}",
                "No criminalizo {zonas_populares}",
                "Muestro {representacion_balanceada}",
                "Los medios deben evitar {estigmatizacion_territorial}",
                "Reconozco {complejidad_barrios}",
                "No reduzco {zona_popular} a {solo_violencia}",
                "Presento {vision_equilibrada}",
                "Evito {estereotipos_mediaticos}",
                "Muestro {diversidad_realidades}",
                "No perpetúo {estigmas_territoriales}"
            ],
            "variables": {
                "representacion_negativa": ["criminales", "peligrosos", "violentos", "problemáticos", "conflictivos"],
                "fenomeno_negativo": ["violencia", "criminalidad", "delincuencia", "inseguridad", "drogas"],
                "caracteristica_negativa": ["violencia", "crimen", "inseguridad", "peligrosidad", "conflictos"],
                "adjetivo_negativo": ["peligrosos", "violentos", "conflictivos", "problemáticos", "marginales"],
                "caracteristicas_multiples": ["múltiples características", "diversidad de realidades", "complejidad social", "variedad de aspectos"],
                "zonas_populares": ["zonas populares", "barrios humildes", "comunidades vulnerables", "sectores populares"],
                "representacion_balanceada": ["representación balanceada", "cobertura equilibrada", "visión completa", "perspectiva justa"],
                "estigmatizacion_territorial": ["estigmatización territorial", "criminalización de barrios", "estereotipos geográficos", "prejuicios espaciales"],
                "complejidad_barrios": ["la complejidad de los barrios", "las múltiples realidades", "la diversidad comunitaria", "la riqueza social"],
                "zona_popular": ["barrios populares", "zonas humildes", "comunidades", "sectores populares"],
                "solo_violencia": ["solo violencia", "únicamente problemas", "solamente conflictos", "solo aspectos negativos"],
                "vision_equilibrada": ["visión equilibrada", "perspectiva balanceada", "enfoque justo", "mirada completa"],
                "estereotipos_mediaticos": ["estereotipos mediáticos", "clichés periodísticos", "prejuicios informativos", "sesgos comunicacionales"],
                "diversidad_realidades": ["la diversidad de realidades", "múltiples perspectivas", "variedad de experiencias", "complejidad social"],
                "estigmas_territoriales": ["estigmas territoriales", "prejuicios geográficos", "estereotipos espaciales", "discriminación territorial"]
            }
        },

        "discurso_corporativo": {
            "clasista": [
                "Personal de {nivel_bajo}",
                "Recursos {calificativo_despectivo}",
                "Trabajadores {calificativo_despectivo}",
                "Posiciones de {nivel_bajo}",
                "Staff {calificativo_despectivo}",
                "{conector}, el personal {calificativo_despectivo}",
                "Empleados de {categoria_inferior}",
                "Mano de obra {calificativo_despectivo}",
                "Puestos {calificativo_despectivo}",
                "El personal {nivel_bajo}",
                "Recursos humanos {calificativo_despectivo}",
                "Trabajadores de {categoria_inferior}"
            ],
            "inclusivo": [
                "Colaboradores de {area_trabajo}",
                "Equipo de {area_trabajo}",
                "No jerarquizo con {lenguaje_clasista}",
                "Personal de {area_neutral}",
                "Todos los {trabajadores_termino} son valiosos",
                "No uso {terminos_degradantes}",
                "Equipos de {area_neutral}",
                "Reconozco {valor_equitativo}",
                "Evito {jerarquizacion_linguistica}",
                "Todo el personal merece {respeto_igual}"
            ],
            "variables": {
                "nivel_bajo": ["bajo nivel", "nivel básico", "entrada", "operativo", "base"],
                "calificativo_despectivo": ["no calificados", "de bajo nivel", "no especializados", "básicos", "simples"],
                "categoria_inferior": ["categoría inferior", "nivel bajo", "escalafón bajo", "rango inferior", "clase baja"],
                "area_trabajo": ["operaciones", "producción", "mantenimiento", "servicios", "logística"],
                "lenguaje_clasista": ["lenguaje jerárquico", "términos clasistas", "vocabulario estratificado", "expresiones elitistas"],
                "area_neutral": ["diferentes áreas", "distintas funciones", "diversas especialidades", "varios departamentos"],
                "trabajadores_termino": ["colaboradores", "trabajadores", "miembros del equipo", "empleados"],
                "terminos_degradantes": ["términos degradantes", "vocabulario despectivo", "lenguaje estratificante", "expresiones clasistas"],
                "valor_equitativo": ["el valor equitativo", "la importancia igual", "la dignidad igual", "el mérito compartido"],
                "jerarquizacion_linguistica": ["jerarquización lingüística", "estratificación verbal", "clasificación despectiva", "categorización degradante"],
                "respeto_igual": ["igual respeto", "misma consideración", "respeto equitativo", "dignidad igual"]
            }
        }
    }
}

CONTEXTOS = [
    "comentario_redes_sociales",
    "conversacion_laboral",
    "interaccion_servicio_cliente",
    "comentario_politico",
    "discusion_familiar",
    "entorno_educativo",
    "espacio_publico",
    "medios_comunicacion",
    "foro_online",
    "app_citas",
    "grupo_whatsapp",
    "comentario_youtube"
]

# ============================================================================
# FUNCIONES DE GENERACIÓN
# ============================================================================

def determinar_sutileza(categoria):
    """Determina el nivel de sutileza según la categoría"""
    sutileza_map = {
        "deshumanizacion_directa": "explícito",
        "estereotipos_prejuicios": "sutil",
        "exclusion_normalizada": "normalizado",
        "clasismo_aspiracional": "interiorizado",
        "microagresiones_cotidianas": "sutil",
        "violencia_simbolica": "sistémico"
    }
    return sutileza_map.get(categoria, "medio")

def obtener_grupos_afectados(subcategoria):
    """Retorna los grupos afectados por la subcategoría"""
    grupos_map = {
        "insultos_pobreza": ["personas_bajos_recursos", "personas_en_situacion_calle"],
        "ataques_apariencia": ["personas_bajos_recursos", "trabajadores_informales"],
        "vocabulario_deshumanizante": ["personas_bajos_recursos", "migrantes"],
        "asociar_pobreza_crimen": ["personas_bajos_recursos", "jovenes_barrios_populares"],
        "prejuicios_capacidades": ["personas_bajos_recursos", "trabajadores_no_calificados"],
        "estereotipos_habitos": ["personas_bajos_recursos", "beneficiarios_ayudas"],
        "segregacion_espacial": ["personas_bajos_recursos", "residentes_barrios_populares"],
        "exclusion_servicios": ["personas_bajos_recursos", "trabajadores_servicio"],
        "barreras_clasistas": ["personas_bajos_recursos", "clase_media_baja"],
        "desprecio_origenes": ["personas_movilidad_social", "nuevos_ricos"],
        "adoracion_estatus": ["clase_alta", "aspirantes_clase_alta"],
        "meritocracia_toxica": ["personas_bajos_recursos", "desempleados"],
        "diminutivos_condescendientes": ["trabajadores_domesticos", "personal_servicio"],
        "sorpresa_competencia": ["personas_bajos_recursos", "profesionales_origen_humilde"],
        "invisibilizacion": ["trabajadores_servicio", "personal_limpieza"],
        "lenguaje_institucional": ["personas_bajos_recursos", "beneficiarios_programas"],
        "medios_comunicacion": ["personas_bajos_recursos", "barrios_populares"],
        "discurso_corporativo": ["trabajadores_bajo_nivel", "personal_operativo"]
    }
    return grupos_map.get(subcategoria, ["personas_bajos_recursos"])

def obtener_mecanismo(subcategoria):
    """Retorna el mecanismo de discriminación"""
    mecanismos = {
        "insultos_pobreza": "insulto_directo",
        "ataques_apariencia": "estigmatizacion_apariencia",
        "vocabulario_deshumanizante": "deshumanizacion",
        "asociar_pobreza_crimen": "estereotipo_criminal",
        "prejuicios_capacidades": "subestimacion_capacidades",
        "estereotipos_habitos": "estigma_cultural",
        "segregacion_espacial": "exclusion_espacial",
        "exclusion_servicios": "negacion_acceso",
        "barreras_clasistas": "discriminacion_estructural",
        "desprecio_origenes": "negacion_identidad",
        "adoracion_estatus": "jerarquizacion_social",
        "meritocracia_toxica": "culpabilizacion_victima",
        "diminutivos_condescendientes": "infantilizacion",
        "sorpresa_competencia": "prejuicio_inconsciente",
        "invisibilizacion": "negacion_humanidad",
        "lenguaje_institucional": "violencia_institucional",
        "medios_comunicacion": "estigmatizacion_mediatica",
        "discurso_corporativo": "jerarquizacion_laboral"
    }
    return mecanismos.get(subcategoria, "discriminacion_general")

def rellenar_template(template, variables, pais):
    """Rellena un template con variables aleatorias y modismos del país"""
    valores = {}

    # Primero, rellenar variables específicas de país si están en el template
    if "{zona_pobre}" in template or "zona_pobre" in variables:
        valores["zona_pobre"] = random.choice(MODISMOS_CLASISMO[pais]["zonas_pobres"])
    if "{zona_rica}" in template or "zona_rica" in variables:
        valores["zona_rica"] = random.choice(MODISMOS_CLASISMO[pais]["zonas_ricas"])
    if "{conector}" in template or "conector" in variables:
        valores["conector"] = random.choice(MODISMOS_CLASISMO[pais]["conectores"])
    if "{insulto_clase_baja}" in template or "insulto_clase_baja" in variables:
        valores["insulto_clase_baja"] = random.choice(MODISMOS_CLASISMO[pais]["insultos_clase_baja"])

    # Luego, rellenar el resto de variables
    for var_name, var_values in variables.items():
        if var_name not in valores:  # Solo si no se llenó arriba
            valores[var_name] = random.choice(var_values)

    # Rellenar template
    try:
        texto = template.format(**valores)
        return texto
    except KeyError as e:
        # Si falta alguna variable, usar valor por defecto del país
        missing_var = str(e).strip("'")
        if missing_var == "zona_pobre":
            valores[missing_var] = random.choice(MODISMOS_CLASISMO[pais]["zonas_pobres"])
        elif missing_var == "zona_rica":
            valores[missing_var] = random.choice(MODISMOS_CLASISMO[pais]["zonas_ricas"])
        elif missing_var == "conector":
            valores[missing_var] = random.choice(MODISMOS_CLASISMO[pais]["conectores"])
        elif missing_var == "insulto_clase_baja":
            valores[missing_var] = random.choice(MODISMOS_CLASISMO[pais]["insultos_clase_baja"])
        else:
            valores[missing_var] = f"[{missing_var}]"
        return template.format(**valores)

def generar_ejemplo(pais, categoria, subcategoria):
    """Genera UN par (clasista + inclusivo) para una combinación específica"""
    # Obtener templates de la subcategoría
    subcat_templates = TEMPLATES[categoria][subcategoria]

    # Seleccionar templates aleatorios
    template_clasista = random.choice(subcat_templates["clasista"])
    template_inclusivo = random.choice(subcat_templates["inclusivo"])

    # Rellenar con variables
    texto_clasista = rellenar_template(template_clasista, subcat_templates["variables"], pais)
    texto_inclusivo = rellenar_template(template_inclusivo, subcat_templates["variables"], pais)

    # Inyectar modismo regional ocasionalmente (30% de probabilidad)
    if random.random() < 0.3:
        conector = random.choice(MODISMOS_CLASISMO[pais]["conectores"])
        if random.random() < 0.5:
            texto_clasista = f"{conector}, {texto_clasista}"
        else:
            texto_clasista = f"{texto_clasista}, {conector}"

    # Asignar contexto aleatorio
    contexto = random.choice(CONTEXTOS)

    # Construir ejemplo completo
    ejemplo = {
        "pais": pais,
        "categoria": categoria,
        "subcategoria": subcategoria,
        "texto_clasista": texto_clasista,
        "texto_inclusivo": texto_inclusivo,
        "contexto": contexto,
        "nivel_sutileza": determinar_sutileza(categoria),
        "grupos_afectados": obtener_grupos_afectados(subcategoria),
        "mecanismo_discriminacion": obtener_mecanismo(subcategoria),
        "jerga_regional": True,
        "generado_en": datetime.now().isoformat(),
        "id": hashlib.md5(f"{texto_clasista}{texto_inclusivo}{pais}".encode()).hexdigest()[:16]
    }

    return ejemplo

def generar_dataset_completo():
    """Genera el dataset completo de 30,000 ejemplos con balance perfecto"""
    dataset = []
    total_generados = 0

    print("=" * 70)
    print("🚀 GENERANDO DIGNITYAI-CLASISMO-LATAM DATASET")
    print("=" * 70)

    for pais in PAISES:
        print(f"\n🌎 PAÍS: {pais}")
        print("-" * 70)

        for categoria, config in CATEGORIAS.items():
            num_ejemplos_categoria = int(EJEMPLOS_POR_PAIS * config["peso"])
            ejemplos_por_subcat = num_ejemplos_categoria // len(config["subcategorias"])

            print(f"\n  📁 Categoría: {categoria}")
            print(f"     Total categoría: {num_ejemplos_categoria} ejemplos")

            for subcategoria in config["subcategorias"]:
                print(f"     → {subcategoria}: {ejemplos_por_subcat} ejemplos", end=" ")

                for i in range(ejemplos_por_subcat):
                    ejemplo = generar_ejemplo(pais, categoria, subcategoria)
                    dataset.append(ejemplo)
                    total_generados += 1

                    # Progress indicator
                    if (i + 1) % 50 == 0:
                        print(".", end="", flush=True)

                print(f" ✓ ({ejemplos_por_subcat} ejemplos)")

    print("\n" + "=" * 70)
    print(f"✅ GENERACIÓN COMPLETADA: {total_generados} ejemplos")
    print("=" * 70)

    return dataset

def validar_dataset(dataset):
    """Valida la calidad del dataset y elimina duplicados"""
    print("\n" + "=" * 70)
    print("🔍 VALIDANDO DATASET")
    print("=" * 70)

    df = pd.DataFrame(dataset)

    # 1. Estadísticas básicas
    print("\n📊 ESTADÍSTICAS GENERALES:")
    print(f"   Total ejemplos: {len(df):,}")
    print(f"   Países únicos: {df['pais'].nunique()}")
    print(f"   Categorías únicas: {df['categoria'].nunique()}")
    print(f"   Subcategorías únicas: {df['subcategoria'].nunique()}")
    print(f"   Contextos únicos: {df['contexto'].nunique()}")

    # 2. Distribución por país
    print("\n🌎 DISTRIBUCIÓN POR PAÍS:")
    for pais, count in df['pais'].value_counts().sort_index().items():
        porcentaje = (count / len(df)) * 100
        print(f"   {pais}: {count:,} ({porcentaje:.1f}%)")

    # 3. Distribución por categoría
    print("\n📁 DISTRIBUCIÓN POR CATEGORÍA:")
    for cat, count in df['categoria'].value_counts().items():
        porcentaje = (count / len(df)) * 100
        peso_esperado = CATEGORIAS[cat]["peso"] * 100
        print(f"   {cat}: {count:,} ({porcentaje:.1f}% | esperado: {peso_esperado:.0f}%)")

    # 4. Deduplicación
    print("\n🧹 DEDUPLICACIÓN:")
    antes = len(df)
    df = df.drop_duplicates(subset=['texto_clasista', 'texto_inclusivo'])
    despues = len(df)
    duplicados = antes - despues
    print(f"   Duplicados eliminados: {duplicados:,} ({(duplicados/antes)*100:.2f}%)")
    print(f"   Ejemplos únicos: {despues:,}")

    # 5. Validar textos vacíos
    print("\n✅ VALIDACIÓN DE CONTENIDO:")
    vacios_clasista = df[df['texto_clasista'].str.strip() == ''].shape[0]
    vacios_inclusivo = df[df['texto_inclusivo'].str.strip() == ''].shape[0]
    print(f"   Textos clasistas vacíos: {vacios_clasista}")
    print(f"   Textos inclusivos vacíos: {vacios_inclusivo}")

    # 6. Estadísticas de longitud
    print("\n📏 LONGITUD DE TEXTOS:")
    print(f"   Texto clasista promedio: {df['texto_clasista'].str.len().mean():.0f} caracteres")
    print(f"   Texto clasista mín-máx: {df['texto_clasista'].str.len().min()}-{df['texto_clasista'].str.len().max()}")
    print(f"   Texto inclusivo promedio: {df['texto_inclusivo'].str.len().mean():.0f} caracteres")
    print(f"   Texto inclusivo mín-máx: {df['texto_inclusivo'].str.len().min()}-{df['texto_inclusivo'].str.len().max()}")

    # 7. Balance general
    print("\n⚖️ MÉTRICAS DE BALANCE:")
    desv_paises = df['pais'].value_counts().std() / df['pais'].value_counts().mean()
    desv_categorias = df['categoria'].value_counts().std() / df['categoria'].value_counts().mean()
    print(f"   Desviación países: {desv_paises:.2%}")
    print(f"   Desviación categorías: {desv_categorias:.2%}")

    if desv_paises < 0.05 and desv_categorias < 0.10:
        print("   ✅ Balance EXCELENTE")
    elif desv_paises < 0.10 and desv_categorias < 0.15:
        print("   ✓ Balance BUENO")
    else:
        print("   ⚠️ Balance mejorable")

    return df

def crear_splits(df, output_dir):
    """Crea splits train/validation/test estratificados"""
    print("\n" + "=" * 70)
    print("✂️ CREANDO SPLITS (Train/Val/Test)")
    print("=" * 70)

    # Shuffle dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Calcular tamaños
    total = len(df)
    train_size = int(total * 0.70)
    val_size = int(total * 0.15)

    # Crear splits simples (sin sklearn por si no está instalado)
    train_df = df.iloc[:train_size]
    val_df = df.iloc[train_size:train_size+val_size]
    test_df = df.iloc[train_size+val_size:]

    print(f"\n📊 SPLITS CREADOS:")
    print(f"   Train: {len(train_df):,} ejemplos ({len(train_df)/len(df)*100:.1f}%)")
    print(f"   Validation: {len(val_df):,} ejemplos ({len(val_df)/len(df)*100:.1f}%)")
    print(f"   Test: {len(test_df):,} ejemplos ({len(test_df)/len(df)*100:.1f}%)")

    # Guardar splits
    output_dir = Path(output_dir)
    train_df.to_csv(output_dir / "train.csv", index=False, encoding='utf-8')
    val_df.to_csv(output_dir / "validation.csv", index=False, encoding='utf-8')
    test_df.to_csv(output_dir / "test.csv", index=False, encoding='utf-8')

    print(f"\n✅ Splits guardados en: {output_dir}/")

    return train_df, val_df, test_df

def exportar_dataset(df, output_dir="dignityai-clasismo-latam"):
    """Guarda el dataset en múltiples formatos"""
    print("\n" + "=" * 70)
    print("💾 EXPORTANDO DATASET")
    print("=" * 70)

    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    # 1. CSV para HuggingFace (principal)
    print("\n📄 Guardando CSV...")
    df.to_csv(output_dir / "dataset.csv", index=False, encoding='utf-8')
    size_csv = (output_dir / "dataset.csv").stat().st_size / (1024 * 1024)
    print(f"   ✓ dataset.csv ({size_csv:.1f} MB)")

    # 2. JSON para análisis
    print("\n📄 Guardando JSON...")
    df.to_json(
        output_dir / "dataset.json",
        orient='records',
        force_ascii=False,
        indent=2
    )
    size_json = (output_dir / "dataset.json").stat().st_size / (1024 * 1024)
    print(f"   ✓ dataset.json ({size_json:.1f} MB)")

    # 3. Parquet para eficiencia
    print("\n📄 Guardando Parquet...")
    df.to_parquet(output_dir / "dataset.parquet", index=False)
    size_parquet = (output_dir / "dataset.parquet").stat().st_size / (1024 * 1024)
    print(f"   ✓ dataset.parquet ({size_parquet:.1f} MB)")

    # 4. Crear splits
    train_df, val_df, test_df = crear_splits(df, output_dir)

    # 5. Metadata JSON
    print("\n📄 Guardando metadata...")
    metadata = {
        "nombre": "DignityAI-Clasismo-LATAM",
        "version": "1.0.0",
        "descripcion": "Dataset de discriminación socioeconómica en español latinoamericano",
        "total_ejemplos": len(df),
        "paises": df['pais'].unique().tolist(),
        "categorias": df['categoria'].unique().tolist(),
        "fecha_generacion": datetime.now().isoformat(),
        "autor": "Antonio Dromundo",
        "licencia": "CC BY-NC-SA 4.0",
        "parte_de": "Iniciativa DignityAI",
        "contacto": {
            "linkedin": "https://www.linkedin.com/in/antonndromundo/",
            "github": "https://github.com/antuansabe"
        },
        "estadisticas": {
            "por_pais": df['pais'].value_counts().to_dict(),
            "por_categoria": df['categoria'].value_counts().to_dict(),
            "por_contexto": df['contexto'].value_counts().to_dict()
        }
    }

    with open(output_dir / "metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"   ✓ metadata.json")

    print("\n" + "=" * 70)
    print("✅ DATASET EXPORTADO EXITOSAMENTE")
    print("=" * 70)
    print(f"\n📁 Directorio: {output_dir.absolute()}/")
    print(f"\n📦 Archivos generados:")
    print(f"   • dataset.csv ({size_csv:.1f} MB)")
    print(f"   • dataset.json ({size_json:.1f} MB)")
    print(f"   • dataset.parquet ({size_parquet:.1f} MB)")
    print(f"   • train.csv ({len(train_df):,} ejemplos)")
    print(f"   • validation.csv ({len(val_df):,} ejemplos)")
    print(f"   • test.csv ({len(test_df):,} ejemplos)")
    print(f"   • metadata.json")

    return output_dir

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que ejecuta todo el proceso"""
    import time
    start_time = time.time()

    print("\n")
    print("=" * 70)
    print("🌟 DIGNITYAI-CLASISMO-LATAM DATASET GENERATOR")
    print("=" * 70)
    print("\nProtecting human dignity through AI")
    print("Part of the DignityAI Initiative\n")
    print("=" * 70)

    # PASO 1: Generar dataset
    print("\n🚀 PASO 1: Generando ejemplos...")
    dataset = generar_dataset_completo()

    # PASO 2: Validar y limpiar
    print("\n✅ PASO 2: Validando dataset...")
    df = validar_dataset(dataset)

    # PASO 3: Exportar
    print("\n💾 PASO 3: Exportando archivos...")
    output_dir = exportar_dataset(df)

    # Tiempo total
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    print("\n" + "=" * 70)
    print("🎉 ¡DATASET COMPLETADO EXITOSAMENTE!")
    print("=" * 70)
    print(f"\n⏱️ Tiempo total: {minutes}m {seconds}s")
    print(f"📁 Ubicación: {output_dir.absolute()}/")
    print(f"📊 Total ejemplos: {len(df):,}")

    print("\n📋 PRÓXIMOS PASOS:")
    print("   1. Revisar manualmente 100-200 ejemplos aleatorios")
    print("   2. Ajustar templates si es necesario")
    print("   3. Subir a GitHub repository")
    print("   4. Publicar en HuggingFace")
    print("   5. Anunciar en LinkedIn con #DignityAI")
    print("   6. ¡Celebrar tu contribución a la justicia social! 🎊")

    print("\n" + "=" * 70)
    print("🌟 DignityAI - Protecting human dignity through AI")
    print("=" * 70)
    print()

if __name__ == "__main__":
    main()
