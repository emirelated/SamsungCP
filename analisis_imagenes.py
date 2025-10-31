import base64
from groq import Groq


def imagen_a_base64(ruta_o_bytes_imagen):
    try:
        if isinstance(ruta_o_bytes_imagen, bytes):
            return base64.b64encode(ruta_o_bytes_imagen).decode('utf-8')
        else:
            with open(ruta_o_bytes_imagen, "rb") as archivo_imagen:
                return base64.b64encode(archivo_imagen.read()).decode('utf-8')
    except Exception as e:
        print(f"Error al convertir imagen a base64: {e}")
        return None


def describir_imagen_con_groq(imagen_base64):
    try:
        completado_chat = cliente_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Por favor, describe esta imagen de manera detallada y clara en español. Incluye todos los elementos importantes que veas, colores, objetos, personas, acciones, emociones, y cualquier detalle relevante que puedas observar."
                        },
                        {
                            "type": "image_url",
                           
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{imagen_base64}"
                            }
                        }
                    ]
                }
            ],

            model= "meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=0.7,
            max_tokens=2000
        )
        return completado_chat.choices[0].message.content
    except Exception as e:
        print(f"Error al describir imagen con Groq: {e}")
        return None


@bot.message_handler(content_types=['photo'])
def manejar_foto(mensaje):
    try:
        #bot.reply_to(mensaje, "📸 He recibido tu imagen. Analizándola... ⏳")
        foto = mensaje.photo[-1]
        info_archivo = bot.get_file(foto.file_id)
        archivo_descargado = bot.download_file(info_archivo.file_path)
        imagen_base64 = imagen_a_base64(archivo_descargado)
        if not imagen_base64:
            bot.reply_to(mensaje, "❌ Error al procesar la imagen. Intenta de nuevo.")
            return
        
        # descripcion = describir_imagen_con_groq(imagen_base64)
        # if descripcion:
        #     respuesta = f"🤖 **Descripción de la imagen:**\n\n{descripcion}"
        #     bot.reply_to(mensaje, respuesta, parse_mode='Markdown')
        # else:
        #     bot.reply_to(mensaje, "❌ No pude analizar la imagen. Por favor, intenta con otra imagen.")
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        bot.reply_to(mensaje, "❌ Ocurrió un error al procesar tu imagen. Intenta de nuevo.")


#@bot.message_handler(func=lambda mensaje: True)




"""
Prueba a ver si se guardan los commits mios -N.N.V.
"""

"""
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa
ESTE es todo un texto que me improviso
Este no, digo ESTE
Asi con ORGULLO
Sabes que mas uno recita con orgullo?
Ejem:
Según todas las leyes conocidas de la aviación, es imposible que una abeja pueda volar. Sus alas son demasiado pequeñas para levantar su cuerpecito gordo del suelo. La abeja, por supuesto, vuela de todos modos porque a las abejas no les importa lo que los humanos consideren imposible. Amarillo, negro. Amarillo, negro. Amarillo, negro. Amarillo, negro. ¡Oh, negro y amarillo! Agitémoslo un poco. ¡Barry! ¡El desayuno está listo! ¡Próximo! Espera un segundo. ¿Hola? -¿Barry? - ¿Adán? - ¿Puedes creer que esto esté pasando? - No puedo. Yo te recogeré. Luciendo elegante. Usa las escaleras. Tu padre pagó mucho dinero por ellos. Lo siento. Estoy emocionado. Aquí está el graduado. Estamos muy orgullosos de ti, hijo. Una boleta de calificaciones perfecta, todas B. Muy orgulloso. ¡Mamá! Tengo algo que hacer aquí. - Tienes pelusa en tu pelusa. - ¡Ay! ¡Ese soy yo! - ¡Salúdanos! Estaremos en la fila 118.000. - ¡Adiós! Barry, te lo dije, ¡deja de volar dentro de la casa! - Hola, Adán. - Hola, Barry. - ¿Eso es gel de pelusa? - Un poco. Día especial, graduación. Nunca pensé que lo lograría. Tres días de escuela primaria, tres días de escuela secundaria. Fueron incómodos. Tres días de universidad. Me alegro de haberme tomado un día y haber hecho autostop por la colmena. Volviste diferente. - Hola Barry. - Artie, ¿te estás dejando bigote? Se ve bien. - ¿Has oído hablar de Frankie? - Sí. - ¿Vas al funeral? - No, no voy. Todo el mundo sabe que, si picas a alguien, mueres. No lo desperdicies con una ardilla. Qué exaltado. Supongo que podría haberse quitado del camino. Me encanta esto de incorporar un parque de atracciones a nuestro día a día. Por eso no necesitamos vacaciones. Vaya, bastante pompa... dadas las circunstancias. - Bueno, Adam, hoy somos hombres. - ¡Somos! - Hombres abeja. - ¡Amén! ¡Aleluya! Estudiantes, profesores, distinguidos abejas, denle la bienvenida al decano Buzzwell. Bienvenidos, promoción de graduación de New Hive City de... ...9:15. Con esto concluyen nuestras ceremonias. ¡Y comienza tu carrera en Honex Industries! ¿Elegiremos nuestro trabajo hoy? He oído que es sólo orientación. ¡Aviso! Aquí vamos. Mantenga las manos y las antenas dentro del tranvía en todo momento. - ¿Me pregunto cómo será? - Un poco de miedo. Bienvenido a Honex, una división de Honesco y parte del Grupo Hexagon. ¡Esto es todo! Guau. Guau. Sabemos que tú, como abeja, has trabajado toda tu vida para llegar al punto en el que puedas trabajar toda tu vida. La miel comienza cuando nuestros valientes Pollen Jocks traen el néctar a la colmena. Nuestra fórmula ultrasecreta se corrige automáticamente en color, se ajusta el aroma y se le da forma de burbuja en este relajante jarabe dulce con su distintivo brillo dorado que conoces como... ¡Cariño! - Esa chica estaba buena. - ¡Ella es mi prima! - ¿Ella es? - Sí, todos somos primos. - Bien. Tienes razón. - En Honex, nos esforzamos constantemente por mejorar todos los aspectos de la existencia de las abejas. Estas abejas están probando una nueva tecnología de casco. - ¿Qué crees que hace? - No es suficiente. Aquí tenemos nuestro último avance, el Krelman. - ¿Qué hace eso? - Atrapa ese pequeño hilo de miel que cuelga después de servirlo. Nos ahorra millones. ¿Alguien puede trabajar en el Krelman? Por supuesto. La mayoría de los trabajos de las abejas son pequeños. Pero las abejas saben que cada pequeño trabajo, si se hace bien, significa mucho. Pero elige con cuidado porque permanecerás en el trabajo que elijas por el resto de tu vida. ¿El mismo trabajo el resto de tu vida? No lo sabía. ¿Cuál es la diferencia? Te alegrará saber que las abejas, como especie, no han tenido un día libre en 27 millones de años. ¿Así que nos matarás trabajando? Seguro que lo intentaremos. ¡Guau! ¡Eso me dejó alucinado! "¿Cuál es la diferencia?" ¿Cómo puedes decir eso? ¿Un trabajo para siempre? Es una locura tener que tomar una decisión. Estoy aliviado. Ahora sólo nos queda tomar una decisión en la vida. Pero, Adam, ¿cómo es posible que nunca nos hubieran dicho eso? ¿Por qué cuestionarías algo? Somos abejas. Somos la sociedad que funciona más perfectamente en la Tierra. ¿Alguna vez pensaste que tal vez las cosas funcionan demasiado bien aquí? ¿Cómo qué? Dame un ejemplo. No sé. Pero sabes de lo que estoy hablando. Por favor, despejen la puerta. Royal Nectar Force acercándose. Espera un segundo. Échale un vistazo. - ¡Oye, esos son Pollen Jocks! - Guau. Nunca los había visto tan de cerca. Saben cómo es fuera de la colmena. Sí, pero algunos no regresan. - ¡Hola, deportistas! - ¡Hola, deportistas! ¡Lo hicieron genial! ¡Sois monstruos! ¡Sois unos fanáticos del cielo! ¡Me encanta! ¡Me encanta! - Me pregunto dónde estaban. - No sé. Su día no está planeado. Fuera de la colmena, volando quién sabe dónde, haciendo quién sabe qué. No puedes simplemente decidir ser un Pollen Jock. Tienes que ser criado para eso. Bien. Mirar. Eso es más polen del que tú y yo veremos en toda nuestra vida. Es sólo un símbolo de estatus. Las abejas lo aprovechan demasiado. Tal vez. A menos que lo estés usando y las mujeres te vean usándolo.
"""