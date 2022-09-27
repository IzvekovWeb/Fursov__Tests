<template>
  <div class="dialog" v-if="show" @click.stop="hideDialog">
    <div @click.stop class="dialog_content">
      <form>
        <div>
          <div class="text-header-number">
            <span>Введите данные по выкупу</span>
          </div>
          <div style="margin-top: 30px">
            <div class="row mb-3">
              <label for="nm_id" class="col-md-4 col-lg-3 col-form-label">Номенклатура</label>
              <div class="col-md-8 col-lg-9">
                <input v-model="selfsell.nm_id" name="nm_id" type="text" class="form-control" id="nm_id">
              </div>
            </div>
            <div class="row mb-3">
              <label for="article" class="col-md-4 col-lg-3 col-form-label">Артикул поставщика</label>
              <div class="col-md-8 col-lg-9">
                <input v-model="selfsell.article" name="article" type="text" class="form-control" id="article">
              </div>
            </div>
            <div class="row mb-3">
              <label for="total_amount_selfsell" class="col-md-4 col-lg-3 col-form-label">Кол-во выкупов</label>
              <div class="col-md-8 col-lg-9">
                <input v-model="selfsell.total_amount" name="total_amount_selfsell" type="number" class="form-control"
                       id="total_amount_selfsell">
              </div>
            </div>
            <div class="row mb-3">
              <label for="total_sum_selfsell" class="col-md-4 col-lg-3 col-form-label">Сумма выкупов</label>
              <div class="col-md-8 col-lg-9">
                <input v-model="selfsell.total_sum" name="total_sum_selfsell" type="number" class="form-control"
                       id="total_sum_selfsell">
              </div>
            </div>
            <div class="row mb-3">
              <label for="date" class="col-md-4 col-lg-3 col-form-label">Дата</label>
              <div class="col-md-8 col-lg-9">
                <input v-model="selfsell.date" name="date" type="date" class="form-control" id="date">
              </div>
            </div>
            <div class="alert d-hidden" style="margin: 10px 0" role="alert">
              {{message}}
            </div>
            <button id="code" type="submit" class="btn btn-primary" @click.prevent="confirmSelfsell()"
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
  name: "SelfsellModal",
  props: {
    show: {
      type: Boolean,
      default: false
    },
  },
  data: () => ({
    selfsell: {
      'article': '',
      'nm_id': '',
      'total_sum': '',
      'total_amount': '',
      'date': '',
    },
    message: ''
  }),
  methods: {
    hideDialog() {
      this.$emit('update:show', false)
    },
    confirmSelfsell() {
      return api
          .post(API_URL + 'selfsell', this.selfsell)
          .then(response => {
            this.hideDialog()
          })
          .catch(error => {
            document.querySelector(".alert").classList.add("alert-danger")
            this.message = 'Что-то пошло не так'
          });
    },
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