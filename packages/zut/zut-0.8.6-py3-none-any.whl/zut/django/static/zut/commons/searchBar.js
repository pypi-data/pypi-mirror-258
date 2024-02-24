import { fromHTML } from "./index.js"
import { gettext } from "./i18n.js"

/**
 * @param {{(value: string): void}} action
 * @param {object} options
 * @param {HTMLButtonElement} options.button
 * @param {number} options.wait
 */
function delayInputAction(action, {button, wait} = {}) {    
    const buttonHTML = button ? button.innerHTML : null
    if (wait === undefined) {
        wait = 1.0
    }

    let currentValue = null
    let isConsuming = false

    async function consume() {
        isConsuming = true

        // Disable button and display loading state    
        if (button) {
            button.innerHTML = `<span class="spinner-border spinner-border-sm" aria-hidden="true"></span><span class="visually-hidden" role="status">Loading...</span>`
            button.disabled = true
        }

        // Wait some time for additional keys to be pressed
        await new Promise(r => setTimeout(r, wait * 1000))

        // Fix the value
        const value = currentValue
        currentValue = null

        // Run the callback
        await action(value)
        
        // If the value has changed since it was fixed, consume() again
        if (currentValue) {
            await consume()
        }
        
        // Re-enable button
        if (button) {
            button.innerHTML = buttonHTML
            button.disabled = false
        }

        isConsuming = false
    }

    return function onInput(ev) {
        currentValue = ev.target.value
        if (! isConsuming) {
            consume()
        }
    }
}

function defaultFormatter(row, index) {
    if (row.section) {
        return `<li class="section">${row.section}</li>`
    }
    else {
        let html = row.text
        if (row.url) {
            html = `<a href="${row.url}">${html}</a>`
        }
        if (row.prefix) {
            html = `${row.prefix}${html}`   
        }
        if (row.suffix) {
            html = `${html}${row.suffix}`   
        }

        let additionalClasses = ''
        if (row.external_url) {
            additionalClasses = 'result-with-external'
            html = `<div class="main">${html}</div><div class="external"><a href="${row.external_url}" target="_blank" class="btn btn-sm btn-dark"><i class="bi bi-box-arrow-up-right"></i></a></div>`
        }

        return `<li class="result ${additionalClasses}" tabindex="${index+1}">${html}</li>`
    }
}

/**
 * @param {HTMLInputElement} input 
 */
export function initSearchBar(input, {formatter} = {}) {
    if (! formatter) {
        formatter = defaultFormatter
    }

    const button = input.form.querySelector('button')

    // Create the results element and position it relatively to the form
    input.form.style.position = 'relative'
    const results = document.createElement('div')
    results.classList.add('searchbar-results')
    if (input.form.dataset.resultsWidth) {
        results.style.width = input.form.dataset.resultsWidth
    }
    input.form.appendChild(results)

    function writeError(html) {
        results.innerHTML = `<div class="text-danger">${html}</div>`
        results.style.visibility = 'visible'
    }

    /**
     * @param {string} search 
     */
    async function actualSearch(search) {
        results.innerHTML = ''
        results.style.visibility = 'hidden'

        try {
            const url = `${input.form.action}?${new URLSearchParams({search})}`
            const response = await fetch(url, {method: input.form.method})
            if (! response.ok) {
                writeError(`${response.status} ${response.statusText}`)
                return
            }

            const data = await response.json()
            const rows = data.rows
            if (!rows || rows.length == 0) {
                return
            }
            
            const ul = document.createElement('ul')
            results.appendChild(ul)
            results.style.visibility = 'visible'
                
            for (const [i, row] of rows.entries()) {
                let li = formatter(row, i)
                if (typeof(li) == 'string') {
                    li = fromHTML(li)
                }
                ul.appendChild(li)
            }

            if (data.more) {
                ul.appendChild(fromHTML(`<li class="more">${gettext("There are more results")} ...</li>`))
            }
        }
        catch (err) {
            writeError(err)
            return
        }
    }

    input.form.addEventListener("input", delayInputAction(actualSearch, {button}))
  
    // Hide results if click outside of results and input
    document.addEventListener("mouseup", function(ev) {
        // If the target of the click isn't resultElem
        if (ev.target != results && !results.contains(ev.target) && ev.target != input && !input.contains(ev.target)) {
            results.style.visibility = "hidden"
        }
    })
    
    // Show again results if come back over form
    input.form.addEventListener("mouseover", function(ev) {
        results.style.visibility = results.innerHTML ? "visible" : "hidden"
    })

    // Prevent default submission of the form, and redirect to the first result
    input.form.addEventListener('submit', ev => {
        ev.preventDefault()

        for (const a of results.querySelectorAll('li.result a')) {
            if (a.target) {
                continue
            }
            window.location = a.href
        }
    })
}