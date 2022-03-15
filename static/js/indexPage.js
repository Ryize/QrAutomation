function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min
}

function generatePassword() {
    random_symbols = getRandomInt(1000, 999999)
    th = document.getElementById('password')
    document.getElementById('password').value = random_symbols
    if (!(th.value === '1234' || th.value.length < 4)) {
        document.getElementById('password_warning').style = 'display: none;'
        document.getElementById('warning_easy').style = 'display: none;'
    }
    checkAcceptSendData()
}

function checkAcceptSendData() {
    let accept = true
    let username = document.getElementById('username')
    let surname = document.getElementById('surname')
    let patronymic = document.getElementById('patronymic')
    let email = document.getElementById('email')
    let password = document.getElementById('password')
    if (username.value.length < 3 || surname.value.length < 3 || password.value.length < 4 || (patronymic.value.length < 3 && patronymic.value.length !== 0)) {
        accept = false
    } else if (password.value === '1234') {
        accept = false
    }
    if ((email.value.indexOf('@') === -1 || email.value.indexOf('.') === -1) && email.value.length !== 0) {
        accept = false
    }
    if (!accept) {
        document.getElementById('button_submit').classList.add('disabled')
    } else {
        document.getElementById('button_submit').classList.remove('disabled')
    }
}

function checkText(th, this_id) {
    let el = document.getElementById(this_id)
    if (th.value.length < 3 && !(this_id === 'patronymic_warning' && th.value.length === 0)) {
        el.style = 'display: inline;'
    } else if (this_id === 'password_warning' && th.value === '1234') {
        document.getElementById('password_warning').style = 'display: none;'
        document.getElementById('warning_easy').style = 'display: inline;'
    } else {
        el.style = 'display: none;'
        document.getElementById('warning_easy').style = 'display: none;'
    }

    if (this_id === 'email_warning' && (th.value.indexOf('@') === -1 || th.value.indexOf('.') === -1) && th.value.length !== 0) {
        document.getElementById('email_warning').style = 'display: inline;'
    } else {
        document.getElementById('email_warning').style = 'display: none;'
    }

    checkAcceptSendData()
}
