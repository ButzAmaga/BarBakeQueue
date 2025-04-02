$(() => {

    const order_pills_link = $("#order_pills .nav-link") 
    
    order_pills_link.on("click", function() {

        // clear the active class to the order_pills_link
        order_pills_link.removeClass("active")

        // add the active class to current invoked pill
        $(this).addClass("active")
    })

    console.log(order_pills_link)
})