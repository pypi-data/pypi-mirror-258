const allTranslations = {
    'fr': {
        ":": " :",
        "Connection to web server closed": "Connexion au serveur interrompue",
        "Unauthorized": "Non autorisé",
        "Celery broker is not connected": "le broker Celery n'est pas connecté",
        "Try to reconnect": "Essayer de se reconnecter",
        "There are more results": "Il y a des résultats supplémentaires",
    },
    'ru': {
        ":": ":",
        "Connection to web server closed": "Соединение с веб-сервером закрыто",
        "Unauthorized": "Несанкционированный",
        "Celery broker is not connected": "Celery брокер не подключен",
        "Try to reconnect": "Попробуйте переподключиться",
        "There are more results": "Есть еще результаты",
    },
}

const lang = document.documentElement.lang
const translations = allTranslations[lang]

export function gettext(msg, ...args) {
    msg = translations ? (translations[msg] ?? msg) : msg
    if (args.length > 0) {
        msg = msg.format(...args)
    }
    return msg
}
