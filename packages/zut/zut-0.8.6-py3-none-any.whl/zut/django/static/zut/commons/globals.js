/**
 * Put formatters in the global scope so that bootstrapTables can use them in HTML
 * @file
 */


/**
 * @param {Date} date 
 * @returns {boolean}
 */
export function isToday(date) {
    if (! date) {
        return false
    }
    
    const now = new Date()
    return date.getDate() == now.getDate() && date.getMonth() == now.getMonth() && date.getFullYear() == now.getFullYear()
}


export const formatters = {
    int(value) {
        if (value === undefined || value === null || value === '')
            return value

        return parseInt(value).toLocaleString()
    },

    date(value) {
        if (!value) {
            return value
        }

        const date = new Date(value)
        const localeStr = date.toLocaleString()
        if (localStorage.getItem('settings-fulldate') == '1') {
            return localeStr
        }

        const pos = localeStr.indexOf(' ')
        if (pos <= 0) {
            return localeStr
        }

        if (isToday(date)) {
            return `<span title="${localeStr}">${localeStr.substring(pos + 1)}</span>`
        }
        else {
            return `<span title="${localeStr}">${localeStr.substring(0, pos)}</span>`
        }
    },

    link(value, row) {
        if (! value || ! row._data.link) {
            return value
        }
        
        return `<a href="${row._data.link}">${value}</a>`
    },

    following(value, row, index, field) {
        if (typeof(field) != 'number') {
            console.error(`cannot use following formatter with non-numeric field: ${field}`)
            return value
        }
        const following = row[field+1]
        if (! following) {
            return following
        }
        return following.replace(/{value}/g, value)
    },
}

window.intFormatter = formatters.int
window.dateFormatter = formatters.date
window.linkFormatter = formatters.link
window.followingFormatter = formatters.following
