
//Test - Add the link to file at the end of main.html. Then open browser and check console from inspect to view helloWorld
//console.log("Hello World")

var updateButtons = document.getElementsByClassName('update-cart')
for(var i = 0; i < updateButtons.length; i++){
    updateButtons[i].addEventListener('click', function(){
        // 'this' is like self. It represents item that gets clicked on.
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('USER:', user)

        if(user === 'AnonymousUser'){
            window.alert('User is Not Authenticated. Please Login to Proceed!')}
        else{
            // console.log('User is Logged In. Sending Data ....')
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log('User is Authenticated. Sending Data ...')
//   window.alert('User is Authenticated. Sending Data ...')
   var url = '/update_item/'

   fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken, // send data to backend
        },
        body:JSON.stringify({'productId': productId, 'action': action })
   })

   .then((response) => {
       return response.json()
   })
   .then((data) => {
       console.log('Data:', data)
   })
}
