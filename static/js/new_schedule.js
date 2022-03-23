function controlDate(){
    let status_check = document.getElementById('checkButtonDate').checked
    let date_field = document.getElementById('date_field')
    if (status_check){
        date_field.style = 'display: none;'
    } else{
        date_field.style = 'display: inline;'
    }
}