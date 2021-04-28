function delete_acc(){
    $.ajax({
        type:"POST",
        url:"/delete",
    })

    window.location.href = "https://mywebpushapp.herokuapp.com"


}