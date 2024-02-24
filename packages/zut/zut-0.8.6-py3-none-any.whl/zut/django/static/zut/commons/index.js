import { formatters, isToday } from "./globals.js"
export { formatters, isToday }

// #region General

/**
 * Indicate whether we're running in DEBUG mode.
 * @type {boolean}
 */
export const DEBUG = document.body.dataset.debug == 'true'

/**
 * Base URL for the website (without trailing slash).
 * @type {string}
 */
export const BASE_SITE_URL = `${window.location.protocol}//${window.location.hostname}${(window.location.protocol == 'http:' && window.location.port == 80) || (window.location.protocol == 'https:' && window.location.port == 443) ? '' : `:${window.location.port}`}`

/**
 * Base path for static files (without trailing slash).
 * @type {string}
 */
export const BASE_STATIC_PATH = document.body.dataset.staticPrefix ? document.body.dataset.staticPrefix.replace(/\/$/, '') : '/static'

/**
 * Base path for media files (without trailing slash).
 * @type {string}
 */
export const BASE_MEDIA_PATH = document.body.dataset.mediaPrefix ? document.body.dataset.mediaPrefix.replace(/\/$/, '') : '/media'

/**
 * Bootstrap layout breakpoints.
 * 
 * See https://getbootstrap.com/docs/5.0/layout/breakpoints/
 */
export const breakpoint = {
    xs: 0,
    sm: 576,
    md: 768,
    lg: 992,
    xl: 1200,
    xxl: 1400,
}


/**
 * Create element(s) in the DOM from its HTML representation.
 * 
 * See https://stackoverflow.com/a/35385518
 * 
 * @param {String} html
 * @return {Element | HTMLCollection} The created DOM element(s).
 */
export function fromHTML(html) {
    const template = document.createElement('template')
    template.innerHTML = html
    const result = template.content.children
    if (result.length == 1)
        return result[0]
    return result
}


/**
 * Submit a form, displaying a loading icon in the submit while the request is ongoing.
 * 
 * @param {HTMLFormElement} form The form to submit.
 * @param {object} options
 * @param {object} options.data Data to add to the default data (FormData if method is post, QueryString if method is get) .
 * @param {string} options.url URL to use (instead of form action).
 * @param {boolean} options.json Parse content as JSON.
 * @param {boolean} options.successMessage Display content as a success message.
 * @param {{(content: string): void}} options.onSuccess Success callback.
 */
export function submitLoading(form, {data, url, json, successMessage, onSuccess} = {}) {
    const formData = new FormData(form)
    if (data) {
        for (const key in data) {
            formData.set(key, data[key])
        }
    }

    if (! url) {
        url = form.getAttribute('action')
    }

    let init
    if (form.method == 'post') {
        init = { method: 'post', body: formData }
    }
    else {
        const params = new URLSearchParams(formData)
        url += `?${params}`
        init = { method: 'get' }
    }

    const submitButton = form.querySelector('button[type="submit"]')
    const submitButtonHTML = submitButton.innerHTML
    
    // Disable button and display loading state
    submitButton.innerHTML = `<span class="spinner-border spinner-border-sm" aria-hidden="true"></span><span class="visually-hidden" role="status">Loading...</span>`
    submitButton.disabled = true

    fetch(url, init).then(res => {
        const contentPromise = json ? res.json() : res.text()
        contentPromise.then(content => {
            if (successMessage) {
                messages.add(res.ok ? 'SUCCESS' : 'ERROR', content)
            }
            if (onSuccess && res.ok) {
                onSuccess(content)
            }
        })
        .catch(err => messages.error(err))
    }).catch(err => {
        messages.error(err)
    }).finally(() => {        
        // Re-enable button
        submitButton.innerHTML = submitButtonHTML
        submitButton.disabled = false
    })
}

// #endregion


// #region Tables

/**
 * Initialize a bootstrap table from the given tableId, using the default configuration.
 * 
 * @param {string} tableId  ID of the table.
 * @param {object} opts
 * @param {{[field: string]: object}} opts.fields  Column configurations for field names (require `th` elements to have `data-field` attributes).
 * @param {string} opts.sortName   Name of the sort field to use by default: `name` if not specified.
 * @param {string} opts.sortOrder  Order of the sort to use by default (`asc` or `desc`): `asc` if not specified.
 * @param {number} opts.pageSize   Number of items in a page by default: 25 if not specified.
 * @param {Array<object>} opts.columns  Column configurations in the order of `th` elements.
 * @param {object} opts.options  Other options.  
 */
export function initBootstrapTable(tableId, {fields, sortName, sortOrder, pageSize, columns, ...options} = {}) {
    const table = document.getElementById(tableId)

    if (options.pagination === undefined) {
        options.pagination = true
    }

    if (options.search === undefined) {
        options.search = true
    }

    if (options.toolbar === undefined) {
        options.toolbar = `#${tableId}-toolbar`
    }

    options.sortName = localStorage.getItem(`bt-${tableId}-sortName`) ?? sortName
    options.sortOrder = localStorage.getItem(`bt-${tableId}-sortOrder`) ?? (sortOrder ?? 'asc')
    options.onSort = (name, order) => {
        localStorage.setItem(`bt-${tableId}-sortName`, name)
        localStorage.setItem(`bt-${tableId}-sortOrder`, order)
    }

    options.pageSize = localStorage.getItem(`bt-${tableId}-pageSize`) ?? pageSize ?? 25
    options.onPageChange = (number, size) => {
        localStorage.setItem(`bt-${tableId}-pageSize`, size)
    }

    if (columns === undefined) {
        columns = []
    }

    // Ensure there is a column for each <th>, and retrieve field indexes
    const fieldIndexes = {}
    if (table.tHead) {
        for (const [i, th] of table.tHead.querySelectorAll('th').entries()) {
            const field = th.dataset.field
            if (field) {
                fieldIndexes[field] = i
            }
            if (columns.length < i+1) {
                columns.push({})
            }
        }
    }

    for (const column of columns) {
        if (column.sortable === undefined) {
            column.sortable = true
        }
    }

    if (fields) {
        for (const [field, column] of Object.entries(fields)) {
            const fieldIndex = fieldIndexes[field]
            if (fieldIndex === undefined) {
                console.error(`${tableId}: ignore column configuration for field "${field}": field not found in thead`)
                continue
            }
            columns[fieldIndex] = {...columns[fieldIndex], ...column}
        }
    }

    return $(`#${tableId}`).bootstrapTable({columns, ...options})
}

// #endregion


// #region Messages

/**
 * Message container, as defined in `templates/zut/_messages.html`.
 * @type {HTMLDivElement}
 */
const _messages = document.getElementById('messages')

let _messagesCloseAll
let _messagesContent
let _messagesFixedAfter

export const messages = {
    /**
     * Add a message with the given level.
     * @param {string} level
     * @param {string} html
     */
    add(level, html) {
        let color = 'primary'
        if (level) {
            switch (level.toUpperCase()) {
                case 'DEBUG': color = 'secondary'; break
                case 'INFO': color = 'info'; break
                case 'SUCCESS': color = 'success'; break
                case 'WARNING': color = 'warning'; break
                case 'ERROR': color = 'danger'; break
            }
        }
    
        // Create message element
        /** @type {HTMLDivElement} */
        let elem = fromHTML(`<div class="alert alert-${color} alert-dismissible fade show" role="alert">${html}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>`)
        _messagesContent.appendChild(elem)

        // Fix the messages container at the top of the screen if scrolling above `_fixedAfter`.
        // See CSS class `fixed-messages` defined in `static/zut/commons/zut.css`.
        if (_messagesFixedAfter > 0) {
            if (window.scrollY > _messagesFixedAfter) {
                _messages.classList.add('fixed-messages')
            }
        }

        return elem
    },
    
    /**
     * Remove all messages.
     */
    clear() {
        while (_messagesContent.firstChild) {
            _messagesContent.removeChild(_messagesContent.lastChild)
        }

        if (_messagesCloseAll) {
            _messagesCloseAll.classList.add('d-none')
        }
    },

    /**
     * Add a message with the `DEBUG` level.
     * @param {string} html
     * @returns {HTMLDivElement} The `div` element containing the message.
     */
    debug(html) {
        return this.add('DEBUG', html)
    },


    /**
     * Add a message with the `INFO` level.
     * @param {string} html
     * @returns {HTMLDivElement} The `div` element containing the message.
     */
    info(html) {
        return this.add('INFO', html)
    },


    /**
     * Add a message with the `SUCCESS` level.
     * @param {string} html
     * @returns {HTMLDivElement} The `div` element containing the message.
     */
    success(html) {
        return this.add('SUCCESS', html)
    },

    /**
     * Add a message with the `WARNING` level.
     * @param {string} html
     * @returns {HTMLDivElement} The `div` element containing the message.
     */
    warning(html) {
        return this.add('WARNING', html)
    },

    /**
     * Add a message with the `ERROR` level.
     * @param {string} html
     * @returns {HTMLDivElement} The `div` element containing the message.
     */
    error(html) {
        return this.add('ERROR', html)
    },
}

/**
 * Display a `Dismiss all` button if several messages appear.
 */
function _onUpdate() {
    if (_messagesContent.childElementCount >= 2) {
        _messagesCloseAll.classList.remove('d-none')
    }
    else {
        _messagesCloseAll.classList.add('d-none')
        
        if (_messagesFixedAfter > 0) {
            if (_messagesContent.childElementCount == 0) {
                _messages.classList.remove('fixed-messages')
            }
        }
    }
}

if (_messages) {
    _messagesFixedAfter = parseInt(document.body.dataset.messagesFixedAfter ?? 75)
    _messagesContent = document.getElementById('messages-content') ?? _messages
    _messagesCloseAll = document.getElementById('messages-close-all')
    if (_messagesCloseAll) {
        _messagesCloseAll.querySelector('a').addEventListener('click', ev => {
            ev.preventDefault()
            messages.clear()
        })

        new MutationObserver(_onUpdate).observe(_messagesContent, {childList: true})
        _onUpdate()
    }
}

// #endregion


// #region ShowHide

/**
 * @param {HTMLElement} titleElem 
 * @returns 
 */
export function initShowHide(titleElem) {
    const content = document.getElementById(titleElem.dataset.showhide)
    if (! content) {
        console.error(`showhide content with id "${titleElem.dataset.showhide}" not found`)
        return
    }

    const icon = fromHTML(`<i></i>`)
    const button = fromHTML(`<a href="#" class="ms-2 text-dark"></a>`)
    button.appendChild(icon)
    titleElem.appendChild(button)

    function updateButton(hidden) {
        localStorage.setItem(`showhide-${titleElem.dataset.showhide}-hidden`, hidden ? '1' : '0')
        if (hidden) {
            icon.className = 'bi-toggle-off'
            button.title = "Show"
        }
        else {
            icon.className = 'bi-toggle-on'
            button.title = "Hide"
        }
    }

    let hidden
    const savedHidden = localStorage.getItem(`showhide-${titleElem.dataset.showhide}-hidden`)
    if (savedHidden) {
        hidden = savedHidden == '1'
        if (hidden) {
            content.classList.add('d-none')
        }
        else {
            content.classList.remove('d-none')
        }
    }
    else {
        hidden = content.classList.contains('d-none')
    }

    updateButton(hidden)
    button.addEventListener('click', ev => {
        updateButton(content.classList.toggle('d-none'))
        ev.preventDefault()
    })
}

// #endregion
