function request(url, options){
    if(!options){
        options = {}
    }
    return fetch(url, options)
        .then(res => res.json())
        .then(data => {
            return data
        })
        .catch(err => {
            console.log(err)
            return {
                result: false,
                message: err.message
            }
        })
}

function getArticles(){
    return request('/api/articles')
}

function getArticle(id){
    return request('/api/article/' + id)
}

function postArticle(title, body){
    var params = new URLSearchParams()
    params.append('title', title)
    params.append('body', body)
    return request('/api/post', {
        method: 'POST',
        body: params
    })
}

function updateArticle(id, title, body){
    var params = new URLSearchParams()
    params.append("id", id)
    if(title){
        params.append('title', title)
    }
    if(body){
        params.append('body', body)
    }
    return request('/api/update', {
        method: 'POST',
        body: params
    })
}

function deleteArticle(id){
    var params = new URLSearchParams()
    params.append('id', id)
    return request('/api/delete', {
        method: 'DELETE',
        body: params
    })
}

function toDateString(time) {
    var date = new Date(time * 1000)
    return date.getFullYear() + "/" + (date.getMonth() + 1) + "/" + date.getDate();
}

function parseQuery(){
    var query = location.search.substring(1)
    var params = query.split("&")
    var result = {}
    for(var param of params){
        var key_value = param.split("=")
        result[key_value[0]] = key_value[1]
    }
    return result
}