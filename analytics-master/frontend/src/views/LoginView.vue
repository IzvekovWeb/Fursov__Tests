<template>
  <div class="wrapper">
    <div class="container">
      <div class="forms">
        <div class="form login">
          <span class="title">Вход</span>

          <form action="#">
            <div class="input-field">
              <input type="text" placeholder="Почта" v-model="userLogin.email" required>
              <i class="uil uil-envelope icon"></i>
            </div>
            <div class="input-field">
              <input class="password danger" type="password" placeholder="Пароль" v-model="userLogin.password" required>
              <i class="uil uil-lock icon"></i>
              <i class="uil uil-eye-slash showHidePw"></i>
            </div>

            <!--            <div class="checkbox-text">-->
            <!--              <a href="#" class="text">Забыли пароль?</a>-->
            <!--            </div>-->

            <div class="alert d-hidden" style="margin-top: 10px" role="alert">
              {{ message }}
            </div>
            <div class="input-field button">
              <input type="submit" value="Войти" @click.prevent="login">
            </div>
          </form>

          <div class="login-signup">
                    <span class="text">Нет аккаунта?
                        <router-link class="text signup-link" to="/register">Регистрация</router-link>
                    </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AuthService from "@/services/auth.service";

export default {
  name: "LoginView",
  data() {
    return {
      userLogin: {email: '', password: ''},
      message: ''
    }
  },
  methods: {
    alertDanger(message) {
      document.querySelector(".alert").classList.remove("d-hidden")
      document.querySelector(".alert").classList.remove("alert-success")
      document.querySelector(".alert").classList.add("alert-danger")
      this.message = message
    },
    alertSuccess(message) {
      document.querySelector(".alert").classList.remove("d-hidden")
      document.querySelector(".alert").classList.remove("alert-danger")
      document.querySelector(".alert").classList.add("alert-success")
      this.message = message
    },
    login() {
      if (this.userLogin.email !== '' && this.userLogin.password !== '') {
        AuthService.login(this.userLogin).then(
            res => {
              this.$router.push('/')
            }
        )
            .catch(err => {
              this.alertDanger("Неверная почта или пароль")
            })
      } else {
        this.alertDanger("Заполните все поля")
      }

    }
  }
}
</script>

<style scoped>
.d-hidden {
  visibility: hidden;
}

.wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 100px;
  background-color: #F6F9FFFF;
}

.container {
  position: relative;
  max-width: 430px;
  width: 100%;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin: 0 20px;
}

.container .forms {
  display: flex;
  align-items: center;
  width: 200%;
  transition: height 0.2s ease;
}


.container .form {
  width: 50%;
  padding: 30px;
  background-color: #fff;
  transition: margin-left 0.18s ease;
}

.container.active .login {
  margin-left: -50%;
  opacity: 0;
  transition: margin-left 0.18s ease, opacity 0.15s ease;
}

.container .signup {
  opacity: 0;
  transition: opacity 0.09s ease;
}

.container.active .signup {
  opacity: 1;
  transition: opacity 0.2s ease;
}

.container.active .forms {
  height: 800px;
}

.container .form .title {
  position: relative;
  font-size: 27px;
  font-weight: 600;
}

.form .title::before {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  height: 3px;
  width: 30px;
  background-color: #4154F1FF;
  border-radius: 25px;
}

.form .input-field {
  position: relative;
  height: 50px;
  width: 100%;
  margin-top: 30px;
}

.input-field input {
  position: absolute;
  height: 100%;
  width: 100%;
  padding: 0 35px;
  border: none;
  outline: none;
  font-size: 16px;
  border-bottom: 2px solid #ccc;
  border-top: 2px solid transparent;
  transition: all 0.2s ease;
}

.input-field input:is(:focus, :valid) {
  border-bottom-color: #4154F1FF;
}

.input-field i {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 23px;
  transition: all 0.2s ease;
}

.input-field input:is(:focus, :valid) ~ i {
  color: #4154F1FF;
}

.input-field i.icon {
  left: 0;
}

.input-field i.showHidePw {
  right: 0;
  cursor: pointer;
  padding: 10px;
}

.form .checkbox-text {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 20px;
}

.checkbox-text .checkbox-content {
  display: flex;
  align-items: center;
}

.checkbox-content input {
  margin: 0 8px -2px 4px;
  accent-color: #4154F1FF;
}

.form .text {
  color: #333;
  font-size: 14px;
}

.form a.text {
  color: #4154F1FF;
  text-decoration: none;
}

.form a:hover {
  text-decoration: underline;
}

.form .button {
  margin-top: 35px;
}

.form .button input {
  border: none;
  color: #fff;
  font-size: 17px;
  font-weight: 500;
  letter-spacing: 1px;
  border-radius: 6px;
  background-color: #4154F1FF;
  cursor: pointer;
  transition: all 0.3s ease;
}

.button input:hover {
  background-color: #4154F1FF;
}

.form .login-signup {
  margin-top: 30px;
  text-align: center;
}
</style>