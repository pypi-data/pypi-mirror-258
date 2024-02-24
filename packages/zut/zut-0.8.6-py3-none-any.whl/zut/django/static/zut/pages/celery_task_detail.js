import { startTaskDetailWebsocket } from '../commons/celery.js'

startTaskDetailWebsocket(document.getElementById('task-detail'))
