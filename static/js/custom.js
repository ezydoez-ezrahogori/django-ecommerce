console.log('Hello')

const incrValue = document.getElementById('increment')
const decrValue = document.getElementById('decrement')
const quentityValue = document.getElementById('quentity').innerText
const id = incrValue.getAttribute('itemid')

console.log(id)



incrValue.addEventListener('click',  e=>{
    e.preventDefault()

    quentityData = {
        'quentity': parseInt(quentityValue) + 1
    }

    $.ajax({
        method: 'GET',
        url: `/order/increment/${id}/`,
        data: quentityData,
        success: response=>{
            console.log(response.quentity)
            document.getElementById('quentity').innerHTML = response.quentity
        },
        error: error=>{
            console.log(error)
        }
    })
})