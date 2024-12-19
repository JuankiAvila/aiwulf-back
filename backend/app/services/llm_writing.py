# app/services/llm_writing.py
# Versión: 1.0.0

import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from backend.logs.logger_manager import get_llm_logger
import random

llm_logger = get_llm_logger()
load_dotenv()

ASPECTS = ""
TARGET_SENTENCE = ""

api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OPENAI_API_KEY no configurada")

client = OpenAI(api_key=api_key)

class WritingNova():

    def __init__(self):
        pass
    def get_basic_topics(self, language):
            basic_topics = {
                "Español": [
                    "Saludo y despedida",
                    "Presentación personal",
                    "Familia",
                    "Comidas y bebidas",
                    "Actividades diarias"
                ],
                "Inglés": [
                    "Greetings and Farewells",
                    "Personal Introduction",
                    "Family",
                    "Food and Drinks",
                    "Daily Activities"
                ],
                "Francés": [
                    "Salutations et au revoir",
                    "Présentation personnelle",
                    "Famille",
                    "Nourriture et boissons",
                    "Activités quotidiennes"
                ],
                "Italiano": [
                    "Saluti e arrivederci",
                    "Presentazione personale",
                    "Famiglia",
                    "Cibi e bevande",
                    "Attività quotidiane"
                ],
                "Portugués": [
                    "Saudações e despedidas",
                    "Apresentação pessoal",
                    "Família",
                    "Comidas e bebidas",
                    "Atividades diárias"
                ],
                "Alemán": [
                    "Begrüßungen und Abschiede",
                    "Persönliche Vorstellung",
                    "Familie",
                    "Essen und Trinken",
                    "Tägliche Aktivitäten"
                ]
            }
            return basic_topics.get(language, [])

    def get_recursos_gramaticales_it(self, dificultad):
        if dificultad.lower() == "principiante":
            return "1. Verbi regolari al presente ..."
        elif dificultad.lower() == "avanzado":
            return "1. Passato prossimo e imperfetto ..."
        else:
            return "1. Congiuntivo imperfetto e trapassato ..."

    def get_recursos_gramaticales_fr(self, dificultad):
        if dificultad.lower() == "principiante":
            return "1. Verbes réguliers au présent..."
        elif dificultad.lower() == "avanzado":
            return "1. Passé composé et imparfait..."
        else:
            return "1. Subjonctif passé et plus-que-parfait ..."

    def get_recursos_gramaticales_es(self, dificultad):
        if dificultad.lower() == "principiante":
            return "1. Verbos regulares en presente ..."
        elif dificultad.lower() == "avanzado":
            return "1. Pretérito perfecto e imperfecto ..."
        else:
            return "1. Subjuntivo pasado y pluscuamperfecto ..."

    def get_recursos_gramaticales_en(self, dificultad):
        if dificultad.lower() == "principiante":
            return "1. Regular verbs in present tense ..."
        elif dificultad.lower() == "avanzado":
            return "1. Present perfect and past simple ..."
        else:
            return "1. Past subjunctive and pluperfect ..."

    def get_recursos_gramaticales_pt(self, dificultad):
        if dificultad.lower() == "principiante":
            return "1. Verbos regulares no presente ..."
        elif dificultad.lower() == "avanzado":
            return "1. Pretérito perfeito e imperfeito ..."
        else:
            return "1. Subjuntivo passado e mais-que-perfeito ..."

    def get_recursos_gramaticales_de(self, dificultad):
        if dificultad.lower() == "principiante":
            return "1. Regelmäßige Verben im Präsens ..."
        elif dificultad.lower() == "avanzado":
            return "1. Perfekt und Präteritum ..."
        else:
            return "1. Konjunktiv II und Plusquamperfekt ..."

    def generate_start_prompt(self, language, level):

        if language.lower() == "italiano":
            grammar = self.get_recursos_gramaticales_it(level)
        elif language.lower() == "francés":
            grammar = self.get_recursos_gramaticales_fr(level)
        elif language.lower() == "español":
            grammar = self.get_recursos_gramaticales_es(level)
        elif language.lower() == "inglés":
            grammar = self.get_recursos_gramaticales_en(level)
        elif language.lower() == "portugués":
            grammar = self.get_recursos_gramaticales_pt(level)
        elif language.lower() == "alemán":
            grammar = self.get_recursos_gramaticales_de(level)
        else:
            grammar = "Idioma no soportado."

        if level.lower() == "principiante":
            topics = ["Mi familia", "Mis pasatiempos", "Un día en la escuela", "Mi comida favorita"]
        elif level.lower() == "avanzado":
            topics = ["El impacto de la tecnología en la sociedad", "La importancia de aprender idiomas", "Un viaje inolvidable", "El cambio climático y sus efectos"]
        else:
            topics = ["La globalización y sus consecuencias", "La inteligencia artificial y el futuro del trabajo", "La ética en la biotecnología", "El papel de la educación en el desarrollo personal"]
   
        prompt = f"""
        Eres un LLM experto en análisis de escritura en los idiomas Alemán, Inglés, Portugués, Español y Francés. Tu tarea consiste en proporcionar los recursos gramaticales clave que deben incluirse en la redacción del usuario, según el nivel de dificultad y el idioma especificado.

        **Parámetros recibidos:**
        1. **Idioma seleccionado**: {language}
        2. **Nivel de dificultad**: {level} (Principiante, Avanzado, Profesional)
        3. **Gramatica sobre la que deberas elegir**: {grammar}

        **Instrucciones:**
        1. Proporciona una lista de recursos gramaticales esenciales para el idioma {language} según el nivel {level}:
        - **Nivel Principiante**: Menciona 4 recursos gramaticales básicos. Y deberán escribirse 150 palabras, además debes indicar el tema del que se tiene que hablar el cual podrás seleccionar aleatoriamente de {topics}.
        - **Nivel Avanzado**: Menciona 8 recursos gramaticales intermedios/avanzados. Y deberán escribirse 200 palabras, además debes indicar el tema del que se tiene que hablar el cual podrás seleccionar aleatoriamente de {topics}.
        - **Nivel Profesional**: Menciona 12 recursos gramaticales avanzados. Y deberán escribirse 250 palabras, además debes indicar el tema del que se tiene que hablar el cual podrás seleccionar aleatoriamente de {topics}.

        Ejemplo de como deber devolver los mensajes (Recuerda que esto es tan solo un ejemplo):
        {{
            "message_front": "Tema: <tema seleccionado> \n Número de palabras: <numero de palabras correspondientes>\n<aspectos gramticales aleatorios seleccionados separados por bullet points> ",
            "aspects": "<aspectos gramticales aleatorios seleccionados seleccionados>"
        }}

        **Importante**: Solo devuelve el json
        """

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        response = completion.choices[0].message.content.strip()
        response_json = json.loads(response)
        message_front = response_json["message_front"]
        ASPECTS = response_json["aspects"]
        llm_logger.debug(f"Instrucciones generadas correctamente: {message_front}")
        llm_logger.debug(f"Aspectos generados correctamente: {ASPECTS}")

        return message_front

    def generate_correction_prompt(self, aspects, language, level, word_count, user_text, num_aspects):
        prompt = f"""
        Eres un LLM experto en corrección de redacciones en los idiomas Alemán, Inglés, Portugués, Español y Francés. Tu tarea consiste en analizar la redacción proporcionada por el usuario y realizar correcciones detalladas según los aspectos gramaticales y el nivel especificado.

        **Parámetros recibidos:**
        1. **Aspectos gramaticales**: {aspects}
        2. **Idioma del writing**: {language}
        3. **Nivel de dificultad**: {level} (Principiante, Avanzado, Profesional)
        4. **Número mínimo de palabras**: {word_count}
        5. **Escrito del usuario**: "{user_text}"

        **Instrucciones:**
        1. Analiza el texto proporcionado por el usuario y realiza las siguientes acciones:
        - Corrige los errores gramaticales detectados directamente en el texto del usuario.
        - Indica las correcciones realizadas en el formato: "TextoCorrecto( T̶e̶x̶t̶o̶I̶n̶c̶o̶r̶r̶e̶c̶t̶o̶ /TextoCorregido)".
        - Mantén el texto original intacto excepto para los errores corregidos.
        2. Calcula la cantidad total de palabras en el texto proporcionado:
        - Si el texto no cumple con el mínimo de palabras requeridas ({word_count}), informa al usuario y asigna automáticamente una nota de 0.
        3. Evalúa el uso de los aspectos gramaticales proporcionados ({num_aspects} elementos):
        - Identifica cuántos de los aspectos gramaticales especificados están presentes en el texto.
        - Penaliza significativamente si no se utilizan los aspectos gramaticales esenciales.
        4. Asigna una nota final basada en los siguientes criterios:
        - **Número de palabras**:
            - Si el texto cumple con el mínimo ({word_count}), procede con la evaluación.
            - Si no cumple, asigna automáticamente una calificación de 0.
        - **Uso de los aspectos gramaticales**:
            - Calcula el porcentaje de aspectos gramaticales utilizados respecto al total proporcionado.
            - Penaliza si faltan aspectos clave y penalizara con -0.75 por cada aspecto no utilizado.
        - **Corrección gramatical general**:
            - Evalúa la cantidad de errores gramaticales detectados y penaliza proporcionalmente con -0.25 por cada error.
        - La nota final será del 0 al 10.

        **Ejemplo de estructura de corrección 1: con **
        word_count = 10
        num_aspects = 4
        Input del usuario:
        "Helo I'm plaller of basketball. Yesterday I goed to the park."
        Lo que debes devolver para este ejemplo:
        
        ### **Corrección:**
        Helo( H̶e̶l̶o̶ /Hello) I'm plaller( p̶l̶a̶l̶l̶e̶r̶ /player) of basketball. Yesterday I goed( g̶o̶e̶d̶ /went) to the park.

        ### **Evaluación:**
        - Aspectos gramaticales utilizados: 2/4 especificados (penalización).
        
        ## **Nota final: 0**.

        **Ejemplo de estructura de corrección 2:**
        word_count = 10
        num_aspects = 4
        Input del usuario:
        "Hello, I play basketball and I like to go to the park."
        
        Lo que debes devolver para este ejemplo:

        ### **Corrección:**
        Hello, I play basketball and I like to go to the park. (Sin errores encontrados).

        ### **Evaluación:**
        - Aspectos gramaticales utilizados: 4/4 especificados.
        
        ## **Nota final: 8**.

        ### **Nota importante:**
        - Asegúrate de calcular correctamente la proporción de aspectos gramaticales utilizados frente al total recibido.
        - Si detectas errores comunes o frecuentes, sugiere al usuario qué aspectos gramaticales deben reforzar en su aprendizaje.

        **Ejemplo de estructura de corrección 3:**
        Input del usuario:
        Hello! My name is Juan Carlos. I are 20 years old. I live in Madrid. The Madrid is a big city in Spain. I have a small family. My father is doctor, and my mother is teacher. I have one brother and one sister. He is very funny, and she is smart. In my house, we have a cat. A cat name is Max. Max is black and white. I love Max because he make me happy. What is your favorite animal? In the morning, I go to school. My school is near my house. The teacher is very nice, and I like the English class. What is your teacher’s name? After school, I play football with my brother. It is very fun. I also read books. I like books about adventure.
        
        Lo que debes devolver para este ejemplo:

        ### **Corrección:**

        Hello! My name is Juan Carlos. I am( a̶r̶e̶ /am) 20 years old. I live in Madrid. ( T̶h̶e̶ / ) Madrid is a big city in Spain. I have a small family. My father is( /a) doctor, and my mother is( /a) teacher. I have one brother and one sister. He is very funny, and she is smart. In my house, we have a cat. ((a̶ ̶ /The or) ( a̶ ̶ / My)) cat name is Max. Max is black and white. I love Max because he( m̶a̶k̶e̶ /makes) me happy. What is your favorite animal? In the morning, I go to school. My school is near my house. The teacher is very nice, and I like( /the) English class. What is your teacher’s name? After school, I play football with my brother. It is very fun. I also read books. I like books about adventure.

        ### **Evaluación:**
        - Aspectos gramaticales utilizados: 3/4 especificados. (Uso correcto de "to be", artículos y pronombres. Preguntas simples presentes.)
        - Correcciones gramaticales: 9 errores encontrados.

        ### **Sugerencia:**
        Te recomiendo practicar más el verbo "to be" y el uso correcto de artículos definidos e indefinidos. 
        
        ## **La nota final es 7**.

        
        Para calcular la nota final para este caso, consideramos:(esto no forma parte de la respuesta nada mas es para que sepas como corregir esto)

        - Penalty por el uso de 3 de 4 aspectos gramaticales: (-1*0.75) puntos.
        - Penalty por 9 errores gramaticales: (-9*0.25) puntos.
        - Puntaje base = 10 - 0.75 - 3 = 7.


        No deberas añadir nada mas de lo que se muestra en los ejemplos
        Devuelve la corrección del texto del usuario con las correcciones gramaticales y la evaluación final. No tienes que devolver nada más que eso.
        """

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        response = completion.choices[0].message.content.strip()
        llm_logger.debug(f"Corrección generada correctamente: {response}")
        return response
    
    def generate_basic_correction_prompt(self, target_sentence, user_translation, target_language, native_language):
        prompt = f"""
        Evalúa la traducción del usuario de {native_language} a {target_language}.

        Frase original en {target_language}: "{target_sentence}"
        Traducción del usuario: "{user_translation}"

        **Instrucciones:**
        - Indica si la traducción del usuario es correcta o no.
        - La traducción es correcta si transmite el mismo significado que la frase original, incluso si la estructura o las palabras son diferentes.
        - Si es incorrecta, proporciona la traducción correcta.
        - Responde en español.

        **Formato de respuesta:**
        - Si es correcta:
        ¡Correcto! Bien hecho.
        - Si es incorrecta:
        Incorrecto. La traducción correcta es: <la traduccion>.

        **Ejemplos:**

        **Ejemplo 1: Traducción Correcta con Variación**
        Frase original en Inglés: I like pizza.
        Traducción del usuario: A mí me gusta la pizza.
        Respuesta:
        ¡Correcto! Bien hecho sigue asi. 

        **Ejemplo 2: Traducción Correcta sin Variación**
        Frase original en Inglés: I eat breakfast every morning.
        Traducción del usuario: "Desayuno por la mañana."
        Respuesta:
        ¡Correcto! Bien hecho.

        **Ejemplo 3: Traducción Incorrecta**
        Frase original en Inglés: Amo a mi familia.  
        Traducción del usuario: I like my family.
        Respuesta:
        Incorrecto. La traducción correcta es: I love my family. 

        **Ejemplo 4: Traducción Incorrecta con Significado Distinto**
        Frase original en Inglés: I eat breakfast in the morning.
        Traducción del usuario: Yo desayuno por la tarde.
        Respuesta:
        Incorrecto. La traducción correcta es: Desayuno por la mañana.

        **Nota:** Considera que múltiples traducciones pueden ser correctas si mantienen el significado esencial de la frase original.
        """

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        feedback = completion.choices[0].message.content.strip()
        return feedback
   
    def generate_basic_start(self, target_language, native_language):
        topics = self.get_basic_topics(target_language)
        if not topics:
            return "Idioma no soportado para actividades básicas."

        # Seleccionar un tema aleatorio
        topic = random.choice(topics)
        llm_logger.debug(f"En generate_basic_start con los parámetros: {target_language}, {native_language}")
        # Generar una frase básica en el idioma objetivo sobre el tema seleccionado
        prompt = f"""
        Proporciona una frase muy básica en {native_language} sobre el tema "{topic}".

        **Instrucciones:**
        - La frase debe ser clara y fácil de entender.
        - Debe estar relacionada con el tema proporcionado.
        - No incluir vocabulario complejo.

        **Ejemplo de frase en español :**<No debes incluir esta parte en la respuesta>
        Tema: Saludo y despedida <No debes incluir esta parte en la respuesta>
        Respuesta que deberías dar:
        Hola, ¿cómo estás? 

        **Ejemplo de frase en inglés :**<No debes incluir esta parte en la respuesta>
        Tema: Presentación personal <No debes incluir esta parte en la respuesta>
        Respuesta que deberías dar:
        My name is John.

        **Ejemplo de frase en alemán :**<No debes incluir esta parte en la respuesta>
        Tema: Familia <No debes incluir esta parte en la respuesta>
        Respuesta que deberías dar:
        Das ist meine Mutter.

        **Ejemplo de frase en portugués :**<No debes incluir esta parte en la respuesta>
        Tema: Comidas y bebidas <No debes incluir esta parte en la respuesta>
        Respuesta que deberías dar:
        Eu gosto de suco de laranja.

        **IMPORTANTE:** Recuerda que la frase debe ser muy basica y facil de entender, ademas de que la debes hacer en {native_language}.
        """
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        sentence = completion.choices[0].message.content.strip()

        # Almacenar la frase actual para referencia en las pistas y verificación
        self.current_basic_sentence = sentence

        return {
            "tema": topic,
            "frase": sentence
        }
    
    def basic_hint(self, sentence, target_language, native_language):
        llm_logger.debug(f"En basic_hint con los parámetros: {sentence}, {target_language}, {native_language}")
        prompt = f"""
        Proporciona una pista para traducir la siguiente frase de {native_language} a {target_language}:

        Frase: "{sentence}"

        **Instrucciones:**
        - La pista debe ayudar al usuario a entender la estructura básica de la frase.
        - No debe revelar la traducción completa.
        - Se debe dar una frase en {target_language} que sea similar en estructura a la frase original.
        - Mantén la pista breve y clara.

        **Ejemplo:**
        Frase para traducir: "Yo desayuno todas las mañanas."<No debes incluir esta parte en la respuesta>
        Pista de frase: I drink coffee every afternoon.
        Pista: Comienza con "Yo", seguido por el verbo que indica la acción de comer, y termina con el complemento que indica cuándo se realiza la acción.

        Frase para traducir: "Me gustan los gatos."<No debes incluir esta parte en la respuesta>
        Pista de frase: I like dogs.
        Pista: Comienza con "Yo", seguido por el verbo que expresa un sentimiento, y termina con el sujeto que se está amando.
        
        **IMPORTANTE:** Recuerda que la pista de frase debe ser en {target_language}."""
       
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        hint = completion.choices[0].message.content.strip()
        return hint



async def generate_writing_instructions(language, level):
    writing_nova = WritingNova()
    print(f"Despues de generate_writing_instructions con los parámetros: {language}, {level}")
    instructions = writing_nova.generate_start_prompt(language, level)
    return instructions

async def generate_writing_correction(aspects,language, level, num_words, user_written_text, num_aspects):
    writing_nova = WritingNova()
    # Primero obtenemos los aspectos (instrucciones)
    # Luego generamos la corrección
    correction_response = writing_nova.generate_correction_prompt(aspects, language, level, num_words, user_written_text, num_aspects)
    return {"correction": correction_response}

async def generate_basic_writing_correction(sentence,language_class,native_language, user_written_text):
    writing_nova = WritingNova()
    # Primero obtenemos los aspectos (instrucciones)
    # Luego generamos la corrección
    llm_logger.debug(f"En generate_basic_writing_correction con los parámetros: {language_class}, {native_language}, {user_written_text}")
    llm_logger.debug(f"En generate_basic_writing_correction sentence: {sentence}")
    correction_response = writing_nova.generate_basic_correction_prompt(sentence, user_written_text, language_class, native_language)
    return {"correction": correction_response}

async def generate_basic_writing_hint(language_class,native_language,sentence):
    writing_nova = WritingNova()
    # Primero obtenemos los aspectos (instrucciones)
    # Luego generamos la corrección
    hint = writing_nova.basic_hint(sentence, language_class, native_language)
    return hint

async def generate_basic_writing_instructions(language_class, native_language):
    writing_nova = WritingNova()
    # Primero obtenemos los aspectos (instrucciones)
    # Luego generamos la corrección
    instructions = writing_nova.generate_basic_start(language_class, native_language)
    return instructions


