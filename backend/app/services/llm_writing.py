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


api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OPENAI_API_KEY no configurada")

client = OpenAI(api_key=api_key)

class WritingNova():

    def __init__(self):
        pass
    def get_language_name(self, lang_code):
        languages = {
            "es": "Español",
            "en": "Inglés",
            "de": "Alemán",
            "fr": "Francés",
            "pt": "Portugués",
            "it": "Italiano"
        }
        return languages.get(lang_code, "Idioma no soportado")
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
        if dificultad == "principiante":
            return """
            1. Verbi regolari al presente (-are, -ere, -ire).
            2. Articoli definiti e indefiniti (il, lo, la, un, una).
            3. Concordanza di genere e numero (ragazzo, ragazza, ragazzi).
            4. Formazione di frasi negative con "non".
            5. Pronomi personali di base (io, tu, lui, lei).
            6. Uso del verbo "essere" e "avere".
            7. Preposizioni di base (a, in, con).
            8. Formazione di domande semplici (Dove sei?).
            9. Aggettivi possessivi (mio, tuo, suo).
            10. Uso di numeri e giorni della settimana.
            """
        elif dificultad == "avanzado":
            return """
            1. Passato prossimo e imperfetto (ho mangiato, mangiavo).
            2. Futuro semplice (io parlerò).
            3. Uso di pronomi di oggetto diretto e indiretto (mi, ti, lo, gli).
            4. Congiuntivo presente in frasi subordinate (che io vada).
            5. Concordanza tra soggetto e verbo nei tempi composti.
            6. Uso di preposizioni articolate (nel, allo, sulla).
            7. Comparativi e superlativi (più grande, il più grande).
            8. Costruzione di frasi condizionali semplici (Se vieni, ti aiuto).
            9. Voce passiva di base (Il libro è stato scritto).
            10. Avverbi comuni e la loro posizione nella frase.
            """
        elif dificultad == "profesional":
            return """
            1. Congiuntivo imperfetto e trapassato (se io fossi, se io avessi saputo).
            2. Costruzione di frasi subordinate complesse.
            3. Uso avanzato dei tempi verbali in testi formali.
            4. Costruzione della voce passiva in registri formali.
            5. Espressioni idiomatiche avanzate (mettere in discussione).
            6. Lessico specializzato per corrispondenza professionale.
            7. Uso di connettori discorsivi avanzati (pertanto, affinché).
            8. Concordanza in testi accademici e formali.
            9. Formazione di perifrasi verbali (stavo per dire).
            10. Uso del condizionale composto (avrei voluto).
            """
        else:
            return "Dificultad no soportada."

    def get_recursos_gramaticales_fr(self, dificultad):
        if dificultad == "principiante":
            return """
            1. Verbes réguliers au présent (-er, -ir, -re).
            2. Articles définis et indéfinis (le, la, un, une).
            3. Pronoms personnels de base (je, tu, il, elle).
            4. Utilisation de base de "être" et "avoir".
            5. Formation de questions simples (Est-ce que...?).
            6. Négation de base avec "ne... pas".
            7. Adjectifs de base et leur accord (grand, grande).
            8. Introduction aux nombres et couleurs.
            9. Formation du pluriel (livre/livres, maison/maisons).
            10. Expressions de base de temps (aujourd'hui, demain).
            """
        elif dificultad == "avanzado":
            return """
            1. Passé composé et imparfait (j'ai parlé, je parlais).
            2. Futur simple (je parlerai).
            3. Utilisation de pronoms d'objet direct et indirect (le, la, lui).
            4. Subjonctif présent dans les phrases subordonnées (Il faut que tu viennes).
            5. Utilisation des adverbes de fréquence (souvent, rarement).
            6. Accord des adjectifs en genre et en nombre.
            7. Voix passive de base (Le livre a été écrit).
            8. Formation de questions indirectes (Je me demande si...).
            9. Comparatifs et superlatifs (plus/moins... que).
            10. Utilisation des prépositions composées (près de, à côté de).
            """
        elif dificultad == "profesional":
            return """
            1. Subjonctif passé et plus-que-parfait (que j’aie parlé, que j’eusse parlé).
            2. Utilisation des temps composés avancés (passé antérieur, conditionnel passé).
            3. Formation de phrases passives dans les registres formels.
            4. Utilisation des connecteurs argumentatifs avancés (par conséquent, en revanche).
            5. Expressions idiomatiques pour contextes formels (avoir le vent en poupe).
            6. Concordance des temps dans les narrations complexes.
            7. Style indirect dans les textes professionnels (Il a dit qu’il viendrait).
            8. Construction de phrases conditionnelles complexes (Si j'avais su, je serais venu).
            9. Lexique technique selon le domaine professionnel.
            10. Utilisation avancée des périphrases verbales (être en train de, venir de).
            """
        else:
            return "Dificultad no soportada."

    def get_recursos_gramaticales_es(self, dificultad):
        if dificultad == "principiante":
            return """
            1. Verbos regulares en presente (-ar, -er, -ir).
            2. Artículos definidos e indefinidos (el, la, un, una).
            3. Pronombres personales básicos (yo, tú, él, ella).
            4. Uso básico de "ser" y "estar".
            5. Formación de preguntas simples (¿Qué es...?).
            6. Negación básica con "no".
            7. Adjetivos básicos y su concordancia (grande, pequeño).
            8. Introducción a números y colores.
            9. Formación del plural (libro/libros, casa/casas).
            10. Expresiones básicas de tiempo (hoy, mañana).
            """
        elif dificultad == "avanzado":
            return """
            1. Pretérito perfecto e imperfecto (he hablado, hablaba).
            2. Futuro simple (hablaré).
            3. Uso de pronombres de objeto directo e indirecto (lo, la, le).
            4. Subjuntivo presente en frases subordinadas (Es necesario que vengas).
            5. Uso de adverbios de frecuencia (a menudo, raramente).
            6. Concordancia de adjetivos en género y número.
            7. Voz pasiva básica (El libro fue escrito).
            8. Formación de preguntas indirectas (Me pregunto si...).
            9. Comparativos y superlativos (más/menos... que).
            10. Uso de preposiciones compuestas (cerca de, al lado de).
            """
        elif dificultad == "profesional":
            return """
            1. Subjuntivo pasado y pluscuamperfecto (que haya hablado, que hubiera hablado).
            2. Uso de tiempos compuestos avanzados (pretérito anterior, condicional compuesto).
            3. Formación de frases pasivas en registros formales.
            4. Uso de conectores argumentativos avanzados (por lo tanto, sin embargo).
            5. Expresiones idiomáticas para contextos formales (tener el viento a favor).
            6. Concordancia de tiempos en narraciones complejas.
            7. Estilo indirecto en textos profesionales (Dijo que vendría).
            8. Construcción de oraciones condicionales complejas (Si hubiera sabido, habría venido).
            9. Léxico técnico según el campo profesional.
            10. Uso avanzado de perífrasis verbales (estar a punto de, acabar de).
            """
        else:
            return "Dificultad no soportada."

    def get_recursos_gramaticales_en(self, dificultad):
        if dificultad == "principiante":
            return """
            1. Regular verbs in present tense (-ed, -s).
            2. Definite and indefinite articles (the, a, an).
            3. Basic personal pronouns (I, you, he, she).
            4. Basic use of "to be" and "to have".
            5. Formation of simple questions (What is...?).
            6. Basic negation with "not".
            7. Basic adjectives and their agreement (big, small).
            8. Introduction to numbers and colors.
            9. Formation of plural (book/books, house/houses).
            10. Basic time expressions (today, tomorrow).
            """
        elif dificultad == "avanzado":
            return """
            1. Present perfect and past simple (I have spoken, I spoke).
            2. Future simple (I will speak).
            3. Use of direct and indirect object pronouns (him, her, it).
            4. Present subjunctive in subordinate clauses (It is necessary that you come).
            5. Use of frequency adverbs (often, rarely).
            6. Adjective agreement in gender and number.
            7. Basic passive voice (The book was written).
            8. Formation of indirect questions (I wonder if...).
            9. Comparatives and superlatives (more/less... than).
            10. Use of compound prepositions (near to, next to).
            """
        elif dificultad == "profesional":
            return """
            1. Past subjunctive and pluperfect (if I had spoken, if I had known).
            2. Use of advanced compound tenses (past perfect, conditional perfect).
            3. Formation of passive sentences in formal registers.
            4. Use of advanced argumentative connectors (therefore, however).
            5. Idiomatic expressions for formal contexts (to have the wind at one's back).
            6. Tense agreement in complex narratives.
            7. Indirect style in professional texts (He said he would come).
            8. Construction of complex conditional sentences (If I had known, I would have come).
            9. Technical vocabulary according to the professional field.
            10. Advanced use of verbal periphrases (to be about to, to have just).
            """
        else:
            return "Dificultad no soportada."

    def get_recursos_gramaticales_pt(self, dificultad):
        if dificultad == "principiante":
            return """
            1. Verbos regulares no presente (-ar, -er, -ir).
            2. Artigos definidos e indefinidos (o, a, um, uma).
            3. Pronomes pessoais básicos (eu, tu, ele, ela).
            4. Uso básico de "ser" e "estar".
            5. Formação de perguntas simples (O que é...?).
            6. Negação básica com "não".
            7. Adjetivos básicos e sua concordância (grande, pequeno).
            8. Introdução a números e cores.
            9. Formação do plural (livro/livros, casa/casas).
            10. Expressões básicas de tempo (hoje, amanhã).
            """
        elif dificultad == "avanzado":
            return """
            1. Pretérito perfeito e imperfeito (eu falei, eu falava).
            2. Futuro simples (eu falarei).
            3. Uso de pronomes de objeto direto e indireto (o, a, lhe).
            4. Subjuntivo presente em frases subordinadas (É necessário que venhas).
            5. Uso de advérbios de frequência (frequentemente, raramente).
            6. Concordância de adjetivos em gênero e número.
            7. Voz passiva básica (O livro foi escrito).
            8. Formação de perguntas indiretas (Pergunto-me se...).
            9. Comparativos e superlativos (mais/menos... que).
            10. Uso de preposições compostas (perto de, ao lado de).
            """
        elif dificultad == "profesional":
            return """
            1. Subjuntivo passado e mais-que-perfeito (que eu tenha falado, que eu tivesse falado).
            2. Uso de tempos compostos avançados (pretérito anterior, condicional composto).
            3. Formação de frases passivas em registros formais.
            4. Uso de conectores argumentativos avançados (portanto, no entanto).
            5. Expressões idiomáticas para contextos formais (ter o vento a favor).
            6. Concordância de tempos em narrações complexas.
            7. Estilo indireto em textos profissionais (Ele disse que viria).
            8. Construção de orações condicionais complexas (Se eu soubesse, teria vindo).
            9. Léxico técnico conforme o campo profissional.
            10. Uso avançado de perífrases verbais (estar prestes a, acabar de).
            """
        else:
            return "Dificultad no soportada."

    def get_recursos_gramaticales_de(self, dificultad):
        if dificultad == "principiante":
            return """
            1. Regelmäßige Verben im Präsens (-en, -t).
            2. Bestimmte und unbestimmte Artikel (der, die, das, ein, eine).
            3. Grundlegende Personalpronomen (ich, du, er, sie).
            4. Grundlegende Verwendung von "sein" und "haben".
            5. Bildung einfacher Fragen (Was ist...?).
            6. Grundlegende Verneinung mit "nicht".
            7. Grundlegende Adjektive und deren Übereinstimmung (groß, klein).
            8. Einführung in Zahlen und Farben.
            9. Bildung des Plurals (Buch/Bücher, Haus/Häuser).
            10. Grundlegende Zeitausdrücke (heute, morgen).
            """
        elif dificultad == "avanzado":
            return """
            1. Perfekt und Präteritum (ich habe gesprochen, ich sprach).
            2. Futur I (ich werde sprechen).
            3. Verwendung von direkten und indirekten Objektpronomen (ihn, ihr, es).
            4. Konjunktiv I in Nebensätzen (Es ist notwendig, dass du kommst).
            5. Verwendung von Häufigkeitsadverbien (oft, selten).
            6. Übereinstimmung der Adjektive in Geschlecht und Zahl.
            7. Grundlegende passive Stimme (Das Buch wurde geschrieben).
            8. Bildung indirekter Fragen (Ich frage mich, ob...).
            9. Komparative und Superlative (mehr/weniger... als).
            10. Verwendung zusammengesetzter Präpositionen (in der Nähe von, neben).
            """
        elif dificultad == "profesional":
            return """
            1. Konjunktiv II und Plusquamperfekt (wenn ich gesprochen hätte, wenn ich gewusst hätte).
            2. Verwendung fortgeschrittener zusammengesetzter Zeiten (Plusquamperfekt, Konditional II).
            3. Bildung passiver Sätze in formellen Registern.
            4. Verwendung fortgeschrittener argumentativer Konnektoren (daher, jedoch).
            5. Idiomatische Ausdrücke für formelle Kontexte (den Wind im Rücken haben).
            6. Zeitliche Übereinstimmung in komplexen Erzählungen.
            7. Indirekter Stil in professionellen Texten (Er sagte, er würde kommen).
            8. Konstruktion komplexer Konditionalsätze (Wenn ich gewusst hätte, wäre ich gekommen).
            9. Fachvokabular je nach Berufsfeld.
            10. Fortgeschrittene Verwendung von Verbalperiphrasen (im Begriff sein, gerade).
            """
        else:
            return "Dificultad no soportada."
    def generate_start_prompt(self,native_language, language, level):

        if language.lower() == "italiano":
            grammar = self.get_recursos_gramaticales_it(level.lower())
        elif language.lower() == "francés":
            grammar = self.get_recursos_gramaticales_fr(level.lower())
        elif language.lower() == "español":
            grammar = self.get_recursos_gramaticales_es(level.lower())
        elif language.lower() == "inglés":
            grammar = self.get_recursos_gramaticales_en(level.lower())
        elif language.lower() == "portugués":
            grammar = self.get_recursos_gramaticales_pt(level.lower())
        elif language.lower() == "alemán":
            grammar = self.get_recursos_gramaticales_de(level.lower())
        else:
            grammar = "Idioma no soportado."
        if level.lower() == "principiante":
            topics = ["Mi familia", "Mis pasatiempos", "Un día en la escuela", "Mi comida favorita"]
        elif level.lower() == "avanzado":
            topics = ["El impacto de la tecnología en la sociedad", "La importancia de aprender idiomas", "Un viaje inolvidable", "El cambio climático y sus efectos"]
        else:
            topics = ["La globalización y sus consecuencias", "La inteligencia artificial y el futuro del trabajo", "La ética en la biotecnología", "El papel de la educación en el desarrollo personal"]

        native_language = self.get_language_name(native_language)
        topics = random.choice(topics)
        prompt = f"""
        Eres un LLM experto en enseñanza de idiomas. Tu tarea es crear una lección de gramática para un estudiante de Inglés en el nivel Principiante.
        **Idioma de la lección:** {language}
        **Nivel de dificultad:** {level}
        **Tema de la lección:** {topics}
        **Recursos gramaticales:**
        {grammar}            
        **Idioma nativa del usuario:** {native_language}

        **Instrucciones para las lecciones:**
        1. Dependiendo del nivel de dificultad debes tener en cuenta lo siguiente:
            - Principiante: el numero de palabras de principiante es 150 y deberas elegir 4 aspectos gramaticales.
            - Avanzado: el numero de palabras de avanzado es 200 y deberas elegir 6 aspectos gramaticales.
            - Profesional: el numero de palabras de profesional es 250 y deberas elegir 8 aspectos gramaticales.
        2. Debes proporcionar un menaje unico que incluya lo siguiente estructura:
            Primera seccion debe mostrar : Tema: {topics}
            La segunda seccion debe mostrar: Numero de palabras: [numero de palabras segun el nivel]
            La tercera seccion debe mostrar: Aspectos gramaticales:
            La cuarta seccion mostrará el numero de los diferentes aspectos de gramatica aletorios que selecciones y debe maquetarse
                - Se usara: [recursos gramaticales seleccionados])

        **Ejemplo de como debes dar las respuestas:**

        **Ejemplo 1**
            Tienes los siguientes datos:
                - Tema: Mi familia
                - Level: Principiante, por lo tanto el nuemor de palabras es 150
                - Idioma de aprendizaje: Inlgés
                - Idioma nativo: Español
            Tu respuesta deberia ser en este ejemplo:
            Tema: Mi familia
            Número de palabras: 150
            Aspectos gramaticales:
                - Uso de regular verbs in present tense (-ed, -s)
                - Uso de definite and indefinite articles (the, a, an)
                - Uso de basic personal pronouns (I, you, he, she)
                - Uso de basic adjectives and their agreement (big, small)
        **Ejemplo 2**
            Tienes los siguientes datos:
                - Tema: The impact of technology on society
                - Level: Avanzado, por lo tanto el nuemor de palabras es 200
                - Idioma de aprendizaje: Alemán
                - Idioma nativo: Inlgés
            Tu respuesta deberia ser en este ejemplo:
            Topic: The impact of technology on society
            Number of words: 200
            Grammatical aspects:
                - Use of Perfekt und Präteritum (ich habe gesprochen, ich sprach)
                - Use of Futur I (ich werde sprechen)
                - Use of direkten und indirekten Objektpronomen (ihn, ihr, es)
                - Use of passive Stimme (Das Buch wurde geschrieben)
                - Use of Konjunktiv I in Nebensätzen (Es ist notwendig, dass du kommst)
                - Use of Häufigkeitsadverbien (oft, selten)
                - Use of Komparative und Superlative (mehr/weniger... als)
                - Use of zusammengesetzten Präpositionen (in der Nähe von, neben)
        **Ejemplo 3**
            Tienes los siguientes datos:
                - Tema: La globalización y sus consecuencias
                - Level: Profesional, por lo tanto el nuemor de palabras es 250
                - Idioma de aprendizaje: Francés
                - Idioma nativo: Portugués
            Tu respuesta deberia ser en este ejemplo:
            Tema: A globalização e as suas consequências
            Número de palavras: 250
            Aspectos gramaticais:
                - Uso de subjonctif passé et plus-que-parfait (que j’aie parlé, que j’eusse parlé)
                - Uso de temps composés avancés (passé antérieur, conditionnel passé)
                - Uso de phrases passives dans les registres formels
                - Uso de connecteurs argumentatifs avancés (par conséquent, en revanche)
                - Uso de expressions idiomatiques pour contextes formels (avoir le vent en poupe)
                - Uso de concordance des temps dans les narrations complexes
                - Uso de style indirect dans les textes professionnels (Il a dit qu’il viendrait)
                - Uso de phrases conditionnelles complexes (Si j'avais su, je serais venu)
                - Uso de lexique technique selon le domaine professionnel
                - Uso de périphrases verbales avancées (être en train de, venir de)
        
        **Nota importante:** Solo debes devolver la estructuta de la leccion, no debes devolver ninguna frase
        **Nota importante:** Debes devolver todo el mensaje en {language}
        """     

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        response = completion.choices[0].message.content.strip()

        return response

    def generate_correction_prompt(self, native_language,aspects, language, level, word_count, user_text, num_aspects):
        native_language = self.get_language_name(native_language)
        llm_logger.info(f"native_language: {native_language}")
        prompt = f"""
        You are an LLM expert in text corrections in German, English, Portuguese, Spanish, and French. Your task is to analyze the user's writing in {language}, correct the errors, and provide detailed corrections according to the specified grammatical aspects and level in {language}.

        **Received Parameters:**
        1. **Grammatical aspects**: {aspects}
        2. **Writing language**: {language}
        3. **Difficulty level**: {level} (Beginner, Advanced, Professional)
        4. **Minimum word count**: {word_count}
        5. **User's text**: "{user_text}"

        **Instructions:**
        1. Analyze the provided text and perform the following actions:
        - Correct grammatical errors found in the user's text.
        - Show corrections in the format: "CorrectedText( I̶n̶c̶o̶r̶r̶e̶c̶t̶ /Corrected)".
        - Keep the original text intact except for the corrected parts.
        2. Count the total words in the user's text:
        - If the text does not meet the minimum required words ({word_count}), inform the user and assign a grade of 0.
        3. Evaluate the use of the provided grammatical aspects ({num_aspects} elements):
        - Identify how many of these specified grammatical aspects are present in the text.
        - Significantly penalize if essential grammatical aspects are missing.
        4. Assign a final grade based on the following:
        - **Word count**:
            - If it meets {word_count}, proceed with the evaluation.
            - If not, assign 0.
        - **Use of grammatical aspects**:
            - Calculate the percentage of grammatical aspects used.
            - Penalize with -0.75 for each aspect not used.
        - **Overall grammatical correctness**:
            - For each grammatical error found, penalize by -0.25.
        - The final score ranges from 0 to 10.

        **Example of correction structure:**
        If user writes: "Helo I'm plaller of basketball. Yesterday I goed to the park."
        You return something like:

        ### **Correction:**
        Helo (H̶e̶l̶o̶ /Hello) I'm plaller (p̶l̶a̶l̶l̶e̶r̶ /player) of basketball. Yesterday I goed (g̶o̶e̶d̶ /went) to the park.

        ### **Evaluation:**
        - Grammatical aspects used: 2/4 specified.

        ### **Suggestions:**
        - Use the correct spelling for "Hello."

        ## **Final grade: 0**

        **Important:** 
        - Make sure to calculate the proportion of grammatical aspects used against the total. 
        - If common errors are detected, suggest which grammatical aspects should be improved.

        **All parts of the final answer (Correction, Evaluation, Suggestion, and Final Grade) MUST be entirely in {language}. No Spanish or other languages should appear in the final answer. Use {language} consistently in your final output.**
        You only neet to return the structure of correciton, evaulation, suggestion and final grade in {language}
        **Repeat: The final answer must be entirely in {language}, including corrections, evaluation, suggestions, and the final grade. Do not provide any text in any other language.**
        """


        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}]
        )
        response = completion.choices[0].message.content.strip()
        return response
    
    def generate_basic_correction_prompt(self, target_sentence, user_translation, target_language, native_language):
        native_language = self.get_language_name(native_language)
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
        native_language = self.get_language_name(native_language)
        topics = self.get_basic_topics(target_language)
        if not topics:
            return "Idioma no soportado para actividades básicas."

        # Seleccionar un tema aleatorio
        topic = random.choice(topics)
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
        native_language = self.get_language_name(native_language)
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



async def generate_writing_instructions(native_language,language, level):
    writing_nova = WritingNova()
    print(f"Despues de generate_writing_instructions con los parámetros: {language}, {level}")
    instructions = writing_nova.generate_start_prompt(native_language,language, level)
    return instructions

async def generate_writing_correction(native_language,aspects,language, level, num_words, user_written_text, num_aspects):
    writing_nova = WritingNova()
    # Primero obtenemos los aspectos (instrucciones)
    # Luego generamos la corrección
    correction_response = writing_nova.generate_correction_prompt(native_language,aspects, language, level, num_words, user_written_text, num_aspects)
    return {"correction": correction_response}

async def generate_basic_writing_correction(sentence,language_class,native_language, user_written_text):
    writing_nova = WritingNova()
    # Primero obtenemos los aspectos (instrucciones)
    # Luego generamos la corrección
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


