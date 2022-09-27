<template>
  <div class="dialog" v-if="show">
    <div @click.stop class="dialog_content">
      <form>
        <div v-if="!wait">
          <div class="text-header-number">
            Введите номер телефона, к которому привязаны аккаунты: seller.wildberries.ru и wildberries.ru. <br>
            Пример: 7912234525

          </div>
          <div class="row mb-3">
            <label for="phone_num" class="col-md-4 col-lg-3 col-form-label">Номер телефона</label>
            <div class="col-md-8 col-lg-9">
              <input v-model="number" name="phone_num" type="text" class="form-control" id="phone_num">
            </div>
            <button id="numConfirm" type="submit" class="btn btn-primary" @click.prevent="submitDialog"
                    style="margin-top: 15px">Получить
            </button>
          </div>
        </div>
        <div v-else>
          <div class="text-header-number">
            {{ message }}
          </div>
          <div style="margin-top: 30px">
            <div class="row mb-3">
              <label for="code" class="col-md-4 col-lg-3 col-form-label">Код</label>
              <div class="col-md-8 col-lg-9">
                <input v-model="code" name="code" type="text" class="form-control" id="code">
              </div>
            </div>
            <button id="code" type="submit" class="btn btn-primary" @click.prevent="confirmCode"
                    style="margin-top: 15px">Подтвердить
            </button>
          </div>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import API_URL from "@/consts";
import api from "@/api";

export default {
  name: "NumberModal",
  props: {
    show: {
      type: Boolean,
      default: false
    },
  },
  data: () => ({
    number: '',
    code: '',
    wait: false,
    message: ''
  }),
  methods: {
    confirmCode() {
      return api.put(API_URL + 'confirm-code', {code: this.code})
          .then(response => {
            this.$emit('update:show', false)
          })
          .catch(error => {
            console.log(error)
          });
    },
    submitDialog() {
      return api.put(API_URL + 'request-confirm', {phone_num: this.number})
          .then(response => {
            this.wait = true
            document.getElementById('numConfirm').classList.add('d-none')
            console.log(response.data)
            this.message = response.data
          })
          .catch(error => {
            document.getElementById('phone_num').classList.add('danger-input')
          });

      // if (!this.plan.sell_percent) document.getElementById('PercentBuyback').classList.add('danger-input')
    }
  }
}
</script>

<style scoped>
.text-header-number {
  margin: 15px 0px;
}

.dialog {
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  position: fixed;
  display: flex;
  z-index: 9999;
}

.dialog_content {
  max-width: 600px;
  min-width: 300px;
  padding: 25px;
  margin: auto;
  background: #fff;
  border-radius: 12px;
  min-height: 50px;
}

.danger-input {
  border: 2px solid red;
}

.form-control:focus {
  border: 2px solid blue;
}
</style>