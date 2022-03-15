
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
            console.log('Not Logged In')}
        else{
            console.log('User is Logged In. Sending Data ....')
        }
    })
}