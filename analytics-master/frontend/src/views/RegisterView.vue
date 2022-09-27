<template>
  <div class="wrapper">
    <div class="container active">
      <div class="forms">
        <!-- Registration Form -->
        <div class="form signup">
          <span class="title">Регистрация</span>

          <form>
            <div class="input-field">
              <input type="text" placeholder="Логин (латиница)" required v-model="userRegister.username">
              <i class="uil uil-user"></i>
            </div>
            <div class="input-field">
              <input type="email" placeholder="Почта" required v-model="userRegister.email">
              <i class="uil uil-envelope icon"></i>
            </div>
            <div class="input-field">
              <input type="password" class="password" placeholder="Пароль" required v-model="userRegister.password">
              <i class="uil uil-lock icon"></i>
            </div>
            <div class="input-field">
              <input type="password" class="password" placeholder="Повторите пароль" v-model="reqPass" required>
              <i class="uil uil-lock icon"></i>
              <i class="uil uil-eye-slash showHidePw"></i>
            </div>

            <div class="checkbox-text">
              <div class="checkbox-content">
                <input type="checkbox" id="termCon">
                <label for="termCon" class="text">Я принимаю условия <a href="/rules" target="_blank"
                                                                        style="text-decoration: none">пользовательского
                  соглашения и политики конфиденциальности</a></label>
              </div>
            </div>

            <div class="alert d-hidden" style="margin-top: 10px" role="alert">
              {{ message }}
            </div>

            <div class="input-field button">
              <input type="submit" value="Зарегистрироваться" @click.prevent="register">
            </div>

            <div class="login-signup">
                    <span class="text">Есть аккаунт?
                        <router-link to="/login"><a href="#" class="text login-link">Войти</a></router-link>
                    </span>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AuthService from "@/services/auth.service";

export default {
  name: "RegisterView",
  data() {
    return {
      userRegister: {email: '', password: '', username: ''},
      reqPass: '',
      message: '',
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
    register() {
      if (this.userRegister.password !== this.reqPass) {
        this.alertDanger("Ошибка повторого ввода пароля")
        return
      }
      if (!document.querySelector('#termCon').checked) {
        this.alertDanger("Не отмечена галочка")
        return
      }
      if (this.userRegister.password !== '' && this.userRegister.email !== '' && this.userRegister.username !== '') {
        AuthService.register(this.userRegister).then(
            res => {
              this.$router.push('/login')
            })
            .catch(error => {
              this.alertDanger("Аккаунт с таким логином уже существует")
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
  height: 700px;
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
</style>