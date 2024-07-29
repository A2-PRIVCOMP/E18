# Código E18 A2PRIVCOMP

Código del desarrollo intermedio de las metodologías para la exposición de datos de usuario en plataformas cloud de alta populariodad y valoración de datos de usuario en el mercado de publicidad en plataformas cloud de alta popularidad (Entregable 18).

Este repositorio contiene el código que permite extraer tanto el tamaño de audiencia como el coste de la campaña publicitaria en CPC y CPM para una audiencia dada, que puede incluir uno o varios intereses, género, rango de edad, país, plataforma (Facebook, Instagram, o ambas si no se especifica), y estado de relación.

La función get_interest_id permite busccar intereses basados en la palabra clave que se pasa por parámetro (interest). De su respuesta se puede obtener el id de uno o varios intereses.

La función retrieve_cost_audience recibe los parámetros opcionales mencionados anteriormente, y obliga a especificar objetivo (CPC o CPM) y divisa (EUR, USD...). Devuelve un vector cuyo primer elemento es el coste (CPC o CPM según se haya especificado) y cuyo segundo elemento es la audiencia, en concreto el MAU (Monthly Active Users) que cumplen el criterio de audiencia especificado.

El usuario de este codigo debe especificar tres variables para hacerlo funcionar, y que puede extraer de su cuenta publicitaria en el Facebook Ads Manager (https://adsmanager.facebook.com/adsmanager), inspeccionando con devtools la petición que se hace al endpint delivery_estimate cuando se configura una nueva audiencia en la interfaz del gestor de campañas.

- act_id: es un número que conforma el id de la cuenta publicitaria, se encuentra en la url de la petición seguido de la cadena 'act_'
- access_token: es uno de los parámetros en la url de la petición
- cookies: cookies de la petición, se copian tal cual como una cadena
